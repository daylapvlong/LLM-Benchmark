# LLM Benchmark Project

A comprehensive evaluation framework for benchmarking Large Language Model (LLM) responses with automated metrics and optional human review.

## Overview

This project provides a modular, extensible system for evaluating LLM outputs against expected answers. It supports multiple evaluation metrics, flexible evaluation modes, and robust error handling to ensure reliable benchmarking at scale.

## Features

- **Multiple Evaluation Metrics**: Built-in metrics for exact matching, token overlap, length ratio, and key phrase containment
- **Flexible Evaluation Modes**: Automated, human-only, or hybrid evaluation workflows
- **Extensible Architecture**: Easy to add custom metrics through a clean interface
- **Fault Tolerant**: Individual metric failures don't stop the evaluation process
- **Multiple Output Formats**: Export results as JSON or CSV
- **Human-in-the-Loop**: Optional human review with customizable scoring criteria
- **Batch Processing**: Efficient evaluation of large datasets
- **Detailed Reporting**: Comprehensive statistics and per-metric breakdowns

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-benchmark.git
cd llm-benchmark

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Prepare Your Data

Create an input file in JSON or CSV format:

**JSON Format** (`data/examples.json`):
```json
[
  {
    "id": "eval_001",
    "question": "What is the capital of France?",
    "response": "The capital of France is Paris",
    "expected": "Paris"
  },
  {
    "id": "eval_002",
    "question": "What is 2+2?",
    "response": "4",
    "expected": "4"
  }
]
```

**CSV Format** (`data/examples.csv`):
```csv
id,question,response,expected
eval_001,"What is the capital of France?","The capital of France is Paris","Paris"
eval_002,"What is 2+2?","4","4"
```

### 2. Run Evaluation

**Automated evaluation with all metrics:**
```bash
python evaluate.py --input data/examples.json --mode auto
```

**Automated evaluation with specific metrics:**
```bash
python evaluate.py --input data/examples.json --mode auto --metrics exact_match token_overlap
```

**Human-only evaluation:**
```bash
python evaluate.py --input data/examples.json --mode human
```

**Hybrid evaluation (human review for low-scoring pairs):**
```bash
python evaluate.py --input data/examples.json --mode hybrid --threshold 0.6
```

### 3. View Results

Results are saved to the `results/` directory by default:

```bash
# View JSON results
cat results/evaluation_results.json

# View CSV summary
cat results/evaluation_summary.csv
```

## Command Line Options

```
usage: evaluate.py [-h] --input INPUT [--output OUTPUT] [--mode {auto,human,hybrid}]
                   [--metrics METRICS [METRICS ...]] [--threshold THRESHOLD]
                   [--format {json,csv,both}]

optional arguments:
  -h, --help            Show this help message and exit
  --input INPUT         Path to input JSON or CSV file
  --output OUTPUT       Output directory for results (default: results/)
  --mode {auto,human,hybrid}
                        Evaluation mode (default: auto)
  --metrics METRICS [METRICS ...]
                        Specific metrics to run (default: all)
  --threshold THRESHOLD
                        Score threshold for hybrid mode (default: 0.5)
  --format {json,csv,both}
                        Output format (default: both)
```

## Built-in Metrics

### ExactMatchMetric
Binary check for exact string match after normalization.
- **Score Range**: 0.0 or 1.0
- **Use Case**: Factual answers requiring precision

### TokenOverlapMetric
Measures semantic similarity using token-level F1 score (ROUGE-like).
- **Score Range**: 0.0 to 1.0
- **Use Case**: Responses with same meaning but different wording
- **Details**: precision, recall, f1, token counts

### LengthRatioMetric
Evaluates if response length is appropriate compared to expected.
- **Score Range**: 0.0 to 1.0
- **Use Case**: Detecting overly brief or verbose responses
- **Details**: word counts, length ratio

### ContainmentMetric
Checks if response contains key phrases from expected answer.
- **Score Range**: 0.0 to 1.0
- **Use Case**: Ensuring critical concepts are present
- **Details**: key phrases found and total

## Evaluation Modes

### Auto Mode
Runs only automated metrics without human interaction.

```bash
python evaluate.py --input data.json --mode auto
```

### Human Mode
Interactive review with scoring on four criteria (1-5 scale):
- **Correctness**: Factual accuracy
- **Relevance**: Alignment with question
- **Completeness**: Coverage of expected information
- **Tone**: Appropriateness of style

```bash
python evaluate.py --input data.json --mode human
```

### Hybrid Mode
Combines automated and human evaluation:
1. Runs automated metrics first
2. Calculates average scores
3. Prompts human review for pairs below threshold
4. Merges results

```bash
python evaluate.py --input data.json --mode hybrid --threshold 0.6
```

## Output Format

### JSON Output
Detailed per-pair results with metric scores and breakdowns:

```json
{
  "id": "eval_001",
  "metrics": {
    "exact_match": 0.0,
    "token_overlap": 0.857,
    "length_ratio": 0.833,
    "key_phrase_containment": 1.0
  },
  "details": {
    "token_overlap": {
      "precision": 0.857,
      "recall": 0.857,
      "f1": 0.857,
      "overlap_tokens": 6,
      "response_tokens": 7,
      "expected_tokens": 7
    }
  },
  "human_scores": {
    "correctness": 5,
    "relevance": 5,
    "completeness": 4,
    "tone": 5
  }
}
```

### CSV Output
Tabular format for easy analysis:

```csv
id,exact_match,token_overlap,length_ratio,containment,correctness,relevance,completeness,tone
eval_001,0.0,0.857,0.833,1.0,5,5,4,5
eval_002,1.0,1.0,1.0,1.0,5,5,5,5
```

### Summary Statistics
Automatically calculated for each metric:
- Mean
- Min
- Max
- Standard Deviation

## Adding Custom Metrics

Create a new metric by implementing the `Metric` interface:

```python
from metrics.base import Metric, MetricResult

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
from metrics.registry import MetricRegistry
MetricRegistry.register(CustomMetric())
```

## Project Structure

```
llm-benchmark/
├── data/                   # Input data files
│   └── examples.json
├── results/                # Output results
│   ├── evaluation_results.json
│   └── evaluation_summary.csv
├── metrics/                # Metric implementations
│   ├── __init__.py
│   ├── base.py            # Metric interface
│   ├── exact_match.py
│   ├── token_overlap.py
│   ├── length_ratio.py
│   ├── containment.py
│   └── registry.py        # Metric registration
├── core/                   # Core evaluation logic
│   ├── __init__.py
│   ├── data_loader.py     # Input data loading
│   ├── evaluation_engine.py
│   ├── models.py          # Data models
│   └── reporter.py        # Results reporting
├── evaluate.py             # Main entry point
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Use Cases

- **Model Development**: Track improvements across training iterations
- **A/B Testing**: Compare different model versions or prompts
- **Quality Assurance**: Validate responses before production deployment
- **Regression Testing**: Ensure updates don't degrade performance
- **Benchmarking**: Compare your LLM against standard datasets

## Examples

### Example 1: Quick Evaluation

```bash
# Run all metrics on a small dataset
python evaluate.py --input data/quick_test.json --mode auto
```

### Example 2: Focused Metric Analysis

```bash
# Only run token overlap and containment metrics
python evaluate.py --input data/semantic_test.json \
                   --metrics token_overlap key_phrase_containment \
                   --format json
```

### Example 3: Quality Control Pipeline

```bash
# Automated evaluation with human review for problem cases
python evaluate.py --input data/production_responses.json \
                   --mode hybrid \
                   --threshold 0.7 \
                   --output results/qa_review/

## Acknowledgments
- Inspired by ROUGE and BLEU evaluation metrics
- Built for practical LLM evaluation workflows
- Designed with extensibility and fault tolerance in mind

## Support
For questions, issues, or feature requests, please open an issue on GitHub or contact the maintainers.

---

**Happy Benchmarking! 🚀**