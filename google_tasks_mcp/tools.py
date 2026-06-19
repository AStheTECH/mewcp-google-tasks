import logging
import json
from typing import List, Annotated
from pydantic import Field
from fastmcp import FastMCP
from .schema import ApiObjectResponse 
from .service import get_tasks_service

logger = logging.getLogger("tasks-mcp-server")

class _ToolCollector:
    """MewCP's enterprise tool registration pattern."""
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func
        return decorator

mcp = _ToolCollector()

def register_tools(real_mcp: FastMCP) -> None:
    """Transfers tools from the collector to the real FastMCP server."""
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)


@mcp.tool(name="list_task_lists", description="List all task lists accessible by the user")
def list_task_lists() -> ApiObjectResponse:
    """List all task folders/lists"""
    logger.info("Executing list_task_lists")
    try:
        service = get_tasks_service()
        results = service.tasklists().list().execute()
        return {"message": "Success", "tasklists": results.get('items', [])}
    except Exception as e:
        logger.error(f"Error in list_task_lists: {e}")
        return {"error": str(e)}

@mcp.tool(name="add_task", description="Create a new task in a specific task list")
def add_task(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    title: Annotated[str, Field(description="The title of the new task.")],
    notes: Annotated[str, Field(default="", description="Optional details or description for the task.")],
    due: Annotated[str, Field(default="", description="Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z').")]
) -> ApiObjectResponse:
    """Create a new task"""
    logger.info(f"Executing add_task: {title}")
    try:
        service = get_tasks_service()
        
        task_body = {'title': title}
        if notes: task_body['notes'] = notes
        if due: task_body['due'] = due
        
        result = service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
        logger.info(f"Task created: {result.get('id')}")
        
        return {"message": "Task created successfully", "task": result}
    except Exception as e:
        logger.error(f"Error in add_task: {e}")
        return {"error": str(e)}
    
@mcp.tool(name="get_task", description="Gets the detail of a specific task from the task list")
def get_task(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    task_id: Annotated[str, Field(description="The unique ID of the Google Task")],
) -> ApiObjectResponse:
    """Gets the details of a specific task"""
    logger.info(f"Executing get_task: {task_id}")
    try:
        service = get_tasks_service()
        result = service.tasks().get(tasklist=tasklist_id,task=task_id).execute()
        return {"message":"Task fetched successfully: ", "task":result}
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        return {"error":str(e)}
    
@mcp.tool(name="get_task_by_name", description="Get the task details from the name of the task")
def get_task_by_name(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    task_title: Annotated[str, Field(description="The title of the new task.")],
) -> ApiObjectResponse:
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
        return {"error":f"No task found with the title {task_title}"}
    except Exception as e:
        logger.error(f"Error searching for task: {e}")
        return {"error":str(e)}

@mcp.tool(name="delete_task",description="Delete a specific task from the tasklist")
def delete_task(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    task_id: Annotated[str, Field(description="The unique ID of the Google Task")],
) -> ApiObjectResponse:
    """Deletes a specific task from the task list"""
    logger.info(f"Executing delete_task: {task_id}")
    try:
        service = get_tasks_service()
        service.tasks().delete(tasklist=tasklist_id,task=task_id).execute()
        return {"message":f"Task {task_id} successfully deleted"} #Since .delete() returns empty string, a message for verification
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return {"error":str(e)}

@mcp.tool(name="complete_task",description="Mark a specific task completed from the task list")
def complete_task(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    task_id: Annotated[str, Field(description="The unique ID of the Google Task")],
) -> ApiObjectResponse:
    """Marks the specific task as completed"""
    try:
        service = get_tasks_service()
        body={"status":"completed"}
        result = service.tasks().patch(tasklist=tasklist_id,task=task_id,body=body).execute()
        return {"message":"Task marked as complete","task":result}
    except Exception as e:
        logger.error(f"Error changing status of the task: {e}")
        return {"error":str(e)}
    
@mcp.tool(name="update_task",description="Update the details of an existing task")
def update_task(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    task_id: Annotated[str, Field(description="The unique ID of the Google Task")],
    task_title: Annotated[str, Field(description="The title of the new task.")],
    notes: Annotated[str, Field(default="", description="Optional details or description for the task.")],
    due: Annotated[str, Field(default="", description="Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z').")]
) -> ApiObjectResponse:
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
        return {"message":"Task successfully updated!","task":result}
    except Exception as e:
        logger.error(f"Error updating the task: {e}")
        return {"error":str(e)}

@mcp.tool(name="create_tasklist",description="Create a brand new tasklist")
def create_tasklist(
    tasklist_name: Annotated[str, Field(description="The name of the Google Tasks list.")]
) -> ApiObjectResponse:
    """Create a new tasklist"""
    try:
        service = get_tasks_service()
        body = {"title":tasklist_name}
        result = service.tasklists().insert(body=body).execute()
        return {"message":"Tasklist successfully created!","tasklist":result}
    except Exception as e:
        logger.error(f"Error creating tasklist: {e}")
        return {"error":str(e)}

@mcp.tool(name="update_tasklist",description="Update the name of a specific tasklist")
def update_tasklist(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
    title: Annotated[str, Field(description="The title or name of the new Google Tasks list")],
) -> ApiObjectResponse:
    """Update name of specific tasklist

    """
    try:
        service = get_tasks_service()
        body={"title":title}
        result = service.tasklists().patch(tasklist=tasklist_id,body=body).execute()
        return {"message":"Tasklist updated successfully!","tasklist":result}
    except Exception as e:
        logger.error(f"Error updating tasklist: {e}")
        return {"error":str(e)}

@mcp.tool(name="list_tasks",description="List all the tasks present in the specific tasklist")
def list_tasks(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")],
) -> ApiObjectResponse:
    """List all tasks present in the tasklist"""
    try:
        service = get_tasks_service()
        result = service.tasks().list(tasklist=tasklist_id).execute()
        return {"message":"Here is the list of tasks","tasks":result}
    except Exception as e:
        logger.error(f"Error updating tasklist: {e}")
        return {"error":str(e)}
    
@mcp.tool(name="get_tasklist",description="Get the details or metadata of a specific tasklist")
def get_tasklist(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")]
) -> ApiObjectResponse:
    """Get the metadata of a specific tasklist"""
    try:
        service = get_tasks_service()
        result = service.tasklists().get(tasklist=tasklist_id).execute()
        return {"message":"Metadata successfully retrieved","Metadata":result}
    except Exception as e:
        logger.error(f"Error retrieving metadata: {e}")
        return {"error":str(e)}

@mcp.tool(name="delete_tasklist",description="Delete an entire tasklist with the tasks in it")
def delete_tasklist(
    tasklist_id: Annotated[str, Field(description="The unique ID of the Google Tasks list.")]
) -> ApiObjectResponse:
    """Delete the entire specified tasklist with all tasks in it"""
    try:
        service = get_tasks_service()
        result = service.tasklists().delete(tasklist=tasklist_id).execute()
        return {"message":"Tasklist successfully deleted"}
    except Exception as e:
        logger.error(f"Error deleting tasklist: {e}")
        return {"error":str(e)}