def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_user_data(user_id: int, data: dict, include_metadata: bool = False) -> dict:
    if not user_id or user_id <= 0:
        raise ValueError("User ID must be a positive integer")
    
    processed = {
        'user_id': user_id,
        'data': data.copy()
    }
    
    if include_metadata:
        processed['metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    return processed

def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

async def fetch_api_data(url: str, timeout: int = 30) -> dict:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            return await response.json()

def merge_sorted_lists(list1: list, list2: list) -> list:
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

