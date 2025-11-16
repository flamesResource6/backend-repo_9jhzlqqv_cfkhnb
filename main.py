import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI(title="Property Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Property Management Backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# Simple create/list endpoints for core resources
class PropertyCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    unit: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    rent: Optional[float] = None
    status: str = "available"

class TenantCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    property_id: Optional[str] = None
    unit: Optional[str] = None
    move_in_date: Optional[str] = None
    is_active: bool = True

class MaintenanceRequestCreate(BaseModel):
    property_id: str
    tenant_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "open"

@app.post("/api/properties")
def create_property(payload: PropertyCreate):
    from schemas import Property
    try:
        doc = Property(**payload.model_dump())
        new_id = create_document("property", doc)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/properties")
def list_properties():
    try:
        docs = get_documents("property", {})
        # Convert ObjectId
        for d in docs:
            d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tenants")
def create_tenant(payload: TenantCreate):
    from schemas import Tenant
    try:
        doc = Tenant(**payload.model_dump())
        new_id = create_document("tenant", doc)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tenants")
def list_tenants():
    try:
        docs = get_documents("tenant", {})
        for d in docs:
            d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/maintenance")
def create_maintenance(payload: MaintenanceRequestCreate):
    from schemas import MaintenanceRequest
    try:
        doc = MaintenanceRequest(**payload.model_dump())
        new_id = create_document("maintenancerequest", doc)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/maintenance")
def list_maintenance():
    try:
        docs = get_documents("maintenancerequest", {})
        for d in docs:
            d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
