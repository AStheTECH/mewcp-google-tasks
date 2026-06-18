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

def get_task(tasklist_id: str, task_id: str) -> str:
    """Gets the details of a specific task"""
    try:
        service = get_tasks_service()
        result = service.tasks().get(tasklist=tasklist_id,task=task_id).execute()
        return json.dumps(result,indent=2)
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        return json.dumps({"error":str(e)})
    
def get_task_by_name(tasklist_id: str, task_title: str) -> str:
    """Searches a task list for a task by its name and returns details of specific task"""
    try:
        service = get_tasks_service()
        results = service.tasks().list(tasklist=tasklist_id).execute()
        items = results.get('items',[])

        for item in items:
            if item.get('title','').lower() == task_title.lower():
                return json.dumps({
                    "message":"Task Found!",
                    "task":item
                }, indent=2)
        return json.dumps({"error":f"No task found with the title {task_title}"})
    except Exception as e:
        logger.error(f"Error searching for task: {e}")
        return json.dumps({"error":str(e)})

def delete_task(tasklist_id: str, task_id: str) -> str:
    """Deletes a specific task from the task list"""
    try:
        service = get_tasks_service()
        service.tasks().delete(tasklist=tasklist_id,task=task_id).execute()
        return json.dumps({"message":f"Task {task_id} successfully deleted"}) #Since .delete() returns empty string, a message for verification
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return json.dumps({"error":str(e)})

def complete_task(tasklist_id: str, task_id: str) -> str:
    """Marks the specific task as completed"""
    try:
        service = get_tasks_service()
        body={"status":"completed"}
        result = service.tasks().patch(tasklist=tasklist_id,task=task_id,body=body).execute()
        return json.dumps({"message":"Task marked as complete","task":result},indent=2)
    except Exception as e:
        logger.error(f"Error changing status of the task: {e}")
        return json.dumps({"error":str(e)})
    
def update_task(tasklist_id: str, task_id: str, task_title: str = "", notes: str = "", due: str = "") -> str:
    """Updates an existing and specific task
    Note: 'due' must be an RFC 3339 timestamp (e.g., 2026-06-17T00:00:00.000Z)."""
    try:
        service = get_tasks_service()
        body = {}
        if task_title:
            body['title']=task_title
        if notes:
            body["notes"] = notes
        if due:
            body['due'] = due
        result = service.tasks().patch(tasklist=tasklist_id,task=task_id,body=body).execute()
        return json.dumps({"message":"Task successfully updated!","task":result},indent=2)
    except Exception as e:
        logger.error(f"Error updating the task: {e}")
        return json.dumps({"error":str(e)})

def create_tasklist(tasklist_name: str) -> str:
    """Create a new tasklist"""
    try:
        service = get_tasks_service()
        body = {"title":tasklist_name}
        result = service.tasklists().insert(body=body).execute()
        return json.dumps({"message":"Tasklist successfully created!","tasklist":result},indent=2)
    except Exception as e:
        logger.error(f"Error creating tasklist: {e}")
        return json.dumps({"error":str(e)})
    
def update_tasklist(tasklist_id: str, title:str) -> str:
    """Update name of specific tasklist"""
    try:
        service = get_tasks_service()
        body={"title":title}
        result = service.tasklists().patch(tasklist=tasklist_id,body=body).execute()
        return json.dumps({"message":"Tasklist updated successfully!","tasklist":result},indent=2)
    except Exception as e:
        logger.error(f"Error updating tasklist: {e}")
        return json.dumps({"error":str(e)})

def list_tasks(tasklist_id: str) -> str:
    """List all tasks present in the tasklist"""
    try:
        service = get_tasks_service()
        result = service.tasks().list(tasklist=tasklist_id).execute()
        return json.dumps({"message":"Here is the list of tasks","tasks":result},indent=2)
    except Exception as e:
        logger.error(f"Error updating tasklist: {e}")
        return json.dumps({"error":str(e)})

def register_tools(mcp: FastMCP):
    """Progammatically adds tools to the MCP server"""
    mcp.add_tool(list_task_lists)
    mcp.add_tool(add_task)
    mcp.add_tool(get_task)
    mcp.add_tool(get_task_by_name)
    mcp.add_tool(delete_task)
    mcp.add_tool(complete_task)
    mcp.add_tool(update_task)
    mcp.add_tool(create_tasklist)
    mcp.add_tool(update_tasklist)
    mcp.add_tool(list_tasks)