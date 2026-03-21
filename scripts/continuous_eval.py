"""Set up a continuous evaluation rule for a Foundry agent.

Unlike quality_eval.py (which runs a one-time batch evaluation against a test
dataset), this script creates a persistent rule that automatically evaluates
sampled agent responses as they occur in production.

Based on:
https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard?tabs=python#set-up-continuous-evaluation

Prerequisites:
    - The project managed identity must have the 'Azure AI User' role.
    - An Application Insights resource must be connected to the project.

Usage:
    python scripts/create_kb_agent.py   # create the agent first
    python scripts/continuous_eval.py
"""

import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ContinuousEvaluationRuleAction,
    EvaluationRule,
    EvaluationRuleEventType,
    EvaluationRuleFilter,
)
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv(override=True)

AGENT_NAME = "kb-only-wellness-advisor"

project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_OPENAI_CHATGPT_DEPLOYMENT"]

credential = AzureCliCredential(process_timeout=60)
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

# ---------------------------------------------------------------------------
# 1. Look up the latest agent version
# ---------------------------------------------------------------------------
agent_versions = list(project_client.agents.list_versions(agent_name=AGENT_NAME))
if not agent_versions:
    raise SystemExit(f"No versions found for agent '{AGENT_NAME}'. Run create_kb_agent.py first.")
agent_version = agent_versions[-1]
print(f"Agent: {agent_version.name}  version: {agent_version.version}")

# ---------------------------------------------------------------------------
# 2. Create the evaluation (continuous data source)
# ---------------------------------------------------------------------------
openai_client = project_client.get_openai_client()

testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "Task Adherence",
        "evaluator_name": "builtin.task_adherence",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
        "initialization_parameters": {"deployment_name": model_deployment},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "Groundedness",
        "evaluator_name": "builtin.groundedness",
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{sample.output_items}}",
        },
        "initialization_parameters": {"deployment_name": model_deployment},
    },
    {
        "type": "azure_ai_evaluator",
        "name": "Violence Detection",
        "evaluator_name": "builtin.violence",
    },
]

eval_object = openai_client.evals.create(
    name=f"Continuous Evaluation - {AGENT_NAME}",
    data_source_config={"type": "azure_ai_source", "scenario": "responses"},
    testing_criteria=testing_criteria,
)
print(f"Created evaluation: {eval_object.id}")

# ---------------------------------------------------------------------------
# 3. Create the continuous evaluation rule
# ---------------------------------------------------------------------------
rule_id = f"continuous-eval-{AGENT_NAME}"

continuous_eval_rule = project_client.evaluation_rules.create_or_update(
    id=rule_id,
    evaluation_rule=EvaluationRule(
        display_name=f"Continuous Eval - {AGENT_NAME}",
        description=f"Evaluates sampled responses from {AGENT_NAME} on completion",
        action=ContinuousEvaluationRuleAction(
            eval_id=eval_object.id,
            max_hourly_runs=100,
        ),
        event_type=EvaluationRuleEventType.RESPONSE_COMPLETED,
        filter=EvaluationRuleFilter(agent_name=agent_version.name),
        enabled=True,
    ),
)
print(f"Continuous evaluation rule created: {continuous_eval_rule.id}  ({continuous_eval_rule.display_name})")
print("\nGenerate agent traffic, then check the Monitor tab in the Foundry portal to see results.")
