"""
Database Schemas for Property Management App

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.

Examples:
- Property -> "property"
- Tenant -> "tenant"
- Lease -> "lease"
- MaintenanceRequest -> "maintenancerequest"
- Payment -> "payment"
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Property(BaseModel):
    name: str = Field(..., description="Property name (e.g., Greenview Apartments)")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., min_length=2, max_length=2, description="State code (e.g., CA)")
    zip_code: str = Field(..., description="ZIP/Postal code")
    unit: Optional[str] = Field(None, description="Unit/Suite number (if applicable)")
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[float] = Field(None, ge=0)
    rent: Optional[float] = Field(None, ge=0, description="Monthly rent for the unit/property")
    status: str = Field("available", description="Status: available, occupied, maintenance")

class Tenant(BaseModel):
    name: str = Field(..., description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    property_id: Optional[str] = Field(None, description="Associated property ID")
    unit: Optional[str] = Field(None, description="Unit number")
    move_in_date: Optional[date] = Field(None, description="Move-in date")
    is_active: bool = Field(True, description="Active tenant")

class Lease(BaseModel):
    property_id: str = Field(..., description="Property ID")
    tenant_id: str = Field(..., description="Tenant ID")
    start_date: date = Field(...)
    end_date: date = Field(...)
    monthly_rent: float = Field(..., ge=0)
    deposit: Optional[float] = Field(0, ge=0)
    status: str = Field("active", description="active, pending, terminated, expired")

class MaintenanceRequest(BaseModel):
    property_id: str = Field(..., description="Property ID")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")
    title: str = Field(..., description="Short title of the issue")
    description: Optional[str] = Field(None, description="Detailed description")
    priority: str = Field("medium", description="low, medium, high, urgent")
    status: str = Field("open", description="open, in_progress, completed, closed")

class Payment(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    lease_id: Optional[str] = Field(None, description="Lease ID")
    amount: float = Field(..., ge=0)
    date: date = Field(...)
    method: str = Field("online", description="online, cash, check, transfer")
    status: str = Field("received", description="received, pending, failed, refunded")
