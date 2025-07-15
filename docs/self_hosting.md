# Self Hosting PromptLab

This guide covers how to deploy PromptLab using Docker containers, both locally and in Azure cloud infrastructure.

## Prerequisites

- Docker installed on your system
- For Azure deployment: Azure CLI and an active Azure subscription
- Basic familiarity with command line operations

## Local Deployment

### Building the Docker Image

1. **Navigate to the project root directory:**
   ```bash
   cd /path/to/promptlab
   ```

2. **Build the Docker image:**
   ```bash
   docker build -t promptlab:latest ./docker
   ```

### Running the Container

#### Basic Setup

Run PromptLab with default settings:

```bash
docker run -p 8000:8000 -p 8001:8001 --name promptlab-container promptlab:latest
```

#### Production Setup with Persistent Data

For production use, mount a volume to persist your database and set security environment variables:

```bash
docker run -p 8000:8000 -p 8001:8001 \
  -v /your/local/data/path:/app/data \
  -e PROMPTLAB_SECRET_KEY="your-secure-32-character-secret-key-here" \
  --name promptlab-container \
  --restart unless-stopped \
  promptlab:latest
```

**Windows Example:**
```powershell
docker run -p 8000:8000 -p 8001:8001 -v C:\work\promptlab_data:/app/data -e PROMPTLAB_SECRET_KEY="your-secure-32-character-secret-key-here" --name promptlab-container --restart unless-stopped promptlab:latest
```

#### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `PROMPTLAB_SECRET_KEY` | **Recommended** | JWT signing key for authentication. Should be 32+ characters for security. | Auto-generated (not persistent) |
| `PROMPTLAB_LOG_LEVEL` | Optional | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) | `INFO` |
| `PROMPTLAB_LOG_DIR` | Optional | Custom directory for log files | Platform-specific default |

**⚠️ Security Note:** Always set `PROMPTLAB_SECRET_KEY` in production to ensure consistent JWT token validation across container restarts.

### Accessing the Application

- **Main Application:** http://localhost:8000
- **API Endpoint:** http://localhost:8001/redoc

## Azure Cloud Deployment

### Method 1: Azure Container Instances (ACI)

This is the simplest method for getting started with cloud hosting.

#### Step 1: Prepare Azure Container Registry

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Create a resource group (if needed):**
   ```bash
   az group create --name promptlab-rg --location eastus
   ```

3. **Create Azure Container Registry:**
   ```bash
   az acr create --resource-group promptlab-rg --name yourregistryname --sku Basic
   ```

4. **Login to your container registry:**
   ```bash
   az acr login --name yourregistryname
   ```

#### Step 2: Push Docker Image to Registry

1. **Tag your local image:**
   ```bash
   docker tag promptlab:latest yourregistryname.azurecr.io/promptlab:latest
   ```

2. **Push the image:**
   ```bash
   docker push yourregistryname.azurecr.io/promptlab:latest
   ```

#### Step 3: Deploy Container Instance

```bash
az container create \
  --resource-group promptlab-rg \
  --name promptlab-aci \
  --image yourregistryname.azurecr.io/promptlab:latest \
  --registry-login-server yourregistryname.azurecr.io \
  --registry-username $(az acr credential show --name yourregistryname --query username --output tsv) \
  --registry-password $(az acr credential show --name yourregistryname --query passwords[0].value --output tsv) \
  --dns-name-label promptlab-unique-dns \
  --ports 8000 8001 \
  --cpu 2 \
  --memory 4 \
  --os-type Linux \
  --restart-policy Always \
  --environment-variables PROMPTLAB_SECRET_KEY="your-secure-32-character-secret-key-here"
```

#### Step 4: Access Your Application

Your application will be available at:
- `http://promptlab-unique-dns.your-azure-region.azurecontainer.io:8000`

### Method 2: Azure Container Apps (Recommended for Production)

Azure Container Apps provides better scaling and management capabilities.

#### Step 1: Create Container Apps Environment

```bash
# Install the containerapp extension
az extension add --name containerapp

# Create a Container Apps environment
az containerapp env create \
  --name promptlab-env \
  --resource-group promptlab-rg \
  --location eastus
```

#### Step 2: Deploy Container App

```bash
az containerapp create \
  --name promptlab-app \
  --resource-group promptlab-rg \
  --environment promptlab-env \
  --image yourregistryname.azurecr.io/promptlab:latest \
  --registry-server yourregistryname.azurecr.io \
  --registry-username $(az acr credential show --name yourregistryname --query username --output tsv) \
  --registry-password $(az acr credential show --name yourregistryname --query passwords[0].value --output tsv) \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --env-vars PROMPTLAB_SECRET_KEY="your-secure-32-character-secret-key-here"
```

**Note:** For Container Apps, you can also set environment variables through the Azure portal or use Azure Key Vault for enhanced security.