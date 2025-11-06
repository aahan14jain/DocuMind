# Environment Setup Guide

## Step 1: Create .env file

In your project root (same folder as `app.py`), create a file called `.env` and add:

```
OPENAI_API_KEY=your_api_key_here
```

**Important:** 
- Replace `your_api_key_here` with your actual OpenAI API key
- **DO NOT** commit the `.env` file to GitHub (it's already in `.gitignore`)
- Keep your API key secure and private

## Step 2: Verify Setup

Run this command to test:

```bash
python3 core/summarizer.py
```

If everything is set up correctly, you'll see generated docstrings for test functions.

## Alternative: Set Environment Variable in Shell

### On macOS/Linux:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### On Windows:
```cmd
set OPENAI_API_KEY=your_api_key_here
```

**Note:** This is temporary and only lasts for the current terminal session. Using a `.env` file is recommended.

## Testing

The `core/summarizer.py` file includes a simple test function. Run:

```bash
python3 core/summarizer.py
```

You should see output like:

```
Testing Docstring Generator
==================================================

Simple function test:
"""Multiplies two numbers.

Args:
    a (int): The first number.
    b (int): The second number.

Returns:
    int: Product of the two numbers.
"""
```

## Using in Streamlit App

Once the `.env` file is set up, you can:
1. Run `streamlit run app.py`
2. Go to the "Docstring Generator" page
3. The app will automatically load your API key from the `.env` file
4. You can also enter the API key directly in the UI if needed

