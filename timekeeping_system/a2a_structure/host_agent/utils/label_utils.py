"""
Label utilities for coordinator.

This module provides utility functions for creating consistent custom labels
for LLM API calls in the coordinator.
"""

import os
import platform
from datetime import datetime
from typing import Dict, Optional

# Import ID extraction utilities
try:
    from .id_extraction_utils import extract_user_id_from_query, extract_organization_id_from_query
except ImportError:
    # Fallback for cases where the import might fail
    def extract_user_id_from_query(query: str) -> str:
        return ""
    def extract_organization_id_from_query(query: str) -> str:
        return ""

def generate_llm_labels(
    agent_name: str,
    operation_type: str,
    user_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    session_id: Optional[str] = None,
    video_uuid: Optional[str] = None,
    image_id: Optional[str] = None,
    query: Optional[str] = None,
    additional_labels: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Generate consistent labels for LLM API calls.
    
    Args:
        agent_name: Name of the agent making the call
        operation_type: Type of operation being performed
        user_id: Optional user identifier
        organization_id: Optional organization identifier
        session_id: Optional session identifier
        video_uuid: Optional video UUID
        image_id: Optional image ID
        additional_labels: Optional additional custom labels
        
    Returns:
        Dictionary of labels for the LLM API call
    """
        # Auto-extract user_id and organization_id from query if not provided
    if not user_id and query:
        user_id = extract_user_id_from_query(query)
    if not organization_id and query:
        organization_id = extract_organization_id_from_query(query)
    
    labels = {
        "agent": agent_name,
        "operation": operation_type,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": os.getenv("VERSION", "1.0"),
        "model_family": "gemini"
    }
    
    # Add optional identifiers
    if user_id:
        labels["user_id"] = str(user_id)  # Ensure user_id is always a string
    if organization_id:
        labels["organization_id"] = str(organization_id)  # Ensure organization_id is always a string
    if session_id:
        labels["session_id"] = session_id
    if video_uuid:
        labels["video_uuid"] = video_uuid
    if image_id:
        labels["image_id"] = image_id
        
    # Add additional custom labels
    if additional_labels:
        labels.update(additional_labels)
        
    return labels

def get_agent_specific_labels(
    agent_name: str = "coordinator",
    operation_type: str = "coordinator_operation",
    user_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    session_id: Optional[str] = None,
    video_uuid: Optional[str] = None,
    image_id: Optional[str] = None,
    query: Optional[str] = None,
    additional_labels: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Get agent-specific labels for coordinator.
    
    Args:
        agent_name: Name of the agent (defaults to "coordinator")
        operation_type: Type of operation being performed
        user_id: Optional user identifier
        organization_id: Optional organization identifier
        session_id: Optional session identifier
        video_uuid: Optional video UUID
        image_id: Optional image ID
        additional_labels: Optional additional custom labels
        
    Returns:
        Dictionary of labels for the LLM API call
    """
    return generate_llm_labels(
        agent_name=agent_name,
        operation_type=operation_type,
        query=query,
        user_id=user_id,
        organization_id=organization_id,
        session_id=session_id,
        video_uuid=video_uuid,
        image_id=image_id,
        additional_labels=additional_labels,
    )
