"""
Mermaid class diagram generator for Python files.
Parses Python code and generates Mermaid-compatible class diagrams.
"""

import ast
import sys


def _normalize_indentation(content: str) -> str:
    """Remove common leading whitespace from code block."""
    lines = content.split('\n')
    if not lines:
        return content
    
    min_indent = None
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            if min_indent is None or indent < min_indent:
                min_indent = indent
    
    if min_indent and min_indent > 0:
        normalized = []
        for line in lines:
            normalized.append(line[min_indent:] if line.strip() else line)
        return '\n'.join(normalized)
    
    return content


def generate_mermaid_diagram_from_code(source_code: str) -> str:
    """
    Generate a Mermaid class diagram from Python source code string.
    
    Args:
        source_code: Python source code as string.
        
    Returns:
        Mermaid diagram string.
    """
    # Normalize indentation
    source_code = _normalize_indentation(source_code)
    
    # Parse and extract classes
    tree = ast.parse(source_code)
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            for item in node.body:
                if isinstance(item, ast.ClassDef):
                    methods = []
                    for method in item.body:
                        if isinstance(method, ast.FunctionDef):
                            # Get parameters (skip 'self')
                            params = [arg.arg for arg in method.args.args]
                            if params and params[0] == 'self':
                                params = params[1:]
                            
                            # Format method signature
                            sig = f"{method.name}({', '.join(params)})" if params else f"{method.name}()"
                            methods.append(sig)
                    
                    classes.append({'name': item.name, 'methods': methods})
            break
    
    # Generate Mermaid diagram
    if not classes:
        return "classDiagram\n    class NoClassesFound"
    
    diagram = ["classDiagram"]
    for cls in classes:
        diagram.append(f"    class {cls['name']} {{")
        for method in cls['methods']:
            diagram.append(f"        + {method}")
        diagram.append("    }")
    
    return "\n".join(diagram)


def generate_mermaid_diagram(file_path: str) -> str:
    """
    Generate a Mermaid class diagram from a Python file.
    
    Args:
        file_path: Path to the Python file to parse.
        
    Returns:
        Mermaid diagram string in format:
        classDiagram
            class ClassName {
                + method1(param1, param2)
                + method2()
            }
    """
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    return generate_mermaid_diagram_from_code(source_code)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/diagram_generator.py <file_path>")
        print("Example: python core/diagram_generator.py test_sample.py")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        diagram = generate_mermaid_diagram(file_path)
        print(diagram)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: Syntax error in file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
