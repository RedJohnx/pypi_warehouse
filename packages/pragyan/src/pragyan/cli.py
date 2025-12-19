"""
Command Line Interface for Pragyan
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm

from pragyan.models import ProgrammingLanguage, VideoConfig
from pragyan.main import Pragyan
from pragyan.logger import get_logger, PragyanLogger


console = Console()


def print_banner():
    """Print the Pragyan banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██████╗  █████╗  ██████╗██╗   ██╗ █████╗ ███╗   ██╗ ║
║   ██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗████╗  ██║ ║
║   ██████╔╝██████╔╝███████║██║  ███╗╚████╔╝ ███████║██╔██╗ ██║ ║
║   ██╔═══╝ ██╔══██╗██╔══██║██║   ██║ ╚██╔╝  ██╔══██║██║╚██╗██║ ║
║   ██║     ██║  ██║██║  ██║╚██████╔╝  ██║   ██║  ██║██║ ╚████║ ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ║
║                                                               ║
║        AI-Powered DSA Solver with Video Explanations          ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def get_language_choice() -> ProgrammingLanguage:
    """Interactive language selection"""
    languages = [
        ("1", "Python", ProgrammingLanguage.PYTHON),
        ("2", "Java", ProgrammingLanguage.JAVA),
        ("3", "C++", ProgrammingLanguage.CPP),
        ("4", "C", ProgrammingLanguage.C),
        ("5", "JavaScript", ProgrammingLanguage.JAVASCRIPT),
        ("6", "TypeScript", ProgrammingLanguage.TYPESCRIPT),
        ("7", "Go", ProgrammingLanguage.GO),
        ("8", "Rust", ProgrammingLanguage.RUST),
        ("9", "Kotlin", ProgrammingLanguage.KOTLIN),
        ("10", "Swift", ProgrammingLanguage.SWIFT),
        ("11", "C#", ProgrammingLanguage.CSHARP),
    ]
    
    console.print("\n[bold yellow]Select Programming Language:[/bold yellow]\n")
    
    table = Table(show_header=False, box=None)
    table.add_column("", style="cyan")
    table.add_column("", style="white")
    
    for num, name, _ in languages:
        table.add_row(f"  [{num}]", name)
    
    console.print(table)
    
    choice = Prompt.ask("\nEnter your choice", default="1")
    
    for num, name, lang in languages:
        if choice == num or choice.lower() == name.lower():
            return lang
    
    console.print("[yellow]Invalid choice, defaulting to Python[/yellow]")
    return ProgrammingLanguage.PYTHON


def get_api_key() -> tuple:
    """Get API key from user"""
    console.print("\n[bold yellow]API Key Configuration:[/bold yellow]\n")
    console.print("  [1] Gemini API Key (Google AI)")
    console.print("  [2] Groq API Key (Free tier available)")
    
    provider_choice = Prompt.ask("\nSelect provider", choices=["1", "2"], default="1")
    
    if provider_choice == "1":
        provider = "gemini"
        console.print("\n[dim]Get your free Gemini API key at: https://makersuite.google.com/app/apikey[/dim]")
    else:
        provider = "groq"
        console.print("\n[dim]Get your free Groq API key at: https://console.groq.com/keys[/dim]")
    
    api_key = Prompt.ask(f"\nEnter your {provider.upper()} API key", password=True)
    
    if not api_key:
        console.print("[red]API key is required![/red]")
        sys.exit(1)
    
    return provider, api_key


def get_question_input() -> tuple:
    """Get question input from user"""
    console.print("\n[bold yellow]Question Input:[/bold yellow]\n")
    console.print("  [1] Enter a LeetCode/Problem URL")
    console.print("  [2] Type/Paste the problem text")
    
    input_choice = Prompt.ask("\nSelect input method", choices=["1", "2"], default="1")
    
    if input_choice == "1":
        url = Prompt.ask("\nEnter the problem URL")
        return "url", url
    else:
        console.print("\n[dim]Enter the problem description (press Enter twice to finish):[/dim]\n")
        lines = []
        empty_count = 0
        while empty_count < 2:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                else:
                    empty_count = 0
                lines.append(line)
            except EOFError:
                break
        
        text = "\n".join(lines).strip()
        return "text", text


@click.group()
@click.version_option(version="1.0.0", prog_name="Pragyan")
def cli():
    """Pragyan - AI-Powered DSA Question Solver with Video Explanations"""
    pass


@cli.command()
@click.option('--url', '-u', help='URL of the problem (LeetCode, GFG, etc.)')
@click.option('--text', '-t', help='Problem description text')
@click.option('--language', '-l', help='Programming language for solution')
@click.option('--provider', '-p', type=click.Choice(['gemini', 'groq']), help='LLM provider')
@click.option('--api-key', '-k', envvar='PRAGYAN_API_KEY', help='API key for the provider')
@click.option('--no-video', is_flag=True, help='Skip video generation')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for video')
@click.option('--quality', '-q', type=click.Choice(['low', 'medium', 'high']), default='medium', help='Video quality')
def solve(url, text, language, provider, api_key, no_video, output_dir, quality):
    """
    Solve a DSA problem and generate an explanation video
    
    Examples:
        pragyan solve -u https://leetcode.com/problems/two-sum
        pragyan solve -t "Given an array, find two numbers that add up to target"
    """
    print_banner()
    
    # Get inputs interactively if not provided
    if not url and not text:
        input_type, input_value = get_question_input()
        if input_type == "url":
            url = input_value
        else:
            text = input_value
    
    if not language:
        lang = get_language_choice()
    else:
        lang = ProgrammingLanguage.from_string(language)
    
    if not provider or not api_key:
        provider, api_key = get_api_key()
    
    # Configure video
    video_config = VideoConfig(
        video_quality=f"{quality}_quality",
        output_dir=Path(output_dir) if output_dir else Path.home() / "Downloads"
    )
    
    # Initialize Pragyan
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        try:
            # Create Pragyan instance
            task = progress.add_task("Initializing Pragyan...", total=None)
            pragyan = Pragyan(
                provider=provider,
                api_key=api_key,
                video_config=video_config
            )
            progress.update(task, description="[green]✓ Initialized[/green]")
            
            # Process question
            if url:
                progress.update(task, description="Scraping question from URL...")
                question = pragyan.scrape_question(url)
            else:
                progress.update(task, description="Parsing question text...")
                question = pragyan.parse_question(text)
            
            progress.update(task, description=f"[green]✓ Question loaded: {question.title[:50]}...[/green]")
            
            # Analyze
            progress.update(task, description="Analyzing question...")
            analysis = pragyan.analyze(question)
            progress.update(task, description="[green]✓ Analysis complete[/green]")
            
            # Generate solution
            progress.update(task, description=f"Generating {lang.value} solution...")
            solution = pragyan.solve(question, lang, analysis)
            progress.update(task, description="[green]✓ Solution generated[/green]")
            
            # Generate video
            video_path = None
            if not no_video:
                progress.update(task, description="Generating explanation video (this may take a few minutes)...")
                try:
                    video_path = pragyan.generate_video(question, solution, analysis)
                    progress.update(task, description=f"[green]✓ Video saved to: {video_path}[/green]")
                except Exception as e:
                    progress.update(task, description=f"[yellow]⚠ Video generation failed: {e}[/yellow]")
            
            progress.update(task, description="[bold green]✓ Complete![/bold green]")
        
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            sys.exit(1)
    
    # Display results
    console.print("\n")
    
    # Question info
    console.print(Panel(
        f"[bold]{question.title}[/bold]\n\n"
        f"[dim]Difficulty: {question.difficulty or 'Unknown'}[/dim]\n"
        f"[dim]Topics: {', '.join(analysis.get('topics', []))[:100]}[/dim]",
        title="[bold blue]Problem[/bold blue]",
        border_style="blue"
    ))
    
    # Solution
    console.print("\n")
    console.print(Panel(
        Syntax(solution.code, lang.value, theme="monokai", line_numbers=True, word_wrap=True),
        title=f"[bold green]Solution ({lang.value})[/bold green]",
        border_style="green",
        expand=True
    ))
    
    # Explanation
    console.print("\n")
    console.print(Panel(
        f"[bold yellow]Concept:[/bold yellow] {solution.concept}\n\n"
        f"[bold yellow]Approach:[/bold yellow] {solution.approach}\n\n"
        f"[bold yellow]Time Complexity:[/bold yellow] {solution.time_complexity}\n"
        f"[bold yellow]Space Complexity:[/bold yellow] {solution.space_complexity}",
        title="[bold yellow]Explanation[/bold yellow]",
        border_style="yellow"
    ))
    
    # Step by step
    if solution.step_by_step:
        console.print("\n")
        steps_text = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(solution.step_by_step)])
        console.print(Panel(
            steps_text,
            title="[bold purple]Step-by-Step Approach[/bold purple]",
            border_style="purple"
        ))
    
    # Example walkthrough
    if solution.example_walkthrough:
        console.print("\n")
        console.print(Panel(
            solution.example_walkthrough,
            title="[bold cyan]Example Walkthrough[/bold cyan]",
            border_style="cyan"
        ))
    
    # Video info
    if video_path:
        console.print("\n")
        console.print(Panel(
            f"[bold green]Video saved to:[/bold green]\n{video_path}",
            title="[bold magenta]Generated Video[/bold magenta]",
            border_style="magenta"
        ))


@cli.command()
@click.argument('url')
@click.option('--provider', '-p', type=click.Choice(['gemini', 'groq']), required=True)
@click.option('--api-key', '-k', envvar='PRAGYAN_API_KEY', required=True)
def analyze(url, provider, api_key):
    """
    Analyze a DSA problem without generating a solution
    
    Example:
        pragyan analyze https://leetcode.com/problems/two-sum -p gemini -k YOUR_KEY
    """
    print_banner()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing problem...", total=None)
        
        pragyan = Pragyan(provider=provider, api_key=api_key)
        question = pragyan.scrape_question(url)
        analysis = pragyan.analyze(question)
        
        progress.update(task, description="[green]✓ Analysis complete[/green]")
    
    # Display analysis
    console.print("\n")
    console.print(Panel(
        f"[bold]Title:[/bold] {analysis.get('title', question.title)}\n"
        f"[bold]Difficulty:[/bold] {analysis.get('difficulty', 'Unknown')}\n"
        f"[bold]Topics:[/bold] {', '.join(analysis.get('topics', []))}\n"
        f"[bold]Main Concept:[/bold] {analysis.get('main_concept', 'N/A')}\n"
        f"[bold]Approach:[/bold] {analysis.get('approach', 'N/A')}\n"
        f"[bold]Intuition:[/bold] {analysis.get('intuition', 'N/A')}",
        title="[bold blue]Problem Analysis[/bold blue]",
        border_style="blue"
    ))
    
    if analysis.get('edge_cases'):
        console.print("\n")
        edge_cases = "\n".join([f"  • {case}" for case in analysis.get('edge_cases', [])])
        console.print(Panel(
            edge_cases,
            title="[bold yellow]Edge Cases[/bold yellow]",
            border_style="yellow"
        ))


@cli.command()
def interactive():
    """
    Start interactive mode with step-by-step prompts
    """
    print_banner()
    
    console.print("\n[bold cyan]Welcome to Pragyan Interactive Mode![/bold cyan]\n")
    
    # Get all inputs interactively
    input_type, input_value = get_question_input()
    language = get_language_choice()
    provider, api_key = get_api_key()
    
    generate_video = Confirm.ask("\nGenerate explanation video?", default=True)
    
    # Video quality
    quality = "medium"
    if generate_video:
        quality = Prompt.ask(
            "Video quality",
            choices=["low", "medium", "high"],
            default="medium"
        )
    
    # Configure
    video_config = VideoConfig(
        video_quality=f"{quality}_quality",
        output_dir=Path.home() / "Downloads"
    )
    
    # Initialize logger for detailed output
    logger = get_logger(verbose=True)
    logger.start_session()
    
    console.print("\n")
    
    try:
        # Initialize Pragyan
        pragyan = Pragyan(
            provider=provider,
            api_key=api_key,
            video_config=video_config
        )
        
        # Scrape/Parse question
        if input_type == "url":
            logger.log_scraping_start(input_value)
            question = pragyan.scrape_question(input_value)
        else:
            logger.log_info("Parsing provided problem text...")
            question = pragyan.parse_question(input_value)
        
        # Log scraped data
        examples = question.examples if hasattr(question, 'examples') and question.examples else []
        logger.log_scraped_question(
            title=question.title,
            description=question.description[:500] if question.description else "",
            difficulty=question.difficulty,
            examples=examples
        )
        
        # Analyze
        logger.log_analysis_start()
        analysis = pragyan.analyze(question)
        logger.log_analysis_result(analysis)
        
        # Generate solution
        logger.log_solving_start(language.value)
        solution = pragyan.solve(question, language, analysis)
        logger.log_solution_generated(solution)
        
        # Log step by step
        if solution.step_by_step:
            logger.log_step_by_step(solution.step_by_step)
        
        # Log example walkthrough as test case simulation
        if solution.example_walkthrough:
            example_input = "See problem examples"
            example_output = "Computed result"
            if question.examples and len(question.examples) > 0:
                example_input = question.examples[0][:50] if len(question.examples[0]) > 50 else question.examples[0]
            logger.log_test_case_simulation(
                test_input=example_input,
                expected_output=example_output,
                walkthrough=solution.example_walkthrough
            )
        
        # Generate video
        video_path = None
        if generate_video:
            logger.log_video_generation_start()
            try:
                video_path = pragyan.generate_video(question, solution, analysis)
                logger.log_video_complete(str(video_path))
            except Exception as e:
                logger.log_video_error(str(e))
        
        logger.log_completion()
        
    except Exception as e:
        logger.log_error("processing", str(e))
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)
    
    # Display final results
    console.print("\n")
    console.print(Panel(
        Syntax(solution.code, language.value, theme="monokai", line_numbers=True, word_wrap=True),
        title=f"[bold green]Solution ({language.value})[/bold green]",
        border_style="green",
        expand=True
    ))
    
    console.print("\n")
    console.print(Panel(
        f"[bold]Concept:[/bold] {solution.concept}\n\n"
        f"[bold]Approach:[/bold] {solution.approach}\n\n"
        f"[bold]Time:[/bold] {solution.time_complexity}\n"
        f"[bold]Space:[/bold] {solution.space_complexity}",
        title="[bold yellow]Explanation[/bold yellow]",
        border_style="yellow"
    ))
    
    if video_path:
        console.print("\n")
        console.print(f"[bold green]Video saved to:[/bold green] {video_path}")


@cli.command()
def languages():
    """List all supported programming languages"""
    print_banner()
    
    console.print("\n[bold cyan]Supported Programming Languages:[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Language", style="cyan")
    table.add_column("Aliases", style="dim")
    
    langs = [
        ("Python", "python, py"),
        ("Java", "java"),
        ("C++", "cpp, c++"),
        ("C", "c"),
        ("JavaScript", "javascript, js"),
        ("TypeScript", "typescript, ts"),
        ("Go", "go, golang"),
        ("Rust", "rust, rs"),
        ("Kotlin", "kotlin, kt"),
        ("Swift", "swift"),
        ("C#", "csharp, c#, cs"),
    ]
    
    for name, aliases in langs:
        table.add_row(name, aliases)
    
    console.print(table)


@cli.command()
def version():
    """Show version information"""
    from pragyan import __version__
    
    console.print(f"\n[bold cyan]Pragyan[/bold cyan] version [bold]{__version__}[/bold]")
    console.print("[dim]AI-Powered DSA Question Solver with Video Explanations[/dim]\n")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
