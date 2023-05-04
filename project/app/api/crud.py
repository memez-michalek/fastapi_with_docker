from typing import Union

from app.models.pydantic import (SummaryPayloadSchema,
                                 SummaryUpdatePayloadSchema)
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="xd")
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary is None:
        return None
    return summary


async def delete(id: int) -> id:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary


async def put(id: int, payload: SummaryUpdatePayloadSchema) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).update(
        url=payload.url, summary=payload.summary
    )
    if summary:
        update_summary = await TextSummary.filter(id=id).first().values()
        return update_summary
    return None
