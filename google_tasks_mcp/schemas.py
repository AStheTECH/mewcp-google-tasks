"""Pydantic schemas for MewCP Google Tasks MCP Server."""

from pydantic import BaseModel, ConfigDict
from typing import Any


class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


class TaskData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str | None = None
    notes: str | None = None
    due: str | None = None
    status: str | None = None
    position: str | None = None
    parent: str | None = None
    links: list[dict[str, Any]] | None = None
    webViewLink: str | None = None
    hidden: bool | None = None
    completed: str | None = None
    deleted: bool | None = None
    etag: str | None = None
    kind: str | None = None
    selfLink: str | None = None


class TaskListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    title: str | None = None
    updated: str | None = None
    etag: str | None = None
    kind: str | None = None
    selfLink: str | None = None


class TaskResult(ToolResult):
    data: TaskData | None = None


class TaskListResult(ToolResult):
    data: TaskListData | None = None


class TaskListListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    tasklists: list[TaskListData]
    next_page_token: str | None = None


class TaskListListResult(ToolResult):
    data: TaskListListData | None = None


class TaskUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: TaskData
    after: TaskData


class TaskUpdateResult(ToolResult):
    data: TaskUpdateData | None = None


class TaskListUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: TaskListData
    after: TaskListData


class TaskListUpdateResult(ToolResult):
    data: TaskListUpdateData | None = None


class TaskListItemsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    tasks: list[TaskData]
    next_page_token: str | None = None


class TaskListItemsResult(ToolResult):
    data: TaskListItemsData | None = None
