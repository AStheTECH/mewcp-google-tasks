import logging
from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger("tasks-mcp-server")

def get_service():
    """Extracts OAuth credentials and builds the Google Tasks service."""
    cred = get_credentials()
    
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
        
    logger.info("Creating Google Tasks API service with provided access token")
    
    # Wrap the raw string token in Google's strict object
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    
    # Build the Tasks service (Tasks is 'tasks', version 'v1')
    service = build("tasks", "v1", credentials=creds)
    
    logger.info("Google Tasks API service created successfully")
    return service