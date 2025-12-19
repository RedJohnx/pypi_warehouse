"""
Data models for Pragyan package
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from pathlib import Path


class ProgrammingLanguage(Enum):
    """Supported programming languages for solutions"""
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    CSHARP = "csharp"
    
    @classmethod
    def from_string(cls, lang: str) -> "ProgrammingLanguage":
        """Convert string to ProgrammingLanguage enum"""
        lang_map = {
            "python": cls.PYTHON,
            "py": cls.PYTHON,
            "java": cls.JAVA,
            "cpp": cls.CPP,
            "c++": cls.CPP,
            "c": cls.C,
            "javascript": cls.JAVASCRIPT,
            "js": cls.JAVASCRIPT,
            "typescript": cls.TYPESCRIPT,
            "ts": cls.TYPESCRIPT,
            "go": cls.GO,
            "golang": cls.GO,
            "rust": cls.RUST,
            "rs": cls.RUST,
            "kotlin": cls.KOTLIN,
            "kt": cls.KOTLIN,
            "swift": cls.SWIFT,
            "csharp": cls.CSHARP,
            "c#": cls.CSHARP,
            "cs": cls.CSHARP,
        }
        return lang_map.get(lang.lower(), cls.PYTHON)


class LLMProvider(Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    GROQ = "groq"


@dataclass
class Question:
    """Represents a DSA question"""
    title: str
    description: str
    examples: List[Dict[str, Any]] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    difficulty: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    url: Optional[str] = None
    raw_text: Optional[str] = None
    
    def to_prompt(self) -> str:
        """Convert question to a prompt string"""
        prompt = f"## {self.title}\n\n"
        prompt += f"{self.description}\n\n"
        
        if self.examples:
            prompt += "### Examples:\n"
            for i, example in enumerate(self.examples, 1):
                prompt += f"\n**Example {i}:**\n"
                if "input" in example:
                    prompt += f"- Input: {example['input']}\n"
                if "output" in example:
                    prompt += f"- Output: {example['output']}\n"
                if "explanation" in example:
                    prompt += f"- Explanation: {example['explanation']}\n"
        
        if self.constraints:
            prompt += "\n### Constraints:\n"
            for constraint in self.constraints:
                prompt += f"- {constraint}\n"
        
        return prompt


@dataclass
class Solution:
    """Represents a solution to a DSA question"""
    code: str
    language: ProgrammingLanguage
    explanation: str
    time_complexity: str
    space_complexity: str
    concept: str
    approach: str
    step_by_step: List[str] = field(default_factory=list)
    example_walkthrough: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert solution to dictionary"""
        return {
            "code": self.code,
            "language": self.language.value,
            "explanation": self.explanation,
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "concept": self.concept,
            "approach": self.approach,
            "step_by_step": self.step_by_step,
            "example_walkthrough": self.example_walkthrough,
        }


@dataclass
class VideoConfig:
    """Configuration for video generation"""
    output_dir: Path = field(default_factory=lambda: Path.home() / "Downloads")
    video_quality: str = "medium_quality"  # low_quality, medium_quality, high_quality
    fps: int = 30
    resolution: str = "1080p"
    background_color: str = "#1e1e1e"
    text_color: str = "#ffffff"
    code_font: str = "Consolas"
    include_audio: bool = False
    animation_speed: float = 1.0
    
    @property
    def pixel_height(self) -> int:
        """Get pixel height based on resolution"""
        res_map = {
            "480p": 480,
            "720p": 720,
            "1080p": 1080,
            "1440p": 1440,
            "4k": 2160,
        }
        return res_map.get(self.resolution, 1080)
    
    @property
    def pixel_width(self) -> int:
        """Get pixel width based on resolution"""
        return int(self.pixel_height * 16 / 9)


@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: LLMProvider
    api_key: str
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 8192
    
    def __post_init__(self):
        """Set default model based on provider"""
        if self.model is None:
            if self.provider == LLMProvider.GEMINI:
                self.model = "gemini-3.0-pro-preview"
            elif self.provider == LLMProvider.GROQ:
                self.model = "openai/gpt-oss-120b"


@dataclass 
class AnimationScene:
    """Represents a scene in the video animation"""
    title: str
    content: str
    scene_type: str  # "intro", "concept", "code", "example", "walkthrough", "complexity", "outro"
    duration: float = 5.0
    animations: List[str] = field(default_factory=list)
    code_snippet: Optional[str] = None
    highlights: List[int] = field(default_factory=list)
