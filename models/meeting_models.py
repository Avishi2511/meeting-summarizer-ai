from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class FileUploadResponse(BaseModel):
    success: bool
    file_type: str
    raw_transcript: Optional[str] = None
    cleaned_transcript: Optional[str] = None
    chunks: Optional[List[Dict]] = None
    metadata: Optional[Dict] = None
    error: Optional[str] = None

class SummaryRequest(BaseModel):
    transcript: str
    analysis_type: str = "comprehensive"
    file_metadata: Optional[Dict] = None

class SummaryResponse(BaseModel):
    success: bool
    analysis_type: str
    comprehensive_summary: Optional[str] = None
    topic_analysis: Optional[str] = None
    action_items: Optional[str] = None
    sentiment_analysis: Optional[str] = None
    input_length: Optional[int] = None
    word_count: Optional[int] = None
    total_chunks: Optional[int] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None

class ProcessingStatus(BaseModel):
    stage: str
    message: str
    progress: int  # 0-100
    timestamp: datetime = datetime.now()

class MeetingMetadata(BaseModel):
    filename: str
    file_type: str
    file_size: Optional[int] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    participants: Optional[List[str]] = None
    meeting_date: Optional[datetime] = None
    meeting_title: Optional[str] = None
