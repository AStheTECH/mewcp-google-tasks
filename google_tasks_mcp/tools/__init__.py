"""MewCP Google Tasks tool registration."""

from fastmcp import FastMCP

from .tasks_tools import register_tasks_tools


def register_tools(mcp: FastMCP) -> None:
    register_tasks_tools(mcp)