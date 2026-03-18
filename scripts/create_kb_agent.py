"""Create a KB-grounded wellness advisor agent (company docs only, no web).

Uses the foundry-agent-knowledge-base (healthdocs/hrdocs AI Search indexes)
as the sole knowledge source via an MCP tool.

Usage:
    python notebooks/create_kb_agent.py
"""

import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv(override=True)

AGENT_NAME = "kb-only-wellness-advisor"
KNOWLEDGE_BASE_NAME = "foundry-agent-knowledge-base"

project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_OPENAI_CHATGPT_DEPLOYMENT"]
search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
project_connection_name = os.environ["PROJECT_CONNECTION_NAME"]

credential = AzureCliCredential(process_timeout=60)
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

mcp_endpoint = (
    f"{search_endpoint}/knowledgebases/{KNOWLEDGE_BASE_NAME}"
    f"/mcp?api-version=2025-11-01-Preview"
)

agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=model_deployment,
        instructions=(
            "You are an employee wellness advisor. "
            "You must use the knowledge base to answer all questions. "
            "You must never answer from your own knowledge under any circumstances. "
            "If the knowledge base does not contain the answer, respond with "
            "'I don't have information about that in my knowledge base.'"
        ),
        tools=[
            MCPTool(
                server_label="knowledge-base",
                server_url=mcp_endpoint,
                require_approval="never",
                allowed_tools=["knowledge_base_retrieve"],
                project_connection_id=project_connection_name,
            )
        ],
    ),
)

print(f"Agent '{agent.name}' created — version: {agent.version}")
