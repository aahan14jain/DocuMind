import ast
import json
import sys
from typing import List, Dict, Any, Optional


def parse_python_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a Python file and extract functions, classes, and docstrings.
    
    Args:
        file_path (str): Path to the Python file to parse
        
    Returns:
        Dict[str, Any]: Dictionary containing parsed information
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
        
        return parse_python_content(source_code)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in file {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error parsing file {file_path}: {e}")


def parse_python_content(content: str) -> Dict[str, Any]:
    """
    Parse Python source code content and extract functions, classes, and docstrings.
    
    Args:
        content (str): Python source code as string
        
    Returns:
        Dict[str, Any]: Dictionary containing parsed information
    """
    try:
        tree = ast.parse(content)
        
        result = {
            'functions': [],
            'classes': [],
            'imports': [],
            'file_info': {
                'total_lines': len(content.split('\n')),
                'total_characters': len(content)
            }
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Regular function
                func_info = _extract_function_info(node, content)
                result['functions'].append(func_info)
            elif isinstance(node, ast.AsyncFunctionDef):
                # Async function
                func_info = _extract_function_info(node, content)
                func_info['is_async'] = True
                result['functions'].append(func_info)
            elif isinstance(node, ast.ClassDef):
                # Class definition
                class_info = _extract_class_info(node, content)
                result['classes'].append(class_info)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                # Import statements
                import_info = _extract_import_info(node)
                result['imports'].append(import_info)
        
        return result
    
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in content: {e}")
    except Exception as e:
        raise Exception(f"Error parsing content: {e}")


def _extract_function_info(node: ast.FunctionDef, content: str) -> Dict[str, Any]:
    """Extract detailed information about a function."""
    lines = content.split('\n')
    
    # Extract docstring
    docstring = None
    if (node.body and 
        isinstance(node.body[0], ast.Expr) and 
        isinstance(node.body[0].value, ast.Constant) and 
        isinstance(node.body[0].value.value, str)):
        docstring = node.body[0].value.value
    
    # Extract parameters
    parameters = []
    for arg in node.args.args:
        param_info = {
            'name': arg.arg,
            'annotation': ast.unparse(arg.annotation) if arg.annotation else None,
            'default': None
        }
        parameters.append(param_info)
    
    # Extract default values
    defaults = node.args.defaults
    for i, default in enumerate(defaults):
        if i < len(parameters):
            parameters[-(i+1)]['default'] = ast.unparse(default)
    
    # Extract return annotation
    return_annotation = ast.unparse(node.returns) if node.returns else None
    
    # Extract decorators
    decorators = [ast.unparse(dec) for dec in node.decorator_list]
    
    return {
        'name': node.name,
        'line_number': node.lineno,
        'docstring': docstring,
        'parameters': parameters,
        'return_annotation': return_annotation,
        'decorators': decorators,
        'is_async': False,
        'is_method': False  # Will be updated if inside a class
    }


def _extract_class_info(node: ast.ClassDef, content: str) -> Dict[str, Any]:
    """Extract detailed information about a class."""
    lines = content.split('\n')
    
    # Extract docstring
    docstring = None
    if (node.body and 
        isinstance(node.body[0], ast.Expr) and 
        isinstance(node.body[0].value, ast.Constant) and 
        isinstance(node.body[0].value.value, str)):
        docstring = node.body[0].value.value
    
    # Extract methods
    methods = []
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method_info = _extract_function_info(item, content)
            method_info['is_method'] = True
            methods.append(method_info)
    
    # Extract base classes
    base_classes = [ast.unparse(base) for base in node.bases]
    
    # Extract decorators
    decorators = [ast.unparse(dec) for dec in node.decorator_list]
    
    return {
        'name': node.name,
        'line_number': node.lineno,
        'docstring': docstring,
        'base_classes': base_classes,
        'decorators': decorators,
        'methods': methods
    }


def _extract_import_info(node: ast.Import | ast.ImportFrom) -> Dict[str, Any]:
    """Extract import statement information."""
    if isinstance(node, ast.Import):
        return {
            'type': 'import',
            'modules': [alias.name for alias in node.names],
            'line_number': node.lineno
        }
    else:  # ast.ImportFrom
        return {
            'type': 'from_import',
            'module': node.module,
            'names': [alias.name for alias in node.names],
            'level': node.level,
            'line_number': node.lineno
        }


def parse_python_file_to_json(file_path: str) -> str:
    """
    Parse a Python file and return the results as a JSON string.
    
    Args:
        file_path (str): Path to the Python file to parse
        
    Returns:
        str: JSON string containing parsed information
    """
    result = parse_python_file(file_path)
    return json.dumps(result, indent=2)


def parse_python_content_to_json(content: str) -> str:
    """
    Parse Python source code content and return the results as a JSON string.
    
    Args:
        content (str): Python source code as string
        
    Returns:
        str: JSON string containing parsed information
    """
    result = parse_python_content(content)
    return json.dumps(result, indent=2)


def extract_docstrings_only(content: str) -> Dict[str, str]:
    """
    Extract only docstrings from Python code.
    
    Args:
        content (str): Python source code as string
        
    Returns:
        Dict[str, str]: Dictionary mapping names to docstrings
    """
    try:
        tree = ast.parse(content)
        docstrings = {}
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    docstrings[node.name] = node.body[0].value.value
        
        return docstrings
    
    except Exception as e:
        raise Exception(f"Error extracting docstrings: {e}")


def main():
    """
    Test function to demonstrate the parser functionality.
    """
    # Test with a sample Python code
    sample_code = '''
import os
from typing import List, Dict, Any

class Calculator:
    """A simple calculator class for basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator with default values."""
        self.result = 0
        self.history = []
    
    def add(self, x: float, y: float) -> float:
        """Add two numbers and return the result.
        
        Args:
            x (float): First number to add.
            y (float): Second number to add.
            
        Returns:
            float: The sum of x and y.
        """
        result = x + y
        self.history.append(f"{x} + {y} = {result}")
        return result
    
    def subtract(self, x: float, y: float) -> float:
        """Subtract y from x and return the result."""
        result = x - y
        self.history.append(f"{x} - {y} = {result}")
        return result
    
    @property
    def last_result(self) -> float:
        """Get the last calculation result."""
        return self.result

async def process_data(data: List[Dict[str, Any]]) -> List[str]:
    """Process a list of data dictionaries asynchronously.
    
    Args:
        data: List of dictionaries containing data to process.
        
    Returns:
        List of processed strings.
    """
    results = []
    for item in data:
        # Process each item
        processed = str(item)
        results.append(processed)
    return results

def greet(name: str = "World") -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

class MathUtils:
    """Utility class for mathematical operations."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of a number.
        
        Args:
            n: Non-negative integer.
            
        Returns:
            Factorial of n.
            
        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n - 1)
'''
    
    print("Testing Enhanced Python Parser")
    print("=" * 50)
    
    # Test parsing content
    try:
        result = parse_python_content(sample_code)
        print("Parsed content:")
        print(json.dumps(result, indent=2))
        
        print("\nSummary:")
        print(f"Found {len(result['functions'])} functions")
        print(f"Found {len(result['classes'])} classes")
        print(f"Found {len(result['imports'])} imports")
        
        print("\nFunctions:")
        for func in result['functions']:
            print(f"  - {func['name']} (line {func['line_number']})")
            if func['docstring']:
                print(f"    Docstring: {func['docstring'][:50]}...")
        
        print("\nClasses:")
        for cls in result['classes']:
            print(f"  - {cls['name']} (line {cls['line_number']})")
            print(f"    Methods: {len(cls['methods'])}")
            if cls['docstring']:
                print(f"    Docstring: {cls['docstring'][:50]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with command line argument if provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"\nTesting with file: {file_path}")
        print("=" * 50)
        
        try:
            result = parse_python_file(file_path)
            print("Parsed file:")
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()