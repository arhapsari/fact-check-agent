# Fact-Check Agent

A multi-agent fact-checking system that verifies user claims using Wikipedia as a data source. Built with Google's Agents Development Kit (ADK) and LangChain.

## Overview

This project implements an automated fact-checking workflow with two specialized agents:

1. **Fact Researcher**: Searches Wikipedia to gather evidence relevant to a claim
2. **Fact Checker**: Evaluates the claim against research data and provides a verdict

The system uses a sequential workflow where the researcher gathers evidence first, and then the fact-checker evaluates the claim based on that evidence.

## Features

- Multi-agent architecture using Google ADK
- Wikipedia integration for evidence gathering
- Automatic claim verification with detailed reasoning
- Structured verdicts: TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIED
- Google Cloud logging integration
- Environment variable configuration

## Prerequisites

- Python 3.x
- Google Cloud credentials (for authentication)
- `.env` file with `MODEL` environment variable set

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fact-check-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```
MODEL=<your-model-name>
```

4. Configure Google Cloud authentication:
Set up your Google Cloud credentials for authentication.

## Usage

Import and use the fact-checking workflow:

```python
from agent import root_agent, fact_check_workflow

# Use the root agent to interact with users
# or directly call the fact_check_workflow for automated fact-checking
```

The workflow will:
1. Accept a claim from the user
2. Research the claim using Wikipedia
3. Evaluate the claim against the gathered evidence
4. Return a verdict with detailed reasoning

## Project Structure

```
fact-check-agent/
├── __init__.py           # Package initialization
├── agent.py              # Main agent definitions and workflow
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Dependencies

- `google-adk==1.14.0` - Google's Agents Development Kit
- `langchain-community==0.3.27` - LangChain community tools
- `wikipedia==1.4.0` - Wikipedia API client

## How It Works

1. The **Greeter Agent** provides an entry point and collects the user's claim
2. The **Fact Researcher Agent** uses Wikipedia tools to search for relevant information
3. The **Fact Checker Agent** analyzes the research data and provides a final verdict with supporting evidence