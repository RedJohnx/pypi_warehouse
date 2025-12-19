"""
Main module for Pragyan - orchestrates all components
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union

from pragyan.models import (
    Question, Solution, VideoConfig, 
    ProgrammingLanguage, LLMProvider
)
from pragyan.llm_client import LLMClient
from pragyan.scraper import QuestionScraper
from pragyan.solver import DSASolver
from pragyan.video_generator import VideoGenerator, SimpleVideoGenerator


class Pragyan:
    """
    Main class for the Pragyan DSA solver and video generator
    
    This class orchestrates all components:
    - Web scraping for questions
    - LLM-based analysis and solution generation
    - Video generation with Manim
    
    Example:
        >>> from pragyan import Pragyan
        >>> 
        >>> # Initialize with Gemini
        >>> pragyan = Pragyan(provider="gemini", api_key="YOUR_API_KEY")
        >>> 
        >>> # Scrape and solve a LeetCode problem
        >>> question = pragyan.scrape_question("https://leetcode.com/problems/two-sum")
        >>> solution = pragyan.solve(question, "python")
        >>> 
        >>> # Generate explanation video
        >>> video_path = pragyan.generate_video(question, solution)
        >>> print(f"Video saved to: {video_path}")
    """
    
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        video_config: Optional[VideoConfig] = None,
    ):
        """
        Initialize Pragyan
        
        Args:
            provider: LLM provider - either "gemini" or "groq"
            api_key: API key for the provider
            model: Optional model name override
            video_config: Optional video configuration
        """
        self.provider = provider.lower()
        self.api_key = api_key
        
        # Initialize LLM client
        self.llm = LLMClient(provider=self.provider, api_key=api_key, model=model)
        
        # Initialize components
        self.scraper = QuestionScraper()
        self.solver = DSASolver(self.llm)
        
        # Video configuration
        self.video_config = video_config or VideoConfig()
        
        # Video generator (lazy initialized)
        self._video_generator = None
        self._simple_video_generator = None
    
    @property
    def video_generator(self) -> VideoGenerator:
        """Get or create the video generator"""
        if self._video_generator is None:
            self._video_generator = VideoGenerator(self.video_config)
        return self._video_generator
    
    @property
    def simple_video_generator(self) -> SimpleVideoGenerator:
        """Get or create the simple video generator"""
        if self._simple_video_generator is None:
            self._simple_video_generator = SimpleVideoGenerator(self.video_config)
        return self._simple_video_generator
    
    def scrape_question(self, url: str) -> Question:
        """
        Scrape a question from a URL
        
        Args:
            url: URL of the problem page (LeetCode, GFG, etc.)
            
        Returns:
            Question object with extracted information
        """
        return self.scraper.scrape_url(url)
    
    def parse_question(self, text: str) -> Question:
        """
        Parse a question from plain text
        
        Args:
            text: Plain text description of the problem
            
        Returns:
            Question object
        """
        return self.scraper.parse_text_question(text)
    
    def analyze(self, question: Question) -> Dict[str, Any]:
        """
        Analyze a question to understand concepts and approach
        
        Args:
            question: The DSA question to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        return self.solver.analyze(question)
    
    def solve(
        self,
        question: Question,
        language: Union[str, ProgrammingLanguage],
        analysis: Optional[Dict[str, Any]] = None
    ) -> Solution:
        """
        Generate a solution for the DSA question
        
        Args:
            question: The DSA question to solve
            language: Programming language (string or enum)
            analysis: Optional pre-computed analysis
            
        Returns:
            Solution object with code and explanation
        """
        if isinstance(language, str):
            language = ProgrammingLanguage.from_string(language)
        
        return self.solver.solve(question, language, analysis)
    
    def solve_complete(
        self,
        question: Question,
        language: Union[str, ProgrammingLanguage]
    ) -> tuple:
        """
        Complete analysis and solution generation
        
        Args:
            question: The DSA question
            language: Programming language
            
        Returns:
            Tuple of (Solution, analysis dict)
        """
        if isinstance(language, str):
            language = ProgrammingLanguage.from_string(language)
        
        return self.solver.solve_with_analysis(question, language)
    
    def generate_video(
        self,
        question: Question,
        solution: Solution,
        analysis: Optional[Dict[str, Any]] = None,
        output_filename: Optional[str] = None,
        use_simple: bool = False
    ) -> Path:
        """
        Generate an explanation video
        
        Args:
            question: The DSA question
            solution: The generated solution
            analysis: Question analysis (will be generated if not provided)
            output_filename: Optional custom output filename
            use_simple: Use simple MoviePy generator instead of Manim
            
        Returns:
            Path to the generated video file
        """
        if analysis is None:
            analysis = self.analyze(question)
        
        if use_simple:
            return self.simple_video_generator.generate_slideshow(
                question, solution, analysis
            )
        
        # Generate video script
        video_script = self.solver.get_video_script(question, solution, analysis)
        
        return self.video_generator.generate_video(
            question, solution, analysis, video_script, output_filename
        )
    
    def process(
        self,
        input_source: str,
        language: Union[str, ProgrammingLanguage] = "python",
        generate_video: bool = True,
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete processing pipeline
        
        Args:
            input_source: URL or text of the problem
            language: Programming language for solution
            generate_video: Whether to generate explanation video
            output_filename: Optional video output filename
            
        Returns:
            Dictionary with question, analysis, solution, and video_path
        """
        # Determine if input is URL or text
        is_url = input_source.startswith(('http://', 'https://'))
        
        # Get question
        if is_url:
            question = self.scrape_question(input_source)
        else:
            question = self.parse_question(input_source)
        
        # Parse language
        if isinstance(language, str):
            language = ProgrammingLanguage.from_string(language)
        
        # Analyze and solve
        solution, analysis = self.solve_complete(question, language)
        
        # Generate video if requested
        video_path = None
        if generate_video:
            try:
                video_path = self.generate_video(
                    question, solution, analysis, output_filename
                )
            except Exception as e:
                # Try simple video generator as fallback
                try:
                    video_path = self.generate_video(
                        question, solution, analysis, output_filename, use_simple=True
                    )
                except:
                    pass  # Video generation failed
        
        return {
            "question": question,
            "analysis": analysis,
            "solution": solution,
            "video_path": video_path,
        }
    
    def generate_test_cases(self, question: Question, num_cases: int = 5) -> list:
        """
        Generate test cases for a problem
        
        Args:
            question: The DSA question
            num_cases: Number of test cases to generate
            
        Returns:
            List of test case dictionaries
        """
        return self.solver.generate_test_cases(question, num_cases)
    
    def explain_concept(self, concept: str) -> str:
        """
        Get a detailed explanation of a DSA concept
        
        Args:
            concept: Name of the concept
            
        Returns:
            Detailed explanation string
        """
        return self.solver.explain_concept(concept)
    
    def compare_approaches(self, question: Question) -> Dict[str, Any]:
        """
        Compare different approaches to solve the problem
        
        Args:
            question: The DSA question
            
        Returns:
            Dictionary with different approaches and trade-offs
        """
        return self.solver.compare_approaches(question)


def solve_from_url(
    url: str,
    language: str = "python",
    provider: str = "gemini",
    api_key: Optional[str] = None,
    generate_video: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to solve a problem from URL
    
    Args:
        url: URL of the problem
        language: Programming language
        provider: LLM provider (gemini or groq)
        api_key: API key
        generate_video: Whether to generate video
        
    Returns:
        Result dictionary
    """
    resolved_key: str
    if not api_key:
        import os
        env_key = os.environ.get("PRAGYAN_API_KEY")
        if not env_key:
            raise ValueError("API key required. Set PRAGYAN_API_KEY environment variable or pass api_key parameter.")
        resolved_key = env_key
    else:
        resolved_key = api_key
    
    pragyan = Pragyan(provider=provider, api_key=resolved_key)
    return pragyan.process(url, language, generate_video)


def solve_from_text(
    text: str,
    language: str = "python",
    provider: str = "gemini",
    api_key: Optional[str] = None,
    generate_video: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to solve a problem from text
    
    Args:
        text: Problem description text
        language: Programming language
        provider: LLM provider (gemini or groq)
        api_key: API key
        generate_video: Whether to generate video
        
    Returns:
        Result dictionary
    """
    resolved_key: str
    if not api_key:
        import os
        env_key = os.environ.get("PRAGYAN_API_KEY")
        if not env_key:
            raise ValueError("API key required. Set PRAGYAN_API_KEY environment variable or pass api_key parameter.")
        resolved_key = env_key
    else:
        resolved_key = api_key
    
    pragyan = Pragyan(provider=provider, api_key=resolved_key)
    return pragyan.process(text, language, generate_video)
