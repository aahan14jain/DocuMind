import subprocess
import re
import ast


class DocstringGenerator:
    """
    Generates Python docstrings using a local Ollama model (e.g., gemma3:4b, phi3, llama3).
    Works completely offline, no API key required.
    """

    def __init__(self, model: str = "gemma3:4b"):
        """
        Initialize the generator and verify Ollama + model availability.
        """
        self.model = model
        self._check_ollama_available()

    def _check_ollama_available(self):
        """Ensure Ollama is installed and the chosen model exists."""
        try:
            # check ollama CLI
            version = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
            if version.returncode != 0:
                raise RuntimeError("Ollama not detected. Install from https://ollama.ai")

            # verify model
            models = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if self.model not in models.stdout:
                raise RuntimeError(
                    f"Model '{self.model}' not found.\nRun: ollama pull {self.model}\n\nAvailable:\n{models.stdout}"
                )

        except FileNotFoundError:
            raise RuntimeError("Ollama not installed or not in PATH. Download from https://ollama.ai")

    def _run_model(self, prompt: str) -> str:
        """Send prompt to Ollama and return its response."""
        result = subprocess.run(["ollama", "run", self.model, prompt],
                                capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")
        return result.stdout.strip()

    def _extract_function_name(self, code: str) -> str:
        """Extract the function name via AST."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except Exception:
            pass
        return "unknown_function"

    def _extract_class_name(self, code: str) -> str:
        """Extract the class name via AST."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    return node.name
        except Exception:
            pass
        return "UnknownClass"

    def _clean_code(self, code: str) -> str:
        """Remove existing docstrings and extra spaces."""
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        return code.strip()

    def generate_function_docstring(self, function_code: str, context: str = None, style: str = "google") -> str:
        """Generate docstring for a Python function."""
        func_name = self._extract_function_name(function_code)
        code_clean = self._clean_code(function_code)
        
        style_guides = {
            "google": """Google-style format:
- One-line summary (no blank line after)
- Blank line
- Detailed description (2-3 sentences max, if needed)
- Blank line
- Args:
    param_name (type): Brief description.
- Returns:
    type: Brief description.
- Raises:
    ExceptionType: Brief description (only if applicable).""",
            "numpy": """NumPy-style format:
- Brief summary (no blank line after)
- Blank line
- Extended summary (2-3 sentences max, if needed)
- Blank line
- Parameters
----------
param_name : type
    Brief description.
- Returns
-------
type
    Brief description.
- Raises
------
ExceptionType
    Brief description (only if applicable).""",
            "sphinx": """Sphinx-style format:
- Brief summary
- Blank line
- Detailed description (2-3 sentences max, if needed)
- :param param_name: Brief description
- :type param_name: type
- :returns: Brief description
- :rtype: type
- :raises ExceptionType: Brief description (only if applicable)"""
        }
        style_guide = style_guides.get(style, style_guides["google"])
        
        context_text = f"\n\nAdditional context: {context}" if context else ""

        prompt = f"""You are an expert Python developer. Generate a clean, concise {style} docstring for this function.

Function name: {func_name}
Code:
```python
{code_clean}
```
{context_text}

Follow this format exactly:
{style_guide}

CRITICAL RULES - READ CAREFULLY:
1. STRICTLY describe ONLY what this code actually does - do not invent or assume extra behavior
2. NO hypothetical validation, error handling, or optimizations that are not in the code
3. If the function simply prints or returns a value, describe exactly that - nothing more
4. Infer return type and behavior DIRECTLY from the code, not from best practices
5. Only document exceptions (Raises) if they are actually raised in the code
6. Only document parameters that actually exist in the function signature
7. Do not add validation checks, error handling, or edge cases that aren't implemented
8. Keep it CONCISE - one sentence per section when possible
9. NO function signature in the docstring (e.g., no "## fun(n)" or "fun(n)")
10. NO repetitive explanations
11. NO markdown headings (use plain text Args/Returns/Raises)
12. Use proper indentation (4 spaces for Args/Returns/Raises sections)

Example: If code is "def add(a, b): return a + b", docstring should say it adds two numbers and returns the sum. 
DO NOT add "raises TypeError if inputs are not numbers" unless that check actually exists in the code.

Return ONLY the docstring content (without triple quotes). Start directly with the one-line summary."""

        response = self._run_model(prompt)
        return self._clean_response(response)
    
    def generate_class_docstring(self, class_code: str, context: str = None, style: str = "google", include_methods: bool = False) -> dict:
        """Generate docstring for a Python class."""
        class_name = self._extract_class_name(class_code)
        code_clean = self._clean_code(class_code)
        
        style_guides = {
            "google": """Google-style format:
- One-line summary (no blank line after)
- Blank line
- Detailed description (2-3 sentences max, if needed)
- Blank line
- Attributes:
    attr_name (type): Brief description.
- Methods:
    method_name: Brief description.""",
            "numpy": """NumPy-style format:
- Brief summary (no blank line after)
- Blank line
- Extended summary (2-3 sentences max, if needed)
- Blank line
- Attributes
----------
attr_name : type
    Brief description.
- Methods
-------
method_name
    Brief description.""",
            "sphinx": """Sphinx-style format:
- Brief summary
- Blank line
- Detailed description (2-3 sentences max, if needed)
- :ivar attr_name: Brief description
- :type attr_name: type
- :method method_name: Brief description"""
        }
        style_guide = style_guides.get(style, style_guides["google"])
        
        context_text = f"\n\nAdditional context: {context}" if context else ""

        prompt = f"""You are an expert Python developer. Generate a clean, concise {style} docstring for this class.

Class name: {class_name}
Code:
```python
{code_clean}
```
{context_text}

Follow this format exactly:
{style_guide}

CRITICAL RULES - READ CAREFULLY:
1. STRICTLY describe ONLY what this class actually does - do not invent or assume extra behavior
2. NO hypothetical validation, error handling, or features that are not in the code
3. Only document attributes and methods that actually exist in the class
4. Infer behavior DIRECTLY from the code, not from best practices or common patterns
5. Do not add functionality, validation, or edge cases that aren't implemented
6. If a method simply returns a value, describe exactly that - nothing more
7. Only document exceptions (Raises) if they are actually raised in the code
8. Keep it CONCISE - one sentence per section when possible
9. NO class signature in the docstring (e.g., no "## ClassName" or "ClassName()")
10. NO repetitive explanations
11. NO markdown headings (use plain text Attributes/Methods)
12. Use proper indentation (4 spaces for Attributes/Methods sections)
13. Focus on the class purpose and main public API as actually implemented

Example: If a method is "def get_value(self): return self.value", docstring should say it returns the value attribute. 
DO NOT add "raises AttributeError if value is not set" unless that check actually exists in the code.

Return ONLY the docstring content (without triple quotes). Start directly with the one-line summary."""

        response = self._run_model(prompt)
        class_docstring = self._clean_response(response)
        
        result = {
            'class_name': class_name,
            'class_docstring': class_docstring,
            'methods': {}
        }
        
        if include_methods:
            # Extract and generate docstrings for methods
            try:
                tree = ast.parse(class_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                                try:
                                    method_code = ast.get_source_segment(class_code, item)
                                    if method_code:
                                        method_docstring = self.generate_function_docstring(method_code, style=style)
                                        result['methods'][item.name] = method_docstring
                                except Exception:
                                    continue
                        break
            except Exception:
                pass
        
        return result
    
    def _clean_response(self, response: str) -> str:
        """Clean up the model response to extract just the docstring."""
        # Remove code block markers
        response = re.sub(r'```python\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        
        # Remove function/class definitions
        lines = response.split('\n')
        cleaned = []
        skip_patterns = [r'^\s*def\s+', r'^\s*class\s+', r'^\s*return\s+']
        
        for line in lines:
            if any(re.match(pattern, line) for pattern in skip_patterns):
                continue
            if line.strip().startswith('```'):
                continue
            cleaned.append(line)
        
        result = '\n'.join(cleaned).strip()
        
        # Remove triple quotes if present
        result = re.sub(r'^"""|"""$', '', result, flags=re.MULTILINE)
        result = re.sub(r"^'''|'''$", '', result, flags=re.MULTILINE)
        
        # Try to extract from quoted blocks
        match = re.search(r'"""(.*?)"""', result, re.DOTALL)
        if match:
            result = match.group(1).strip()
        else:
            match = re.search(r"'''(.*?)'''", result, re.DOTALL)
            if match:
                result = match.group(1).strip()
        
        return result.strip()


# Convenience function
def generate_docstring(function_code: str, model: str = "gemma3:4b") -> str:
    """Simple function to generate a docstring."""
    generator = DocstringGenerator(model=model)
    return generator.generate_function_docstring(function_code)


if __name__ == "__main__":
    # Test
    gen = DocstringGenerator()
    sample = "def add(a, b): return a + b"
    print(gen.generate_function_docstring(sample))