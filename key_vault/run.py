#pip install the following libraries first and foremost by  opening the file in an integrated terminal
#pip install azure-ai-textanalytics==5.3.0
#pip install azure-identity==1.5.0
#pip install azure-keyvault-secrets==4.2.0

from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


def main():
    global cog_endpoint
    global cog_key

   
    # Get Configuration Settings
    load_dotenv()
    cog_endpoint = 'YOUR_COGNITIVE_SERVICE_ENDPOINT'
    key_vault_name = 'THE_KEY_VAULT_NAME'
    app_tenant = 'YOUR_TENANT_ID'
    app_id = 'YOUR_APP_ID'
    app_password = 'YOUR_APP_PASSWORD'

    # Get Azure AI services key from keyvault using the service principal credentials
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    credential = ClientSecretCredential(app_tenant, app_id, app_password)
    keyvault_client = SecretClient(key_vault_uri, credential)
    secret_key = keyvault_client.get_secret("Cognitive-Services-Key")
    cog_key = secret_key.value
    print(cog_key)

        




if __name__ == "__main__":
    main()
