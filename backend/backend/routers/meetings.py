from datetime import datetime
from datetime import timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import Query
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.schemas.models import SlotsBase
from db.models import Slot

router = APIRouter(
    prefix="/meetings/slots",
    tags=["Meeting Slots"],
    responses={404: {"description": "Not found"}},
)

SLOT_LENGTH = timedelta(minutes=30)


@router.get("/",
            response_model=List[SlotsBase],
            )
def list_available_meeting_slots(
        start_time: Optional[datetime] = Query(default=None),
        end_time: Optional[datetime] = Query(default=None),
        db: Session = Depends(get_db)
):
    """Return list of all meeting slots"""
    query = db.query(Slot)
    if start_time is not None:
        query = query.filter(Slot.start_time >= start_time)
    if end_time is not None:
        query = query.filter(Slot.start_time + timedelta <= end_time)
    # Make sure the slot isn't assigned to a user
    query = query.filter(Slot.user_id == None)
    slots = query.all()

    return [
        SlotsBase(
            start_time=slot.start_time,
            end_time=slot.start_time + SLOT_LENGTH,
            advisor_name=slot.advisor_name,
            user_id=slot.user_id,
        )
        for slot in slots
    ]
