import streamlit as st
import random
import time

import torch
import torch.nn.functional as F

import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field
from typing import List
from transitions import Machine
from dotenv import dotenv_values
from rich import print


secret = dotenv_values('../../.secret')

llama3 = dspy.GROQ(
    # model='llama3-70b-8192',
    model='llama-3.1-70b-versatile',
    api_key=secret['GROQ_API_KEY'],
    max_tokens=1024,
    temperature=0.0
)
dspy.settings.configure(lm=llama3)


from typing import Any, Dict, Type
from pydantic import BaseModel, Field, create_model
import dspy


type_mapping: Dict[str, Type[Any]] = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    # Add more mappings as needed
}

field_type = type_mapping.get("str")

# Define the fields dynamically
fields = {
    'previous_conversation_history': (field_type, Field(description="Previous conversation history")),
    'utterance': (field_type, Field(description="User utterance input")),
    'previous_task': (field_type, Field(description="User already completed task")),
    'current_task': (field_type, Field(description="User current task to be completed")),
    'next_task': (field_type, Field(description="User next task to be completed")),
    'tasks_completed': (field_type, Field(description="Useful for validate Tasks already completed")),
    'previous_state': (field_type, Field(description="User previous state")),
    'current_state': (field_type, Field(description="User current state")),
}

# Create a dynamic model
Input = create_model('Input', **fields)

# class Input(BaseModel):
#     previous_conversation_history: str = Field(description="Previous conversation history")
#     utterance: str = Field(description="User utterance input")
#     previous_task: str = Field(description="User already completed task")
#     current_task: str = Field(description="User current task to be completed")
#     next_task: str = Field(description="User next task to be completed")
#     tasks_completed: str = Field(description="Useful for validate Tasks already completed")
#     previous_state: str = Field(description="User previous state")
#     current_state: str = Field(description="User current state")

class Output(BaseModel):
    response: str = Field(description=f"AI response")
    share_link: bool = Field(description="True if: (1) you are asking the user to fill out a form for the first time, (2) the user is requesting to share the form.")
    schedule: bool = Field(description="True if: (1) If the user for some reason cannot continue with the task, ask them to schedule them and continue later, (2) The user decides to abandon the process.")
    company_question: bool = Field(description="True if: the user's intent is related to a company-related question. Respond with 'True' if the question pertains to a company, its operations, products, services, or related topics.")
    abort_scheduled_state: bool = Field(description="True if: the user agrees to continue with the current task even if it is in 'Scheduled' state.")

class DSTSignature(dspy.Signature):
    user_input: Input = dspy.InputField()
    output: Output = dspy.OutputField()

class DST(dspy.Module):
    def __init__(self, signature: dspy.Signature):
        super().__init__()
        self.predict = dspy.TypedChainOfThought(signature=signature)

    def forward(self, user_input: Input) -> dspy.Prediction:
        return self.predict(user_input=user_input)

tasks = {1: "Talent entry form", 2: "Grammar Assessment form", 3: "Scripted text", 4: "Open question", 5: "End_of_Task"}
states = {
    "In Progress": "",
    "Scheduled": "",
    "Completed": ""
  }

if 'previous_state' not in st.session_state:
    st.session_state.previous_state = ""


# Create a radio button for task selection
task_keys = list(tasks.keys())
task_options = [tasks[key] for key in task_keys]

state_options = list(states.keys())

cols = st.columns(2)
index_s = 1
with cols[0]:
  task = st.radio("Choose a task:", task_options)
  index = next(key for key, value in tasks.items() if value == task)
  index = int(index)
  st.write(f"Task: {task} (index: {index})")
with cols[1]:
  state = st.radio("Choose a state:", state_options)
  st.write(f"Previous state {st.session_state.previous_state}")
  st.write(f"Current state: {state}")


print(st.session_state.previous_state)

def main_signature(index: int, states: list, current_state: str, previous_state: str) -> str:
  task_instruct = ""
  if index == 1:
    task_instruct = "Rephrase the following message: Welcome! the purpose here is to get to know you better. I'll guide you through a quick assessment to check your grammar and English fluency. It only takes about 10 minutes to complete! Instead of spending weeks going to an office, this assessment happens right here, right now.\n\nReady to start?"
  if index == 2:
    task_instruct = "Rephrase the following message: Just a few steps to your job! 🙌🏼\nYour next step is to fill in the assessment."
  if index == 3:
    task_instruct = "Rephrase the following message: You've made great progress—well done! 🚀 Next, read the text aloud and send it as a voice note: `PLACEHOLDER_1`"
  if index == 4:
    task_instruct = "Rephrase the following message: Got your voice note! ✅  You've made substantial progress—fantastic job! 🚀 The last task involves recording a voice note (1+ minute) that thoughtfully addresses the following prompt: `PLACEHOLDER_2`"
  # if index == 5:
  #   task_instruct = "Rephrase the following message: Your voice note has landed! Well done on completing all the steps, thanks!"

  state_instruct = ""
  main_body_instruct = ""
  if previous_state == "Scheduled" and current_state != "Scheduled":
     state_instruct = "Welcome back to the user, as the previous status was 'Scheduled'."
  elif current_state == "Scheduled" and previous_state == "Scheduled":
     main_body_instruct = "Ask the user if they want to continue with the current task."
     task_instruct = ""
  elif current_state == "Scheduled":
     main_body_instruct = "Thanks the user for scheduling, see you later."
     task_instruct = ""
  elif current_state == "In Progress":
    main_body_instruct = """Ask the user to complete the following sequence tasks:
            - Talent entry form
              Fields: Name, English level and policy acceptance
              Delivery: Share in this chat
              IMPORTANT: The form is self-contained. You are not informed about its content.

            - Grammar Assessment form
              Fields: Two questions
              Delivery:  Share in this chat
              IMPORTANT: The form is self-contained. You are not informed about its content.

            - Scripted text
              Fields: read aloud the text `PLACEHOLDER_1` and share as a voice note
              Delivery:  Share in this chat

            - Open question
              Fields: answer the question `PLACEHOLDER_2` aloud and share as a voice note
              Delivery:  Share in this chat

            - End_of_Task


            Your task is to validate that the sequence of tasks are completed by the user, If current task is NOT completed, ask again.
            Respond to any concerns while keeping track of tasks.
            If the user decides to abandon the process, politely remind them of the excellent job opportunity at hand. Highlight the career growth, supportive team, and exciting challenges that align with their skills. Reassure them that continuing could be a significant step forward in their career. Offer to address any concerns they may have and emphasize that opportunities like this are rare.
            Ask the user to schedule if: (1) the user for some reason cannot continue with the task, ask them to schedule them and continue later, (2) The user decides to abandon the process.
  """
    
  if current_state == "Completed" and previous_state != "Completed":
    task_instruct = "Rephrase the following message: Your voice note has landed! Well done on completing all the steps, thanks!"
  elif current_state == "Completed" and previous_state == "Completed":
    main_body_instruct = "At this point the user has completed the task sequence, If the user asks for additional information about the process, respond shortly and politely and provide the necessary details. If no further information is needed, kindly say goodbye."
    task_instruct = ""

  s = f"""You are Maria, a virtual assistant at a call center recruiting company.
          You are only able to answer in English.
          If the user uses a language different from English, ask politely to switch to English.

          {main_body_instruct}

          {task_instruct}

          {state_instruct}
          
          """
  return s


previous_conversation_history = []


def generate(_input: str):
    user_input = Input(
        utterance=_input,
        previous_task=tasks.get(index - 1) if index > 1 else "",
        current_task=task,
        next_task=tasks.get(index + 1) if index < len(tasks) else "",
        tasks_completed="\n ".join([tasks.get(i) for i in range(1, index)]),
        previous_conversation_history="\n".join(previous_conversation_history),
        current_state=state,
        previous_state=st.session_state.previous_state
    )
    DSTSignature.__doc__ = main_signature(index=index, states=states, current_state=state, previous_state=st.session_state.previous_state)
    dst = DST(signature=DSTSignature)
    out = dst(user_input=user_input)
    previous_conversation_history.extend(
        [f"User: {_input}", f"AI: {out.output.response}"]
    )
    return out.output


st.title("conversational 0.2")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    

# Streamed response emulator
def response_generator(response: str):
    if prompt:
        for word in response.split():
            yield word + " "
            time.sleep(0.01)

def response_generator_media(response: str):
    if prompt:
        for word in response.split():
            yield word + " "
            time.sleep(0.001)            

if prompt:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        output = generate(prompt)
        content = output.response
        share_link = output.share_link
        schedule = output.schedule
        company_question = output.company_question
        abort_scheduled_state = output.abort_scheduled_state
        content = st.write_stream(response_generator(content))
        st.session_state.previous_state = state
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": content})
    

if prompt:
    # Define the status indicators
    status_indicators = {
        "share_link": share_link,  # Use "Active" or "Inactive" to indicate status
        "schedule": schedule,
        "company_question": company_question,
        "abort_scheduled_state": abort_scheduled_state,
    }

    # Display the status indicators
    cols = st.columns(len(status_indicators))
    for i, (flag, status) in enumerate(status_indicators.items()):
        with cols[i]:
            # st.metric(label=flag, value=status)
            # Optional: color styling based on status
            if status == True:
                st.markdown(f'<div style="color: green;font-size:10px;">🟢 {flag}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color: red;font-size:10px;">🔴 {flag}</div>', unsafe_allow_html=True)
