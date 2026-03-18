# [MVP Summit 2026](https://mvp.microsoft.com)

## LAB006: Build Agentic Knowledge Bases: Next-Level RAG with Azure AI Search

### Session Description

In this hands-on lab, you'll build an Azure AI Search Knowledge Base powered by agentic RAG and extend it with Model Context Protocol (MCP) knowledge sources. You'll connect the Knowledge Base to both indexed enterprise content and live MCP servers, enabling smart, tool-driven source selection across multiple systems. By the end, you'll have a working Agentic Knowledge Base that itself can be consumed as an MCP endpoint—so agents and developer tools can retrieve grounded answers over enterprise data through standard MCP connections.

### Lab Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `part1-multiple-knowledge-sources.ipynb` | Build a multi-source knowledge base with indexed HR and health documents |
| 2 | `part2-kb-as-mcp-endpoint.ipynb` | Consume the knowledge base as an MCP endpoint from GitHub Copilot CLI |
| 3 | `part3-mcp-unauthenticated.ipynb` | Add a non-authenticated MCP source (Microsoft Learn) |
| 4 | `part4-mcp-authenticated.ipynb` | Add an authenticated MCP source (GitHub) with Bearer token |
| 5 | `part5-foundry-agent.ipynb` | Connect the knowledge base to a Microsoft Foundry Agent |

### Getting Started

See [infra/deploy-yourself/README.md](infra/deploy-yourself/README.md) for self-deployment instructions, or follow the guided lab instructions in the `lab/` folder.


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
