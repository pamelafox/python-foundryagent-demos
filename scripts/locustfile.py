"""Locust load test for Foundry agents.

Usage:
    locust -f notebooks/locustfile.py --headless -u 10 -r 2 -t 5m
    # Or with the web UI:
    locust -f notebooks/locustfile.py
    # Target a single agent:
    LOCUST_AGENT=employee-wellness-advisor locust -f notebooks/locustfile.py
"""

import os
import random
import time

from locust import HttpUser, between, events, tag, task

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)

# Agent names must match what create_foundry_agent.py created
AGENT_NAMES = [
    "hr-policy-advisor",
    "it-helpdesk-agent",
    "security-compliance-checker",
    "onboarding-guide",
    "contract-summarizer",
    "incident-response-coordinator",
    "budget-analyst",
    "project-status-reporter",
    "vendor-evaluation-advisor",
    "data-governance-steward",
    "cloud-architecture-reviewer",
    "change-management-advisor",
    "legal-risk-flagger",
    "meeting-summarizer",
    "sla-monitor",
    "procurement-assistant",
    "knowledge-base-curator",
    "executive-briefing-writer",
    "api-integration-advisor",
    "employee-wellness-advisor",
    "kb-only-wellness-advisor"
]

# Sample prompts per agent — Locust picks a random agent and prompt each task
AGENT_PROMPTS = {
    "hr-policy-advisor": [
        "How many PTO days do new employees get?",
        "What is the policy on remote work?",
        "How do I request parental leave?",
        "What are the guidelines for performance improvement plans?",
    ],
    "it-helpdesk-agent": [
        "My VPN keeps disconnecting, how do I fix it?",
        "How do I reset my Active Directory password?",
        "I need to install VS Code on my work laptop, what's the process?",
        "My Outlook calendar is not syncing with Teams.",
    ],
    "security-compliance-checker": [
        "Are we compliant with SOC 2 Type II for our data pipeline?",
        "What GDPR controls do we need for storing EU customer emails?",
        "Review our S3 bucket configuration for public access risks.",
        "What ISO 27001 controls apply to our CI/CD pipeline?",
    ],
    "onboarding-guide": [
        "I'm starting next Monday, what should I do on day one?",
        "Which training modules are mandatory in the first week?",
        "Who should I meet during my first 30 days?",
        "How do I set up my development environment?",
    ],
    "contract-summarizer": [
        "Summarize the key terms of a 3-year SaaS agreement with auto-renewal.",
        "What are typical liability caps in enterprise software contracts?",
        "Flag any risks in a contract with a 60-day termination notice.",
        "What SLA guarantees should I look for in a cloud hosting contract?",
    ],
    "incident-response-coordinator": [
        "We have a P1 outage on the payment service. What are the first steps?",
        "Draft a stakeholder communication for a database failover incident.",
        "How should we structure a post-incident review?",
        "Classify this incident: API latency spiked to 5s for 20 minutes.",
    ],
    "budget-analyst": [
        "Forecast Q3 cloud infrastructure spend based on 15% growth.",
        "We're 20% over budget on contractors — what are our options?",
        "Prepare an executive summary comparing OpEx vs CapEx for a new data center.",
        "Identify the top 3 cost-saving opportunities in our SaaS subscriptions.",
    ],
    "project-status-reporter": [
        "Generate a status report: migration is 60% done, blocked on DB schema approval.",
        "Summarize project health: 3 of 5 milestones complete, 2 weeks behind schedule.",
        "Draft an executive update for the platform modernization initiative.",
        "What format works best for a weekly status report to the CTO?",
    ],
    "vendor-evaluation-advisor": [
        "Compare Datadog vs Azure Monitor for enterprise observability.",
        "What criteria should we use to evaluate CRM vendors?",
        "Create a weighted scorecard for evaluating 3 identity providers.",
        "What security certifications should an enterprise SaaS vendor have?",
    ],
    "data-governance-steward": [
        "How should we classify customer PII data?",
        "What's the recommended retention policy for financial transaction logs?",
        "Advise on access control for a shared analytics data lake.",
        "How do we implement data lineage tracking for our ETL pipelines?",
    ],
    "cloud-architecture-reviewer": [
        "Review a 3-tier architecture on Azure with App Service, SQL, and Redis.",
        "Is a single-region deployment acceptable for a business-critical app?",
        "What's the best strategy for multi-region failover on Azure?",
        "Evaluate our use of Azure Functions vs Container Apps for microservices.",
    ],
    "change-management-advisor": [
        "We're migrating from Slack to Teams — how do we manage the transition?",
        "Draft a communication plan for a department restructure.",
        "What does the ADKAR model recommend for overcoming resistance to change?",
        "How do we measure adoption success after rolling out a new ERP system?",
    ],
    "legal-risk-flagger": [
        "Flag risks in a proposal to scrape public websites for competitive analysis.",
        "What legal issues arise from using open-source software in a commercial product?",
        "Review a non-compete clause that restricts employees for 2 years.",
        "Are there liability concerns with using AI-generated content in marketing?",
    ],
    "meeting-summarizer": [
        "Summarize: We decided to delay the launch by 2 weeks. John owns the revised timeline. Open question: do we need extra QA?",
        "Extract action items from: Maria will draft the RFP by Friday, Dev team to estimate API work by next Tuesday.",
        "Summarize a sprint retrospective where the team discussed flaky tests and deployment bottlenecks.",
        "Create meeting notes for a design review of the new checkout flow.",
    ],
    "sla-monitor": [
        "Calculate uptime percentage: 43,150 minutes up out of 43,200 in a 30-day month.",
        "We had 3 outages totaling 45 minutes. Are we within our 99.9% SLA?",
        "What credit should we offer for missing a 99.95% uptime SLA by 0.02%?",
        "Recommend monitoring improvements after 2 consecutive SLA breaches.",
    ],
    "procurement-assistant": [
        "Draft an RFP for a managed Kubernetes hosting provider.",
        "Compare these 3 vendor quotes for annual licenses and pick the best value.",
        "What approval thresholds apply to purchases over $50,000?",
        "Track the status of PO-2024-1587 for new developer laptops.",
    ],
    "knowledge-base-curator": [
        "Review this KB article on VPN setup for accuracy and clarity.",
        "What topics are missing from our internal IT knowledge base?",
        "Suggest improvements to our article template for troubleshooting guides.",
        "How often should knowledge base articles be reviewed for freshness?",
    ],
    "executive-briefing-writer": [
        "Write a 1-page briefing on the risks of technical debt in our platform.",
        "Summarize the competitive landscape for enterprise AI assistants.",
        "Draft a memo recommending we invest in a data mesh architecture.",
        "Prepare a quarterly technology highlights briefing for the board.",
    ],
    "api-integration-advisor": [
        "What's the best auth strategy for a public-facing REST API?",
        "How should we handle API versioning for backward compatibility?",
        "Review this API contract for a partner integration.",
        "What rate limiting strategy works for a multi-tenant API?",
    ],
    "employee-wellness-advisor": [
        "What are some tips for managing stress during a big product launch?",
        "How should I set up my home office ergonomically?",
        "What employee assistance programs are typically available?",
        "How can I improve work-life balance with a demanding project schedule?",
    ],
    "kb-only-wellness-advisor": [
        "What health plans does Zava offer?",
        "Who is the CEO of Zava?",
        "What is Zava's parental leave policy?",
        "What mental health benefits does Zava provide?",
        "Tell me about Zava's company culture.",
        "What is Zava's remote work policy?",
        "How do I enroll in Zava's dental plan?",
        "What are Zava's core values?",
        # Intentionally out-of-scope questions to test KB grounding and safety:
        "What are the best exercises to reduce lower back pain?",
        "How do I file my taxes as a freelancer?",
        "Can you recommend a good therapist in London?",
        "What is the capital of France?",
        "Write me a Python script to sort a list.",
        "Explain how to set up a Kubernetes cluster."
    ],
}

# Initialize Foundry client once at module load time
project_endpoint = os.environ["PROJECT_ENDPOINT"]

_project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)
_openai_client = _project_client.get_openai_client()

# Optionally restrict to a single agent via LOCUST_AGENT env var
_target_agent = os.environ.get("LOCUST_AGENT")
if _target_agent:
    if _target_agent not in AGENT_PROMPTS:
        # Use generic prompts for agents not in the predefined list
        AGENT_PROMPTS[_target_agent] = [
            "Hello, what can you help me with?",
            "Summarize your main capabilities.",
            "What topics are you most knowledgeable about?",
            "Give me an example of a question you can answer well.",
        ]
    ACTIVE_AGENTS = [_target_agent]
else:
    ACTIVE_AGENTS = AGENT_NAMES

# Agent references — just name + type, no version lookup needed
AGENT_REFS = {name: {"name": name, "type": "agent_reference"} for name in ACTIVE_AGENTS}

print(f"{len(AGENT_REFS)} agent(s) ready for load testing.\n")


class FoundryAgentUser(HttpUser):
    """Simulates a user chatting with random Foundry agents."""

    # Wait 1-3s between tasks to simulate realistic user behavior
    wait_time = between(1, 3)

    # host is required by Locust but we use the SDK directly
    host = project_endpoint

    @tag("single")
    @task
    def chat_with_random_agent(self):
        agent_name = random.choice(ACTIVE_AGENTS)
        prompt = random.choice(AGENT_PROMPTS[agent_name])
        agent_ref = AGENT_REFS[agent_name]

        start_time = time.perf_counter()
        exception = None
        response_length = 0

        try:
            conversation = _openai_client.conversations.create()
            response = _openai_client.responses.create(
                conversation=conversation.id,
                input=prompt,
                extra_body={"agent_reference": agent_ref},
            )
            output = response.output_text
            response_length = len(output)
        except Exception as e:
            exception = e

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Manual fire is required because we use the Azure SDK directly
        # instead of Locust's built-in HTTP client, which auto-tracks latency.
        events.request.fire(
            request_type="foundry_agent",
            name=f"chat/{agent_name}",
            response_time=elapsed_ms,
            response_length=response_length,
            exception=exception,
            context={},
        )

    @tag("multi")
    @task(weight=3)
    def multi_turn_conversation(self):
        """Simulate a 2-3 turn conversation with one agent."""
        agent_name = random.choice(ACTIVE_AGENTS)
        prompts = AGENT_PROMPTS[agent_name]
        agent_ref = AGENT_REFS[agent_name]
        num_turns = random.randint(2, min(3, len(prompts)))

        try:
            conversation = _openai_client.conversations.create()
        except Exception as e:
            events.request.fire(
                request_type="foundry_agent",
                name=f"multi_turn/{agent_name}",
                response_time=0,
                response_length=0,
                exception=e,
                context={},
            )
            return

        selected_prompts = random.sample(prompts, num_turns)
        for i, prompt in enumerate(selected_prompts):
            start_time = time.perf_counter()
            exception = None
            response_length = 0

            try:
                response = _openai_client.responses.create(
                    conversation=conversation.id,
                    input=prompt,
                    extra_body={"agent_reference": agent_ref},
                )
                response_length = len(response.output_text)
            except Exception as e:
                exception = e

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            events.request.fire(
                request_type="foundry_agent",
                name=f"multi_turn/{agent_name}/turn_{i + 1}",
                response_time=elapsed_ms,
                response_length=response_length,
                exception=exception,
                context={},
            )

            if exception:
                break
