"""Upstream API client for MewCP Google Tasks MCP Server."""

import logging

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger("google-tasks-mcp.service")


def get_tasks_service():
    """Builds the Google Tasks service using the MewCP credentials gateway."""
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")

    logger.info("Creating Google Tasks API service with provided access token")
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    service = build("tasks", "v1", credentials=creds)

    logger.info("Google Tasks API service created successfully")
    return service