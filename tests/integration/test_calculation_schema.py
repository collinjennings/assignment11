# app/schemas/calculation.py

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CalculationBase(BaseModel):
    """
    Base schema for Calculation models.
    
    """
    type : str = Field(..., description="Type of calculation (e.g., addition, subtraction)", example="addition")

    inputs: List[float] = Field(..., description="List of input numbers for the calculation", example=[1.0, 2.0, 3.0])
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate that type is not empty and is a valid calculation type."""
        if not v or not v.strip():
            raise ValueError("Calculation type cannot be empty")
        
        valid_types = ['addition', 'subtraction', 'multiplication', 'division']
        if v not in valid_types:
            raise ValueError(f"Invalid calculation type: {v}. Must be one of {valid_types}")
        return v
    

class CalculationCreate(CalculationBase):
    """
    Schema for creating a new Calculation.
    
    """
    user_id: UUID = Field(..., description="ID of the user who created the calculation", example="123e4567-e89b-12d3-a456-426614174000")
    
    
class CalculationRead(CalculationBase):
    """
    Schema for reading Calculation data.
    
    """
    pass 

class CalculationUpdate(BaseModel):
    """
    Schema for updating an existing Calculation.
    
    """
    inputs: Optional[List[float]] = Field(None, description="Updated list of input numbers for the calculation", example=[4.0, 5.0])
    
    model_config = ConfigDict(from_attributes=True)
    
class CalculationResponse(CalculationBase):
    """
    Schema for returning Calculation data.
    
    """
    id: UUID = Field(..., description="Unique identifier for the calculation", example="123e4567-e89b-12d3-a456-426614174000")
    user_id: UUID = Field(..., description="ID of the user who created the calculation", example="123e4567-e89b-12d3-a456-426614174000")
    created_at: datetime = Field(..., description="Timestamp when the calculation was created", example="2023-10-01T12:00:00Z")
    updated_at: datetime = Field(..., description="Timestamp when the calculation was last updated", example="2023-10-01T12:30:00Z")
    
    model_config = ConfigDict(from_attributes=True)