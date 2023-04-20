from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/summaries/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    id = await crud.post(payload)
    response = {
        "id": id,
        "url": payload.url,
    }

    return response


@router.get("/summaries/{id}/", status_code=200, response_model=SummarySchema)
async def list_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
