"""
Pragyan - AI-powered DSA Question Solver with Video Explanations

This package provides:
- LeetCode question scraping
- DSA problem analysis and solution generation
- Multi-language code generation
- Animated video explanations using Manim
"""

__version__ = "1.0.4"
__author__ = "Kamal"

from pragyan.main import Pragyan, solve_from_url, solve_from_text
from pragyan.models import (
    Question, 
    Solution, 
    VideoConfig, 
    ProgrammingLanguage,
    LLMProvider,
    LLMConfig,
)
from pragyan.scraper import QuestionScraper
from pragyan.solver import DSASolver
from pragyan.llm_client import LLMClient
from pragyan.video_generator import VideoGenerator, SimpleVideoGenerator
from pragyan.logger import PragyanLogger, get_logger

__all__ = [
    # Main class
    "Pragyan",
    
    # Convenience functions
    "solve_from_url",
    "solve_from_text",
    
    # Models
    "Question",
    "Solution",
    "VideoConfig",
    "ProgrammingLanguage",
    "LLMProvider",
    "LLMConfig",
    
    # Components
    "QuestionScraper",
    "DSASolver",
    "LLMClient",
    "VideoGenerator",
    "SimpleVideoGenerator",
    
    # Logger
    "PragyanLogger",
    "get_logger",
    
    # Metadata
    "__version__",
    "__author__",
]
