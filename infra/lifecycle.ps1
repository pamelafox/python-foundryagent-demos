# ===========================================
# Download GitHub Repo to Skillable Desktop
# ===========================================

# Set variables
$repoUrl = "https://github.com/microsoft/mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search"
$zipUrl = "$repoUrl/archive/refs/heads/main.zip"
$downloadPath = "$env:USERPROFILE\Downloads\LAB006.zip"
$extractPath = "$env:USERPROFILE\Desktop"

# Download the ZIP file from GitHub
Log "Downloading repo ZIP..."
Invoke-WebRequest -Uri $zipUrl -OutFile $downloadPath -UseBasicParsing

# Create the target folder if it doesn't exist
if (!(Test-Path -Path $extractPath)) {
    New-Item -ItemType Directory -Path $extractPath | Out-Null
}

# Extract the zip file to Desktop
Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force

Log "Repository downloaded and extracted to: $extractPath"

# Lifecycle — Write a self-contained background script that handles everything
# after az login: deploy, poll, fetch outputs, run setup.
# This lets the Skillable lifecycle action exit quickly (< 600s).

$bgScriptPath = "C:\Users\LabUser\Desktop\deploy-background.ps1"
$logFile = "C:\Users\LabUser\Desktop\lifecycle-log.txt"

$bgScript = @'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$logFile = "C:\Users\LabUser\Desktop\lifecycle-log.txt"
function Log {
    param([string]$msg)
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Host $line
    Add-Content -Path $logFile -Value $line
}

Log "=== Background deploy script started ==="

$subscriptionId = $env:BG_SUBSCRIPTION_ID
$resourceGroupName = $env:BG_RESOURCE_GROUP
$labUserObjectId = $env:BG_LAB_USER_OID
$bicepFilePath = $env:BG_BICEP_PATH

# Reuse the az CLI session from the foreground script (token cache in ~/.azure/)
az config set core.only_show_errors=yes --only-show-errors
az config set bicep.use_binary_from_path=false --only-show-errors

$deploymentName = "deployment"

Log "Starting Bicep deployment..."
$deploymentOutput = az deployment group create `
  --name $deploymentName `
  --resource-group $resourceGroupName `
  --template-file $bicepFilePath `
  --parameters principalId="$labUserObjectId" `
  --parameters location="eastus2" `
  --query properties.outputs -o json 2>&1
$deployExitCode = $LASTEXITCODE

if ($deployExitCode -ne 0) {
    Log "Deployment failed (exit code $deployExitCode):"
    Add-Content -Path $logFile -Value $deploymentOutput
    $opErrors = az deployment operation group list `
      --resource-group $resourceGroupName `
      --name $deploymentName `
      --query "[?properties.provisioningState=='Failed'].{Resource:properties.targetResource.resourceName, Type:properties.targetResource.resourceType, Error:properties.statusMessage.error}" `
      -o json 2>&1
    Log "Operation errors:"
    Add-Content -Path $logFile -Value $opErrors
    Log "=== Background deploy script FAILED ==="
    exit 1
}

Log "Deployment succeeded."

Add-Content -Path $logFile -Value $deploymentOutput
$outs = $deploymentOutput | ConvertFrom-Json

$searchName          = $outs.AZURE_SEARCH_SERVICE_NAME.value
$searchEndpoint      = $outs.AZURE_SEARCH_SERVICE_ENDPOINT.value
$openaiName          = $outs.AZURE_OPENAI_SERVICE_NAME.value
$openaiEndpoint      = $outs.AZURE_OPENAI_ENDPOINT.value
$projectEndpoint     = $outs.MICROSOFT_FOUNDRY_PROJECT_ENDPOINT.value
$projectResourceId   = $outs.MICROSOFT_FOUNDRY_PROJECT_ID.value

$searchAdminKey = az rest --method POST `
  --url "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Search/searchServices/$searchName/listAdminKeys?api-version=2023-11-01" `
  --query primaryKey -o tsv

$openaiKey = az cognitiveservices account keys list -g $resourceGroupName -n $openaiName --query key1 -o tsv

# Validate all required values before calling setup-knowledge.ps1
# (empty mandatory params cause PowerShell to hang waiting for interactive input)
Log "searchEndpoint=$searchEndpoint"
Log "searchAdminKey length=$($searchAdminKey.Length)"
Log "openaiEndpoint=$openaiEndpoint"
Log "openaiKey length=$($openaiKey.Length)"
Log "projectEndpoint=$projectEndpoint"
Log "projectResourceId=$projectResourceId"

$missingParams = @()
if ([string]::IsNullOrWhiteSpace($searchEndpoint))      { $missingParams += "SearchEndpoint" }
if ([string]::IsNullOrWhiteSpace($searchAdminKey))       { $missingParams += "SearchAdminKey" }
if ([string]::IsNullOrWhiteSpace($openaiEndpoint))       { $missingParams += "OpenAIEndpoint" }
if ([string]::IsNullOrWhiteSpace($openaiKey))            { $missingParams += "OpenAIKey" }
if ($missingParams.Count -gt 0) {
    Log "ERROR: Missing required values: $($missingParams -join ', ')"
    exit 1
}

$localInfraPath = "C:\Users\LabUser\Desktop\mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search-main\infra"
$setupLocal = Join-Path $localInfraPath "setup-knowledge.ps1"

if (-not (Test-Path $setupLocal)) {
    Log "ERROR: Setup file not found at: $setupLocal"
    exit 1
}

$docsPath = "C:\Users\LabUser\Desktop\mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search-main\data\ai-search-data"
[Environment]::SetEnvironmentVariable("LOCAL_DOCS_PATH", $docsPath, "Process")

Log "Running setup-knowledge.ps1..."
powershell -ExecutionPolicy Bypass -File $setupLocal `
  -SearchEndpoint $searchEndpoint `
  -SearchAdminKey $searchAdminKey `
  -OpenAIEndpoint $openaiEndpoint `
  -OpenAIKey $openaiKey `
  -ProjectEndpoint $projectEndpoint `
  -ProjectResourceId $projectResourceId 2>&1 | Tee-Object -FilePath $logFile -Append

Log "=== Background deploy script completed ==="
'@

# Write the background script to disk
Set-Content -Path $bgScriptPath -Value $bgScript -Encoding UTF8

# --- Quick inline work that must finish within ~600s ---

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
function Log {
    param([string]$msg)
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Host $line
    Add-Content -Path $logFile -Value $line
}
Log "=== Lifecycle script started ==="

$clientId = "@lab.CloudSubscription.AppId"
$clientSecret = "@lab.CloudSubscription.AppSecret"
$tenantId = "@lab.CloudSubscription.TenantId"
$subscriptionId = "@lab.CloudSubscription.Id"

Log "Logging in to Azure..."
az login --service-principal -u $clientId -p $clientSecret --tenant $tenantId --only-show-errors -o none
az account set -s $subscriptionId --only-show-errors
az config set core.only_show_errors=yes --only-show-errors
az config set bicep.use_binary_from_path=false --only-show-errors

$resourceGroupName = "@lab.CloudResourceGroup(LAB006Final-ResourceGroup).Name"
$bicepFilePath = "C:\Users\LabUser\Desktop\mvp26-LAB006-build-agentic-knowledge-bases-next-level-rag-with-azure-ai-search-main\infra\main.bicep"

if (-not (Test-Path $bicepFilePath)) {
    Log "ERROR: Bicep file not found at: $bicepFilePath"
    throw "Bicep file not found at: $bicepFilePath"
}

$labUserUpn = "@lab.CloudPortalCredential(User1).Username"
$labUserObjectId = az ad user show --id $labUserUpn --query id -o tsv

# Pass values to background script via environment variables
# (az CLI session is already cached in ~/.azure/, no need to pass credentials)
$env:BG_SUBSCRIPTION_ID = $subscriptionId
$env:BG_RESOURCE_GROUP = $resourceGroupName
$env:BG_LAB_USER_OID = $labUserObjectId
$env:BG_BICEP_PATH = $bicepFilePath

Log "Launching background deploy process..."
Start-Process -FilePath "powershell.exe" `
  -ArgumentList "-ExecutionPolicy Bypass -File `"$bgScriptPath`"" `
  -WindowStyle Hidden

Log "=== Lifecycle script exiting (background process handles deployment) ==="

