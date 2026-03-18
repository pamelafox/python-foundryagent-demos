$ErrorActionPreference = "Stop"

Write-Host "Running postprovision hook..."

# Fetch API keys (not available as Bicep outputs)
$searchAdminKey = az search admin-key show `
    --resource-group $env:AZURE_RESOURCE_GROUP `
    --service-name $env:AZURE_SEARCH_SERVICE_NAME `
    --query primaryKey -o tsv

$openaiKey = az cognitiveservices account keys list `
    --resource-group $env:AZURE_RESOURCE_GROUP `
    --name $env:AZURE_OPENAI_SERVICE_NAME `
    --query key1 -o tsv

# Write .env file for notebooks
$envContent = @"
# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_ENDPOINT=$($env:AZURE_SEARCH_SERVICE_ENDPOINT)
AZURE_SEARCH_ADMIN_KEY=$searchAdminKey

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=$($env:AZURE_OPENAI_ENDPOINT)
AZURE_OPENAI_KEY=$openaiKey
AZURE_OPENAI_CHATGPT_DEPLOYMENT=$($env:AZURE_OPENAI_CHATGPT_DEPLOYMENT)
AZURE_OPENAI_CHATGPT_MODEL_NAME=gpt-4.1

# Microsoft Foundry Configuration (for Part 5)
PROJECT_ENDPOINT=$($env:MICROSOFT_FOUNDRY_PROJECT_ENDPOINT)
PROJECT_RESOURCE_ID=$($env:MICROSOFT_FOUNDRY_PROJECT_ID)
PROJECT_CONNECTION_NAME=kb-mcp-connection

# GitHub Token (for Part 4 - authenticated MCP source)
# GITHUB_TOKEN=
"@

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path $PWD ".env"), $envContent, $utf8NoBom)

Write-Host "Created .env file"

# Create indexes and upload data
Write-Host "Creating search indexes and uploading data..."
$createIndexesPath = Join-Path $PWD "infra\deploy-yourself\create-indexes.py"
$createKnowledgePath = Join-Path $PWD "infra\create-knowledge.py"

if (Test-Path $createIndexesPath) {
    python -m pip install -r notebooks\requirements.txt --quiet 2>$null
    python $createIndexesPath
    Write-Host "Indexes created and data uploaded"
} elseif (Test-Path $createKnowledgePath) {
    python -m pip install -r notebooks\requirements.txt --quiet 2>$null
    python $createKnowledgePath
    Write-Host "Knowledge base setup complete"
} else {
    Write-Host "No index creation script found, skipping data upload"
}

Write-Host "Postprovision complete! Open notebooks/ to start the lab."
