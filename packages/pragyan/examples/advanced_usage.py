"""
Example: Advanced usage of Pragyan

This example demonstrates advanced features like:
- Comparing different approaches
- Generating test cases
- Custom video configuration
- Concept explanations
"""

from pathlib import Path
from pragyan import Pragyan, VideoConfig, ProgrammingLanguage

# Custom video configuration
video_config = VideoConfig(
    output_dir=Path("./output_videos"),  # Custom output directory
    video_quality="high_quality",  # Options: low_quality, medium_quality, high_quality
    resolution="1080p",  # Options: 480p, 720p, 1080p, 1440p, 4k
    fps=30,
    background_color="#1a1a2e",  # Dark blue background
)

# Initialize Pragyan with custom config
pragyan = Pragyan(
    provider="gemini",
    api_key="YOUR_API_KEY",
    video_config=video_config
)

# Scrape a problem
url = "https://leetcode.com/problems/longest-substring-without-repeating-characters"
question = pragyan.scrape_question(url)

print("=" * 60)
print(f"Problem: {question.title}")
print("=" * 60)

# Get detailed analysis
analysis = pragyan.analyze(question)
print("\n📊 ANALYSIS:")
print(f"  Difficulty: {analysis.get('difficulty', 'Unknown')}")
print(f"  Topics: {', '.join(analysis.get('topics', []))}")
print(f"  Main Concept: {analysis.get('main_concept', 'N/A')}")
print(f"  Intuition: {analysis.get('intuition', 'N/A')[:200]}...")

# Compare different approaches
print("\n🔄 COMPARING APPROACHES:")
comparison = pragyan.compare_approaches(question)

for i, approach in enumerate(comparison.get("approaches", []), 1):
    print(f"\n  Approach {i}: {approach['name']}")
    print(f"    Time: {approach['time_complexity']}")
    print(f"    Space: {approach['space_complexity']}")
    print(f"    Description: {approach['description'][:100]}...")

print(f"\n  ✅ Recommended: {comparison.get('recommended', 'N/A')}")

# Generate solution in multiple languages
print("\n💻 GENERATING SOLUTIONS:")

languages = [
    ProgrammingLanguage.PYTHON,
    ProgrammingLanguage.CPP,
    ProgrammingLanguage.JAVA
]

solutions = {}
for lang in languages:
    print(f"  Generating {lang.value} solution...")
    solutions[lang] = pragyan.solve(question, lang, analysis)
    print(f"    ✓ Done")

# Print solutions
for lang, solution in solutions.items():
    print(f"\n{'=' * 40}")
    print(f"{lang.value.upper()} SOLUTION:")
    print("=" * 40)
    print(solution.code[:500] + "..." if len(solution.code) > 500 else solution.code)

# Generate test cases
print("\n🧪 GENERATING TEST CASES:")
test_cases = pragyan.generate_test_cases(question, num_cases=5)

for i, tc in enumerate(test_cases, 1):
    print(f"\n  Test Case {i}:")
    print(f"    Input: {tc.get('input', 'N/A')}")
    print(f"    Expected: {tc.get('expected_output', 'N/A')}")
    print(f"    Description: {tc.get('description', 'N/A')}")

# Get concept explanation
print("\n📚 CONCEPT EXPLANATION:")
concept = analysis.get('main_concept', 'Sliding Window')
explanation = pragyan.explain_concept(concept)
print(f"\n{concept}:\n{explanation[:500]}...")

# Generate video for the best solution
print("\n🎥 GENERATING VIDEO...")
try:
    video_path = pragyan.generate_video(
        question, 
        solutions[ProgrammingLanguage.PYTHON], 
        analysis
    )
    print(f"  ✅ Video saved to: {video_path}")
except Exception as e:
    print(f"  ⚠️ Video generation failed: {e}")
    print("  Trying simple video generator...")
    try:
        video_path = pragyan.generate_video(
            question,
            solutions[ProgrammingLanguage.PYTHON],
            analysis,
            use_simple=True
        )
        print(f"  ✅ Simple video saved to: {video_path}")
    except Exception as e2:
        print(f"  ❌ Simple video also failed: {e2}")

print("\n✨ Done!")
