import os
import re
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import ast
import inspect

# Load environment variables
load_dotenv()

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class DocstringGenerator:
    """
    A class for generating Python docstrings using OpenAI API.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the DocstringGenerator.
        
        Args:
            api_key (str, optional): OpenAI API key. If None, loads from environment.
            model (str): OpenAI model to use. Defaults to "gpt-3.5-turbo".
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file or pass it directly.")
        
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_docstring(self, function_code: str, function_name: Optional[str] = None) -> str:
        """
        Generate a docstring for a Python function using OpenAI API.
        
        Args:
            function_code (str): The Python function code as a string.
            function_name (str, optional): Name of the function. If None, will be extracted from code.
            
        Returns:
            str: Generated docstring content (without triple quotes).
        """
        try:
            # Extract function name if not provided
            if not function_name:
                function_name = self._extract_function_name(function_code)
            
            # Clean and prepare the function code
            cleaned_code = self._clean_function_code(function_code)
            
            # Create the prompt
            prompt = f"""Write a Python docstring for the following function following Google/NumPy style conventions:

Function name: {function_name}

Function code:
```python
{cleaned_code}
```

Generate a proper docstring with:
- Brief one-line summary
- Detailed description if needed
- Args section with parameter types and descriptions
- Returns section with return type and description
- Raises section if applicable

Return only the docstring content without triple quotes."""

            # Generate docstring using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer who writes clear, concise, and comprehensive docstrings following Google/NumPy style conventions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            docstring = response.choices[0].message.content.strip()
            
            # Clean up the response
            docstring = self._clean_docstring(docstring)
            
            return docstring
            
        except Exception as e:
            # Fallback to mock docstring if API fails
            return self._generate_mock_docstring(function_code, function_name)
    
    def generate_docstring_with_context(self, function_code: str, context: str = "", function_name: Optional[str] = None) -> str:
        """
        Generate a docstring with additional context about the function's purpose.
        
        Args:
            function_code (str): The Python function code as a string.
            context (str): Additional context about the function's purpose or usage.
            function_name (str, optional): Name of the function. If None, will be extracted from code.
            
        Returns:
            str: Generated docstring content (without triple quotes).
        """
        try:
            # Extract function name if not provided
            if not function_name:
                function_name = self._extract_function_name(function_code)
            
            # Clean and prepare the function code
            cleaned_code = self._clean_function_code(function_code)
            
            # Create the prompt with context
            context_info = f"\nAdditional context: {context}\n" if context else ""
            
            prompt = f"""Write a Python docstring for the following function following Google/NumPy style conventions:

Function name: {function_name}
{context_info}
Function code:
```python
{cleaned_code}
```

Generate a proper docstring with:
- Brief one-line summary
- Detailed description if needed
- Args section with parameter types and descriptions
- Returns section with return type and description
- Raises section if applicable

Return only the docstring content without triple quotes."""

            # Generate docstring using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer who writes clear, concise, and comprehensive docstrings following Google/NumPy style conventions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            docstring = response.choices[0].message.content.strip()
            
            # Clean up the response
            docstring = self._clean_docstring(docstring)
            
            return docstring
            
        except Exception as e:
            # Fallback to mock docstring if API fails
            return self._generate_mock_docstring(function_code, function_name)
    
    def _extract_function_name(self, function_code: str) -> str:
        """Extract function name from function code."""
        try:
            tree = ast.parse(function_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
                elif isinstance(node, ast.AsyncFunctionDef):
                    return node.name
            return "unknown_function"
        except:
            return "unknown_function"
    
    def _clean_function_code(self, function_code: str) -> str:
        """Clean and format function code for better processing."""
        # Remove leading/trailing whitespace
        cleaned = function_code.strip()
        
        # Remove existing docstrings to avoid confusion
        cleaned = re.sub(r'""".*?"""', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"'''.*?'''", '', cleaned, flags=re.DOTALL)
        
        # Remove extra blank lines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        return cleaned.strip()
    
    def _clean_docstring(self, docstring: str) -> str:
        """Clean up the generated docstring."""
        # Remove triple quotes if present
        docstring = re.sub(r'^"""|"""$', '', docstring, flags=re.MULTILINE)
        docstring = re.sub(r"^'''|'''$", '', docstring, flags=re.MULTILINE)
        
        # Remove leading/trailing whitespace
        docstring = docstring.strip()
        
        return docstring
    
    def _generate_mock_docstring(self, function_code: str, function_name: str) -> str:
        """Generate a mock docstring when API is not available."""
        # Extract parameters from function signature
        try:
            tree = ast.parse(function_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
                    args = []
                    for arg in node.args.args:
                        if arg.arg != 'self':  # Skip self parameter
                            args.append(f"{arg.arg} (Any): Parameter {arg.arg}")
                    
                    # Generate basic docstring
                    docstring = f"{function_name.replace('_', ' ').title()} function.\n\n"
                    
                    if args:
                        docstring += "Args:\n"
                        for arg in args:
                            docstring += f"    {arg}.\n"
                    
                    docstring += "\nReturns:\n    Any: The result of the function."
                    
                    return docstring
        except:
            pass
        
        # Fallback simple docstring
        return f"{function_name.replace('_', ' ').title()} function.\n\nReturns:\n    Any: The result of the function."
    
    def format_docstring_for_function(self, function_code: str, docstring: str) -> str:
        """
        Format the function code with the generated docstring.
        
        Args:
            function_code (str): Original function code.
            docstring (str): Generated docstring content.
            
        Returns:
            str: Function code with docstring properly inserted.
        """
        try:
            # Parse the function to find where to insert the docstring
            tree = ast.parse(function_code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Find the line after the function definition
                    func_line = node.lineno
                    
                    # Split code into lines
                    lines = function_code.split('\n')
                    
                    # Find the function definition line
                    func_def_line = None
                    for i, line in enumerate(lines):
                        if f"def {node.name}" in line or f"async def {node.name}" in line:
                            func_def_line = i
                            break
                    
                    if func_def_line is not None:
                        # Find the next non-empty line or the end of the function
                        insert_line = func_def_line + 1
                        
                        # Skip empty lines and comments
                        while insert_line < len(lines) and (
                            lines[insert_line].strip() == '' or 
                            lines[insert_line].strip().startswith('#')
                        ):
                            insert_line += 1
                        
                        # Insert the docstring
                        docstring_lines = docstring.split('\n')
                        formatted_docstring = ['    """'] + [f'    {line}' for line in docstring_lines] + ['    """']
                        
                        # Insert the docstring
                        for i, doc_line in enumerate(formatted_docstring):
                            lines.insert(insert_line + i, doc_line)
                        
                        return '\n'.join(lines)
            
            # Fallback: just prepend the docstring
            return f'    """\n{docstring}\n    """\n{function_code}'
            
        except Exception as e:
            # Fallback: just prepend the docstring
            return f'    """\n{docstring}\n    """\n{function_code}'


def generate_docstring(function_code: str, api_key: Optional[str] = None, context: str = "") -> str:
    """
    Convenience function to generate a docstring for a Python function.
    
    Args:
        function_code (str): The Python function code as a string.
        api_key (str, optional): OpenAI API key. If None, loads from environment.
        context (str): Additional context about the function's purpose.
        
    Returns:
        str: Generated docstring content (without triple quotes).
    """
    generator = DocstringGenerator(api_key=api_key)
    
    if context:
        return generator.generate_docstring_with_context(function_code, context)
    else:
        return generator.generate_docstring(function_code)


def main():
    """
    Test function to demonstrate the docstring generator.
    """
    # Sample function for testing
    sample_function = '''
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
'''
    
    print("Testing OpenAI Docstring Generator")
    print("=" * 50)
    
    try:
        # Test the generator
        generator = DocstringGenerator()
        
        print("Generating docstring for sample function...")
        docstring = generator.generate_docstring(sample_function)
        
        print("\nGenerated Docstring:")
        print("-" * 30)
        print(docstring)
        
        print("\nFormatted Function:")
        print("-" * 30)
        formatted_function = generator.format_docstring_for_function(sample_function, docstring)
        print(formatted_function)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure to set OPENAI_API_KEY in your .env file")
        print("Or install OpenAI: pip install openai")


if __name__ == "__main__":
    main()