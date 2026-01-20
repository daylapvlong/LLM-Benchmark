# Benchmark CLI

A modular CLI tool for evaluating chatbot responses with automated metrics and human-in-the-loop support. **Now with automatic API fetching!**

## Features

- **Multiple Evaluation Metrics**: Built-in metrics for exact matching, token overlap, length ratio, and key phrase containment
- **Flexible Evaluation Modes**: Automated, human-only, or hybrid evaluation workflows
- **Extensible Architecture**: Clean layered architecture with easy-to-add custom metrics
- **Auto-Fetch Mode**: Automatically fetch bot responses from APIs
- **Fault Tolerant**: Individual metric failures don't stop the evaluation process
- **Multiple Output Formats**: Export results as JSON or CSV
- **Human-in-the-Loop**: Optional human review with customizable scoring criteria
- **Batch Processing**: Efficient evaluation of large datasets
- **Detailed Reporting**: Comprehensive statistics and per-metric breakdowns

## Project Structure

```
BenchmarkCLI/
├── benchmark_cli/          # Main package
│   ├── models/            # Data models (domain entities)
│   │   ├── evaluation.py  # EvaluationPair, MetricResult, EvaluationResult
│   │   └── question.py    # QuestionInput
│   │
│   ├── interfaces/        # User-facing interfaces
│   │   └── cli.py         # Command-line interface
│   │
│   ├── services/          # Business logic services
│   │   ├── evaluation_service.py  # Core evaluation logic
│   │   ├── api_service.py         # API client for fetching responses
│   │   ├── review_service.py      # Human review service
│   │   └── fetch_service.py       # Fetch orchestration
│   │
│   ├── helpers/           # Utility functions
│   │   ├── loaders.py     # Data loading utilities
│   │   ├── reporters.py   # Result reporting utilities
│   │   ├── response_appender.py  # File appending utilities
│   │   └── config.py     # Configuration management
│   │
│   ├── metrics/           # Metrics package
│   │   ├── base.py        # Metric interface
│   │   ├── builtin.py     # Built-in metrics
│   │   └── registry.py   # Metric registry
│   │
│   ├── auto_fetch.py      # Auto-fetch orchestration
│   └── __init__.py        # Package exports
│
├── inputs/                # Input data files
│   ├── sample_data.json   # Sample JSON data
│   ├── sample_data.csv    # Sample CSV data
│   └── questions.json     # Questions-only file (for auto-fetch)
│
├── outputs/               # Output results (auto-generated)
├── config.json            # API configuration (create from config.json.example)
├── config.json.example    # Configuration template
├── main.py                # Entry point
└── requirements.txt       # Dependencies
```

## Architecture

The project follows a **layered architecture** pattern:

### Layer Responsibilities

1. **Models Layer** (`models/`)
   - Domain entities and data structures
   - Pure data classes with no business logic
   - Examples: `EvaluationPair`, `MetricResult`, `QuestionInput`

2. **Interfaces Layer** (`interfaces/`)
   - User-facing interfaces (CLI, API endpoints)
   - Handles user input/output and command parsing
   - Example: `EvaluationCLI`

3. **Services Layer** (`services/`)
   - Business logic and orchestration
   - Coordinates between models, helpers, and metrics
   - Examples: `EvaluationService`, `APIService`, `ReviewService`

4. **Helpers Layer** (`helpers/`)
   - Utility functions and helper classes
   - File I/O, configuration, formatting
   - Examples: `DataLoader`, `ResultsReporter`, `Config`

5. **Metrics Layer** (`metrics/`)
   - Evaluation metrics implementation
   - Extensible metric system with registry pattern
   - Examples: `ExactMatchMetric`, `TokenOverlapMetric`

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd BenchmarkCLI

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 🚀 Auto-Fetch Mode (Default)

The tool automatically fetches bot responses from an API when configured!

1. **Create configuration file** (copy from `config.json.example`):
```bash
cp config.json.example config.json
```

2. **Edit `config.json`** with your API settings:
```json
{
  "api_url": "https://your-api-endpoint.com/chat",
  "api_key": "your-api-key",
  "delay": 0.5,
  "auto_fetch": true
}
```

3. **Place question files in `inputs/` directory** (JSON or CSV with just questions):
```json
[
  {
    "id": "q1",
    "question": "What is the capital of France?",
    "expected": "Paris"
  }
]
```

4. **Run the tool** - it will automatically fetch responses!
```bash
python main.py
```

The tool will:
- ✅ Automatically detect all files in `inputs/` directory
- ✅ Fetch bot responses for all questions via API
- ✅ Save results to `outputs/` directory with `_responses` suffix

### Manual Evaluation Mode

#### List available metrics
```bash
python main.py --list-metrics
```

#### Run automated evaluation
```bash
# Using JSON input
python main.py inputs/sample_data.json --mode auto --output outputs/results.json

# Using CSV input
python main.py inputs/sample_data.csv --mode auto --output outputs/results.csv
```

#### Run with specific metrics
```bash
python main.py inputs/sample_data.json --metrics exact_match token_overlap --output outputs/results.json
```

#### Hybrid mode (auto + human review for low scores)
```bash
python main.py inputs/sample_data.json --mode hybrid --threshold 0.5 --output outputs/results.json
```

#### Human review mode
```bash
python main.py inputs/sample_data.json --mode human --output outputs/results.json
```

## Input File Formats

### JSON Format (Full Evaluation Pairs)
```json
[
  {
    "id": "pair_001",
    "question": "What is the capital of France?",
    "response": "The capital of France is Paris.",
    "expected": "Paris is the capital of France.",
    "metadata": {
      "category": "geography",
      "difficulty": "easy"
    }
  }
]
```

### CSV Format (Full Evaluation Pairs)
```csv
id,question,response,expected
pair_001,"What is the capital of France?","The capital of France is Paris.","Paris is the capital of France."
```

### JSON Format (Questions Only - for Auto-Fetch)
```json
[
  {
    "id": "q1",
    "question": "What is the capital of France?",
    "expected": "Paris",
    "metadata": {
      "category": "geography"
    }
  }
]
```

### CSV Format (Questions Only - for Auto-Fetch)
```csv
id,question,expected
q1,"What is the capital of France?","Paris"
```

## Available Metrics

- **exact_match**: Exact string match (case-insensitive)
- **token_overlap**: Token overlap F1 score (ROUGE-like)
- **length_ratio**: Response length similarity score
- **key_phrase_containment**: Key phrase containment score

## Output Formats

Results can be saved as:
- **JSON**: Detailed results with all metric scores and details
- **CSV**: Summary table with metric scores per evaluation pair

### JSON Output Example
```json
{
  "id": "pair_001",
  "metrics": {
    "exact_match": 0.0,
    "token_overlap": 0.667,
    "length_ratio": 1.0,
    "key_phrase_containment": 0.75
  },
  "details": {
    "token_overlap": {
      "precision": 0.667,
      "recall": 0.667,
      "f1": 0.667
    }
  },
  "human_scores": {
    "correctness": 4,
    "relevance": 5
  }
}
```

## Auto-Fetch Configuration

### Environment Variables Alternative

Instead of `config.json`, you can use environment variables:

```bash
export API_URL="https://api.example.com/chat"
export API_KEY="your-api-key"
export API_DELAY="0.5"
python main.py
```

### API Response Format

The API client expects one of these response formats:
- `{"response": "..."}`
- `{"answer": "..."}`
- `{"text": "..."}`
- Or a plain string response

## Command Line Options

```
usage: main.py [-h] [--mode {auto,human,hybrid}] [--metrics METRICS [METRICS ...]]
               [--threshold THRESHOLD] [--output OUTPUT] [--list-metrics]
               [--verbose] [--no-expected] [input_file]

positional arguments:
  input_file            Input file (JSON or CSV) with evaluation pairs

options:
  -h, --help            show this help message and exit
  --mode {auto,human,hybrid}
                        Evaluation mode (default: auto)
  --metrics METRICS [METRICS ...]
                        Specific metrics to use (default: all)
  --threshold THRESHOLD
                        Score threshold for human review in hybrid mode
  --output, -o OUTPUT   Output file path (JSON or CSV)
  --list-metrics        List available metrics and exit
  --verbose, -v         Enable verbose logging
  --no-expected         Hide expected answers during human review
```

## Adding Custom Metrics

Create a new metric by implementing the `Metric` interface:

```python
from benchmark_cli.metrics.base import Metric
from benchmark_cli.models.evaluation import MetricResult

class CustomMetric(Metric):
    @property
    def name(self) -> str:
        return "custom_metric"
    
    def compute(self, response: str, expected: str) -> MetricResult:
        # Your custom logic here
        score = calculate_custom_score(response, expected)
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details={"custom_info": "value"}
        )

# Register your metric
from benchmark_cli.metrics.registry import MetricRegistry
registry = MetricRegistry()
registry.register(CustomMetric())
```

## Evaluation Modes

### Auto Mode
Runs only automated metrics without human interaction.

```bash
python main.py inputs/data.json --mode auto --output outputs/results.json
```

### Human Mode
Interactive review with scoring on four criteria (1-5 scale):
- **Correctness**: Factual accuracy
- **Relevance**: Alignment with question
- **Completeness**: Coverage of expected information
- **Tone**: Appropriateness of style

```bash
python main.py inputs/data.json --mode human --output outputs/results.json
```

### Hybrid Mode
Combines automated and human evaluation:
1. Runs automated metrics first
2. Calculates average scores
3. Prompts human review for pairs below threshold
4. Merges results

```bash
python main.py inputs/data.json --mode hybrid --threshold 0.6 --output outputs/results.json
```

## Sample Data

The `inputs/` directory contains sample data files for testing:
- `sample_data.json`: 5 evaluation pairs in JSON format
- `sample_data.csv`: 5 evaluation pairs in CSV format
- `questions.json`: Questions-only file for auto-fetch testing

You can use these files to test the tool:
```bash
# Auto-fetch mode (if config.json exists)
python main.py

# Manual evaluation mode
python main.py inputs/sample_data.json --mode auto --output outputs/test.json
```

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
  - `requests>=2.31.0` (for API functionality)

## Use Cases

- **Model Development**: Track improvements across training iterations
- **A/B Testing**: Compare different model versions or prompts
- **Quality Assurance**: Validate responses before production deployment
- **Regression Testing**: Ensure updates don't degrade performance
- **Benchmarking**: Compare your LLM against standard datasets
- **Automated Testing**: Continuous evaluation with API integration

## Development

### Project Structure Benefits

The layered architecture provides:
- **Clear Separation of Concerns**: Each layer has a specific responsibility
- **Easy Navigation**: Find code quickly by layer
- **Better Testability**: Services can be easily mocked
- **Scalability**: Easy to add new features without affecting other layers
- **Maintainability**: Changes are localized to specific layers

### Extending the System

1. **Add a new metric**: Implement `Metric` interface in `metrics/`
2. **Add a new service**: Create service class in `services/`
3. **Add a new helper**: Add utility function in `helpers/`
4. **Add a new interface**: Create interface in `interfaces/`

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

---

**Happy Benchmarking! 🚀**
