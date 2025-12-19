# Pragyan

**AI-Powered DSA Question Solver with Video Explanations**

---

## 🚀 Quick Install

```bash
pip install pragyan
```

---

## ⚡ Quick Start

### In Your Python Script

```python
from pragyan import Pragyan

# Initialize with your API key
solver = Pragyan(api_key="your-gemini-api-key")

# Solve from LeetCode URL
result = solver.solve("https://leetcode.com/problems/two-sum/", language="python")
print(result.solution.code)
```

### From Terminal

```bash
# Interactive mode (recommended)
pragyan interactive

# Quick solve from URL
pragyan solve "https://leetcode.com/problems/two-sum/" --video
```

---

Pragyan is a Python package that helps developers understand and solve Data Structures and Algorithms (DSA) problems. It leverages AI to analyze problems, generate optimized solutions, and create animated explanation videos.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Python API](#python-api)
- [Configuration](#configuration)
- [Supported Languages](#supported-languages)
- [Video Generation](#video-generation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-Platform Scraping | Extract problems from LeetCode, GeeksforGeeks, Codeforces, HackerRank |
| AI-Powered Analysis | Identify patterns, data structures, and optimal approaches |
| Multi-Language Solutions | Generate code in 11+ programming languages |
| Video Explanations | Animated visualizations using Manim |
| Step-by-Step Breakdown | Detailed algorithm walkthroughs |
| Test Case Generation | Auto-generate test cases for validation |
| Verbose Logging | Real-time progress updates during execution |

---

## Architecture

### System Overview

```
+------------------------------------------------------------------+
|                         PRAGYAN SYSTEM                            |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------+     +-------------+     +------------------+     |
|  |   INPUT     |     |   CORE      |     |    OUTPUT        |     |
|  +-------------+     +-------------+     +------------------+     |
|  | - URL       |     | - Scraper   |     | - Solution Code  |     |
|  | - Text      |---->| - Analyzer  |---->| - Explanation    |     |
|  | - API Key   |     | - Solver    |     | - Video (MP4)    |     |
|  +-------------+     | - Generator |     | - Test Cases     |     |
|                      +-------------+     +------------------+     |
|                                                                   |
+------------------------------------------------------------------+
```

### Component Architecture

```
pragyan/
|
+-- cli.py              Command Line Interface (Click + Rich)
|      |
|      +-- Interactive prompts
|      +-- Progress logging
|      +-- Result display
|
+-- main.py             Orchestration Layer
|      |
|      +-- Pragyan class (main entry point)
|      +-- Component coordination
|      +-- Pipeline management
|
+-- scraper.py          Web Scraping Module
|      |
|      +-- LeetCode adapter
|      +-- GFG adapter
|      +-- Generic HTML parser
|      +-- Selenium for dynamic content
|
+-- llm_client.py       AI Integration Layer
|      |
|      +-- Gemini client (Google AI)
|      +-- Groq client (open models)
|      +-- Response parsing
|      +-- Error handling
|
+-- solver.py           Solution Generation
|      |
|      +-- Problem analysis
|      +-- Code generation
|      +-- Complexity analysis
|      +-- Test case creation
|
+-- video_generator.py  Video Creation Module
|      |
|      +-- Manim scene generation
|      +-- Animation templates
|      +-- Rendering pipeline
|
+-- models.py           Data Models (Pydantic)
|      |
|      +-- Question, Solution
|      +-- VideoConfig, LLMConfig
|      +-- ProgrammingLanguage enum
|
+-- logger.py           Logging System
       |
       +-- Rich console output
       +-- Progress tracking
       +-- User engagement
```

### Processing Pipeline

```
+--------+    +----------+    +----------+    +--------+    +-------+
| INPUT  |--->| SCRAPE   |--->| ANALYZE  |--->| SOLVE  |--->| VIDEO |
+--------+    +----------+    +----------+    +--------+    +-------+
    |              |               |              |             |
    v              v               v              v             v
  URL or       Question        Analysis       Solution      MP4 File
  Text         Object          Dict           Object        
                 |               |              |
                 v               v              v
            - Title         - Topics       - Code
            - Description   - Concept      - Explanation
            - Examples      - Approach     - Complexity
            - Constraints   - Edge Cases   - Steps
```

### Data Flow Diagram

```
                    +------------------+
                    |    User Input    |
                    | (URL/Text/API)   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |  QuestionScraper |
                    |  - Fetch HTML    |
                    |  - Parse content |
                    |  - Extract data  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |   LLM Client     |
                    |  - Gemini API    |
                    |  - Groq API      |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
     +----------------+            +----------------+
     |   Analyzer     |            |    Solver      |
     | - Identify     |            | - Generate     |
     |   patterns     |            |   code         |
     | - Find concept |            | - Explain      |
     | - Edge cases   |            |   steps        |
     +-------+--------+            +-------+--------+
              |                             |
              +-------------+---------------+
                            |
                            v
                   +------------------+
                   | Video Generator  |
                   | - Build scenes   |
                   | - Render Manim   |
                   | - Export MP4     |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   |     Output       |
                   | - Code + Explain |
                   | - Video file     |
                   +------------------+
```

---

## Installation

### Basic Installation

```bash
pip install pragyan
```

### Video Generation Dependencies

For video generation with Manim:

**Windows:**
```bash
pip install manim
choco install ffmpeg
```

**macOS:**
```bash
pip install manim
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
pip install manim
sudo apt-get install ffmpeg
```

### Verify Installation

```bash
pragyan version
```

---

## Quick Start

### Interactive Mode (Recommended)

```bash
pragyan interactive
```

This launches a guided session that:
1. Prompts for problem URL or text
2. Selects programming language
3. Configures API provider
4. Displays real-time progress
5. Generates solution and video

### Command Line

```bash
# Solve from URL
pragyan solve -u https://leetcode.com/problems/two-sum -p gemini -k YOUR_API_KEY

# Solve from text
pragyan solve -t "Find two numbers that add up to target" -l python -p gemini -k KEY

# Analyze only (no solution)
pragyan analyze https://leetcode.com/problems/two-sum -p gemini -k KEY
```

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `pragyan interactive` | Interactive mode with prompts |
| `pragyan solve` | Solve a problem |
| `pragyan analyze` | Analyze without solving |
| `pragyan languages` | List supported languages |
| `pragyan version` | Show version |

### Solve Options

| Option | Short | Description |
|--------|-------|-------------|
| `--url` | `-u` | Problem URL |
| `--text` | `-t` | Problem text |
| `--language` | `-l` | Programming language |
| `--provider` | `-p` | AI provider (gemini/groq) |
| `--api-key` | `-k` | API key |
| `--no-video` | | Skip video generation |
| `--output-dir` | `-o` | Video output directory |
| `--quality` | `-q` | Video quality (low/medium/high) |

---

## Python API

### Basic Usage

```python
from pragyan import Pragyan

# Initialize
pragyan = Pragyan(
    provider="gemini",
    api_key="YOUR_API_KEY"
)

# Solve from URL
result = pragyan.process(
    "https://leetcode.com/problems/two-sum",
    language="python",
    generate_video=True
)

# Access results
print(result["solution"].code)
print(result["solution"].time_complexity)
print(f"Video: {result['video_path']}")
```

### Advanced Usage

```python
from pragyan import Pragyan, ProgrammingLanguage, VideoConfig

# Custom configuration
video_config = VideoConfig(
    output_dir="./videos",
    video_quality="high_quality",
    resolution="1080p"
)

pragyan = Pragyan(
    provider="gemini",
    api_key="YOUR_API_KEY",
    video_config=video_config
)

# Step-by-step control
question = pragyan.scrape_question("https://leetcode.com/problems/binary-search")
analysis = pragyan.analyze(question)
solution = pragyan.solve(question, ProgrammingLanguage.JAVA, analysis)
video_path = pragyan.generate_video(question, solution, analysis)

# Print details
print(f"Title: {question.title}")
print(f"Topics: {analysis['topics']}")
print(f"Concept: {analysis['main_concept']}")
print(f"Approach: {solution.approach}")
print(f"Time: {solution.time_complexity}")
print(f"Space: {solution.space_complexity}")
```

### Class Reference

#### Pragyan

| Method | Description | Returns |
|--------|-------------|---------|
| `scrape_question(url)` | Fetch problem from URL | `Question` |
| `parse_question(text)` | Parse problem from text | `Question` |
| `analyze(question)` | Analyze problem | `Dict` |
| `solve(question, lang, analysis)` | Generate solution | `Solution` |
| `generate_video(question, solution, analysis)` | Create video | `Path` |
| `process(input, lang, video)` | Complete pipeline | `Dict` |
| `generate_test_cases(question, n)` | Generate test cases | `List` |

---

## Configuration

### Environment Variables

```bash
export PRAGYAN_API_KEY="your_api_key"
```

### API Keys

**Google Gemini (Recommended):**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Use with `provider="gemini"`

**Groq:**
1. Visit [Groq Console](https://console.groq.com/keys)
2. Create API key
3. Use with `provider="groq"`

### VideoConfig Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_dir` | Path | ~/Downloads | Video output directory |
| `video_quality` | str | medium_quality | low/medium/high_quality |
| `fps` | int | 30 | Frames per second |
| `pixel_width` | int | 1920 | Video width |
| `pixel_height` | int | 1080 | Video height |
| `background_color` | str | #1e1e1e | Background hex color |

---

## Supported Languages

| Language | Aliases |
|----------|---------|
| Python | python, py |
| Java | java |
| C++ | cpp, c++ |
| C | c |
| JavaScript | javascript, js |
| TypeScript | typescript, ts |
| Go | go, golang |
| Rust | rust, rs |
| Kotlin | kotlin, kt |
| Swift | swift |
| C# | csharp, c#, cs |

---

## Video Generation

### Video Structure

1. **Introduction** - Problem title and topics
2. **Problem Overview** - Description and key points
3. **Concept Explanation** - Core algorithm/technique
4. **Step-by-Step Approach** - Algorithm walkthrough
5. **Code Display** - Syntax-highlighted solution
6. **Example Walkthrough** - Trace through example
7. **Complexity Analysis** - Time and space complexity
8. **Summary** - Key takeaways

### Quality Settings

| Quality | Resolution | Render Time |
|---------|------------|-------------|
| low | 480p | Fast |
| medium | 720p | Moderate |
| high | 1080p | Slow |

---

## Examples

### Two Sum Problem

```python
from pragyan import Pragyan

pragyan = Pragyan(provider="gemini", api_key="KEY")
result = pragyan.process("https://leetcode.com/problems/two-sum")

print(result["solution"].code)
# def twoSum(nums, target):
#     seen = {}
#     for i, num in enumerate(nums):
#         complement = target - num
#         if complement in seen:
#             return [seen[complement], i]
#         seen[num] = i
#     return []
```

### Custom Problem Text

```python
from pragyan import Pragyan

pragyan = Pragyan(provider="groq", api_key="KEY")

problem = """
Given an array of integers, find the maximum subarray sum.

Example:
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6 (subarray [4, -1, 2, 1])

Constraints:
- 1 <= length <= 10^5
- -10^4 <= array[i] <= 10^4
"""

question = pragyan.parse_question(problem)
solution = pragyan.solve(question, "cpp")
print(solution.code)
```

### Multiple Languages

```python
from pragyan import Pragyan, ProgrammingLanguage

pragyan = Pragyan(provider="gemini", api_key="KEY")
question = pragyan.scrape_question("https://leetcode.com/problems/binary-search")
analysis = pragyan.analyze(question)

for lang in [ProgrammingLanguage.PYTHON, ProgrammingLanguage.JAVA, ProgrammingLanguage.CPP]:
    solution = pragyan.solve(question, lang, analysis)
    print(f"\n--- {lang.value} ---")
    print(solution.code)
```

---

## Troubleshooting

### Common Issues

**API Key Error:**
```
Error: Invalid API key
```
Solution: Verify your API key is correct and active.

**Video Generation Fails:**
```
Error: Manim not found
```
Solution: Install Manim and FFmpeg:
```bash
pip install manim
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

**Scraping Fails:**
```
Error: Could not fetch URL
```
Solution: Some sites require Selenium. Install Chrome/ChromeDriver:
```bash
pip install selenium webdriver-manager
```

---

## Project Structure

```
pragyan/
├── src/
│   └── pragyan/
│       ├── __init__.py
│       ├── main.py
│       ├── cli.py
│       ├── models.py
│       ├── llm_client.py
│       ├── scraper.py
│       ├── solver.py
│       ├── video_generator.py
│       ├── animations.py
│       ├── logger.py
│       └── utils.py
├── tests/
├── examples/
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Contributing

Contributions are welcome. Please submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit PR

---

## License

MIT License - see LICENSE file.

---

## Links

- **Repository:** [github.com/Kamalllx/pragyan_pypi](https://github.com/Kamalllx/pragyan_pypi)
- **PyPI:** [pypi.org/project/pragyan](https://pypi.org/project/pragyan/)
- **Issues:** [github.com/Kamalllx/pragyan_pypi/issues](https://github.com/Kamalllx/pragyan_pypi/issues)

---

Built by Kamal
