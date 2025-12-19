"""
DSA Solver module for analyzing and solving DSA questions
"""

from typing import Optional, Dict, Any, Tuple

from pragyan.models import Question, Solution, ProgrammingLanguage
from pragyan.llm_client import LLMClient


class DSASolver:
    """
    Analyzes DSA questions and generates solutions with explanations
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize the solver
        
        Args:
            llm_client: Configured LLM client for generating solutions
        """
        self.llm = llm_client
    
    def analyze(self, question: Question) -> Dict[str, Any]:
        """
        Analyze a DSA question to understand concepts and approach
        
        Args:
            question: The DSA question to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        return self.llm.analyze_question(question)
    
    def solve(
        self,
        question: Question,
        language: ProgrammingLanguage,
        analysis: Optional[Dict[str, Any]] = None
    ) -> Solution:
        """
        Generate a solution for the DSA question
        
        Args:
            question: The DSA question to solve
            language: Programming language for the solution
            analysis: Optional pre-computed analysis
            
        Returns:
            Solution object with code and explanation
        """
        if analysis is None:
            analysis = self.analyze(question)
        
        return self.llm.generate_solution(question, language, analysis)
    
    def solve_with_analysis(
        self,
        question: Question,
        language: ProgrammingLanguage
    ) -> Tuple[Solution, Dict[str, Any]]:
        """
        Analyze and solve a question, returning both results
        
        Args:
            question: The DSA question
            language: Programming language for the solution
            
        Returns:
            Tuple of (Solution, analysis dict)
        """
        analysis = self.analyze(question)
        solution = self.solve(question, language, analysis)
        return solution, analysis
    
    def get_video_script(
        self,
        question: Question,
        solution: Solution,
        analysis: Dict[str, Any]
    ) -> list:
        """
        Generate a video script for explaining the solution
        
        Args:
            question: The DSA question
            solution: The generated solution
            analysis: Question analysis
            
        Returns:
            List of scene dictionaries for video generation
        """
        return self.llm.generate_video_script(question, solution, analysis)
    
    def generate_test_cases(self, question: Question, num_cases: int = 5) -> list:
        """
        Generate additional test cases for the problem
        
        Args:
            question: The DSA question
            num_cases: Number of test cases to generate
            
        Returns:
            List of test case dictionaries
        """
        prompt = f"""Generate {num_cases} test cases for this problem:

{question.to_prompt()}

Return a JSON array of test cases, each with:
- "input": the input values
- "expected_output": the expected output
- "description": why this test case is important (edge case, normal case, etc.)

Format:
[
    {{"input": "...", "expected_output": "...", "description": "..."}},
    ...
]"""
        
        result = self.llm.generate_json(prompt)
        
        if isinstance(result, list):
            return result
        return result.get("test_cases", result.get("cases", []))
    
    def explain_concept(self, concept: str) -> str:
        """
        Get a detailed explanation of a DSA concept
        
        Args:
            concept: Name of the concept (e.g., "Dynamic Programming", "Binary Search")
            
        Returns:
            Detailed explanation string
        """
        prompt = f"""Explain the DSA concept "{concept}" in detail:

1. What is {concept}?
2. When is it used?
3. How does it work? (step by step)
4. Time and space complexity implications
5. Common patterns and templates
6. Tips for recognizing when to use it

Provide a clear, educational explanation suitable for a tutorial video."""
        
        return self.llm.generate(prompt)
    
    def compare_approaches(self, question: Question) -> Dict[str, Any]:
        """
        Compare different approaches to solve the problem
        
        Args:
            question: The DSA question
            
        Returns:
            Dictionary with different approaches and their trade-offs
        """
        prompt = f"""Analyze different approaches to solve this problem:

{question.to_prompt()}

Compare at least 2-3 different approaches:
1. Brute force / naive approach
2. Optimized approach(es)

For each approach, provide:
- Description of the approach
- Time complexity
- Space complexity
- Pros and cons
- When to use this approach

Return as JSON:
{{
    "approaches": [
        {{
            "name": "Approach name",
            "description": "How it works",
            "time_complexity": "O(?)",
            "space_complexity": "O(?)",
            "pros": ["..."],
            "cons": ["..."],
            "best_for": "When to use this"
        }},
        ...
    ],
    "recommended": "Name of recommended approach",
    "recommendation_reason": "Why this is recommended"
}}"""
        
        return self.llm.generate_json(prompt)
