"""Tasks group: list_task_lists, add_task, get_task, get_task_by_name, delete_task, complete_task, update_task, create_tasklist, update_tasklist, list_tasks, get_tasklist, delete_tasklist"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    TaskData,
    TaskListData,
    TaskListListData,
    TaskListItemsData,
    TaskResult,
    TaskListResult,
    TaskListListResult,
    TaskListItemsResult,
    TaskUpdateResult,
    TaskListUpdateResult,
    TaskUpdateData,
    TaskListUpdateData,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-tasks-mcp.tools.tasks")


def register_tasks_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_task_lists",
        description=(
            "List all task lists accessible by the user. "
            "Returns task list IDs, titles, and metadata. "
            "Use the task list ID from the response to access tasks within a list."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_task_lists() -> TaskListListResult:
        tlog = ToolLogger(logger, "list_task_lists")
        try:
            svc = service.get_tasks_service()
            results = svc.tasklists().list().execute()
            items = results.get("items", [])
            tlog.success()
            return TaskListListResult(
                success=True, statusCode=200,
                data=TaskListListData(
                    count=len(items),
                    tasklists=[TaskListData(**item) for item in items],
                    next_page_token=results.get("nextPageToken"),
                ),
            )
        except Exception as exc:
            return _handle_request_exc(TaskListListResult, tlog, exc)

    @mcp.tool(
        name="add_task",
        description=(
            "Create a new task in a specific task list. "
            "Provide the task list ID, title, and optional notes and due date. "
            "Returns the created task with its assigned ID."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def add_task(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        title: str = Field(description="The title of the new task."),
        notes: str = Field(default="", description="Optional details or description for the task."),
        due: str = Field(default="", description="Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z')."),
    ) -> TaskResult:
        tlog = ToolLogger(logger, "add_task")
        try:
            svc = service.get_tasks_service()
            task_body = {"title": title}
            if notes:
                task_body["notes"] = notes
            if due:
                task_body["due"] = due
            result = svc.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
            tlog.success()
            return TaskResult(success=True, statusCode=200, data=TaskData(**result))
        except Exception as exc:
            return _handle_request_exc(TaskResult, tlog, exc)

    @mcp.tool(
        name="get_task",
        description=(
            "Gets the detail of a specific task from the task list. "
            "Returns the full task object including title, notes, due date, status, and position."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_task(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        task_id: str = Field(description="The unique ID of the Google Task"),
    ) -> TaskResult:
        tlog = ToolLogger(logger, "get_task")
        try:
            svc = service.get_tasks_service()
            result = svc.tasks().get(tasklist=tasklist_id, task=task_id).execute()
            tlog.success()
            return TaskResult(success=True, statusCode=200, data=TaskData(**result))
        except Exception as exc:
            return _handle_request_exc(TaskResult, tlog, exc)

    @mcp.tool(
        name="get_task_by_name",
        description=(
            "Get the task details from the name of the task. "
            "Searches a task list for a task by its title and returns the matching task details."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_task_by_name(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        task_title: str = Field(description="The title of the task to search for."),
    ) -> TaskResult:
        tlog = ToolLogger(logger, "get_task_by_name")
        try:
            svc = service.get_tasks_service()
            results = svc.tasks().list(tasklist=tasklist_id).execute()
            items = results.get("items", [])
            for item in items:
                if item.get("title", "").lower() == task_title.lower():
                    tlog.success()
                    return TaskResult(success=True, statusCode=200, data=TaskData(**item))
            return _err(TaskResult, tlog, "NOT_FOUND", f"No task found with the title {task_title}", 404)
        except Exception as exc:
            return _handle_request_exc(TaskResult, tlog, exc)

    @mcp.tool(
        name="delete_task",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes a specific task from the task list. "
            "This action is irreversible — the deleted task and all its data cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_task(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        task_id: str = Field(description="The unique ID of the Google Task"),
    ) -> TaskResult:
        tlog = ToolLogger(logger, "delete_task")
        try:
            svc = service.get_tasks_service()
            svc.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
            tlog.success()
            return TaskResult(success=True, statusCode=200, data=TaskData(id=task_id))
        except Exception as exc:
            return _handle_request_exc(TaskResult, tlog, exc)

    @mcp.tool(
        name="complete_task",
        description=(
            "Mark a specific task as completed from the task list. "
            "Sets the task status to 'completed'. Returns the updated task object."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def complete_task(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        task_id: str = Field(description="The unique ID of the Google Task"),
    ) -> TaskResult:
        tlog = ToolLogger(logger, "complete_task")
        try:
            svc = service.get_tasks_service()
            body = {"status": "completed"}
            result = svc.tasks().patch(tasklist=tasklist_id, task=task_id, body=body).execute()
            tlog.success()
            return TaskResult(success=True, statusCode=200, data=TaskData(**result))
        except Exception as exc:
            return _handle_request_exc(TaskResult, tlog, exc)

    @mcp.tool(
        name="update_task",
        description=(
            "Updates an existing task. Only the fields you provide are changed — others keep their current value. "
            "NOTE: this overwrites the current field values — the original state is not stored after the call. "
            "The response includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def update_task(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        task_id: str = Field(description="The unique ID of the Google Task"),
        task_title: str = Field(description="The title of the task."),
        notes: str = Field(default="", description="Optional details or description for the task."),
        due: str = Field(default="", description="Optional due date. MUST be an RFC 3339 timestamp (e.g., '2026-06-17T00:00:00.000Z')."),
    ) -> TaskUpdateResult:
        tlog = ToolLogger(logger, "update_task")
        try:
            svc = service.get_tasks_service()
            before = svc.tasks().get(tasklist=tasklist_id, task=task_id).execute()
            body = {}
            if task_title:
                body["title"] = task_title
            if notes:
                body["notes"] = notes
            if due:
                body["due"] = due
            result = svc.tasks().patch(tasklist=tasklist_id, task=task_id, body=body).execute()
            tlog.success()
            return TaskUpdateResult(
                success=True, statusCode=200,
                data=TaskUpdateData(before=TaskData(**before), after=TaskData(**result)),
            )
        except Exception as exc:
            return _handle_request_exc(TaskUpdateResult, tlog, exc)

    @mcp.tool(
        name="create_tasklist",
        description=(
            "Create a brand new task list. "
            "Returns the created task list with its assigned ID and metadata."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def create_tasklist(
        tasklist_name: str = Field(description="The name of the Google Tasks list."),
    ) -> TaskListResult:
        tlog = ToolLogger(logger, "create_tasklist")
        try:
            svc = service.get_tasks_service()
            body = {"title": tasklist_name}
            result = svc.tasklists().insert(body=body).execute()
            tlog.success()
            return TaskListResult(success=True, statusCode=200, data=TaskListData(**result))
        except Exception as exc:
            return _handle_request_exc(TaskListResult, tlog, exc)

    @mcp.tool(
        name="update_tasklist",
        description=(
            "Updates the name of a specific task list. "
            "The response includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def update_tasklist(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
        title: str = Field(description="The title or name of the Google Tasks list"),
    ) -> TaskListUpdateResult:
        tlog = ToolLogger(logger, "update_tasklist")
        try:
            svc = service.get_tasks_service()
            before = svc.tasklists().get(tasklist=tasklist_id).execute()
            body = {"title": title}
            result = svc.tasklists().patch(tasklist=tasklist_id, body=body).execute()
            tlog.success()
            return TaskListUpdateResult(
                success=True, statusCode=200,
                data=TaskListUpdateData(before=TaskListData(**before), after=TaskListData(**result)),
            )
        except Exception as exc:
            return _handle_request_exc(TaskListUpdateResult, tlog, exc)

    @mcp.tool(
        name="list_tasks",
        description=(
            "List all the tasks present in the specific task list. "
            "Returns task IDs, titles, statuses, and other metadata for all tasks in the list."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_tasks(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
    ) -> TaskListItemsResult:
        tlog = ToolLogger(logger, "list_tasks")
        try:
            svc = service.get_tasks_service()
            result = svc.tasks().list(tasklist=tasklist_id).execute()
            items = result.get("items", [])
            tlog.success()
            return TaskListItemsResult(
                success=True, statusCode=200,
                data=TaskListItemsData(
                    count=len(items),
                    tasks=[TaskData(**item) for item in items],
                    next_page_token=result.get("nextPageToken"),
                ),
            )
        except Exception as exc:
            return _handle_request_exc(TaskListItemsResult, tlog, exc)

    @mcp.tool(
        name="get_tasklist",
        description=(
            "Get the details or metadata of a specific task list. "
            "Returns the task list ID, title, and last updated timestamp."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_tasklist(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
    ) -> TaskListResult:
        tlog = ToolLogger(logger, "get_tasklist")
        try:
            svc = service.get_tasks_service()
            result = svc.tasklists().get(tasklist=tasklist_id).execute()
            tlog.success()
            return TaskListResult(success=True, statusCode=200, data=TaskListData(**result))
        except Exception as exc:
            return _handle_request_exc(TaskListResult, tlog, exc)

    @mcp.tool(
        name="delete_tasklist",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes an entire task list with all tasks in it. "
            "This action is irreversible — the task list and all its tasks cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_tasklist(
        tasklist_id: str = Field(description="The unique ID of the Google Tasks list."),
    ) -> TaskListResult:
        tlog = ToolLogger(logger, "delete_tasklist")
        try:
            svc = service.get_tasks_service()
            svc.tasklists().delete(tasklist=tasklist_id).execute()
            tlog.success()
            return TaskListResult(success=True, statusCode=200, data=TaskListData(id=tasklist_id))
        except Exception as exc:
            return _handle_request_exc(TaskListResult, tlog, exc)