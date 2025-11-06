# Ollama Setup Guide

## Step 1: Install Ollama

If you just downloaded Ollama, you may need to:

### On macOS:
1. Open the downloaded `.dmg` file
2. Drag Ollama to Applications
3. Open Ollama from Applications (it will start the service)
4. Or install via Homebrew:
   ```bash
   brew install ollama
   ```

### Verify Installation:
```bash
ollama --version
```

If you get "command not found", you may need to:
- Restart your terminal
- Add Ollama to your PATH
- Or start Ollama from Applications

## Step 2: Pull a Model

After Ollama is installed, pull a model:

```bash
# Recommended: llama3 (good balance of quality and speed)
ollama pull llama3

# Or try phi3 (smaller, faster)
ollama pull phi3

# Or codellama (specialized for code)
ollama pull codellama
```

## Step 3: Test the Setup

Run the test script:
```bash
python3 core/summarizer.py
```

You should see:
```
Testing Ollama Docstring Generator
==================================================

1. Testing simple function docstring generation...
Generated Docstring:
[Generated docstring here]
```

## Step 4: Use in Streamlit App

Once Ollama is working:
1. Start Streamlit: `streamlit run app.py`
2. Go to the Docstring Generator page
3. Select your model (llama3, phi3, etc.)
4. Paste your code and generate docstrings!

## Troubleshooting

### "Ollama not found"
- Make sure Ollama is installed and running
- Try restarting your terminal
- On macOS: Open Ollama from Applications to start the service

### "Model not available"
- Pull the model: `ollama pull <model-name>`
- Check available models: `ollama list`

### Slow responses
- Try a smaller model like `phi3`
- Or use `codellama` which is optimized for code

## Quick Start Commands

```bash
# Install Ollama (if not installed)
brew install ollama

# Start Ollama service (macOS)
open -a Ollama

# Pull a model
ollama pull llama3

# Test it
ollama run llama3 "Say hello"

# Test the docstring generator
python3 core/summarizer.py
```

