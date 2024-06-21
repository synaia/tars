
import dspy
from dsp.templates import passages2text
from samantha.src.machinery import DataManager
from .configs import retriever_model


class_names = [
    "greetings",
    "company", 
    "feedbacks", 
    "continue_later", 
    "stop_continue",
    "trouble",
    "himself",
    "continue_yes",
    "thanks"
]


class UtteranceSignature(dspy.Signature):
    """A basic utterance classifier in a chat conversation."""
    utterance: str = dspy.InputField(desc="An user utterance")
    utterance_type: str = dspy.OutputField(desc=f"One type in the following list {str(class_names)}")


class UtteranceClassificator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot = dspy.ChainOfThought(UtteranceSignature)

    def forward(self, utterance: str) -> dspy.Prediction:
        return self.cot(utterance=utterance)
    

class ApplicanStateSignature(dspy.Signature):
    """Respond in a friendly way, often between 7 and 12 words, that the user process is in '{}' step."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
    

class ApplicantState(dspy.Module):
    def __init__(self, msisdn: str,  data: DataManager) -> None:
        super().__init__()
        self.msisdn = msisdn
        self.data = data

    def forward(self, question: str) -> dspy.Prediction:
        state = self.data.get_applicant_state(msisdn=self.msisdn)
        ApplicanStateSignature.__doc__ = ApplicanStateSignature.__doc__.format(state)
        applicant = dspy.ChainOfThought(ApplicanStateSignature)
        response = applicant(question=question)
        return response
    

class LaterContinueSignature(dspy.Signature):
    """Reply we appreciate your time, it will only take a minute or two, if you can\'t yet, when can I write to you? 📆"""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 10 and 12 words")


class NotContinueSignature(dspy.Signature):
    """Reply we appreciate your time, If you change your mind, we will be gladly waiting for you."""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 10 and 12 words")


class NotFound(dspy.Signature):
    # """Generates a denial response related to the question in context"""
    """Respond that you do not have that information available, but it was requested."""
    context: str = dspy.InputField()
    response: str = dspy.OutputField(desc="often between 5 and 10 words")


class Veracity(dspy.Signature):
    context_provided: str = dspy.InputField(desc="may contain relevant facts")
    answer: str = dspy.InputField()
    answer_is_in_context_provided: bool = dspy.OutputField(desc="verify that the answer is in the context_provided, respond True or False")


class CompanySignature(dspy.Signature):
    """Answer questions with short factoid answers and friendly, use emoji. Answer should be in the context."""
    chat_history: list[str] = dspy.InputField(format=passages2text, desc="Must consider relevant facts in the history of conversation.")
    context: str = dspy.InputField(desc="may contain relevant facts")
    question: str = dspy.InputField(desc="User question to be answered")
    answer: str = dspy.OutputField(desc="Contains the AI message output, often between 6 and 12 words")


class CompanyRelated(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retriever = retriever_model
        self.predict = dspy.ChainOfThought(CompanySignature)
        self.veracity = dspy.TypedChainOfThought(Veracity)
        self.not_found = dspy.Predict(NotFound)
    
    def forward(self, question: str, chat_history: list[str]) -> dict:
        context = self.retriever(question)
        context = [ctx['text'] for ctx in context]
        response = self.predict(context=context, chat_history=chat_history, question=question)
        veracity = self.veracity(context_provided=str(context), answer=response.answer)
        if veracity.answer_is_in_context_provided:
            r = response
            return {
                "answer": r.answer,
                "answer_is_in_context_provided": veracity.answer_is_in_context_provided
            }
        else:
            r = self.not_found(context=question)
            return {
                "answer": r.response,
                "answer_is_in_context_provided": veracity.answer_is_in_context_provided
            }
        

class EvalSignature(dspy.Signature):
    """Does the text contain the question about completing a form?"""
    text: str = dspy.InputField(desc="text to be evaluated")
    passed: bool = dspy.OutputField(desc="Should be True or False")

class EvalNewSignature(dspy.Signature):
    """Does the text contain the question about filling an assessment?"""
    text: str = dspy.InputField(desc="text to be evaluated")
    passed: bool = dspy.OutputField(desc="Should be True or False")

class GreetingSignature(dspy.Signature):
    """Generate a greeting back to the user without offering assistance, use emoji."""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 3 and 5 words")


class ThanksSignature(dspy.Signature):
    """Generate a "you're welcome" response to the user's thanks without offering assistance, use emoji."""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 5 and 7 words")

class NoFeedBackSignature(dspy.Signature):
    """Kindly reply back that there is no feedback yet"""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 3 and 5 words")


class SelfSignature(dspy.Signature):
    """Respond according to the text, be supportive and friendly"""
    text: str = dspy.InputField(desc="user input text")
    response: str = dspy.OutputField(desc="often between 10 and 12 words")


class DraftSignature(dspy.Signature):
    """"Ask user to please take a moment to complete the form."""
    chat_history: list[str] = dspy.InputField(format=passages2text, desc="Must consider relevant facts in the chat history of conversation.")
    user_input: str = dspy.InputField(format=lambda x: "\n===\n" + str(x) + "\n===\n")
    response: str = dspy.OutputField(desc="Please take a moment to complete the form below ⤵️, often between 10 and 12 words")


class Draft(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = DraftSignature
        self.predict = dspy.ChainOfThoughtWithHint(self.signature)
        self.eval = dspy.TypedChainOfThought(EvalSignature)
        # self.classificator = UtteranceClassificator()
        # self.classificator.load('./samantha/src/compiled_json_ref/utterance_module_v3.json')
        self.greeting = dspy.ChainOfThought(GreetingSignature)
        self.thanksback = dspy.ChainOfThought(ThanksSignature)
        self.company = CompanyRelated()
        self.later_continue = dspy.ChainOfThoughtWithHint(LaterContinueSignature)
        self.not_continue = dspy.ChainOfThought(NotContinueSignature)

    def forward(self, user_input: str, chat_history: list[str], utterance_type: str) -> str:
        # utterance_type = self.classificator(utterance=user_input).utterance_type
        if utterance_type == "continue_later":
            return self.later_continue(text=user_input, hint="It can only be scheduled to continue through chat").response, utterance_type
        
        if utterance_type == "stop_continue":
            return self.not_continue(text=user_input).response, utterance_type
        
        response = self.predict(chat_history=chat_history, user_input=user_input, hint="The form is below, it is inside this chat session, you don't need to find anything outside.")
        evaluation = self.eval(text=response.response)
        dspy.Suggest(evaluation.passed, "The response must contain a request to the user to complete the form.")
        
        output: list[str] = []
        if utterance_type == "greetings":
             output.append(self.greeting(text=user_input).response)
        elif utterance_type == "company":
            output.append(self.company(question=user_input, chat_history=chat_history)['answer'])
        elif utterance_type == "thanks":
            output.append(self.thanksback(text=user_input).response)
       
        output.append(response.response)
        return "\n".join(output), utterance_type


class NewSignature(dspy.Signature):
    """"Kindly request the user to take a moment to fill the assessment"""
    chat_history: list[str] = dspy.InputField(format=passages2text, desc="Must consider relevant facts in the chat history of conversation.")
    user_input: str = dspy.InputField(format=lambda x: "\n===\n" + str(x) + "\n===\n")
    response: str = dspy.OutputField(desc="Please take a moment to fill the assessment below ⤵️, often between 10 and 12 words")


class New(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = NewSignature
        self.predict = dspy.ChainOfThoughtWithHint(self.signature)
        self.eval = dspy.TypedChainOfThought(EvalNewSignature)
        # self.classificator = UtteranceClassificator()
        # self.classificator.load('./samantha/src/compiled_json_ref/utterance_module_v3.json')
        self.greeting = dspy.ChainOfThought(GreetingSignature)
        self.thanksback = dspy.ChainOfThought(ThanksSignature)
        self.company = CompanyRelated()
        self.later_continue = dspy.ChainOfThoughtWithHint(LaterContinueSignature)
        self.not_continue = dspy.ChainOfThought(NotContinueSignature)
        self.non_feedback = dspy.Predict(NoFeedBackSignature)
        self.self_back = dspy.Predict(SelfSignature)


    def forward(self, user_input: str, chat_history: list[str], utterance_type: str) -> str:
        # utterance_type = self.classificator(utterance=user_input).utterance_type
        if utterance_type == "continue_later":
            return self.later_continue(text=user_input, hint="It can only be scheduled to continue through chat, do not propose a new date").response, utterance_type
        
        if utterance_type == "stop_continue":
            return self.not_continue(text=user_input).response, utterance_type
        
        response = self.predict(chat_history=chat_history, user_input=user_input, hint="The form is below, it is inside this chat, you don't need to find anything outside.")
        evaluation = self.eval(text=response.response)
        dspy.Suggest(evaluation.passed, "The response must contain a request to the user to fill the assessment.")
        
        output: list[str] = []
        if utterance_type == "greetings":
             output.append(self.greeting(text=user_input).response)
        elif utterance_type == "company":
            output.append(self.company(question=user_input, chat_history=chat_history)['answer'])
        elif utterance_type == "feedbacks":
            output.append(self.non_feedback(text=user_input).response)
        elif utterance_type == "trouble":
            pass
        elif utterance_type == "himself":
            output.append(self.self_back(text=user_input).response)
        elif utterance_type == "thanks":
            output.append(self.thanksback(text=user_input).response)
        
        output.append(response.response)
        return "\n".join(output), utterance_type



class RecordingSignature(dspy.Signature):
    """"Kindly ask the user to take a moment and send a voice note 🗣️ of no more than 2 minutes for evaluation purposes"""
    chat_history: list[str] = dspy.InputField(format=passages2text, desc="Must consider relevant facts in the chat history of conversation.")
    user_input: str = dspy.InputField(format=lambda x: "\n===\n" + str(x) + "\n===\n")
    response: str = dspy.OutputField(desc="Please take a moment and send a voice note 🗣️ of no more than 2 minutes for evaluation purposes, often between 10 and 12 words")


class Recording(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = RecordingSignature
        self.predict = dspy.ChainOfThought(self.signature)
        # self.classificator = UtteranceClassificator()
        # self.classificator.load('./samantha/src/compiled_json_ref/utterance_module_v3.json')
        self.greeting = dspy.ChainOfThought(GreetingSignature)
        self.thanksback = dspy.ChainOfThought(ThanksSignature)
        self.company = CompanyRelated()
        self.later_continue = dspy.ChainOfThoughtWithHint(LaterContinueSignature)
        self.not_continue = dspy.ChainOfThought(NotContinueSignature)
        self.non_feedback = dspy.Predict(NoFeedBackSignature)
        self.self_back = dspy.Predict(SelfSignature)

    def forward(self, user_input: str, chat_history: list[str], utterance_type: str) -> str:
        # utterance_type = self.classificator(utterance=user_input).utterance_type
        if utterance_type == "continue_later":
            return self.later_continue(text=user_input, hint="It can only be scheduled to continue through chat, do not propose a new date").response, utterance_type
        
        if utterance_type == "stop_continue":
            return self.not_continue(text=user_input).response, utterance_type
        
        response = self.predict(chat_history=chat_history, user_input=user_input)
        
        output: list[str] = []
        if utterance_type == "greetings":
             output.append(self.greeting(text=user_input).response)
        elif utterance_type == "company":
            output.append(self.company(question=user_input, chat_history=chat_history)['answer'])
        elif utterance_type == "feedbacks":
            output.append(self.non_feedback(text=user_input).response)
        elif utterance_type == "trouble":
            pass
        elif utterance_type == "himself":
            output.append(self.self_back(text=user_input).response)
        elif utterance_type == "thanks":
            output.append(self.thanksback(text=user_input).response)            
        
        output.append(response.response)
        return "\n".join(output), utterance_type
    

class EvaluationSignature(dspy.Signature):
    """"Kindly response or interact with user inputs"""
    chat_history: list[str] = dspy.InputField(format=passages2text, desc="Must consider relevant facts in the chat history of conversation.")
    user_input: str = dspy.InputField(format=lambda x: "\n===\n" + str(x) + "\n===\n")
    response: str = dspy.OutputField(desc="Often between 10 and 12 words")


class Evaluation(dspy.Module):
    def __init__(self, msisdn: str, data: DataManager):
        super().__init__()
        self.signature = EvaluationSignature
        self.predict = dspy.ChainOfThought(self.signature)
        # self.classificator = UtteranceClassificator()
        # self.classificator.load('./samantha/src/compiled_json_ref/utterance_module_v3.json')
        self.greeting = dspy.ChainOfThought(GreetingSignature)
        self.thanksback = dspy.ChainOfThought(ThanksSignature)
        self.company = CompanyRelated()
        self.later_continue = dspy.ChainOfThoughtWithHint(LaterContinueSignature)
        self.not_continue = dspy.ChainOfThought(NotContinueSignature)
        self.applicant = ApplicantState(msisdn=msisdn, data=data)
        self.self_back = dspy.Predict(SelfSignature)

    def forward(self, user_input: str, chat_history: list[str], utterance_type: str) -> str:
        # utterance_type = self.classificator(utterance=user_input).utterance_type
        if utterance_type == "continue_later":
            return self.later_continue(text=user_input, hint="It can only be scheduled to continue through chat, do not propose a new date").response, utterance_type
        
        if utterance_type == "stop_continue":
            return self.not_continue(text=user_input).response, utterance_type
        
        response = self.predict(chat_history=chat_history, user_input=user_input)
        
        output: list[str] = []
        if utterance_type == "greetings":
             output.append(self.greeting(text=user_input).response)
        elif utterance_type == "company": # TODO: training new category: 'complaint'
            output.append(self.company(question=user_input, chat_history=chat_history)['answer'])
        elif utterance_type == "feedbacks":
            output.append(self.applicant(question=user_input).answer)
        elif utterance_type == "trouble":
            pass
        elif utterance_type == "himself":
            output.append(self.self_back(text=user_input).response)
        elif utterance_type == "thanks":
            output.append(self.thanksback(text=user_input).response)

        output.append(response.response)
        return "\n".join(output), utterance_type
