import os
import streamlit as st

from dotenv import load_dotenv

from sympy import (
    symbols,
    Eq,
    solve,
    sympify
)

from langchain_openai import ChatOpenAI

from langchain_core.tools import tool

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)

load_dotenv()

st.set_page_config(
    page_title="Math Agent",
    page_icon="🧮"
)

st.title("🧮 Text to Math Agent")


# --------------------------------------------------
# Task 1
# --------------------------------------------------

st.header("About this Assignment")

st.write("""

This application solves mathematical questions
using a LangChain Agent.

Instead of solving every problem directly,
the agent decides whether it needs
an external tool.

The agent currently has two tools:

• Calculator

• Equation Solver

""")


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0

)



# --------------------------------------------------
# Tool 1
# --------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Performs arithmetic calculations.
    """

    try:

        result = sympify(expression)

        return str(result)

    except Exception:

        return "Unable to evaluate expression."



# --------------------------------------------------
# Tool 2
# --------------------------------------------------

@tool
def equation_solver(equation: str) -> str:
    """
    Solves equations.

    Example

    x+5=10

    2*x=18
    """

    try:

        x = symbols("x")

        left, right = equation.split("=")

        equation = Eq(

            sympify(left),

            sympify(right)

        )

        answer = solve(

            equation,

            x

        )

        return str(answer)

    except Exception:

        return "Unable to solve equation."



tools = [

    calculator,

    equation_solver

]



# --------------------------------------------------
# Prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

"""
You are an AI Math Agent.

Your job is NOT to solve problems directly.

First understand the user's question.

Then decide which tool should be used.

Rules

Arithmetic
→ calculator

Percentages
→ calculator

Equations
→ equation_solver

Always explain

1. What type of problem it is.

2. Which tool you selected.

3. Tool output.

4. Final answer.

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



agent = create_tool_calling_agent(

    llm,

    tools,

    prompt

)



agent_executor = AgentExecutor(

    agent=agent,

    tools=tools,

    verbose=True,

    return_intermediate_steps=True

)


st.success("Math Agent Ready")

# --------------------------------------------------
# Task 2
# --------------------------------------------------

st.header("Try the Agent")

st.write(
    "The agent decides which tool should be used. "
    "There is no manual routing in the application."
)


def ask_agent(question):

    """
    All questions go directly to the agent.

    The application itself does not decide
    which tool to call.
    """

    try:

        response = agent_executor.invoke(

            {

                "input": question

            }

        )

        return response

    except Exception as e:

        return {

            "output": "Something went wrong.",

            "intermediate_steps": [],

            "error": str(e)

        }



sample_questions = [

    "Calculate 25+85",

    "What is 30% of 900?",

    "Solve x+12=30",

    "Solve 3*x=27",

    "Calculate (45*12)+180"

]


selected = st.selectbox(

    "Choose a sample question",

    sample_questions

)


if st.button("Run Sample"):

    result = ask_agent(selected)

    st.subheader("Question")

    st.write(selected)

    st.subheader("Final Answer")

    st.success(result["output"])



    st.subheader("Agent Activity")

    if len(result["intermediate_steps"]) == 0:

        st.info(

            "No tool was required."

        )

    else:

        for index, step in enumerate(

            result["intermediate_steps"]

        ):

            st.write(

                f"Step {index+1}"

            )

            st.code(str(step))

st.divider()

st.subheader("What I Observed")

st.write("""

In my previous version I checked
whether a question contained

+, = or %

and then manually selected a tool.

After changing the implementation,
every question now goes directly
to the Agent.

The Agent decides

• whether a tool is required

• which tool should be used

• when to return the final answer

This is much closer to how
LangChain Agents are designed
to work.

""")
# --------------------------------------------------
# Task 3
# --------------------------------------------------

st.header("Math Chat")

st.write(
    "Ask any arithmetic, percentage or algebra question."
)

# ------------------------------
# Session State
# ------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Display Previous Conversation
# ------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


user_question = st.chat_input(

    "Enter your math question..."

)

# ------------------------------
# Send Question to Agent
# ------------------------------

if user_question:

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_question

        }

    )

    with st.chat_message("user"):

        st.markdown(user_question)


    with st.spinner("Agent is thinking..."):

        result = ask_agent(user_question)


    answer = result["output"]


    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer

        }

    )


    with st.chat_message("assistant"):

        st.markdown(answer)


    # ----------------------------------
    # Show Tool Selection
    # ----------------------------------

    if result["intermediate_steps"]:

        with st.expander(

            "Agent Reasoning"

        ):

            st.write(

                "The agent selected the following tool(s):"

            )

            for i, step in enumerate(

                result["intermediate_steps"]

            ):

                st.write(

                    f"Step {i+1}"

                )

                st.code(str(step))

    else:

        with st.expander(

            "Agent Reasoning"

        ):

            st.write(

                "The agent answered without using a tool."

            )


# ------------------------------
# Conversation Summary
# ------------------------------

st.divider()

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

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Questions",

        user_count

    )

with col2:

    st.metric(

        "Responses",

        assistant_count

    )


if st.button("Clear Conversation"):

    st.session_state.messages = []

    st.rerun()


st.info("""

Initially I manually checked the question
to decide whether it was arithmetic or algebra.

After changing the implementation,
every question now goes directly to the Agent.

The Agent itself decides

• whether a tool is needed

• which tool should be selected

• when to return the final answer

Using session_state also helped me keep
the conversation until the user clears it.

""")

# --------------------------------------------------
# Task 4
# --------------------------------------------------

st.header("Testing the Agent")

st.write(
    "These sample questions were used to verify "
    "that the agent selects the appropriate tool."
)

examples = [

    "Calculate 125 + 375",

    "Calculate (45 * 8) + 90",

    "What is 18% of 650?",

    "Solve x + 15 = 40",

    "Solve 5*x = 60",

    "What is Machine Learning?"

]

example = st.selectbox(

    "Choose a question",

    examples

)

if st.button("Run Test"):

    result = ask_agent(example)

    st.subheader("Question")

    st.write(example)

    st.subheader("Answer")

    st.success(result["output"])

    st.subheader("Tool Calls")

    if result["intermediate_steps"]:

        for i, step in enumerate(result["intermediate_steps"]):

            st.write(f"Tool Call {i+1}")

            st.code(str(step))

    else:

        st.info("No external tool was required.")
# --------------------------------------------------
# Validation
# --------------------------------------------------

st.divider()

st.header("Try Your Own Question")

custom_question = st.text_input(

    "Enter any mathematical question"

)

if st.button("Solve"):

    if custom_question.strip() == "":

        st.warning("Please enter a question.")

    else:

        try:

            result = ask_agent(custom_question)

            st.success(result["output"])

            if result["intermediate_steps"]:

                with st.expander("Tool Activity"):

                    for step in result["intermediate_steps"]:

                        st.code(str(step))

        except Exception as e:

            st.error("Unable to process your request.")

            st.code(str(e))
st.divider()

st.header("My Observations")

st.write("""

Initially I manually identified arithmetic
and algebra questions in Python.

After rebuilding the application,
every question now goes directly to the Agent.

The agent itself decides whether a tool
should be used.

Using SymPy also improved equation solving
compared to my earlier implementation.

I also tested a few invalid inputs.
Adding exception handling prevented the
application from crashing.

""")

st.divider()

st.subheader("Validation Testing")

invalid_inputs = [

    "",

    "x+=",

    "25//",

    "Solve x=",

    "abc"

]

for item in invalid_inputs:

    st.code(item)

st.write("""

These inputs were tested to check whether
the application crashes.

Instead of terminating unexpectedly,
the application displays an appropriate
error message.

""")

# --------------------------------------------------
# Final Reflection
# --------------------------------------------------

st.divider()

st.header("What I Learned")

st.write("""

This assignment helped me understand that an
AI Agent is different from a normal LLM.

A language model can answer questions directly,
but an Agent first decides whether a tool
is required before generating the response.

I also learned that SymPy is much safer than
using eval() for solving mathematical problems.

While rebuilding this assignment, I realised
that manually checking whether a question
contained '+' or '=' was not the right approach.
Instead, the Agent should make that decision.

Using Streamlit session_state also helped me
maintain the conversation history until
the user cleared the chat.

""")