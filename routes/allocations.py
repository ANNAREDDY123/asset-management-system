from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.allocation import Allocation
from models.asset import Asset
from models.user import User

from schemas.allocation import AllocationCreate

router = APIRouter(
    prefix="/allocations",
    tags=["Allocations"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_allocation(
    allocation: AllocationCreate,
    db: Session = Depends(get_db)
):

    asset = db.query(Asset).filter(
        Asset.id == allocation.asset_id,
        Asset.is_active == True
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found."
        )

    employee = db.query(User).filter(
        User.id == allocation.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    active = db.query(Allocation).filter(
        Allocation.asset_id == allocation.asset_id,
        Allocation.allocation_status == "Assigned"
    ).first()

    if active:
        raise HTTPException(
            status_code=400,
            detail="This asset is already assigned to another employee."
        )

    new_allocation = Allocation(
        asset_id=allocation.asset_id,
        employee_id=allocation.employee_id,
        assigned_date=allocation.assigned_date,
        return_date=allocation.return_date,
        allocation_status="Assigned"
    )

    asset.status = "Assigned"

    db.add(new_allocation)
    db.commit()
    db.refresh(new_allocation)

    return new_allocation


@router.get("/")
def get_allocations(
    employee_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Allocation)

    if employee_id:
        query = query.filter(
            Allocation.employee_id == employee_id
        )

    total = query.count()

    allocations = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": allocations
    }


@router.get("/{allocation_id}")
def get_allocation(
    allocation_id: int,
    db: Session = Depends(get_db)
):

    allocation = db.query(Allocation).filter(
        Allocation.id == allocation_id
    ).first()

    if not allocation:
        raise HTTPException(
            status_code=404,
            detail="Allocation not found."
        )

    return allocation


@router.put("/{allocation_id}")
def update_allocation(
    allocation_id: int,
    allocation: AllocationCreate,
    db: Session = Depends(get_db)
):

    db_allocation = db.query(Allocation).filter(
        Allocation.id == allocation_id
    ).first()

    if not db_allocation:
        raise HTTPException(
            status_code=404,
            detail="Allocation not found."
        )

    db_allocation.return_date = allocation.return_date

    if allocation.return_date:
        db_allocation.allocation_status = "Returned"

        asset = db.query(Asset).filter(
            Asset.id == db_allocation.asset_id
        ).first()

        asset.status = "Available"

    db.commit()

    return {
        "message": "Allocation updated successfully."
    }


@router.get("/employee/{employee_id}")
def employee_assets(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Allocation).filter(
        Allocation.employee_id == employee_id
    ).all()
