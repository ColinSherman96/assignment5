# calculator_calculations.py

# -----------------------------------------------------------------------------------
# Import Statements
# -----------------------------------------------------------------------------------
# Colin Sherman - 6/14/2026. Trying to implement the statements for the calcultor classes, based off the template from Prof. Keith Williams. Much of this code is my attempt to build a version off of this template: it is not a copy, but rather an attempt to build my own version of the calculator classes. I have added comments to explain my thought process and the design choices I made in implementing this code. 

# Importing ABC allows us to specify that Calculation is an Abstract Base Class, which means it cannot be instantiated directly and must be subclassed. The abstractmethod decorator is used to indicate that the execute method must be implemented by any subclass of Calculation.
from abc import ABC, abstractmethod

# We also need to import the operation class from the app.operation module. Had to adjust slightly from the template, as my naming conventions were slightly different.

from app.operations import operations

# -----------------------------------------------------------------------------------
# Abstract Base Class: Operation
# -----------------------------------------------------------------------------------
class Operation(ABC):
    """
    The Operation class is an Abstract Base Class (ABC) that defines a blueprint 
    for all mathematical operations in the calculator program. This class establishes 
    a consistent interface that all operation types (such as addition, subtraction, etc.) 
    must follow. 

    This Operation class makes a layout for the calculator - which will be used for all calculations it attempts. It establishes conventions/norms for the various operations.
    
    The template had a very good definition written for ABCs - so rather than attempt to reinvent the wheel, I've included it here:
    
    Why Use an Abstract Base Class?
    - **Abstraction**: By using an ABC, we focus on "what" calculations need to do (execute an operation) 
      rather than "how" each specific operation is implemented. This simplifies our design.
    - **Polymorphism**: By providing a standard interface, any Operation subclass can be used 
      interchangeably, allowing the program to treat each type of operation in a consistent manner.
    - **Enforcing Consistency**: The abstract `execute` method enforces that all subclasses implement 
      their own specific version of the calculation logic, making sure that each type of calculation 
      has an `execute` method.
    """

    def __init__(self, a: float, b: float) -> None:
        """
        We know that, for the most basic cases, we will need two numbers to perform calculations on the calculator. This initializer method sets up the basic structure for any Calculation object, ensuring that it has the necessary operands to perform its function.
        
        Once again leaving the definition here, as it is sufficiently detailed and well-written:
        **Why Have an Initializer?**
        - This initializer method ensures that each Operation object will have two numbers (`a` and `b`) 
          to work with, no matter the specific type of operation.
        - Encapsulating the operands within an instance allows each Operation object to maintain its own 
          state (values of `a` and `b`), supporting **Object-Oriented Design** principles.

        **Parameters:**
        It takes two parameters, 'a' and 'b', which represent the two numbers that will be used in the calculation. These are stored as instance variables for use in the `execute` method of each subclass.
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.

        """
        self.a: float = a  # Stores the first operand as a floating-point number.
        self.b: float = b  # Stores the second operand as a floating-point number.

    @abstractmethod
    def execute(self) -> float:
        """
        I had a bit of trouble wrapping my head around the concept of abstract methods, but I think I understand it now. An abstract method is a method that is declared in an abstract class but does not have an implementation in that class. Instead, it must be implemented by a subclass that inherits it from the abstract class.

        Once again, the template had a very good definition of abstract methods, so I have included it here:
        **Why Use an Abstract Method?**
        - Enforces that each subclass provides its own specific version of `execute`, 
          which is crucial for following the interface defined by Operation.
        - Abstract methods define "must-have" methods for subclasses. By including `execute` here, 
          we ensure that any class inheriting from Operation will have this method, making 
          it easier to work with multiple types of operations in a flexible way.
        
        **Returns:**
        - `float`: The result of the operation.
        """
        pass  # Since we write the implementation in the subclasses, we do not need to implement it here. # pragma: no cover

    def __str__(self) -> str:
        """
        Just wanted to preface here: I figured I would attempt to rewrite every comment that was in the original template in my own words. I think writing with my own take will help me to further understand the program that we are working with.
        The `__str__` method provides a string representation of the Operation instance (one that is considered user-friendly), showing the operation and its result in a readable format. It allows results to the user in a clear and concise way.

        **Returns:**
        - `str`: A string describing the operation and its result.
        """
        
        result = self.execute()  # Run the operation to get the result.
        class_name = self.__class__.__name__
        operation_name = self.__class__.__name__.replace('Operation', '')  # Derive operation name.
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"

    def __repr__(self) -> str:
        """
        I wasn't as sure what this does at first - but it seems like it provides a more detailed string representation of the Calculation instance! This is useful for debugging and development purposes. It shows the class name and the operands in a format that is more informative.

        **Returns:**
        - `str`: A string containing the class name and operands.
        """
        return f"{self.__class__.__name__}(a={self.a}, b={self.b})"

# -----------------------------------------------------------------------------------
# Factory Class: CalculationFactory
# -----------------------------------------------------------------------------------
class CalculationFactory:
    """
    Since the assignment specifies using CalculationFactory, I have refrained from renaming it,
    though for the sake of the naming conventions I used, "OperationFactory" might have been a more fitting name. 
    However, I will keep the name as is to avoid confusion with the template and to stay consistent with the assignment requirements.
    
    The CalculationFactory is the "bread and butter" of this program and this assignment,
    if such a thing exists. It is the class that allows us to create instances of the various
    operations and calculations (i.e. addition, subtraction, multiplication, division) without
    needing to know the specific details of how each of those calculations was implemented.
    For us as students, it's a great example of how to use the factory design pattern, and incorporate
    encapsulation and abstraction into our code.

    Once again keeping the template's definition here, as it is sufficiently detailed and well-written:
    **Why Use a Factory Class?**
    - **Single Responsibility Principle (SRP)**: The factory only deals with object creation. 
      This keeps our code organized, as the logic for creating different calculations is 
      separated from the calculations themselves.
    - **Open/Closed Principle (OCP)**: We can add new calculation types without changing 
      the existing codebase. We simply register new calculation classes, making our 
      code extensible and flexible to future modifications.
    """

    # _operations_log is a dictionary type - I wanted to try using my own to see if I can understand the implementation! 
    # It holds a mapping of calculation types (like "add" or "subtract") to their respective classes.
    # Here, we're just initializing it as an empty dictionary, and we will populate it using the register_calculation decorator method.
    _operations_log = {}

    @classmethod
    def register_operation(cls, type_of_operation: str):
        """
        register_operation is my version of a decorator! It is used to register a specific 
        Calculation subclass under a unique calculation type, which is then stored in 
        the _operations_log dictionary. Registering classes with string identifiers -like 
        "add" or "multiply" -enables easy access to different operations dynamically at runtime.

        This became easier to understand once I thought of it as a way to note each new operation
        that we create, and to keep track of it in a way that allows us to easily access it later.

        Once again, why reinvent the wheel when the wheel is well constructed? Here are the
        parameters and benefits of using this decorator, as explained in the original template:
        **Parameters:**
        - `type_of_operation(str)`: A short identifier for the type of calculation 
          (e.g., 'add' for addition).
        
        **Benefits of Using a Decorator for Registration:**
        - **Modularity**: By using a decorator, we can easily add new calculations by 
          annotating new subclasses with `@CalculationFactory.add_to_log`.
        - **Dynamic Binding**: This approach binds each calculation type to a class dynamically, 
          allowing us to extend our application without altering the core logic.
        """
        def decorator(subclass):
            print(f"Attempting to register operation: {type_of_operation}")
            # Convert the type of the operation to lowercase to ensure consistency.
            operation_type_lower = type_of_operation.lower()
            # Check if the calculation type has already been registered (avoid dupes)
            if operation_type_lower in cls._operations_log:
                print(f"Duplicate registration detected for: {type_of_operation}")
                raise ValueError(f"The operation type '{type_of_operation}' is already registered.")
            # Register the subclass in the _operations_log dictionary.
            cls._operations_log[operation_type_lower] = subclass
            print(f"Registered {type_of_operation}")
            return subclass  # Return the subclass for chaining or additional use.
        return decorator  # Return the decorator function.

    @classmethod

    def create_operation(cls, type_of_operation: str, a: float, b: float) -> Operation:
        """
        This is a factory method that creates instances of Operation subclasses based on 
        the type of operation that is specified.

        **Parameters:**
        - `type_of_operation (str)`: The type of operation occurred ('add', 'subtract', 'multiply', 'divide').
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.
        
        **Returns:**
        - `Operation`: An instance of the appropriate Operation subclass.

        **How Does This Help?**
        - By centralizing object creation here, we only need to specify operation types 
          as strings, making it easy to choose different operations dynamically. 
        - **Error Handling**: If the specified type is not available, we provide a 
          clear error message listing valid options, helping prevent errors and 
          ensuring the user knows the supported types.
        """
    
        operation_class = cls._operations_log.get(type_of_operation.lower())
        # If the type is unsupported, raise an error with the available types.
        if not operation_class:
            available_types = ', '.join(cls._operations_log.keys())
            raise ValueError(f"Unsupported operation type: '{type_of_operation}'. Available types: {available_types}")
        # Create and return an instance of the requested operation class with the provided operands.
        return operation_class(a, b)

# -----------------------------------------------------------------------------------
# Concrete Operation Classes
# -----------------------------------------------------------------------------------

# Each of these classes defines a specific operation type (addition, subtraction, 
# multiplication, or division). These classes inherit from Operation, implementing 
# the `execute` method to perform the specific arithmetic operation. 
@CalculationFactory.register_operation('add')  # Registering the AdditionOperation class with the factory under the 'add' type.
class AdditionOperation(Operation):
    """
    AddititonOperation represents a single instance of an addition operation between two numbers.
    
    **Why Create Separate Classes for Each Operation?**
    - **Polymorphism**: Each operation type can be used interchangeably through the `execute` method.
    - **Modularity**: Encapsulating each operation in a separate class makes it easy to 
      modify, test, or extend without affecting other operations.
    - **Clear Responsibility**: Each class has a clear, single purpose, making the code easier to read.
    """

    def execute(self) -> float:
        # Calls the addition method from the Operation module to perform the addition.
        return operations.addition(self.a, self.b)

@CalculationFactory.register_operation('subtract')  # Registering the SubtractOperation class with the factory under the 'subtract' type.
class SubtractOperation(Operation):
    """
    SubtractOperation represents a single instance of a subtraction operation between two numbers.
    
    **Implementation Note**: This class specifically handles subtraction, keeping 
    the implementation separate from other operations.
    """

    def execute(self) -> float:
        # Calls the subtraction method from the Operation module to perform the subtraction.
        return operations.subtraction(self.a, self.b)

@CalculationFactory.register_operation('multiply')  # Registering the MultiplyOperation class with the factory under the 'multiply' type.
class MultiplyOperation(Operation):
    """
    MultiplyOperation represents a single instance of a multiplication operation between two numbers.
    
    By encapsulating the multiplication logic here, we achieve a clear separation of 
    concerns, making it easy to adjust the multiplication logic without affecting other calculations.
    """

    def execute(self) -> float:
        # Calls the multiplication method from the Operation module to perform the multiplication.
        return operations.multiplication(self.a, self.b)

@CalculationFactory.register_operation('divide')  # Registering the DivideOperation class with the factory under the 'divide' type.
class DivideOperation(Operation):
    """
    DivideOperation represents a single instance of a division operation between two numbers.
    
    **Special Case - Division by Zero**: Division requires extra error handling to 
    prevent dividing by zero, which would cause an error in the program. This class 
    checks if the second operand is zero before performing the operation.
    """

    def execute(self) -> float:
        # Before performing division, check if `b` is zero to avoid ZeroDivisionError.
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        # Calls the division method from the Operation module to perform the division.
        return operations.division(self.a, self.b)

@CalculationFactory.register_operation('power')  # Registering the PowerOperation class with the factory under the 'power' type.
class PowerOperation(Operation):
    """
    PowerOperation represents a single instance of an exponentiation operation between two numbers. 
    """
    def execute(self) -> float:
        # Calls the power method from the Operation module to perform the exponentiation.
        return operations.power(self.a, self.b) # pragma: no cover

@CalculationFactory.register_operation('modulus')  # Registering the ModulusOperation class with the factory under the 'modulus' type.
class ModulusOperation(Operation):
    """
    ModulusOperation represents a single instance of a modulus operation between two numbers. 
    """
    def execute(self) -> float:
        # Calls the modulus method from the Operation module to perform the modulus operation.
        return operations.modulus(self.a, self.b) # pragma: no cover