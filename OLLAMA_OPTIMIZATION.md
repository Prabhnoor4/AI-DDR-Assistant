# Ollama Performance Optimization Guide

## Current Issue
The `llama3.2` (3.2B parameters) model is timing out when processing large DDR prompts.

## ✅ Solution Applied
Switched to **llama3.2:1b** - a much faster 1 billion parameter model.

### Speed Comparison
- **llama3.2** (3.2B): ~30-60 seconds per request on CPU
- **llama3.2:1b** (1B): ~5-15 seconds per request on CPU ⚡

## Alternative Fast Models

If `llama3.2:1b` still has issues, try these even smaller models:

### 1. Phi-3 Mini (Recommended for quality)
```bash
ollama pull phi3:mini
```
Then in `config.py`:
```python
OLLAMA_MODEL = "phi3:mini"
```
- Size: 3.8B parameters
- Speed: Fast on CPU
- Quality: Excellent for structured tasks

### 2. TinyLlama (Fastest)
```bash
ollama pull tinyllama
```
Then in `config.py`:
```python
OLLAMA_MODEL = "tinyllama"
```
- Size: 1.1B parameters
- Speed: Very fast
- Quality: Good for simple extraction

### 3. Gemma 2B
```bash
ollama pull gemma:2b
```
Then in `config.py`:
```python
OLLAMA_MODEL = "gemma:2b"
```
- Size: 2B parameters
- Speed: Fast
- Quality: Good balance

## Additional Optimizations

### 1. Reduce Token Limits
In `config.py`, reduce the max output tokens:
```python
MAX_OUTPUT_TOKENS = 4096  # Instead of 8192
```

### 2. Enable Caching
In `config.py`:
```python
ENABLE_CACHE = True
```
This will cache responses and avoid re-processing the same prompts.

### 3. Use Mock Mode for Testing
When developing/testing the UI:
```python
USE_MOCK = True
```

## Monitoring Ollama Performance

Check if Ollama is using GPU:
```bash
ollama ps
```

Check available models:
```bash
ollama list
```

## Expected Performance with llama3.2:1b

- **Extraction tasks**: 5-10 seconds
- **DDR generation**: 10-20 seconds
- **Total pipeline**: 30-60 seconds

This should be well within the 300-second timeout.
