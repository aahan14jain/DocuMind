import streamlit as st
import json
from core.parser import parse_python_file, parse_python_content
from core.summarizer import DocstringGenerator, generate_docstring
from core.diagram_generator import generate_mermaid_diagram, generate_mermaid_diagram_from_code

# Enhanced CSS for eye-catching UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        border: none;
        color: white;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        transition: all 0.5s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }
    
    .metric-card:hover::before {
        top: -30%;
        right: -30%;
    }
    
    .metric-card h3 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .function-card, .class-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .function-card:hover, .class-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Sidebar styling - fix visibility */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        background-color: rgba(255, 255, 255, 0.1) !important;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stInfo {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] .stInfo > div {
        color: white !important;
    }
    
    /* Glowing text effect */
    .glow-text {
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.8),
                     0 0 20px rgba(102, 126, 234, 0.6),
                     0 0 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Animated section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    /* Code block styling */
    .stCodeBlock {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Input styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="DocuMind - Python Code Parser & Docstring Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Animated Header with gradient
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 800;">📚 DocuMind</h1>
    <p style="margin: 1rem 0 0 0; font-size: 1.4rem; opacity: 0.95; font-weight: 400;">
        Python Code Parser & Docstring Generator
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.85;">
        Transform your code into beautiful documentation ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    st.markdown("---")
    
    page = st.radio(
        "Choose a tool",
        ["🔍 Parser", "✨ Docstring Generator", "📊 Diagram Generator"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info("""
    **DocuMind** helps you:
    - 🔍 Analyze Python code structure
    - 📝 Extract functions, classes, and docstrings
    - ✨ Generate comprehensive docstrings
    - 📊 Create class diagrams
    - 🎯 Improve code documentation
    """)
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Stats")
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <p style="margin: 0; font-size: 2rem; font-weight: 800;">🚀</p>
            <p style="margin: 0;">Fast & Powerful</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Parser Page
if "Parser" in page:
    st.markdown('<div class="section-header"><h2 style="margin: 0;">🔍 Python Code Parser</h2></div>', unsafe_allow_html=True)
    st.markdown("### Upload a Python file or paste your code to extract functions, classes, imports, and docstrings.")
    
    # Two columns for upload and paste
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Upload File")
        uploaded_file = st.file_uploader(
            "Choose a Python file",
            type=["py"],
            label_visibility="collapsed",
            help="Upload a .py file to parse"
        )
    
    with col2:
        st.markdown("### 📝 Or Paste Code")
        use_file = st.checkbox("Use uploaded file", value=bool(uploaded_file))
    
    # Code input area
    if uploaded_file and use_file:
        try:
            code_content = uploaded_file.read().decode("utf-8")
            code_input = st.text_area(
                "Code Preview:",
                code_content,
                height=300,
                key="code_preview"
            )
        except Exception as e:
            st.error(f"Error reading file: {e}")
            code_input = st.text_area("Or paste Python code here:", height=300)
    else:
        code_input = st.text_area(
            "Paste Python code here:",
            height=300,
            placeholder="def calculate_sum(a, b):\n    \"\"\"Add two numbers.\"\"\"\n    return a + b",
            key="code_input"
        )
    
    # Parse button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        parse_button = st.button("🚀 Parse Code", use_container_width=True, type="primary")
    
    if parse_button or (uploaded_file and use_file):
        if not code_input.strip():
            st.warning("⚠️ Please upload a file or enter Python code to parse.")
        else:
            try:
                with st.spinner("🔄 Parsing your code..."):
                    result = parse_python_content(code_input)
                
                st.success("✅ Code parsed successfully!")
                st.markdown("---")
                
                # Enhanced Metrics in cards
                st.markdown("### 📊 Code Statistics")
                
                # Get metrics from new structure
                metrics_data = result.get('structure', {}).get('complexity_metrics', {})
                total_functions = metrics_data.get('total_functions', len(result.get('functions', [])))
                total_classes = metrics_data.get('total_classes', len(result.get('classes', [])))
                total_imports = metrics_data.get('total_imports', len(result.get('imports', [])))
                file_lines = result.get('file_info', {}).get('total_lines', 0)
                
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                colors = [
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                    "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                    "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
                    "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
                    "linear-gradient(135deg, #30cfd0 0%, #330867 100%)"
                ]
                
                metrics = [
                    (total_functions, "Functions", "🔧"),
                    (total_classes, "Classes", "🏷️"),
                    (total_imports, "Imports", "📦"),
                    (file_lines, "Lines", "📄"),
                    (len(result.get('variables', [])), "Variables", "📝"),
                    (len(result.get('constants', [])), "Constants", "⭐")
                ]
                
                for idx, (col, metric) in enumerate(zip([col1, col2, col3, col4, col5, col6], metrics)):
                    with col:
                        st.markdown(f"""
                        <div class="metric-card" style="background: {colors[idx]};">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{metric[2]}</div>
                            <h3>{metric[0]}</h3>
                            <p>{metric[1]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Display file info
                if result.get('file_info'):
                    file_info = result['file_info']
                    with st.expander("📄 File Information", expanded=False):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Lines", file_info.get('total_lines', 0))
                        with col2:
                            st.metric("Code Lines", file_info.get('code_lines', 0))
                        with col3:
                            st.metric("Comment Lines", file_info.get('comment_lines', 0))
                        with col4:
                            st.metric("Blank Lines", file_info.get('blank_lines', 0))
                
                # Display imports
                if result.get('imports'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">📦 Imports</h3></div>', unsafe_allow_html=True)
                    for imp in result['imports']:
                        if imp['type'] == 'import':
                            imports_list = ', '.join([f"`{i['name']}`" for i in imp['imports']])
                            st.markdown(f"- **Line {imp['line']}:** `import {imports_list}`")
                        else:
                            imports_list = ', '.join([f"`{i['name']}`" for i in imp['imports']])
                            module = imp.get('module', '')
                            st.markdown(f"- **Line {imp['line']}:** `from {module} import {imports_list}`")
                    st.markdown("---")
                
                # Display constants and variables
                if result.get('constants'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">⭐ Constants</h3></div>', unsafe_allow_html=True)
                    const_cols = st.columns(3)
                    for idx, const in enumerate(result['constants']):
                        with const_cols[idx % 3]:
                            st.markdown(f"**`{const['name']}`** (Line {const['line']})")
                            st.caption(f"Type: {const.get('type', 'unknown')}")
                    st.markdown("---")
                
                if result.get('variables'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">📝 Variables</h3></div>', unsafe_allow_html=True)
                    var_cols = st.columns(3)
                    for idx, var in enumerate(result['variables']):
                        with var_cols[idx % 3]:
                            st.markdown(f"**`{var['name']}`** (Line {var['line']})")
                            st.caption(f"Type: {var.get('type', 'unknown')}")
                    st.markdown("---")
                
                # Display functions
                if result.get('functions'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">🔧 Functions</h3></div>', unsafe_allow_html=True)
                    for func in result['functions']:
                        line_num = func.get('line', func.get('line_number', 'N/A'))
                        complexity_info = func.get('complexity', {})
                        complexity_badge = f" | Complexity: {complexity_info.get('cyclomatic', 'N/A')}" if complexity_info else ""
                        
                        with st.expander(f"**{func['name']}** `(Line {line_num}{complexity_badge})`", expanded=False):
                            cols = st.columns([3, 1])
                            with cols[0]:
                                if func.get('is_async'):
                                    st.badge("⚡ Async", type="secondary")
                                if func.get('decorators'):
                                    for dec in func['decorators']:
                                        st.badge(f"@{dec}", type="secondary")
                            
                            if func.get('docstring'):
                                st.markdown("**📄 Docstring:**")
                                st.info(func['docstring'])
                            
                            if func.get('parameters'):
                                st.markdown("**📥 Parameters:**")
                                param_cols = st.columns(2)
                                for idx, param in enumerate(func['parameters']):
                                    with param_cols[idx % 2]:
                                        param_info = f"**`{param['name']}`**"
                                        if param.get('annotation'):
                                            param_info += f": `{param['annotation']}`"
                                        if param.get('default'):
                                            param_info += f" = `{param['default']}`"
                                        if param.get('kind') and param['kind'] != 'positional_or_keyword':
                                            param_info += f" [{param['kind']}]"
                                        st.markdown(f"- {param_info}")
                            
                            if func.get('return_annotation'):
                                st.markdown(f"**📤 Returns:** `{func['return_annotation']}`")
                            
                            if complexity_info:
                                st.markdown("**📊 Complexity Metrics:**")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Cyclomatic", complexity_info.get('cyclomatic', 0))
                                with col2:
                                    st.metric("Line Count", complexity_info.get('line_count', 0))
                                with col3:
                                    st.metric("Parameters", complexity_info.get('parameter_count', 0))
                            
                            if func.get('variables_used'):
                                st.markdown(f"**🔗 Variables Used:** {', '.join([f'`{v}`' for v in func['variables_used']])}")
                    
                    st.markdown("---")
                
                # Display classes
                if result.get('classes'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">🏷️ Classes</h3></div>', unsafe_allow_html=True)
                    for cls in result['classes']:
                        line_num = cls.get('line', cls.get('line_number', 'N/A'))
                        metrics_info = cls.get('metrics', {})
                        method_count = metrics_info.get('total_methods', len(cls.get('methods', [])))
                        
                        with st.expander(f"**{cls['name']}** `(Line {line_num}, {method_count} methods, {metrics_info.get('attribute_count', 0)} attributes)`", expanded=False):
                            if cls.get('docstring'):
                                st.markdown("**📄 Docstring:**")
                                st.info(cls['docstring'])
                            
                            if cls.get('base_classes'):
                                base_list = [f"`{bc['name']}`" if isinstance(bc, dict) else f"`{bc}`" for bc in cls['base_classes']]
                                st.markdown(f"**🔗 Base Classes:** {', '.join(base_list)}")
                            
                            if cls.get('decorators'):
                                st.markdown(f"**🎨 Decorators:** {', '.join([f'`@{d}`' for d in cls['decorators']])}")
                            
                            if cls.get('attributes'):
                                st.markdown("**📋 Attributes:**")
                                attr_cols = st.columns(3)
                                for idx, attr in enumerate(cls['attributes']):
                                    with attr_cols[idx % 3]:
                                        attr_info = f"**`{attr['name']}`**"
                                        if attr.get('annotation'):
                                            attr_info += f": `{attr['annotation']}`"
                                        st.markdown(f"- {attr_info}")
                                        if attr.get('value_preview'):
                                            st.caption(attr['value_preview'])
                            
                            if cls.get('methods'):
                                st.markdown("**⚙️ Methods:**")
                                method_cols = st.columns(2)
                                for idx, method in enumerate(cls['methods']):
                                    with method_cols[idx % 2]:
                                        method_info = f"**`{method['name']}`**"
                                        method_type = method.get('method_type', 'instance')
                                        if method_type != 'instance':
                                            method_info += f" [{method_type}]"
                                        if method.get('return_annotation'):
                                            method_info += f" → `{method['return_annotation']}`"
                                        st.markdown(f"- {method_info}")
                            
                            if metrics_info:
                                st.markdown("**📊 Class Metrics:**")
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Total Methods", metrics_info.get('total_methods', 0))
                                with col2:
                                    st.metric("Public", metrics_info.get('public_methods', 0))
                                with col3:
                                    st.metric("Private", metrics_info.get('private_methods', 0))
                                with col4:
                                    st.metric("Magic", metrics_info.get('magic_methods', 0))
                            
                            if cls.get('nested_classes'):
                                st.markdown("**🏷️ Nested Classes:**")
                                for nested in cls['nested_classes']:
                                    st.markdown(f"- **`{nested['name']}`** (Line {nested.get('line', 'N/A')})")
                    
                    st.markdown("---")
                
                # Display structure information
                if result.get('structure'):
                    st.markdown('<div class="section-header"><h3 style="margin: 0;">🏗️ Code Structure</h3></div>', unsafe_allow_html=True)
                    
                    if result['structure'].get('dependencies'):
                        st.markdown(f"**📦 Dependencies:** {', '.join([f'`{d}`' for d in result['structure']['dependencies']])}")
                    
                    if result['structure'].get('complexity_metrics'):
                        cm = result['structure']['complexity_metrics']
                        st.markdown("**📈 Overall Complexity:**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Avg Function Complexity", f"{cm.get('average_function_complexity', 0):.2f}")
                        with col2:
                            st.metric("Total Variables", cm.get('total_variables', 0))
                    
                    st.markdown("---")
                
                # JSON output in expander
                with st.expander("📋 View Raw JSON Output"):
                    st.code(json.dumps(result, indent=2), language="json")
                    
            except Exception as e:
                st.error(f"❌ Error parsing code: {e}")
                st.exception(e)

# Docstring Generator Page
elif "Docstring Generator" in page:
    st.markdown('<div class="section-header"><h2 style="margin: 0;">✨ Docstring Generator</h2></div>', unsafe_allow_html=True)
    st.markdown("### Generate comprehensive Python docstrings for functions and classes using Ollama (local LLM).")
    
    # Ollama Model selection
    with st.expander("⚙️ Model Configuration", expanded=False):
        model = st.selectbox(
            "Ollama Model:",
            ["phi3", "gemma3:4b", "llama3", "codellama", "mistral"],
            index=0,
            help="Select the Ollama model to use. Make sure the model is installed: ollama pull <model_name>"
        )
        st.info("💡 Using local Ollama models - no API keys needed! Install Ollama from https://ollama.ai")
    
    # Code type selection
    code_type = st.radio(
        "Select code type:",
        ["🔧 Function", "🏷️ Class"],
        horizontal=True,
        help="Choose whether you're generating docstring for a function or class"
    )
    
    # Docstring style selection
    style = st.selectbox(
        "📝 Docstring Style:",
        ["google", "numpy", "sphinx"],
        index=0,
        help="Choose the docstring style format"
    )
    
    # Code input area
    if "Function" in code_type:
        st.markdown("### 📝 Function Code")
        code_input = st.text_area(
            "Enter Python function code:",
            height=300,
            placeholder="""def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)""",
            help="Paste the Python function you want to generate a docstring for",
            key="function_code"
        )
    else:
        st.markdown("### 🏷️ Class Code")
        code_input = st.text_area(
            "Enter Python class code:",
            height=300,
            placeholder="""class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y""",
            help="Paste the Python class you want to generate a docstring for",
            key="class_code"
        )
        
        include_methods = st.checkbox(
            "✨ Also generate docstrings for all methods",
            value=False,
            help="Generate docstrings for all methods in the class"
        )
    
    context = st.text_input(
        "📖 Additional Context (Optional):",
        placeholder="This code is part of a math utilities library...",
        help="Provide additional context about the code's purpose or usage"
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("✨ Generate Docstring", use_container_width=True, type="primary")
    
    if generate_button:
        if not code_input.strip():
            st.warning("⚠️ Please enter code to generate a docstring.")
        else:
            try:
                generator = DocstringGenerator(model=model)
                
                if "Function" in code_type:
                    with st.spinner("🤖 Generating function docstring with AI..."):
                        docstring = generator.generate_function_docstring(
                            code_input,
                            context=context if context else None,
                            style=style
                        )
                    
                    st.success("✅ Function docstring generated successfully!")
                    st.markdown("---")
                    
                    st.markdown("### 📄 Generated Docstring")
                    st.code(docstring, language="python")
                    
                    st.markdown("---")
                    
                    # Show formatted function
                    try:
                        formatted = generator.format_docstring_for_function(code_input, docstring)
                        st.markdown("### 🎨 Formatted Function with Docstring")
                        st.code(formatted, language="python")
                    except Exception as e:
                        st.warning(f"⚠️ Could not format function automatically: {e}")
                
                else:  # Class
                    with st.spinner("🤖 Generating class docstring with AI..."):
                        result = generator.generate_class_docstring(
                            code_input,
                            context=context if context else None,
                            style=style,
                            include_methods=include_methods
                        )
                    
                    st.success("✅ Class docstring generated successfully!")
                    st.markdown("---")
                    
                    st.markdown(f"### 📄 Generated Class Docstring for `{result['class_name']}`")
                    st.code(result['class_docstring'], language="python")
                    
                    st.markdown("---")
                    
                    # Show formatted class
                    try:
                        formatted = generator.format_docstring_for_class(code_input, result['class_docstring'])
                        st.markdown("### 🎨 Formatted Class with Docstring")
                        st.code(formatted, language="python")
                    except Exception as e:
                        st.warning(f"⚠️ Could not format class automatically: {e}")
                    
                    # Show method docstrings if generated
                    if result.get('methods') and include_methods:
                        st.markdown("---")
                        st.markdown("### ⚙️ Generated Method Docstrings")
                        for method_name, method_docstring in result['methods'].items():
                            with st.expander(f"**`{method_name}`** method", expanded=False):
                                st.code(method_docstring, language="python")
                                
                                # Show formatted method
                                try:
                                    method_code = generator._extract_method_code(code_input, method_name)
                                    if method_code:
                                        formatted_method = generator.format_docstring_for_function(method_code, method_docstring)
                                        st.markdown("**Formatted method:**")
                                        st.code(formatted_method, language="python")
                                except:
                                    pass
                    
            except RuntimeError as e:
                st.error(f"❌ Setup Error: {e}")
                if "not installed" in str(e).lower():
                    st.info("""
                    💡 **To fix this:**
                    1. Install Ollama from https://ollama.ai
                    2. Pull a model: `ollama pull llama3`
                    3. Or try: `ollama pull phi3`
                    """)
                elif "not available" in str(e).lower():
                    st.info(f"""
                    💡 **To fix this:**
                    Install the model with: `ollama pull {model}`
                    """)
            except Exception as e:
                st.error(f"❌ Error generating docstring: {e}")
                st.info("💡 Make sure Ollama is installed and running. Check the error message above for details.")

# Diagram Generator Page
elif "Diagram Generator" in page:
    st.markdown('<div class="section-header"><h2 style="margin: 0;">📊 Diagram Generator</h2></div>', unsafe_allow_html=True)
    st.markdown("### Generate Mermaid class diagrams from Python code. Visualize class structures and relationships.")
    
    # File upload and code input
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Upload File")
        uploaded_file = st.file_uploader(
            "Choose a Python file",
            type=["py"],
            label_visibility="collapsed",
            help="Upload a .py file to generate diagram",
            key="diagram_file_uploader"
        )
    
    with col2:
        st.markdown("### 📝 Or Paste Code")
        use_file = st.checkbox("Use uploaded file", value=bool(uploaded_file), key="diagram_use_file")
    
    # Code input area
    # Always show a text area - either with file content or for pasting
    if uploaded_file and use_file:
        # Show uploaded file content
        try:
            uploaded_file.seek(0)
            file_content = uploaded_file.read().decode("utf-8")
            code_input = st.text_area(
                "Code Preview:",
                value=file_content,
                height=300,
                key="diagram_code_preview"
            )
        except Exception as e:
            st.error(f"Error reading file: {e}")
            code_input = st.text_area(
                "Paste Python code here:",
                height=300,
                placeholder="class Calculator:\n    def __init__(self):\n        self.value = 0\n    \n    def add(self, x, y):\n        return x + y",
                key="diagram_code_input"
            )
    else:
        # Show text input for pasting code
        code_input = st.text_area(
            "Paste Python code here:",
            height=300,
            placeholder="class Calculator:\n    def __init__(self):\n        self.value = 0\n    \n    def add(self, x, y):\n        return x + y",
            key="diagram_code_input"
        )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("📊 Generate Diagram", use_container_width=True, type="primary", key="diagram_generate")
    
    if generate_button:
        # Get code from session state - check which text area is currently active
        code_to_process = ""
        
        # Determine which text area is active based on checkbox and file upload
        if uploaded_file and use_file:
            # Using uploaded file - check preview key
            if 'diagram_code_preview' in st.session_state:
                code_to_process = st.session_state.diagram_code_preview or ""
        else:
            # Using paste code - check input key
            if 'diagram_code_input' in st.session_state:
                code_to_process = st.session_state.diagram_code_input or ""
        
        # Fallback: if still empty, check both keys
        if not code_to_process or not code_to_process.strip():
            if 'diagram_code_preview' in st.session_state:
                code_to_process = st.session_state.diagram_code_preview or ""
            if not code_to_process or not code_to_process.strip():
                if 'diagram_code_input' in st.session_state:
                    code_to_process = st.session_state.diagram_code_input or ""
        
        if not code_to_process or not code_to_process.strip():
            st.warning("⚠️ Please upload a file or enter Python code to generate a diagram.")
        else:
            try:
                with st.spinner("📊 Generating class diagram..."):
                    # Generate diagram directly from code (no temp file needed)
                    diagram = generate_mermaid_diagram_from_code(code_to_process)
                
                st.success("✅ Diagram generated successfully!")
                st.markdown("---")
                
                # Display diagram
                st.markdown("### 📊 Mermaid Class Diagram")
                st.code(diagram, language="text")
                
                # Copy button info
                st.info("💡 **Tip:** Copy the diagram code above and paste it into:\n- GitHub markdown files (with ```mermaid code block)\n- [Mermaid Live Editor](https://mermaid.live)\n- Documentation tools that support Mermaid")
                
                # Display in markdown format for easy copying
                st.markdown("---")
                st.markdown("### 📋 Copy This (Markdown Format)")
                markdown_diagram = f"```mermaid\n{diagram}\n```"
                st.code(markdown_diagram, language="markdown")
                        
            except SyntaxError as e:
                st.error(f"❌ Syntax error in code: {e}")
            except Exception as e:
                st.error(f"❌ Error generating diagram: {e}")
                st.exception(e)

# Simple Footer matching color theme
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem;">
        <p style="margin: 0; font-size: 1rem; font-weight: 500;">
            Made with ❤️ by DocuMind
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
