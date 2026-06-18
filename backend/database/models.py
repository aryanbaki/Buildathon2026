from sqlalchemy import (
    Column, String, Integer, Float, Date, DateTime, Text,
    ForeignKey, Enum, JSON, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class DocType(str, enum.Enum):
    TITLE = "title"
    REGISTRATION = "registration"
    INSURANCE = "insurance"
    MAINTENANCE = "maintenance"
    FUEL_RECEIPT = "fuel_receipt"
    TAX_FORM = "tax_form"
    INSPECTION = "inspection"
    REPAIR_INVOICE = "repair_invoice"
    OTHER = "other"


class Truck(Base):
    __tablename__ = "trucks"

    id = Column(String, primary_key=True)          # e.g. "truck_84"
    unit_number = Column(Integer, unique=True, nullable=False)
    vin = Column(String(17), unique=True)
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    license_plate = Column(String(20))
    state = Column(String(2))
    status = Column(String(20), default="active")  # active, inactive, sold
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    odometer = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    documents = relationship("Document", back_populates="truck")
    assignments = relationship("DriverAssignment", back_populates="truck")
    maintenance_records = relationship("MaintenanceRecord", back_populates="truck")
    fuel_records = relationship("FuelRecord", back_populates="truck")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    cdl_number = Column(String(30))
    cdl_expiry = Column(Date)
    phone = Column(String(20))
    email = Column(String(100))
    hire_date = Column(Date)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, server_default=func.now())

    assignments = relationship("DriverAssignment", back_populates="driver")
    documents = relationship("Document", back_populates="driver")


class Trailer(Base):
    __tablename__ = "trailers"

    id = Column(String, primary_key=True)
    unit_number = Column(Integer, unique=True)
    trailer_type = Column(String(50))
    capacity_tons = Column(Float)
    license_plate = Column(String(20))
    state = Column(String(2))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, server_default=func.now())

    documents = relationship("Document", back_populates="trailer")


class DriverAssignment(Base):
    __tablename__ = "driver_assignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(String, ForeignKey("trucks.id"), nullable=False)
    driver_id = Column(String, ForeignKey("drivers.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_primary = Column(Boolean, default=True)

    truck = relationship("Truck", back_populates="assignments")
    driver = relationship("Driver", back_populates="assignments")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    truck_id = Column(String, ForeignKey("trucks.id"))
    driver_id = Column(String, ForeignKey("drivers.id"))
    trailer_id = Column(String, ForeignKey("trailers.id"))
    doc_type = Column(Enum(DocType), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500))
    raw_text = Column(Text)
    extracted_metadata = Column(JSON)         # Claude's structured extraction
    doc_date = Column(Date)
    expiry_date = Column(Date)
    amount = Column(Float)                    # dollar value if applicable
    vendor = Column(String(200))
    notes = Column(Text)
    chroma_doc_id = Column(String(100))       # pointer into vector store
    confidence_score = Column(Float)          # extraction confidence 0-1
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    truck = relationship("Truck", back_populates="documents")
    driver = relationship("Driver", back_populates="documents")
    trailer = relationship("Trailer", back_populates="documents")


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(String, ForeignKey("trucks.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"))
    service_date = Column(Date)
    service_type = Column(String(100))        # oil change, tire rotation, brake pad, etc.
    vendor = Column(String(200))
    parts_cost = Column(Float, default=0.0)
    labor_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    odometer_at_service = Column(Integer)
    description = Column(Text)
    next_service_date = Column(Date)
    next_service_miles = Column(Integer)

    truck = relationship("Truck", back_populates="maintenance_records")


class FuelRecord(Base):
    __tablename__ = "fuel_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(String, ForeignKey("trucks.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"))
    fill_date = Column(Date)
    gallons = Column(Float)
    price_per_gallon = Column(Float)
    total_cost = Column(Float)
    location = Column(String(200))
    odometer = Column(Integer)

    truck = relationship("Truck", back_populates="fuel_records")
