# Python Foundry Agent SDK Demos



## Prerequisites

- **Azure subscription** with sufficient permissions to create resources
- **Azure Developer CLI (azd)** installed ([Install guide](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd))
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- **Git** (to clone this repository)
- **VS Code** or **GitHub Codespaces** with Jupyter extension (recommended)

### Required Azure Permissions

You'll need permissions to:

- Create resource groups
- Deploy Bicep templates
- Create and manage:
  - Azure AI Search services
  - Microsoft Foundry projects
  - Azure OpenAI model deployments
- Assign Azure RBAC roles

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/microsoft/mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search.git
cd mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Deploy with azd

```bash
azd auth login
azd up
```

This will:

- Provision all Azure resources
- Fetch API keys and write a `.env` file
- Create search indexes and upload sample data

> **Note:** After setup, you'll need to manually add `GITHUB_TOKEN` to your `.env` file for Part 4 (authenticated MCP source).

### 4. Start the Lab

Open the [notebooks](../../notebooks) folder in VS Code and **start with `part1-multiple-knowledge-sources.ipynb`**.

## Repository Structure

### `scripts/`

| File | Description |
|------|-------------|
| `create_foundry_agent.py` | Creates 20 Foundry agents with different enterprise personas (HR advisor, IT helpdesk, budget analyst, etc.) using the Azure AI Projects SDK. |
| `create_kb_agent.py` | Creates a knowledge-base-grounded wellness advisor agent that uses Azure AI Search indexes (healthdocs/hrdocs) as its sole knowledge source via an MCP tool. |
| `quality_eval.py` | Runs a quality evaluation against the KB-only wellness advisor agent, testing both in-scope and out-of-scope queries with evaluators for task adherence, intent resolution, and groundedness. |
| `red_team_scan.py` | Runs an AI red teaming scan against the wellness advisor agent, testing for safety risks (self-harm, sexual content, violence, sensitive data leakage) using attack strategies and custom taxonomies. |
| `create-indexes.py` | Standalone script to manually create Azure AI Search indexes and upload sample data (alternative to the `azd` post-provision hook). |
| `locustfile.py` | Locust load test that sends random prompts to all created Foundry agents, useful for stress-testing agent throughput and latency. |
| `requirements.txt` | Python dependencies for all scripts. |

#### `scripts/eval_output/`

Contains output from quality evaluations and the test query dataset (`test_queries.jsonl`).

#### `scripts/red_team_output/`

Contains output from red team scans for each agent.

### `data/`

| Folder | Description |
|--------|-------------|
| `ai-search-data/healthdocs/` | Source health-related documents for the AI Search index. |
| `ai-search-data/hrdocs/` | Source HR documents (e.g., `Zava_Company_Overview.md`) for the AI Search index. |
| `index-data/` | Exported JSONL data and index schema (`index.json`) used to create the Azure AI Search indexes. |

### `infra/`

| File | Description |
|------|-------------|
| `main.bicep` | Bicep template that provisions all Azure resources (AI Search, Foundry project, OpenAI deployments). |
| `main.parameters.json` | Parameters for the Bicep deployment. |
| `setup-knowledge.ps1` | PowerShell script to create search indexes and upload sample data. |
| `hooks/` | `azd` lifecycle hooks (`postprovision.ps1`/`.sh`) that run after provisioning. |
| `deploy-yourself/` | Standalone instructions for manually deploying outside of `azd`. |

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
