"""
Teja — api/schemas.py
Pydantic request/response models. The contract between backend and frontend.
"""
from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    question: str
    truck_id: Optional[str] = None
    trailer_id: Optional[str] = None


class Source(BaseModel):
    doc_id: str
    filename: str
    truck_id: str
    trailer_id: Optional[str] = None
    snippet: str
    score: float


class AskResponse(BaseModel):
    answer: str
    query_type: str        # sql | rag | hybrid
    sql_query: Optional[str] = None
    sources: list[Source] = []


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    truck_id: Optional[str]
    doc_type: str
    confidence_score: float
    message: str


class TruckResponse(BaseModel):
    id: str
    unit_number: int
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    status: str


class DocumentResponse(BaseModel):
    id: str
    filename: str
    doc_type: str
    doc_date: Optional[str]
    expiry_date: Optional[str]
    amount: Optional[float]
    vendor: Optional[str]
    confidence_score: Optional[float]


class FleetStatsResponse(BaseModel):
    total_trucks: int
    total_documents: int
    total_spend_mtd: float
    expiring_soon: int
