# Deploy to Your Own Azure Subscription

This folder contains resources for deploying the LAB006 Knowledge Base infrastructure to your own Azure subscription.

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
