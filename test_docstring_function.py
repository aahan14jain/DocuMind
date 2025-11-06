def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)


def process_user_data(user_id: int, data: dict, include_metadata: bool = False) -> dict:
    """Process user data and return formatted result."""
    processed = {}
    processed['id'] = user_id
    processed['data'] = data
    if include_metadata:
        processed['metadata'] = {'processed_at': '2024-01-01'}
    return processed


def validate_email(email: str) -> bool:
    """Validate email address format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def find_prime_numbers(n: int) -> list:
    """Find first n prime numbers."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes


def merge_sorted_lists(list1: list, list2: list) -> list:
    """Merge two sorted lists into one sorted list."""
    result = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result


def calculate_statistics(numbers: list) -> dict:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    
    return {
        'mean': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'count': len(numbers)
    }


def fetch_api_data(url: str, timeout: int = 30, retries: int = 3) -> dict:
    """Fetch data from API endpoint."""
    import requests
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            continue


class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    def __init__(self, initial_value: float = 0.0):
        """Initialize calculator with optional starting value."""
        self.result = initial_value
        self.history = []
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers and return result."""
        self.result = x + y
        self.history.append(f"{x} + {y} = {self.result}")
        return self.result
    
    def subtract(self, x: float, y: float) -> float:
        """Subtract y from x and return result."""
        self.result = x - y
        self.history.append(f"{x} - {y} = {self.result}")
        return self.result

