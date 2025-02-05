import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential
from typing import Any, Callable, Set
from pathlib import Path
import requests
import msal


def get_access_token():
    # app = msal.ConfidentialClientApplication(
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        #client_credential=CLIENT_SECRET,
    )
    accounts = app.get_accounts()

    result = app.acquire_token_by_auth_code_flow(scopes=SCOPE)
    # result = app.acquire_token_for_client(scopes=SCOPE)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception("Could not obtain access token")

def get_outlook_tasks(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/todo/lists', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching tasks: {response.status_code} - {response.text}")    

user_functions: Set[Callable[..., Any]] = {
    get_outlook_tasks,
}

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

def chat(new_message):
    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=new_message,
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    # Get the last message from the sender
    last_msg = messages.get_last_text_message_by_role("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")
    
    return last_msg.text.value


project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# Initialize agent toolset with user functions
# functions = FunctionTool(user_functions)
# toolset = ToolSet()
# toolset.add(functions)

# Get access token from Microsoft Graph
# access_token = get_access_token()

# with project_client:

# The CodeInterpreterTool needs to be included in creation of the agent
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are helpful agent that helps users manage their tasks and to do list using Microsoft Outlook.",
    #tools=[CodeInterpreterTool(), get_outlook_tasks]
)
print(f"Created agent, agent ID: {agent.id}")

# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")


# Delete the agent once done
# project_client.agents.delete_agent(agent.id)
# print("Deleted agent")