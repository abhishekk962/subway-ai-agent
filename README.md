# Subway AI Agent

This repository contains detailed instructions on how to build a Subway AI Agent capable of handling complex queries related to real-time train arrivals.

<p align="center">
  <img 
    width="200" 
    height="auto" 
    alt="image" 
    src="https://github.com/user-attachments/assets/0ecc14ca-9cd1-4703-a6e3-3279e5e224c1"
    style="border-radius:50%;"
  />
</p>

## Overview

- **`agent.ipynb`**: A Python notebook that provides an overview of how the agent is built.
- **Local Development Server**: The project is structured to verify and test your agent using LangSmith.
- **Agent Chat UI**: A ready-made simple interface to interact with your agent.

## Prerequisites

- **Python**: > 3.11
- **Groq API Key**: Required for the LLM provider. [Get one here](http://console.groq.com/docs/quickstart).
- **LangSmith Account & API Key**: Required if you want to use the web-based interface or LangSmith features. [Sign up here](https://docs.langchain.com/oss/python/langchain/studio#prerequisites).

## Installation

1.  Set up the environment:
    ```bash
    pip install langchain langchain-groq "langgraph-cli[inmem]"
    ```
    *(Note: If you are running the notebook only, you can switch the LLM provider if preferred, but Groq is the default).*

2.  Environment Configuration:
    - Copy the `.env.example` file to `.env`.
    - Add your API keys to the `.env` file.

## Usage

### Running the Notebook

Open `agent.ipynb` to explore the agent's logic and testing instructions.

### Running the Local Development Server

1.  Start the local server:
    ```bash
    langgraph dev
    ```
2.  The deployment URL should be available at `http://127.0.0.1:2024`.
3.  The graph ID is `agent` (as defined in `agent.py`).

### Using Agent Chat UI

The [Agent Chat UI](https://agentchat.vercel.app/) serves as a frontend for the agent.

1.  Ensure your local server is running.
2.  Go to [https://agentchat.vercel.app/](https://agentchat.vercel.app/).
3.  Connect to your local agent instance.

## Resources

- [Agent Chat UI Documentation](https://docs.langchain.com/oss/python/langchain/ui)
- [LangSmith Studio Documentation](https://docs.langchain.com/oss/python/langchain/studio) - Instructions on running the development server and structuring the project.
