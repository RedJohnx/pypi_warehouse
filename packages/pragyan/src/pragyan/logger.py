"""
Logger module for Pragyan - provides rich, engaging console output
Shows detailed progress information to keep users informed about the solving process
"""

from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from datetime import datetime
import textwrap


console = Console()


class PragyanLogger:
    """
    Rich-based logger for displaying detailed progress information
    Keeps users engaged by showing what's happening at each step
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the logger
        
        Args:
            verbose: Whether to show detailed output
        """
        self.verbose = verbose
        self.start_time = None
        self.step_count = 0
    
    def start_session(self):
        """Mark the start of a processing session"""
        self.start_time = datetime.now()
        self.step_count = 0
        if self.verbose:
            console.print()
            console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]")
            console.print("[bold cyan]  PRAGYAN - AI-Powered DSA Solver[/bold cyan]")
            console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]")
            console.print()
    
    def _step_header(self, title: str) -> str:
        """Create a step header"""
        self.step_count += 1
        return f"[bold white]STEP {self.step_count}:[/bold white] [bold yellow]{title}[/bold yellow]"
    
    def log_scraping_start(self, url: str):
        """Log the start of web scraping"""
        if not self.verbose:
            return
        
        console.print(self._step_header("Fetching Problem"))
        console.print(f"   [dim]Source:[/dim] {url}")
        console.print()
    
    def log_scraped_question(self, title: str, description: str, difficulty: Optional[str], examples: List[str]):
        """Log the scraped question details"""
        if not self.verbose:
            return
        
        # Create a panel showing what was scraped
        content = []
        content.append(f"[bold white]Title:[/bold white] {title}")
        if difficulty:
            diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(difficulty.lower(), "white")
            content.append(f"[bold white]Difficulty:[/bold white] [{diff_color}]{difficulty}[/{diff_color}]")
        
        # Truncate description for display
        desc_preview = description[:300] + "..." if len(description) > 300 else description
        content.append(f"\n[bold white]Problem Statement:[/bold white]\n[dim]{desc_preview}[/dim]")
        
        if examples:
            content.append(f"\n[bold white]Examples Found:[/bold white] {len(examples)}")
            for i, ex in enumerate(examples[:2], 1):
                ex_preview = ex[:100] + "..." if len(ex) > 100 else ex
                content.append(f"   [dim]Example {i}: {ex_preview}[/dim]")
        
        console.print(Panel(
            "\n".join(content),
            title="[bold green]Scraped Question[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        console.print()
    
    def log_analysis_start(self):
        """Log the start of question analysis"""
        if not self.verbose:
            return
        
        console.print(self._step_header("Analyzing Problem"))
        console.print("   [dim]Identifying patterns, data structures, and optimal approach...[/dim]")
        console.print()
    
    def log_analysis_result(self, analysis: Dict[str, Any]):
        """Log the analysis results with thought process"""
        if not self.verbose:
            return
        
        # Create a tree structure showing the analysis
        tree = Tree("[bold magenta]Analysis Results[/bold magenta]")
        
        # Topics
        topics = analysis.get("topics", [])
        if topics:
            topics_branch = tree.add("[bold]Topics Identified[/bold]")
            for topic in topics[:5]:
                topics_branch.add(f"[cyan]{topic}[/cyan]")
        
        # Main concept
        main_concept = analysis.get("main_concept", "")
        if main_concept:
            concept_branch = tree.add("[bold]Core Concept[/bold]")
            concept_branch.add(f"[yellow]{main_concept}[/yellow]")
        
        # Approach
        approach = analysis.get("approach", "")
        if approach:
            approach_branch = tree.add("[bold]Recommended Approach[/bold]")
            # Wrap long approach text
            wrapped = textwrap.wrap(approach, width=60)
            for line in wrapped[:3]:
                approach_branch.add(f"[white]{line}[/white]")
        
        # Complexity hints
        time_hint = analysis.get("time_hint", "")
        space_hint = analysis.get("space_hint", "")
        if time_hint or space_hint:
            complexity_branch = tree.add("[bold]Expected Complexity[/bold]")
            if time_hint:
                complexity_branch.add(f"[green]Time: {time_hint}[/green]")
            if space_hint:
                complexity_branch.add(f"[blue]Space: {space_hint}[/blue]")
        
        # Edge cases
        edge_cases = analysis.get("edge_cases", [])
        if edge_cases:
            edge_branch = tree.add("[bold]Edge Cases to Handle[/bold]")
            for case in edge_cases[:4]:
                edge_branch.add(f"[red]{case}[/red]")
        
        console.print(Panel(tree, title="[bold magenta]Thought Process[/bold magenta]", border_style="magenta"))
        console.print()
    
    def log_solving_start(self, language: str):
        """Log the start of solution generation"""
        if not self.verbose:
            return
        
        console.print(self._step_header(f"Generating {language.title()} Solution"))
        console.print("   [dim]Crafting optimal solution with explanations...[/dim]")
        console.print()
    
    def log_solution_generated(self, solution: Any):
        """Log the generated solution details"""
        if not self.verbose:
            return
        
        # Show approach and complexity
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style="bold white")
        table.add_column("Value", style="white")
        
        table.add_row("Concept:", solution.concept if hasattr(solution, 'concept') else "N/A")
        table.add_row("Approach:", (solution.approach[:80] + "...") if hasattr(solution, 'approach') and len(solution.approach) > 80 else (solution.approach if hasattr(solution, 'approach') else "N/A"))
        table.add_row("Time Complexity:", solution.time_complexity if hasattr(solution, 'time_complexity') else "N/A")
        table.add_row("Space Complexity:", solution.space_complexity if hasattr(solution, 'space_complexity') else "N/A")
        
        console.print(Panel(table, title="[bold blue]Solution Summary[/bold blue]", border_style="blue"))
        console.print()
    
    def log_step_by_step(self, steps: List[str]):
        """Log the step-by-step approach"""
        if not self.verbose or not steps:
            return
        
        console.print("[bold white]Algorithm Steps:[/bold white]")
        for i, step in enumerate(steps[:6], 1):
            console.print(f"   [cyan]{i}.[/cyan] {step}")
        console.print()
    
    def log_test_case_simulation(self, test_input: str, expected_output: str, walkthrough: str):
        """Log a test case simulation"""
        if not self.verbose:
            return
        
        console.print(self._step_header("Example Walkthrough"))
        
        content = []
        content.append(f"[bold white]Input:[/bold white] [green]{test_input}[/green]")
        content.append(f"[bold white]Expected Output:[/bold white] [yellow]{expected_output}[/yellow]")
        content.append("")
        content.append("[bold white]Trace:[/bold white]")
        
        # Parse walkthrough into steps
        walkthrough_lines = walkthrough.split('\n')[:8]
        for line in walkthrough_lines:
            if line.strip():
                content.append(f"   [dim]{line.strip()}[/dim]")
        
        console.print(Panel(
            "\n".join(content),
            title="[bold cyan]Test Case Execution[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
    
    def log_video_generation_start(self):
        """Log the start of video generation"""
        if not self.verbose:
            return
        
        console.print(self._step_header("Generating Explanation Video"))
        console.print("   [dim]Creating animated visualization with Manim...[/dim]")
        console.print("   [dim]This may take 1-3 minutes depending on complexity.[/dim]")
        console.print()
    
    def log_video_progress(self, stage: str):
        """Log video generation progress"""
        if not self.verbose:
            return
        console.print(f"   [dim]> {stage}[/dim]")
    
    def log_video_complete(self, path: str):
        """Log successful video generation"""
        if not self.verbose:
            return
        
        console.print(Panel(
            f"[bold green]Video saved to:[/bold green]\n{path}",
            title="[bold green]Video Generated[/bold green]",
            border_style="green"
        ))
        console.print()
    
    def log_video_error(self, error: str):
        """Log video generation error"""
        if not self.verbose:
            return
        
        console.print(f"   [yellow]Video generation skipped: {error}[/yellow]")
        console.print()
    
    def log_completion(self):
        """Log session completion"""
        if not self.verbose:
            return
        
        elapsed = ""
        if self.start_time:
            duration = datetime.now() - self.start_time
            elapsed = f" in {duration.total_seconds():.1f}s"
        
        console.print()
        console.print("[bold green]" + "=" * 60 + "[/bold green]")
        console.print(f"[bold green]  Processing Complete{elapsed}[/bold green]")
        console.print("[bold green]" + "=" * 60 + "[/bold green]")
        console.print()
    
    def log_error(self, stage: str, error: str):
        """Log an error"""
        console.print(f"[bold red]Error in {stage}:[/bold red] {error}")
    
    def log_info(self, message: str):
        """Log an info message"""
        if self.verbose:
            console.print(f"[dim]{message}[/dim]")
    
    def log_warning(self, message: str):
        """Log a warning message"""
        console.print(f"[yellow]Warning: {message}[/yellow]")


# Global logger instance
_logger: Optional[PragyanLogger] = None


def get_logger(verbose: bool = True) -> PragyanLogger:
    """Get or create the global logger instance"""
    global _logger
    if _logger is None or _logger.verbose != verbose:
        _logger = PragyanLogger(verbose=verbose)
    return _logger


def set_verbose(verbose: bool):
    """Set global verbosity"""
    global _logger
    if _logger:
        _logger.verbose = verbose
    else:
        _logger = PragyanLogger(verbose=verbose)
