def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_data(data_list):
    """Process a list of data items."""
    results = []
    for item in data_list:
        processed = str(item).upper()
        results.append(processed)
    return results

class DataProcessor:
    """A class for processing various types of data."""
    
    def __init__(self, name):
        self.name = name
        self.processed_count = 0
    
    def process_item(self, item):
        """Process a single data item."""
        self.processed_count += 1
        return f"Processed {item} by {self.name}"
    
    def get_stats(self):
        """Get processing statistics."""
        return {
            'name': self.name,
            'processed_count': self.processed_count
        }

def validate_email(email):
    """Validate email address format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


