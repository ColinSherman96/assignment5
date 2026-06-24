"""These are the unit tests for the operations module. While it may not be necessary for me to write this description, we are practicing coding conventions - so I figured it would be a good habit to get in the practice of describing what each section of my project does. Here, we introduce parameterized tests - allowing for the same testing as with Assignment 2, but with less duplicate code."""

import pytest
from decimal import Decimal
from typing import Any, Dict, Type
 # Looking at the template, seems like this is used for the type hinting mentioned in the modules

from app.exceptions import OperationError
from app.operations import OperationFactory
from app.operations import(
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory
)
import operator


"""
Hello Prof. Williams, Arash, or whoever may be reading this! Just wanted to say that I am enjoying the course and hope you are doing well. Here's a coding duck to brighten your day a bit!

⡀⣠⣴⣶⣶⣿⣿⣷⣶⣶⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢶⣾⣿⡿⠿⠉⠉⠉⠉⠹⠿⣿⣿⣿⣆⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣴⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⣙⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠿⠙⣿⣿⡤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⣿⡇⠀⣀⣀⠀⠀⠀⠀⣰⣦⣤⣠⣤⣤⣤⣄⡘⣿⣷⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⡇⠘⣿⣿⠇⠀⠀⣴⡿⢁⣉⣭⣥⣤⣼⣿⠇⢹⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢺⣿⣧⠀⠀⠀⢀⣴⡿⢏⣴⣿⠟⢉⣩⣽⠟⠁⠀⠀⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣿⡆⠀⢀⣾⣏⣴⡿⣛⣥⣶⠿⠋⠁⠀⠀⠀⠀⢸⣿⣿⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣿⣷⠀⣾⣿⣿⡿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣶⣄⡙⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⡍⠛⠿⢿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣾⣿⠀⠀⠀⠀⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣮⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⣿⣿⠀⠀⠀⠀⠈⢿⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣇⠄⠀⠀⠀⠀⠀⠀⠀
⢐⣿⣿⣿⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⢸⣿⠀⣿⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⠀⠀⠀⠀⠀⠀⠀
⢸⣿⠀⠈⠙⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀
⢸⣿⡄⠀⠀⠀⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣷⠀⠀⠀⠀⠀⠀
⠹⣿⣧⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡗⡀⠀⠀⠀⠀
⠀⢻⣿⣆⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡧⡇⠀⠀⠀⠀
⠀⢸⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣇⠃⠀⠀⠀⠀
⠀⠘⣿⣧⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡟⠀⠀⠀⠀⠀⠀
⠀⠀⠙⢿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⠹⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣧⣶⣧⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠈⠻⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣾⣿⣿⡿⡟⣿⣿⣶⣀⠀⠀⡀
⠀⠀⠀⠀⠀⠀⠈⠈⢟⢿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣟⣟⡻⢏⣳⣽⣷⢎⡽⢻⣿⣷⣿⡷
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⠿⣿⣮⡷⣋⢾⡻⣝⣮⣼⣿⣿⡿⠏⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣯⣿⣿⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠉⠻⠿⡿⠾⠿⠿⠿⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣇⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

class TestOperation:
    """Test base Operation class functionality."""

    def test_str_representation(self):
        """Test that string representation returns class name."""
        class TestOp(Operation):
            def _execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a + b

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """Base test class for all operations."""

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test operation with valid inputs."""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test operation with invalid inputs raises appropriate errors."""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", OperationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


class TestAddition(BaseOperationTest):
    """Test Addition operation."""

    operation_class = Addition
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "8"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-8"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-2"},
        "zero_sum": {"a": "5", "b": "-5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "8.8"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e10",
            "expected": "20000000000"
        },
    }
    invalid_test_cases = {}  # Addition has no invalid cases


class TestSubtraction(BaseOperationTest):
    """Test Subtraction operation."""

    operation_class = Subtraction
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-8"},
        "zero_result": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e9",
            "expected": "9000000000"
        },
    }
    invalid_test_cases = {}  # Subtraction has no invalid cases


class TestMultiplication(BaseOperationTest):
    """Test Multiplication operation."""

    operation_class = Multiplication
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "15"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "15"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-15"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "18.15"},
        "large_numbers": {
            "a": "1e5",
            "b": "1e5",
            "expected": "10000000000"
        },
    }
    invalid_test_cases = {}  # Multiplication has no invalid cases


class TestDivision(BaseOperationTest):
    """Test Division operation."""

    operation_class = Division
    valid_test_cases = {
        "positive_numbers": {"a": "6", "b": "2", "expected": "3"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-6", "b": "2", "expected": "-3"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2.75"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": OperationError,
            "message": "Division by zero is not allowed"
        },
    }


class TestPower(BaseOperationTest):
    """Test Power operation."""

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": "2", "b": "3", "expected": "8"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "one_exponent": {"a": "5", "b": "1", "expected": "5"},
        "decimal_base": {"a": "2.5", "b": "2", "expected": "6.25"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "2",
            "b": "-3",
            "error": OperationError,
            "message": "Negative exponents not supported"
        },
    }


class TestRoot(BaseOperationTest):
    """Test Root operation."""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "27", "b": "3", "expected": "3"},
        "fourth_root": {"a": "16", "b": "4", "expected": "2"},
        "decimal_root": {"a": "2.25", "b": "2", "expected": "1.5"},
    }
    invalid_test_cases = {
        "negative_base": {
            "a": "-9",
            "b": "2",
            "error": OperationError,
            "message": "Cannot calculate root of negative number"
        },
        "zero_root": {
            "a": "9",
            "b": "0",
            "error": OperationError,
            "message": "Zero root is undefined"
        },
    }


class TestOperationFactory:
    """Test OperationFactory functionality."""

    def test_create_valid_operations(self):
        """Test creation of all valid operations."""
        operation_map = {
            'add': Addition,
            'subtract': Subtraction,
            'multiply': Multiplication,
            'divide': Division,
            'power': Power,
            'root': Root,
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)
            # Test case-insensitive
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):
        """Test creation of invalid operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")

    def test_register_valid_operation(self):
        """Test registering a new valid operation."""
        class NewOperation(Operation):
            def _execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a + b

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test registering an invalid operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)

def test_operation_execute_invalid_operands():
    operation = OperationFactory.create_operation('add')

    with pytest.raises(OperationError, match="Invalid operand"):
        operation.execute("invalid", "data")

def test_division_by_zero_triggers_exception():
    # Create the division operation
    division_op = OperationFactory.create_operation('divide')
    
    # Call execute with divisor zero to trigger exception
    with pytest.raises(OperationError) as excinfo:
        division_op.execute(Decimal('1'), Decimal('0'))
    
    # Verify the exception message contains "Calculation failed:"
    assert "Calculation failed:" in str(excinfo.value)