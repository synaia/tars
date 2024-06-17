import re
import json
import dspy
from dspy import settings
from typing import Literal
from dsp.modules.gpt3 import chat_request, completions_request, GPT3
from dotenv import dotenv_values

secret = dotenv_values('.secret')

MESSAGES = [] # TODO: It can be a conversation history from a database.
MEM_SIZE = 8

class ChatGPT(GPT3):
    def __init__(self, model: str = "gpt-3.5-turbo-instruct", messages: list[str] = [], mem_size: int = 4, api_key: str | None = None, api_provider: Literal['openai'] = "openai", api_base: str | None = None, model_type: Literal['chat'] | Literal['text'] = None, system_prompt: str | None = None, **kwargs):
      super().__init__(model, api_key, api_provider, api_base, model_type, system_prompt, **kwargs)
      self.messages = messages
      self.mem_size = mem_size * 2
      
    def basic_request(self, prompt: str, **kwargs):
        raw_kwargs = kwargs

        kwargs = {**self.kwargs, **kwargs}
        if self.model_type == "chat":
            if len(self.messages) > self.mem_size:
                self.messages.pop(1) # keep instruction message
            
            if self.system_prompt:
                self.messages.insert(0, {"role": "system", "content": self.system_prompt})

            # Prepare the messages with history
            if len(self.history) == 0:
                self.messages = [{"role": "user", "content": prompt}] # TODO: first input is contained in prompt!.....
            
            _msglist = [msg['content'] for msg in self.messages][-3:-1]

            # pattern = r'\n' + INPUT_FIELD + ':.+'
            # matches = re.findall(pattern, prompt)
            # user_input = matches[-1].replace(f'\n{INPUT_FIELD}: ', '')
            user_input = kwargs.pop('__user_input')

            self.messages.append({"role": "user", "content": user_input})
            
            kwargs["messages"] = self.messages
            kwargs = {"stringify_request": json.dumps(kwargs)}
            response = chat_request(**kwargs)

            if user_input in _msglist:
                self.messages.pop()

            with open("chat_gpt_dump.json", "w") as file:
                json.dump(kwargs, file)

            if user_input not in _msglist:
                ans = response["choices"][0]['message']['content']
                pattern = r'\n.+:.+'
                matches = re.findall(pattern, ans)
                if len(matches) > 0:
                    # lm_answer = matches[-1].replace(f'\n{OUTPUT_FIELD}: ', '')
                    lm_answer = re.sub(r'\n.+:\ ', '', matches[-1])
                else:
                    lm_answer = ans

                if lm_answer not in _msglist:
                    self.messages.append({"role": "assistant", "content": lm_answer})
        else:
            kwargs["prompt"] = prompt
            response = completions_request(**kwargs)

        history = {
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
            "raw_kwargs": raw_kwargs,
        }
        self.history.append(history)

        return response


import copy
import dsp
from dsp.templates.template_v3 import Template
from typing import Any, Callable, Optional
from dsp.primitives.demonstrate import Example
from dsp.primitives.predict import get_all_fields_following_missing_field, generate, Completions
from dsp.utils.utils import dotdict


def _generate(template: Template, **kwargs) -> Callable:
    """Returns a callable function that generates completions for a given example using the provided template."""
    if not dsp.settings.lm:
        raise AssertionError("No LM is loaded.")

    generator = dsp.settings.lm

    def extend_generation(completion: Example, field_names: list[str], stage:str, max_depth: int, original_example:Example):
        """If the required fields are not present in the completion, extend the generation."""
        assert max_depth > 0, "Max depth exceeded - failed to complete in one pass - increase max_tokens"
        # remove content of last field to avoid half-completed content
        for field_name in get_all_fields_following_missing_field(completion, field_names):
            completion.pop(field_name, None)

        # Recurse with greedy decoding and a shorter length.
        max_tokens = (kwargs.get("max_tokens") or 
                    kwargs.get("max_output_tokens") or
                    dsp.settings.lm.kwargs.get("max_tokens") or 
                    dsp.settings.lm.kwargs.get('max_output_tokens'))


        if max_tokens is None:
            raise ValueError("Required 'max_tokens' or 'max_output_tokens' not specified in settings.")
        max_tokens = min(max(75, max_tokens // 2), max_tokens)
        keys = list(kwargs.keys()) + list(dsp.settings.lm.kwargs.keys()) 
        max_tokens_key = "max_tokens" if "max_tokens" in keys else "max_output_tokens"
        new_kwargs = {
            **kwargs,
            max_tokens_key: max_tokens,
            "n": 1,
            "temperature": 0.0,
        }

        _, finished_completion = generate(template, **new_kwargs)(
            completion,
            stage=stage,
            max_depth=max_depth - 1,
            original_example=original_example,
        )
        return finished_completion.data[0]
        

    def do_generate(
        example: Example, stage: str, max_depth: int = 2, original_example=None,
    ):
        if not dsp.settings.lm:
            raise AssertionError("No LM is loaded.")
        original_example = original_example or example
        assert stage is not None

        # Look up the appropriate fields in each demonstration.
        example = example.demos_at(lambda d: d[stage])

        # Generate and extract the fields.
        prompt = template(example)
        ex = copy.deepcopy(example)
        ex.pop('demos', None)
        ex.pop('context', None)
        ex.pop('passages', None)
        ex.pop('rationale', None)
        kwargs['__user_input'] = ', '.join([ex[k] for k in ex.keys()])
        completions: list[dict[str, Any]] = generator(prompt, **kwargs)
        completions: list[Example] = [template.extract(example, p) for p in completions]

        # Find the completions that are unfinished.
        field_names: list[str] = [field.input_variable for field in template.fields]

        finished_completions = []
        for completion in completions:
            if all((completion.get(key, "") != "") for key in field_names):
                finished_completions.append(completion)
                continue
            finished_completions.append(
                extend_generation(completion, field_names, stage, max_depth, original_example),
            )

        completions = Completions(finished_completions, template=template)
        example = example.copy(completions=completions)

        if len(completions) == 1:
            completion = completions[0]
            example[stage] = example.copy(**completion)

            if dsp.settings.compiling:
                inputs_ = set(original_example.keys())
                inputs = [
                    f.input_variable
                    for f in template.fields
                    if f.input_variable in inputs_
                ]
                outputs = [
                    f.output_variable
                    for f in template.fields
                    if f.input_variable not in inputs_
                ]

                example.compiling_stages = example.get("compiling_stages", [])
                example.compiling_stages.append(
                    {
                        "name": stage,
                        "template": template,
                        "inputs": inputs,
                        "outputs": outputs,
                    },
                )
        else:
            # assert not dsp.settings.compiling, "TODO: At this point, cannot compile n>1 generations"
            example[stage] = dotdict(completions=completions)

        return example, completions

    return do_generate
    

#TODO: ovverride 
from dsp.primitives import predict
predict._generate = _generate


    
# system_prompt= "IMPORTANT INSTRUCT AS A SYSTEM"
custom_gtp = ChatGPT('gpt-3.5-turbo', messages=MESSAGES, mem_size=MEM_SIZE, api_key=secret['OPEN_AI_API_KEY'], model_type="chat", max_tokens=250,)
settings.configure(lm=custom_gtp, )


class ConversationalSignature(dspy.Signature):
    """You are a helpful assistant. Answer all questions to the best of your ability."""
    message = dspy.InputField(desc='Contains the user message input.', memorize=True)
    # context = dspy.InputField(desc="Before responding, AI must consider relevant facts in the history of conversation.")
    answer = dspy.OutputField(desc='Contains the assistant message output, use a short response')


class ConversationalModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.conversation = dspy.ChainOfThought(ConversationalSignature)

    def forward(self, message: str):
        response = self.conversation(message=message)
        return response
    

compiled_module = ConversationalModule()
# compiled_module.load("samantha/notebook/conversational_module.json")

response = compiled_module(message="Hi, my name is Rolando Espinal.")
print(response)

response = compiled_module(message="Do you remember my lastname?")
print(response)

response = compiled_module(message="Wilton prepares for a 15 km walk, advancing 1.5 km per hour. If Wilton starts at 7 am, how many kilometers has Wilton traveled at 9 am?")
print(response)

response = compiled_module(message="His wife, Priscila, joins the walk at 10 am. How many kilometers has Wilton traveled?")
print(response)

response = compiled_module(message="Priscila is fast and moves at a speed of 2 km per hour, when Wilton has already traveled 12 kilometers. How many kilometers has Priscila traveled?")
print(response)

response = compiled_module(message="Do you remember my lastname?")
print(response)



