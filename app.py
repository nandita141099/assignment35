import os

import streamlit as st

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tools import tool

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from langchain_core.prompts import MessagesPlaceholder

load_dotenv()

st.set_page_config(

    page_title="Text-to-Math Agent",

    page_icon="🧮",

    layout="wide"

)

st.title("🧮 Assignment 35 - Text-to-Math Agent")



# Task 1


st.header("Task 1 - Text-to-Math Agent Overview")

st.markdown("""

### 1. What is a Text-to-Math Problem?

A text-to-math problem is a word problem written in natural language.
The agent first understands the question, converts it into mathematical
operations, performs the calculation and finally generates the answer.

---

### 2. Why are AI Agents useful?

Instead of directly guessing an answer, an AI Agent can decide
whether it should use a calculator tool before responding.

---

### 3. Difference between a normal LLM and an Agent

**Normal LLM**

- Generates responses directly
- May make calculation mistakes

**Agent**

- Understands the question
- Uses tools when required
- Performs accurate calculations
- Explains the final answer

""")


st.info("""

Initially I thought an LLM could solve every
math problem accurately.

After learning about tool calling,
I understood that an Agent can use
a calculator whenever calculations
are required.

""")



# Task 2


llm = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0

)



@tool
def calculator(expression: str) -> str:
    """
    Performs mathematical calculations.
    """

    try:

        answer = eval(expression)

        return str(answer)

    except Exception:

        return "Invalid Expression"



prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are a Math Problem Solver.

Always solve the problem step-by-step.

Whenever mathematical calculations
are required,

use the calculator tool.

Explain the reasoning clearly.

"""

        ),

        (

            "human",

            "{input}"

        ),

        MessagesPlaceholder(

            variable_name="agent_scratchpad"

        )

    ]

)


tools = [

    calculator

]


agent = create_tool_calling_agent(

    llm,

    tools,

    prompt

)


agent_executor = AgentExecutor(

    agent=agent,

    tools=tools,

    verbose=True

)

st.success("Text-to-Math Agent Created Successfully")


# Task 2


st.header("Task 2 - Testing the Text-to-Math Agent")

st.write(
    "The agent should understand the problem, "
    "perform calculations when required and "
    "return the final answer."
)


def solve_math(problem):

    """
    Initially I directly asked the LLM.

    Later I realised the assignment expects
    the agent to decide when the calculator
    should be used.
    """

    result = agent_executor.invoke(

        {

            "input": problem

        }

    )

    return result["output"]


# -----------------------------------------------------
# Arithmetic Problems
# -----------------------------------------------------

st.subheader("Arithmetic Problems")

arithmetic_questions = [

    "What is 245 + 378?",

    "Multiply 56 by 28.",

    "What is (45 × 12) + 180 ?"

]

for question in arithmetic_questions:

    st.write("Question")

    st.write(question)

    answer = solve_math(question)

    st.success(answer)



# -----------------------------------------------------
# Percentage Problems
# -----------------------------------------------------

st.subheader("Percentage Problems")

percentage_questions = [

    "What is 20% of 450?",

    "A product costs ₹2500. It has a 15% discount. What is the final price?",

    "Find 35% of 920."

]

for question in percentage_questions:

    st.write("Question")

    st.write(question)

    answer = solve_math(question)

    st.success(answer)



# -----------------------------------------------------
# Simple Algebra
# -----------------------------------------------------

st.subheader("Simple Algebra")

algebra_questions = [

    "If x + 12 = 30, what is x?",

    "If 4x = 40, find x.",

    "A number increased by 8 becomes 25. Find the number."

]

for question in algebra_questions:

    st.write("Question")

    st.write(question)

    answer = solve_math(question)

    st.success(answer)



st.markdown("---")

st.subheader("My Observation")

st.write("""

While testing, I noticed that arithmetic questions
always triggered the calculator tool.

Simple algebra questions were mostly solved
using reasoning first and calculations afterwards.

The verbose output also helped me understand
when the agent decided to use the calculator.

""")

# Task 3


st.header("Task 3 - Session State for Application")


# I first stored the questions inside a normal list.
# Every Streamlit refresh removed the conversation.
# Using session_state solved this problem.

if "messages" not in st.session_state:

    st.session_state.messages = []


st.subheader("Conversation History")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


user_question = st.chat_input(

    "Ask any math question..."

)


if user_question:

    # Store User Question

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_question

        }

    )

    with st.chat_message("user"):

        st.markdown(user_question)


    # Generate Answer

    with st.spinner("Solving..."):

        answer = solve_math(

            user_question

        )


    # Store Assistant Answer

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer

        }

    )


    with st.chat_message("assistant"):

        st.markdown(answer)



st.markdown("---")

st.subheader("Current Session Information")

st.write(

    "Total Messages :",

    len(st.session_state.messages)

)

if st.button("Clear Conversation"):

    st.session_state.messages = []

    st.rerun()



st.markdown("---")

st.subheader("Suggested Questions")

examples = [

    "What is 18 + 45?",

    "Find 35% of 640.",

    "If x + 12 = 25 then find x.",

    "A shop gives 20% discount on ₹2500. What is the final price?",

    "Multiply 48 by 36."

]

for question in examples:

    st.write("•", question)



st.markdown("---")

st.subheader("Observation")

st.write("""

Initially every interaction was treated as a new question because
I wasn't storing previous messages.

After introducing **st.session_state**, the previous questions
and answers remained available throughout the session.

This makes the application behave like a real conversational
assistant instead of a single-question calculator.

""")


# Task 4


st.header("Task 4 - Interactive Text-to-Math Agent")

st.write(
    "The agent remembers previous questions during the current session."
)


def solve_and_store(question):

    """
    Solves the math problem and stores it
    in session history.
    """

    result = agent_executor.invoke(

        {

            "input": question

        }

    )

    answer = result["output"]

    st.session_state.messages.append(

        {

            "role": "user",

            "content": question

        }

    )

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer

        }

    )

    return answer



st.subheader("Try Multi-turn Questions")

example_questions = [

    "What is 250 + 450?",

    "Now multiply the previous answer by 5.",

    "Find 20% of that value.",

    "If I subtract 100 from the previous answer, what do I get?"

]

for question in example_questions:

    if st.button(question):

        with st.spinner("Thinking..."):

            response = solve_and_store(question)

        st.success(response)



st.markdown("---")

st.subheader("Testing Different Types of Problems")

tests = {

    "Arithmetic":

    "Calculate 785 + 215.",

    "Percentage":

    "Find 18% of 2400.",

    "Algebra":

    "If x + 18 = 50, find x."

}

for category, question in tests.items():

    st.write(f"### {category}")

    st.write(question)

    if st.button(f"Run {category}"):

        result = solve_math(question)

        st.success(result)



st.markdown("---")

st.subheader("Error Handling")

invalid_question = st.text_input(

    "Try entering an invalid expression or unclear math question"

)

if st.button("Solve Custom Question"):

    if invalid_question.strip() == "":

        st.warning("Please enter a question.")

    else:

        try:

            answer = solve_math(invalid_question)

            st.success(answer)

        except Exception:

            st.error("Unable to solve this question.")



st.markdown("---")

st.subheader("Session Summary")

user_count = len(

    [

        m

        for m in st.session_state.messages

        if m["role"] == "user"

    ]

)

assistant_count = len(

    [

        m

        for m in st.session_state.messages

        if m["role"] == "assistant"

    ]

)

st.metric("Questions Asked", user_count)

st.metric("Answers Generated", assistant_count)



st.info("""

During testing I noticed that simple arithmetic
questions consistently triggered the calculator tool.

For word problems, the agent first interpreted the
question before deciding whether the calculator
was required.

Using session_state also ensured that the previous
conversation remained available until the chat
was cleared.

""")

# Task 5


st.header("Task 5 - Final Observations")

st.markdown("""

### What I Learned

**1. Why use an AI Agent?**

A normal language model can answer questions directly, but it may not always
perform calculations accurately.

An AI Agent can decide when a calculator is required, execute the calculation,
and then generate the final response.

---

**2. Importance of Tool Calling**

Tool calling allows the model to perform reliable mathematical calculations
instead of estimating answers.

This makes the responses more accurate for arithmetic and numerical problems.

---

**3. Role of Session State**

Initially every interaction behaved like a fresh conversation.

Using `st.session_state` allowed the application to remember previous
questions and answers during the session.

---

**4. Overall Learning**

This assignment helped me understand how an LLM, tools, and an agent work
together to solve real-world mathematical problems.

I also learned how Streamlit can be used to build an interactive AI application
without writing frontend code.

""")


st.success("Assignment 35 Completed Successfully")