# Assignment 35

## Objective

The objective of this assignment was to build a Text-to-Math AI Agent using LangChain and Streamlit. The agent understands mathematical questions written in natural language, uses a calculator tool whenever required, and provides step-by-step solutions.

---

## GitHub Repository

(Add GitHub Link)

---

## Streamlit Deployment

(Add Streamlit Link)

---

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

---

## Features

- Text-to-Math AI Agent
- Calculator Tool
- LangChain Tool Calling
- Step-by-step Problem Solving
- Arithmetic Questions
- Percentage Questions
- Algebra Questions
- Streamlit Chat Interface
- Session State
- Conversation History

---

## What I Learned

This assignment helped me understand that solving mathematical word problems involves more than just generating text. An AI Agent first interprets the user's request, decides whether a calculation is needed, and then uses the appropriate tool before generating the final answer.

I also learned how Streamlit session state preserves conversation history, making the application behave like a real interactive assistant rather than a single-use calculator.

---

## Challenges

One challenge was handling different styles of mathematical questions, such as arithmetic, percentages, and simple algebra, using the same workflow.

Another challenge was maintaining the conversation across multiple interactions. After implementing `st.session_state`, the application was able to retain previous questions and answers until the conversation was cleared.

---

## Conclusion

This assignment provided practical experience in combining LangChain Agents, tool calling, and Streamlit to build an interactive Text-to-Math application. It also strengthened my understanding of how AI Agents can improve accuracy by using external tools instead of relying only on language generation.