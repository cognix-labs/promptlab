## Self Hosting

### Running locally

        docker build -t promptlab:latest ./docker

        docker run -p 8000:8000 -p 8001:8001 -v C:\work\promptlab_test\data:/app/data --name promptlab-container promptlab:latest

### Hosting in Azure

Publish docker image to Azure Container Registry. You can use dockerhub as well.

- az login
- az acr login --name REGISTRY_NAME
- docker tag promptlab:latest REGISTRY_NAME.azurecr.io/promptlab:latest
- docker push REGISTRY_NAME.azurecr.io/promptlab:latest

Create an Azure Container Instance

az container create `
  --resource-group container `
  --name pl `
  --image registry0101010101.azurecr.io/pl:latest `
  --registry-login-server registry0101010101.azurecr.io `
  --registry-username (az acr credential show --name registry0101010101 --query username --output tsv) `
  --registry-password (az acr credential show --name registry0101010101 --query passwords[0].value --output tsv) `
  --dns-name-label pl01010101 `
  --ports 8000 8001 `
  --cpu 2 `
  --memory 4 `
  --os-type Linux `
  --restart-policy Always