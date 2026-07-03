from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.asset import Asset
from schemas.asset import AssetCreate

from services.asset_service import valid_asset_status

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Asset).filter(
        Asset.asset_tag == asset.asset_tag
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Asset tag already exists."
        )

    if not valid_asset_status(asset.status):
        raise HTTPException(
            status_code=400,
            detail="Invalid asset status."
        )

    new_asset = Asset(
        asset_name=asset.asset_name,
        asset_type=asset.asset_type,
        asset_tag=asset.asset_tag,
        purchase_date=asset.purchase_date,
        status=asset.status
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/")
def get_assets(
    asset_name: str = None,
    asset_tag: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Asset).filter(
        Asset.is_active == True
    )

    if asset_name:
        query = query.filter(
            Asset.asset_name.contains(asset_name)
        )

    if asset_tag:
        query = query.filter(
            Asset.asset_tag.contains(asset_tag)
        )

    if status:
        query = query.filter(
            Asset.status == status
        )

    total = query.count()

    assets = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": assets
    }


@router.get("/{asset_id}")
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):

    asset = db.query(Asset).filter(
        Asset.id == asset_id,
        Asset.is_active == True
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found."
        )

    return asset


@router.put("/{asset_id}")
def update_asset(
    asset_id: int,
    asset: AssetCreate,
    db: Session = Depends(get_db)
):

    db_asset = db.query(Asset).filter(
        Asset.id == asset_id,
        Asset.is_active == True
    ).first()

    if not db_asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found."
        )

    db_asset.asset_name = asset.asset_name
    db_asset.asset_type = asset.asset_type
    db_asset.asset_tag = asset.asset_tag
    db_asset.purchase_date = asset.purchase_date
    db_asset.status = asset.status

    db.commit()

    return {
        "message": "Asset updated successfully."
    }


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found."
        )

    asset.is_active = False

    db.commit()

    return {
        "message": "Asset deactivated successfully."
    }
