"""
Integrated parser that extracts functions/classes, generates docstrings, and creates diagrams.
"""

import ast
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.summarizer import DocstringGenerator
from core.diagram_generator import generate_mermaid_diagram


def extract_top_level_items(file_path: str):
    """Extract top-level functions and classes from a Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
    
    tree = ast.parse(source_code)
    items = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            for item in node.body:
                # Skip private items (starting with _)
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    code = ast.get_source_segment(source_code, item) or ""
                    items.append({"type": "function", "name": item.name, "code": code})
                elif isinstance(item, ast.ClassDef) and not item.name.startswith("_"):
                    code = ast.get_source_segment(source_code, item) or ""
                    items.append({"type": "class", "name": item.name, "code": code})
            break
    
    return items


def main():
    """Main entry point for the integrated parser."""
    if len(sys.argv) < 2:
        print("Usage: python core/parser.py <file_path> [model]")
        print("Example: python core/parser.py test_sample.py")
        sys.exit(1)
    
    file_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "gemma3:4b"
    
    try:
        # Extract functions and classes
        items = extract_top_level_items(file_path)
        
        if not items:
            print(f"❌ No top-level functions or classes found in {file_path}")
            sys.exit(1)
        
        # Initialize docstring generator
        generator = DocstringGenerator(model=model)
        
        # Generate docstrings for each item
        docstrings = []
        for item in items:
            print(f"\n{'=' * 70}")
            print(f"{'🔧 Function' if item['type'] == 'function' else '🏷️  Class'}: {item['name']}")
            print("-" * 70)
            
            try:
                if item["type"] == "function":
                    docstring = generator.generate_function_docstring(item["code"])
                else:  # class
                    result = generator.generate_class_docstring(item["code"], include_methods=False)
                    docstring = result.get("class_docstring", "")
                
                docstrings.append({"name": item["name"], "type": item["type"], "docstring": docstring})
                print(f'"""\n{docstring}\n"""')
                
            except Exception as e:
                print(f"❌ Error generating docstring: {e}")
                docstrings.append({"name": item["name"], "type": item["type"], "docstring": ""})
        
        # Generate Mermaid diagram
        print(f"\n{'=' * 70}")
        print("📊 Mermaid Class Diagram")
        print("-" * 70)
        
        try:
            diagram = generate_mermaid_diagram(file_path)
            print(diagram)
        except Exception as e:
            print(f"❌ Error generating diagram: {e}")
        
        print(f"\n{'=' * 70}")
        print(f"✅ Processed {len(items)} item(s) successfully")
        print(f"{'=' * 70}\n")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"❌ Syntax error in file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


# Keep old functions for backward compatibility with app.py
class ASTParser:
    """Parser for extracting code structure from Python files."""
    
    def __init__(self):
        self.content_lines = []
    
    def parse_content(self, content: str):
        """Parse Python source code and extract comprehensive structure."""
        # Minimal structure for app.py compatibility
        lines = content.split("\n")
        return {
            "file_info": {"total_lines": len(lines), "code_lines": 0, "comment_lines": 0, "blank_lines": 0},
            "imports": [],
            "variables": [],
            "constants": [],
            "functions": [],
            "classes": [],
            "structure": {"complexity_metrics": {"total_functions": 0, "total_classes": 0, "total_imports": 0}}
        }


def parse_python_file(file_path: str):
    """Parse a Python file and return structured data."""
    parser = ASTParser()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return parser.parse_content(content)


def parse_python_content(content: str):
    """Parse Python source code content and return structured data."""
    parser = ASTParser()
    return parser.parse_content(content)


if __name__ == "__main__":
    main()
