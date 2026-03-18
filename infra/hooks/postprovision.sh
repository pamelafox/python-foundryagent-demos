#!/bin/sh
set -e

echo "Running postprovision hook..."

# Fetch API keys (not available as Bicep outputs)
SEARCH_ADMIN_KEY=$(az search admin-key show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --service-name "$AZURE_SEARCH_SERVICE_NAME" \
    --query primaryKey -o tsv)

OPENAI_KEY=$(az cognitiveservices account keys list \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$AZURE_OPENAI_SERVICE_NAME" \
    --query key1 -o tsv)

# Write .env file for notebooks
cat > .env << EOF
# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_ENDPOINT=${AZURE_SEARCH_SERVICE_ENDPOINT}
AZURE_SEARCH_ADMIN_KEY=${SEARCH_ADMIN_KEY}

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
AZURE_OPENAI_KEY=${OPENAI_KEY}
AZURE_OPENAI_CHATGPT_DEPLOYMENT=${AZURE_OPENAI_CHATGPT_DEPLOYMENT}
AZURE_OPENAI_CHATGPT_MODEL_NAME=gpt-4.1

# Microsoft Foundry Configuration (for Part 5)
PROJECT_ENDPOINT=${MICROSOFT_FOUNDRY_PROJECT_ENDPOINT}
PROJECT_RESOURCE_ID=${MICROSOFT_FOUNDRY_PROJECT_ID}
PROJECT_CONNECTION_NAME=kb-mcp-connection

# GitHub Token (for Part 4 - authenticated MCP source)
# GITHUB_TOKEN=
EOF

echo "Created .env file"

# Create indexes and upload data
echo "Creating search indexes and uploading data..."
if [ -f "infra/deploy-yourself/create-indexes.py" ]; then
    python3 -m pip install -r notebooks/requirements.txt --quiet 2>/dev/null
    python3 infra/deploy-yourself/create-indexes.py
    echo "Indexes created and data uploaded"
elif [ -f "infra/create-knowledge.py" ]; then
    python3 -m pip install -r notebooks/requirements.txt --quiet 2>/dev/null
    python3 infra/create-knowledge.py
    echo "Knowledge base setup complete"
else
    echo "No index creation script found, skipping data upload"
fi

echo "Postprovision complete! Open notebooks/ to start the lab."
