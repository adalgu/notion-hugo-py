from typing import Dict, List, Any, TypedDict, Optional

class BatchProcessError(TypedDict):
    pageId: str
    error: str

class BatchProcessSkipped(TypedDict):
    pageId: str
    reason: str

class BatchProcessResult(TypedDict):
    totalProcessed: int
    success: List[str]
    errors: List[BatchProcessError]
    skipped: List[BatchProcessSkipped]

class NotionBlock(TypedDict):
    object: str
    id: str
    type: str
    has_children: bool
    archived: bool
    created_time: str
    last_edited_time: str

class NotionPage(TypedDict):
    object: str
    id: str
    created_time: str
    last_edited_time: str
    archived: bool
    url: str
    properties: Dict[str, Any]
