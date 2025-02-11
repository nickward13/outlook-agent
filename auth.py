import os
import requests
from msal import PublicClientApplication
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient

# Configuration for Microsoft Graph API
CLIENT_ID = os.environ["OUTLOOK_AGENT_CLIENT_ID"]
CLIENT_SECRET = os.environ["OUTLOOK_AGENT_CLIENT_SECRET"]
TENANT_ID = 'common'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['User.Read']

app = PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
    )

def get_access_token():
    
    return get_access_token(SCOPE)
    
    

def get_access_token(scopes: list[str]):

    result = None
    accounts = app.get_accounts()
    if accounts:
        chosen_account = accounts[0]
        result = app.acquire_token_silent(scopes=scopes, account=chosen_account)
    
    if not result:
        result = app.acquire_token_interactive(scopes=scopes)
    
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception("Could not obtain access token")
    
def get_graph_client(scopes: list[str]):
    credentials = InteractiveBrowserCredential(
        client_id=CLIENT_ID, 
        tenant_id=TENANT_ID,
        )
    client = GraphServiceClient(credentials=credentials, scopes=scopes)
    return client