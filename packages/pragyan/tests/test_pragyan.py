"""
Tests for Pragyan package
"""

import pytest
from pragyan.models import (
    Question, Solution, ProgrammingLanguage, 
    VideoConfig, LLMConfig, LLMProvider
)


class TestModels:
    """Test data models"""
    
    def test_programming_language_from_string(self):
        """Test language parsing"""
        assert ProgrammingLanguage.from_string("python") == ProgrammingLanguage.PYTHON
        assert ProgrammingLanguage.from_string("py") == ProgrammingLanguage.PYTHON
        assert ProgrammingLanguage.from_string("java") == ProgrammingLanguage.JAVA
        assert ProgrammingLanguage.from_string("cpp") == ProgrammingLanguage.CPP
        assert ProgrammingLanguage.from_string("c++") == ProgrammingLanguage.CPP
        assert ProgrammingLanguage.from_string("javascript") == ProgrammingLanguage.JAVASCRIPT
        assert ProgrammingLanguage.from_string("js") == ProgrammingLanguage.JAVASCRIPT
        assert ProgrammingLanguage.from_string("unknown") == ProgrammingLanguage.PYTHON  # default
    
    def test_question_to_prompt(self):
        """Test question prompt generation"""
        question = Question(
            title="Two Sum",
            description="Given an array of integers, return indices of the two numbers that add up to a target.",
            examples=[
                {"input": "[2,7,11,15], target=9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9"}
            ],
            constraints=["2 <= nums.length <= 10^4"]
        )
        
        prompt = question.to_prompt()
        
        assert "Two Sum" in prompt
        assert "Given an array of integers" in prompt
        assert "Example 1" in prompt
        assert "[2,7,11,15]" in prompt
        assert "Constraints" in prompt
    
    def test_solution_to_dict(self):
        """Test solution serialization"""
        solution = Solution(
            code="def twoSum(nums, target): pass",
            language=ProgrammingLanguage.PYTHON,
            explanation="Use a hash map",
            time_complexity="O(n)",
            space_complexity="O(n)",
            concept="Hash Table",
            approach="One-pass hash table",
            step_by_step=["Step 1", "Step 2"]
        )
        
        d = solution.to_dict()
        
        assert d["code"] == "def twoSum(nums, target): pass"
        assert d["language"] == "python"
        assert d["time_complexity"] == "O(n)"
    
    def test_video_config_defaults(self):
        """Test video config default values"""
        config = VideoConfig()
        
        assert config.pixel_height == 1080
        assert config.pixel_width == 1920
        assert config.fps == 30
        assert config.video_quality == "medium_quality"
    
    def test_video_config_resolution(self):
        """Test different resolutions"""
        config = VideoConfig(resolution="720p")
        assert config.pixel_height == 720
        
        config = VideoConfig(resolution="4k")
        assert config.pixel_height == 2160
    
    def test_llm_config_default_models(self):
        """Test default model selection"""
        gemini_config = LLMConfig(provider=LLMProvider.GEMINI, api_key="test")
        assert gemini_config.model == "gemini-2.0-flash"
        
        groq_config = LLMConfig(provider=LLMProvider.GROQ, api_key="test")
        assert groq_config.model == "llama-3.3-70b-versatile"


class TestScraper:
    """Test web scraper"""
    
    def test_parse_text_question(self):
        """Test parsing text questions"""
        from pragyan.scraper import QuestionScraper
        
        scraper = QuestionScraper()
        
        text = """Two Sum
        
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
"""
        
        question = scraper.parse_text_question(text)
        
        assert "Two Sum" in question.title
        assert "array of integers" in question.description
    
    def test_extract_examples(self):
        """Test example extraction"""
        from pragyan.scraper import QuestionScraper
        
        scraper = QuestionScraper()
        
        text = """
Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9.

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]
"""
        
        examples = scraper._extract_examples(text)
        
        assert len(examples) >= 1


class TestUtils:
    """Test utility functions"""
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        from pragyan.utils import sanitize_filename
        
        assert sanitize_filename("Hello World") == "Hello_World"
        assert sanitize_filename("file<>:name") == "filename"
        assert sanitize_filename("  spaces  ") == "spaces"
    
    def test_is_valid_url(self):
        """Test URL validation"""
        from pragyan.utils import is_valid_url
        
        assert is_valid_url("https://leetcode.com/problems/two-sum")
        assert is_valid_url("http://example.com")
        assert not is_valid_url("not a url")
        assert not is_valid_url("ftp://example.com")
    
    def test_truncate_text(self):
        """Test text truncation"""
        from pragyan.utils import truncate_text
        
        assert truncate_text("short", 10) == "short"
        assert truncate_text("this is a long text", 10) == "this is..."
        assert len(truncate_text("very long text here", 10)) == 10
    
    def test_format_complexity(self):
        """Test complexity formatting"""
        from pragyan.utils import format_complexity
        
        assert format_complexity("n") == "O(n)"
        assert format_complexity("O(n)") == "O(n)"
        assert format_complexity("(n^2)") == "O(n^2)"


# Integration tests (require API keys)
class TestIntegration:
    """Integration tests - these require actual API keys"""
    
    @pytest.mark.skip(reason="Requires API key")
    def test_full_pipeline(self):
        """Test the full processing pipeline"""
        from pragyan import Pragyan
        
        pragyan = Pragyan(provider="gemini", api_key="YOUR_KEY")
        
        result = pragyan.process(
            "Given an array, find two numbers that sum to target",
            language="python",
            generate_video=False
        )
        
        assert result["solution"] is not None
        assert result["solution"].code != ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
