# Assignment 35

## Objective

The objective of this assignment was to build a Text-to-Math Agent using LangChain and Streamlit. The application accepts mathematical questions written in natural language and lets the agent decide which tool should be used to solve them.

---
## github link 

https://github.com/nandita141099/assignment35

## streamit link

https://assignment35-myd9cxqymrbdc8wrmxyxzn.streamlit.app/

## Project Structure

```
Assignment35/

app.py
README.md
requirements.txt
.env
.gitignore
```

---

## Setup

Create a `.env` file.

```text
OPENAI_API_KEY=your_api_key
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run

```bash
streamlit run app.py
```

---

## Features

- LangChain Tool Calling Agent
- Calculator Tool
- Equation Solver Tool
- SymPy Integration
- Streamlit Interface
- Session State
- Conversation History
- Tool Call Display
- Error Handling

---

## What I Learned

Before this assignment I thought the application itself should decide whether a calculator or equation solver was required.

While rebuilding it, I understood that this decision should be made by the LangChain Agent instead. The application only sends the user's question to the agent, and the agent decides which tool should be called.

I also learned why SymPy is preferred over `eval()`. It is safer and provides much better support for solving equations.

Another useful concept was Streamlit's `session_state`, which helped preserve conversation history without using an external database.

---

## Challenges

The main challenge was understanding how tool-calling agents actually work.

Initially I wrote Python code to identify arithmetic and algebra questions manually. After revisiting the LangChain documentation, I changed the design so that every question goes directly to the agent, allowing it to choose the appropriate tool.

I also spent time testing invalid inputs to make sure the application displayed meaningful error messages instead of crashing.

---

## Conclusion

This assignment helped me understand how LangChain Agents, tool calling, SymPy and Streamlit can be combined to build an interactive mathematical assistant. It also showed me the difference between writing application logic manually and allowing the agent to make decisions using available tools.