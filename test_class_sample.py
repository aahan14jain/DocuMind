class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    result: float = 0.0
    history: list = []
    
    def __init__(self, initial_value: float = 0.0):
        """Initialize the calculator with an optional initial value."""
        self.result = initial_value
        self.history = []
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers and return the result."""
        result = x + y
        self.result = result
        self.history.append(f"{x} + {y} = {result}")
        return result
    
    def subtract(self, x: float, y: float) -> float:
        """Subtract y from x and return the result."""
        result = x - y
        self.result = result
        self.history.append(f"{x} - {y} = {result}")
        return result
    
    def multiply(self, x: float, y: float) -> float:
        result = x * y
        self.result = result
        self.history.append(f"{x} * {y} = {result}")
        return result
    
    def divide(self, x: float, y: float) -> float:
        if y == 0:
            raise ValueError("Cannot divide by zero")
        result = x / y
        self.result = result
        self.history.append(f"{x} / {y} = {result}")
        return result
    
    @property
    def last_result(self) -> float:
        return self.result
    
    def get_history(self) -> list:
        return self.history.copy()
    
    def clear_history(self) -> None:
        self.history.clear()
        self.result = 0.0
    
    @staticmethod
    def calculate_power(base: float, exponent: float) -> float:
        return base ** exponent
    
    @classmethod
    def create_from_result(cls, previous_result: float):
        instance = cls()
        instance.result = previous_result
        return instance

