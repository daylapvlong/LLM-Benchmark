# Auto-Fetch Guide

## Overview

The Benchmark CLI now supports automatic fetching of bot responses from an API! Simply configure your API settings and the tool will automatically fetch responses for all questions in your input files.

## Quick Setup

### 1. Create Configuration File

Copy the example config file:
```bash
cp config.json.example config.json
```

Edit `config.json` with your API settings:
```json
{
  "api_url": "https://your-api-endpoint.com/chat",
  "api_key": "your-api-key-here",
  "delay": 0.5,
  "auto_fetch": true
}
```

### 2. Prepare Question Files

Place your question files in the `inputs/` directory. You can use JSON or CSV format.

**JSON Format:**
```json
[
  {
    "id": "q1",
    "question": "What is the capital of France?",
    "expected": "Paris"
  },
  {
    "id": "q2",
    "question": "Explain photosynthesis.",
    "expected": "Process where plants convert sunlight to energy"
  }
]
```

**CSV Format:**
```csv
id,question,expected
q1,"What is the capital of France?","Paris"
q2,"Explain photosynthesis.","Process where plants convert sunlight to energy"
```

### 3. Run Auto-Fetch

Simply run:
```bash
python main.py
```

The tool will:
- ✅ Automatically detect all files in `inputs/` directory
- ✅ Fetch bot responses for all questions via API
- ✅ Save results to `outputs/` directory with `_responses` suffix

Example output:
```
======================================================================
🤖 AUTO-FETCH MODE - Fetching Bot Responses
======================================================================
API: https://your-api-endpoint.com/chat
Input files: 2
----------------------------------------------------------------------

📄 Processing: questions.json
   Questions: 3
   ✓ Saved to: questions_responses.json

======================================================================
✓ Successfully processed 1 file(s)
======================================================================
```

## Environment Variables Alternative

Instead of `config.json`, you can use environment variables:

```bash
export API_URL="https://api.example.com/chat"
export API_KEY="your-api-key"
export API_DELAY="0.5"
python main.py
```

## API Response Format

The API client expects one of these response formats:
- `{"response": "..."}`
- `{"answer": "..."}`
- `{"text": "..."}`
- Or a plain string response

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `api_url` | API endpoint URL | Required |
| `api_key` | API authentication key | Optional |
| `delay` | Delay between API requests (seconds) | 0.5 |
| `auto_fetch` | Enable auto-fetch mode | true |

## How It Works

1. **Configuration Check**: Tool checks for `config.json` or environment variables
2. **Input Detection**: Scans `inputs/` directory for JSON/CSV files
3. **Question Loading**: Loads questions from each file
4. **API Fetching**: Makes API calls with retry logic and rate limiting
5. **Response Saving**: Appends responses to `outputs/` directory

## Error Handling

- **API Failures**: Retries up to 3 times with exponential backoff
- **Missing Files**: Skips files that can't be loaded
- **Empty Responses**: Continues processing even if some API calls fail

## Next Steps

After fetching responses, you can evaluate them:
```bash
python main.py outputs/questions_responses.json --mode auto --output outputs/evaluation.json
```
