
# Lab 006: Build Agentic Knowledge Bases with Azure AI Search

These instructions are for participants of the **instructor-led** Workshop "Build Agentic Knowledge Bases: Next-Level RAG with Azure AI Search" at MVP Summit 2026.

## Lab Overview

In this hands-on lab, you'll build an Azure AI Search Knowledge Base powered by agentic RAG and extend it with Model Context Protocol (MCP) knowledge sources. You'll connect the Knowledge Base to both indexed enterprise content and live MCP servers, enabling smart, tool-driven source selection across multiple systems. By the end, you'll have a working Agentic Knowledge Base that itself can be consumed as an MCP endpoint and wired into a Microsoft Foundry Agent.

## Pre-Requisites

## Prerequisites

To get the most out of this lab, you should have a basic understanding of the following:

- **Python and Jupyter Notebooks** – You will write and run code cells directly inside a Jupyter environment.  
- **Azure Fundamentals** – Familiarity with Azure services and concepts such as resource groups, storage accounts, and authentication.  
- **Retrieval-Augmented Generation (RAG)** – A general understanding of how LLMs use external data for grounding will help you better follow the agentic retrieval flow.  
- **Azure AI Search and OpenAI** – Basic knowledge of what these services do (indexing, querying, embeddings, completions) is helpful but not required.

> [!NOTE]  
> You do **not** need to provision any Azure services or deploy infrastructure manually for this lab. All required resources including Azure AI Search, OpenAI deployments, and data sources — are pre-created and ready to use.

## Get Started

To begin, open the **notebooks/** folder and start with **part1-multiple-knowledge-sources.ipynb**. Work through all 5 notebooks sequentially:

1. **part1-multiple-knowledge-sources.ipynb** — Build a multi-source knowledge base
2. **part2-kb-as-mcp-endpoint.ipynb** — Expose KB as an MCP endpoint
3. **part3-mcp-unauthenticated.ipynb** — Add Microsoft Learn as a live MCP source
4. **part4-mcp-authenticated.ipynb** — Add GitHub as an authenticated MCP source
5. **part5-foundry-agent.ipynb** — Wire KB into a Foundry Agent

Once you've completed all 5 notebooks, return to this page and select **Next >** to view the wrap-up and summary section.

## Discussions

If you’d like to contribute, raise an issue, or provide feedback, please open an issue in this repo.

If you enjoyed this workshop, consider giving the repository a ⭐ on GitHub and sharing it with your peers or community.

## Source Code

The source code for this session is available in the [notebooks folder](../notebooks) of this repository.  
You can use it as a reference for future projects, extend it with additional capabilities, or integrate it into your own solutions built on Azure AI Search and agentic retrieval.