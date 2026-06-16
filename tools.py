import os.path
import logging
from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

logger = logging.getLogger("tasks-local-server")

# The exact scope needed for full Google Tasks access
SCOPES = ['https://www.googleapis.com/auth/tasks']

def get_tasks_service():
    """
    Handles local OAuth 2.0 authentication. 
    Pops open a browser on first run and saves a token.json file.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('tasks', 'v1', credentials=creds)


def list_task_lists(max_results: int=10) -> str:
    """Retrieves all Google Task lists for the authenticated user."""
    try:
        service = get_tasks_service()
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        
        return json.dumps({"count": len(items), "task_lists": items})
    except Exception as e:
        logger.error(f"Error fetching task lists: {e}")
        return json.dumps({"error": str(e)})

def add_task(tasklist_id: str, title: str, notes: str = "") -> str:
    """Creates a new task in a specific task list."""
    try:
        service = get_tasks_service()
        task_body = {'title': title, 'notes': notes}
        
        result = service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
        return json.dumps({"message": "Task created successfully", "task": result})
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return json.dumps({"error": str(e)})
    
def register_tools(mcp: FastMCP):
    """Progammatically adds tools to the MCP server"""
    mcp.add_tool(list_task_lists)
    mcp.add_tool(add_task)