# app/models/calculation.py

from abc import ABC, abstractmethod
from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, declarative_mixin, declared_attr
from sqlalchemy.orm import DeclarativeMeta
from abc import ABCMeta

from app.database import Base  # Import the EXISTING Base

# Create a combined metaclass
class CombinedMeta(DeclarativeMeta, ABCMeta):
    pass

# Use the combined metaclass with your existing Base
class Calculation(Base, metaclass=CombinedMeta):
    __tablename__ = 'calculations'

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    calculation_type = Column(String(50), nullable=False)
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
    def create(cls, calculation_type: str, user_id: uuid.UUID, inputs: list[float]) -> 'Calculation':
        """Factory method to create specific calculation instances."""
        calculation_classes = {
            'addition': Addition,
            'subtraction': Subtraction,
            'multiplication': Multiplication,
            'division': Division,
        }
        calculation_class = calculation_classes.get(calculation_type.lower())
        
        if not calculation_class:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calculation_class(user_id=user_id, input_data={'inputs': inputs})
    
    @abstractmethod
    def get_result(self) -> float:
        """Abstract method to compute the result of the calculation."""
        raise NotImplementedError
    
    @property
    def inputs(self):
        """Get inputs from input_data JSON."""
        return self.input_data.get('inputs', []) if self.input_data else []
    
    def __repr__(self):
        return f"<Calculation(type={self.calculation_type}, inputs={self.inputs})>"


class Addition(Calculation):
    __mapper_args__ = {'polymorphic_identity': 'addition'}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        return sum(self.inputs)


class Subtraction(Calculation):
    __mapper_args__ = {'polymorphic_identity': 'subtraction'}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Inputs must be a list of at least two numbers.")
        result = self.inputs[0]
        for num in self.inputs[1:]:
            result -= num
        return result


class Multiplication(Calculation):
    __mapper_args__ = {'polymorphic_identity': 'multiplication'}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Multiplication inputs must be a list of numbers.")
        result = 1
        for num in self.inputs:
            result *= num
        return result


class Division(Calculation):
    __mapper_args__ = {'polymorphic_identity': 'division'}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Division inputs must be a list of at least two numbers.")
        result = self.inputs[0]
        for num in self.inputs[1:]:
            if num == 0:
                raise ValueError("Division by zero is not allowed.")
            result /= num
        return result