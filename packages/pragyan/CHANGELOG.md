# Pragyan Changelog

All notable changes to this project will be documented in this file.

---

## [1.0.8] - 2024-12-19

### 🐛 Critical Bug Fix
- **Fixed video generation crash**: `name 'i' is not defined`
- Root cause: The entire Manim scene code was inside a Python f-string, causing loop variables (`i`, `j`, etc.) to be interpreted as f-string placeholders
- Solution: Split the scene code into a header (with f-string substitutions for data) and a body (regular string with no f-string processing)
- Simplified and cleaned up the video generator code

---

## [1.0.7] - 2024-12-19

### 🐛 Bug Fix
- **Fixed video generation error**: `sequence item 0: expected str instance, dict found`
- Fixed `_extract_example_array()` to properly handle examples that are dictionaries
- Examples from scraped questions now correctly parsed for array extraction

---

## [1.0.6] - 2024-12-19

### 🐛 Critical Bug Fix
- **Completely rewrote code deduplication algorithm** to properly handle sliding window repetition patterns
- New multi-stage deduplication approach:
  - Detects code block boundaries (class/function definitions)
  - Checks for repeated significant lines
  - Validates code completeness before truncation
- Added `_is_complete_code()` helper to ensure code blocks are complete

### 📦 Repository
- Added pragyan to pypi_warehouse collection repository
- Updated README with all PyPI package links

---

## [1.0.5] - 2024-12-18

### 🎬 Major Video Overhaul
- **Complete rewrite of video generator** with proper Manim animations
- **Visual data structure representations**: Arrays with boxes, values, and indices
- **Algorithm-specific animations**:
  - Two-pointer technique with animated L/R pointers
  - Sliding window with moving yellow highlight
  - Binary search with range narrowing visualization
  - Hash map operations with key-value boxes
  - Stack/queue push-pop animations
  - Dynamic programming table building
- **Complexity graphs**: Visual O(1), O(log n), O(n), O(n²) curves
- **Algorithm icons**: Visual representations for each technique
- **Smart algorithm detection**: Auto-detects algorithm type from solution

### 🐛 Bug Fixes
- **Fixed code duplication bug**: Solutions no longer show repeated code blocks
- Added deduplication logic to clean LLM responses
- Improved prompt engineering to prevent repetition

### 📚 Documentation
- Added highlighted `pip install pragyan` at top of README
- Added quick start code snippets for Python and CLI usage
- Improved installation visibility

---

## [1.0.4] - 2024-12-17

### Added
- **Verbose logging system** with real-time progress updates
- New `logger.py` module with Rich console output
- Step-by-step feedback during solving process
- Professional README with ASCII architecture diagrams

### Fixed
- Fixed repository URLs in pyproject.toml
- Improved error handling and user feedback

---

## [1.0.3] - 2024-12-17

### Fixed
- Fixed Manim Code parameter compatibility issue
- Removed `code_style` parameter causing errors

---

## [1.0.2] - 2024-12-17

### Fixed
- Fixed VGroup import error in video generation
- Corrected Manim imports for animation components

---

## [1.0.1] - 2024-12-17

### Fixed
- Fixed JSON parsing for LLM responses
- Improved error handling for malformed JSON

---

## [1.0.0] - 2024-12-17

### Added
- Initial release of Pragyan
- Web scraping support for LeetCode, GeeksforGeeks, Codeforces, HackerRank
- LangChain-based intelligent web scraping
- Google Gemini API integration (gemini-2.0-flash model)
- Groq API integration (llama-3.3-70b-versatile model)
- Solution generation in 11 programming languages
- Manim-based video generation with animations
- MoviePy fallback for simple video generation
- Command-line interface with interactive mode
- Step-by-step solution explanations
- Test case generation
- Approach comparison feature
- Concept explanation feature

### Supported Languages
- Python
- Java
- C++
- C
- JavaScript
- TypeScript
- Go
- Rust
- Kotlin
- Swift
- C#

### Video Features
- Introduction scene with problem title
- Problem overview
- Concept explanation
- Step-by-step approach walkthrough
- Code display with syntax highlighting
- Example walkthrough
- Complexity analysis
- Summary/outro
