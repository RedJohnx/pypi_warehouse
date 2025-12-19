"""
Example: Basic usage of Pragyan

This example demonstrates how to use Pragyan to solve a DSA problem
and generate an explanation video.
"""

from pragyan import Pragyan

# Initialize with your API key
# You can use either Gemini or Groq
pragyan = Pragyan(
    provider="gemini",  # or "groq"
    api_key="YOUR_API_KEY"  # Replace with your actual API key
)

# Option 1: Solve from a LeetCode URL
url = "https://leetcode.com/problems/two-sum"
result = pragyan.process(
    url,
    language="python",
    generate_video=True
)

# Print the solution
print("=" * 50)
print("QUESTION:", result["question"].title)
print("=" * 50)
print("\nCONCEPT:", result["solution"].concept)
print("\nAPPROACH:", result["solution"].approach)
print("\nCODE:")
print(result["solution"].code)
print("\nTIME COMPLEXITY:", result["solution"].time_complexity)
print("SPACE COMPLEXITY:", result["solution"].space_complexity)

if result["video_path"]:
    print(f"\nVIDEO SAVED TO: {result['video_path']}")


# Option 2: Solve from text
problem_text = """
Maximum Subarray

Given an integer array nums, find the contiguous subarray (containing at least one number) 
which has the largest sum and return its sum.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""

question = pragyan.parse_question(problem_text)
analysis = pragyan.analyze(question)
solution = pragyan.solve(question, "java", analysis)

print("\n" + "=" * 50)
print("QUESTION:", question.title)
print("=" * 50)
print("\nJAVA SOLUTION:")
print(solution.code)
