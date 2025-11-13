# app/models/calculation.py

from abc import ABC, abstractmethod
from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship 

from app.database import Base

class Calculation(Base, ABC):
    __tablename__ = 'calculations'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    calculation_type = Column(String(50), nullable=False) ## Type of calculation - addition, subtraction, etc.
    input_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="calculations")
    
    __mapper_args__ = { 
        'polymorphic_on': calculation_type,
        'polymorphic_identity': 'calculation',
        'with_polymorphic': '*',  
    }
    @classmethod
    def create(cls, calulation_type: str, user_id: uuid.UUID, inputs: list[float]) -> 'Calculation':
        """Factory method to create specific calculation instances."""
        calculation_classes = {
            'addition': Addition,
            'subtraction': Subtraction,
            'multiplication': Multiplication,
            'division': Division,
        }
        calculation_classes = calculation_classes.get(calulation_type.lower())
        
        if not calculation_classes:
            raise ValueError(f"Unsupported calculation type: {calulation_type}")
        return calculation_classes(user_id=user_id, input_data={'inputs': inputs})
    
    @abstractmethod
    def get_result(self) -> float:
        """Abstract method to compute the result of the calculation."""
        raise NotImplementedError 
    
    def __repr__(self):
        return f"<Calculation(type={self.type}, inputs={self.inputs})>"
    
    
class Addition(Calculation):
    __mapper_args__ = {'polymorphic_identity': 'addition'}
    