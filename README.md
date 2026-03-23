# Python Foundry Agent SDK Demos

This repository demonstrates how to build, evaluate, and load-test AI agents using the [Azure AI Foundry Agent SDK](https://learn.microsoft.com/azure/ai-services/agents/) and [Azure AI Search](https://learn.microsoft.com/azure/search/). It includes scripts to create prompt-based Foundry agents, ground them in enterprise knowledge bases via MCP tools, run quality evaluations, perform AI red teaming scans, and stress-test agent endpoints with Locust. Infrastructure is provisioned with `azd` and Bicep.

## Prerequisites

- **Azure subscription** with sufficient permissions to create resources
- **Azure Developer CLI (azd)** installed ([Install guide](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd))
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- **Git** (to clone this repository)
- **VS Code** or **GitHub Codespaces** with Jupyter extension (recommended)

### Required Azure permissions

You'll need permissions to:

- Create resource groups
- Deploy Bicep templates
- Create and manage:
  - Azure AI Search services
  - Microsoft Foundry projects
  - Azure OpenAI model deployments
- Assign Azure RBAC roles

## Getting started

### Clone the repository

```bash
git clone https://github.com/pamelafox/python-foundryagent-demos.git
cd python-foundryagent-demos
```

### Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r scripts/requirements.txt
```

### Deploy with the Azure Developer CLI

1. Login to Azure:

    ```bash
    azd auth login
    ```

2. Run the deployment:

    ```bash
    azd up
    ```

    This will:

    - Provision all Azure/Foundry resources
    - Write a `.env` file
    - Create search indexes and upload sample data

### 4. Create Foundry agents

Create 20 different Foundry prompt agents with various enterprise personas:

```bash
python scripts/create_foundry_agents.py
```

Create a Foundry agent grounded in Foundry IQ (Azure AI Search knowledge bases):

```bash
python scripts/create_kb_agent.py
```

Run a one-off quality evaluation against the Foundry IQ agent:

```bash
python scripts/quality_eval.py
```

Run a one-off red-teaming scan against the Foundry IQ agent:

```bash
python scripts/red_team_scan.py
```

Setup continuous evaluation for the Foundry IQ agent:

```bash
python scripts/setup_continuous_eval.py
```

Setup a daily scheduled quality evaluation (runs at 9 AM UTC):

```bash
python scripts/scheduled_eval.py
```

Setup a daily scheduled red-teaming run (runs at 9 AM UTC):

```bash
python scripts/scheduled_red_team.py
```

Simulate user traffic across all agents to populate monitoring charts:

```bash
locust -f scripts/locustfile.py
```

## Cleanup

To delete all resources and avoid ongoing charges:

```bash
azd down
```

## Additional Resources

- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Microsoft Foundry Community Discord](https://aka.ms/AIFoundryDiscord-Ignite25)
