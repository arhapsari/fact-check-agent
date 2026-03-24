import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# Greet user and save their claim

def add_claim_to_state(
    tool_context: ToolContext, claim: str
) -> dict[str, str]:
    """Saves the user's initial claim to the state."""
    tool_context.state["CLAIM"] = claim
    logging.info(f"[State updated] Added to CLAIM: {claim}")
    return {"status": "success"}

# Configuring the Wikipedia Tool
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# 1. Researcher Agent
fact_researcher = Agent(
    name="fact_researcher",
    model=model_name,
    description="Researches a given claim using Wikipedia to find relevant evidence.",
    instruction="""
    You are a meticulous research assistant. Your goal is to gather evidence to verify the user's CLAIM.
    You have access to a tool to search Wikipedia.

    Analyze the user's CLAIM. Search Wikipedia for information relevant to the claim.
    Synthesize the results from the tool into preliminary data outputs containing evidence.

    CLAIM:
    { CLAIM }
    """,
    tools=[
        wikipedia_tool
    ],
    output_key="research_data" # A key to store the research findings
)

# 2. Fact Checker Agent
fact_checker = Agent(
    name="fact_checker",
    model=model_name,
    description="Evaluates the claim based on research data and provides a verdict.",
    instruction="""
    You are a rigorous Fact-Checker. Your task is to evaluate the user's CLAIM
    against the gathered RESEARCH_DATA and provide a final verdict.

    - First, state the original claim.
    - Second, provide a verdict: TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIED.
    - Third, provide a clear, objective explanation based on the research data.
    - Cite the specific information from the research data that supports your verdict.

    CLAIM:
    { CLAIM }

    RESEARCH_DATA:
    { research_data }
    """
)

fact_check_workflow = SequentialAgent(
    name="fact_check_workflow",
    description="The main workflow for fact-checking a user's claim.",
    sub_agents=[
        fact_researcher, # Step 1: Gather evidence
        fact_checker,    # Step 2: Evaluate claim and format the final response
    ]
)

root_agent = Agent(
    name="greeter",
    model=model_name,
    description="The main entry point for the Fact Checker Agent.",
    instruction="""
    - Let the user know you are a Fact-Checking Assistant and ask them what claim they would like you to verify.
    - When the user provides a claim, use the 'add_claim_to_state' tool to save their response.
    - After using the tool, transfer control to the 'fact_check_workflow' agent.
    """,
    tools=[add_claim_to_state],
    sub_agents=[fact_check_workflow]
)