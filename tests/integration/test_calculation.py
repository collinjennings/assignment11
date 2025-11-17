# tests/integration/test_calculation.py

import pytest
from sqlalchemy.exc import IntegrityError
from app.models.calculation import Calculation, Addition, Subtraction, Multiplication, Division
from app.models.user import User
import uuid


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user for calculations."""
    user = User(
        first_name="Test",
        last_name="User",
        email=f"test_{uuid.uuid4()}@gmail.com",
        username=f"testuser_{uuid.uuid4()}",
        password=User.hash_password("TestPass123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user


class TestAddition:
    """Tests for Addition calculation."""
    
    def test_addition_basic(self, db_session, test_user):
        """Test basic addition calculation."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [1.0, 2.0, 3.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 6.0
        assert calc.calculation_type == 'addition'
        assert calc.inputs == [1.0, 2.0, 3.0]
    
    def test_addition_single_number(self, db_session, test_user):
        """Test addition with single number."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [5.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 5.0
    
    def test_addition_negative_numbers(self, db_session, test_user):
        """Test addition with negative numbers."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [-1.0, -2.0, 3.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 0.0
    
    def test_addition_invalid_inputs(self, db_session, test_user):
        """Test addition with invalid inputs."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': 'not-a-list'}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Inputs must be a list of numbers"):
            calc.get_result()


class TestSubtraction:
    """Tests for Subtraction calculation."""
    
    def test_subtraction_basic(self, db_session, test_user):
        """Test basic subtraction calculation."""
        calc = Subtraction(
            user_id=test_user.id,
            input_data={'inputs': [10.0, 3.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 5.0
        assert calc.calculation_type == 'subtraction'
    
    def test_subtraction_two_numbers(self, db_session, test_user):
        """Test subtraction with two numbers."""
        calc = Subtraction(
            user_id=test_user.id,
            input_data={'inputs': [8.0, 3.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 5.0
    
    def test_subtraction_negative_result(self, db_session, test_user):
        """Test subtraction resulting in negative number."""
        calc = Subtraction(
            user_id=test_user.id,
            input_data={'inputs': [5.0, 10.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == -5.0
    
    def test_subtraction_insufficient_inputs(self, db_session, test_user):
        """Test subtraction with less than 2 inputs."""
        calc = Subtraction(
            user_id=test_user.id,
            input_data={'inputs': [5.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Inputs must be a list of at least two numbers"):
            calc.get_result()
    
    def test_subtraction_invalid_inputs(self, db_session, test_user):
        """Test subtraction with invalid inputs."""
        calc = Subtraction(
            user_id=test_user.id,
            input_data={'inputs': 'not-a-list'}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Inputs must be a list of at least two numbers"):
            calc.get_result()


class TestMultiplication:
    """Tests for Multiplication calculation."""
    
    def test_multiplication_basic(self, db_session, test_user):
        """Test basic multiplication calculation."""
        calc = Multiplication(
            user_id=test_user.id,
            input_data={'inputs': [2.0, 3.0, 4.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 24.0
        assert calc.calculation_type == 'multiplication'
    
    def test_multiplication_with_zero(self, db_session, test_user):
        """Test multiplication with zero."""
        calc = Multiplication(
            user_id=test_user.id,
            input_data={'inputs': [5.0, 0.0, 3.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 0.0
    
    def test_multiplication_negative_numbers(self, db_session, test_user):
        """Test multiplication with negative numbers."""
        calc = Multiplication(
            user_id=test_user.id,
            input_data={'inputs': [-2.0, 3.0, -4.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 24.0
    
    def test_multiplication_single_number(self, db_session, test_user):
        """Test multiplication with single number."""
        calc = Multiplication(
            user_id=test_user.id,
            input_data={'inputs': [7.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 7.0
    
    def test_multiplication_invalid_inputs(self, db_session, test_user):
        """Test multiplication with invalid inputs."""
        calc = Multiplication(
            user_id=test_user.id,
            input_data={'inputs': 'not-a-list'}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Multiplication inputs must be a list of numbers"):
            calc.get_result()


class TestDivision:
    """Tests for Division calculation."""
    
    def test_division_basic(self, db_session, test_user):
        """Test basic division calculation."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [24.0, 4.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 3.0
        assert calc.calculation_type == 'division'
    
    def test_division_two_numbers(self, db_session, test_user):
        """Test division with two numbers."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [10.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 5.0
    
    def test_division_decimal_result(self, db_session, test_user):
        """Test division resulting in decimal."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [10.0, 4.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 2.5
    
    def test_division_by_zero(self, db_session, test_user):
        """Test division by zero raises error."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [10.0, 0.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            calc.get_result()
    
    def test_division_negative_numbers(self, db_session, test_user):
        """Test division with negative numbers."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [-24.0, 4.0, -2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.get_result() == 3.0
    
    def test_division_insufficient_inputs(self, db_session, test_user):
        """Test division with less than 2 inputs."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': [5.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Division inputs must be a list of at least two numbers"):
            calc.get_result()
    
    def test_division_invalid_inputs(self, db_session, test_user):
        """Test division with invalid inputs."""
        calc = Division(
            user_id=test_user.id,
            input_data={'inputs': 'not-a-list'}
        )
        db_session.add(calc)
        db_session.commit()
        
        with pytest.raises(ValueError, match="Division inputs must be a list of at least two numbers"):
            calc.get_result()


class TestCalculationFactory:
    """Tests for Calculation.create factory method."""
    
    def test_create_addition(self, test_user):
        """Test creating addition through factory."""
        calc = Calculation.create('addition', test_user.id, [1.0, 2.0, 3.0])
        assert isinstance(calc, Addition)
        assert calc.inputs == [1.0, 2.0, 3.0]
        assert calc.user_id == test_user.id
    
    def test_create_subtraction(self, test_user):
        """Test creating subtraction through factory."""
        calc = Calculation.create('subtraction', test_user.id, [10.0, 5.0])
        assert isinstance(calc, Subtraction)
        assert calc.inputs == [10.0, 5.0]
    
    def test_create_multiplication(self, test_user):
        """Test creating multiplication through factory."""
        calc = Calculation.create('multiplication', test_user.id, [2.0, 3.0])
        assert isinstance(calc, Multiplication)
        assert calc.inputs == [2.0, 3.0]
    
    def test_create_division(self, test_user):
        """Test creating division through factory."""
        calc = Calculation.create('division', test_user.id, [10.0, 2.0])
        assert isinstance(calc, Division)
        assert calc.inputs == [10.0, 2.0]
    
    def test_create_invalid_type(self, test_user):
        """Test creating calculation with invalid type."""
        with pytest.raises(ValueError, match="Unsupported calculation type: invalid"):
            Calculation.create('invalid', test_user.id, [1.0, 2.0])
    
    def test_create_case_insensitive(self, test_user):
        """Test factory method is case insensitive."""
        calc = Calculation.create('ADDITION', test_user.id, [1.0, 2.0])
        assert isinstance(calc, Addition)


class TestCalculationModel:
    """Tests for Calculation model functionality."""
    
    def test_calculation_repr(self, db_session, test_user):
        """Test calculation string representation."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [1.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        
        repr_str = repr(calc)
        assert 'addition' in repr_str
        assert '[1.0, 2.0]' in repr_str
    
    def test_calculation_relationship_with_user(self, db_session, test_user):
        """Test calculation has relationship with user."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [1.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        assert calc.user == test_user
        assert calc in test_user.calculations.all()
    
    def test_calculation_timestamps(self, db_session, test_user):
        """Test calculation has created_at and updated_at timestamps."""
        calc = Addition(
            user_id=test_user.id,
            input_data={'inputs': [1.0, 2.0]}
        )
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        assert calc.created_at is not None
        assert calc.updated_at is not None
        assert calc.id is not None
    
    def test_calculation_without_user_fails(self, db_session_with_savepoint):
        """Test calculation without user_id fails."""
        calc = Addition(
            input_data={'inputs': [1.0, 2.0]}
        )
        db_session_with_savepoint.add(calc)
        
        with pytest.raises(IntegrityError):
            db_session_with_savepoint.commit()
    
    def test_calculation_inputs_property_empty_data(self, db_session, test_user):
        """Test inputs property with empty input_data."""
        calc = Addition(
            user_id=test_user.id,
            input_data={}
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.inputs == []
    
    def test_calculation_inputs_property_none_data(self, db_session, test_user):
        """Test inputs property with None input_data."""
        calc = Addition(
            user_id=test_user.id,
            input_data=None
        )
        db_session.add(calc)
        db_session.commit()
        
        assert calc.inputs == []