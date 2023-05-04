from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path

from app.api import crud
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)


router = APIRouter()


@router.post("/summaries/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
) -> SummaryResponseSchema:
    id = await crud.post(payload)

    background_tasks.add_task(generate_summary, id, payload.url)
    response = {
        "id": id,
        "url": payload.url,
    }

    return response


@router.get("/summaries/{id}/", response_model=SummarySchema)
async def list_summary(id: Annotated[int, Path(gt=0)]) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.delete("/summaries/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: Annotated[int, Path(gt=0)]) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id)
    return summary


@router.put("/summaries/{id}/", response_model=SummarySchema)
async def update_summary(
    id: Annotated[int, Path(gt=0)], payload: SummaryUpdatePayloadSchema
) -> SummarySchema:
    summary = await crud.put(id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
