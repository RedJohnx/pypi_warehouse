"""
Video Generator module using Manim for creating educational DSA explanation videos
with proper animations, visual data structures, and algorithm visualizations
"""

import os
import re
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from pragyan.models import Question, Solution, VideoConfig, AnimationScene


class VideoGenerator:
    """
    Generates educational videos explaining DSA problems and solutions using Manim
    with proper animations, visual data structures, and algorithm visualizations
    """
    
    def __init__(self, config: Optional[VideoConfig] = None):
        self.config = config or VideoConfig()
        self._temp_dir = None
        self._verify_manim_installation()
    
    def _verify_manim_installation(self):
        """Verify that Manim is properly installed"""
        try:
            import manim
            self.manim_version = manim.__version__
        except ImportError:
            raise ImportError(
                "Manim is not installed. Please install it with: pip install manim\n"
                "You may also need to install additional dependencies. "
                "See: https://docs.manim.community/en/stable/installation.html"
            )
    
    def _get_temp_dir(self) -> Path:
        if self._temp_dir is None:
            self._temp_dir = Path(tempfile.mkdtemp(prefix="pragyan_"))
        return self._temp_dir
    
    def _cleanup_temp_dir(self):
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None
    
    def generate_video(
        self,
        question: Question,
        solution: Solution,
        analysis: Dict[str, Any],
        video_script: List[Dict[str, Any]],
        output_filename: Optional[str] = None
    ) -> Path:
        temp_dir = self._get_temp_dir()
        scene_code = self._generate_animated_scene(question, solution, analysis)
        scene_file = temp_dir / "dsa_explanation.py"
        with open(scene_file, "w", encoding="utf-8") as f:
            f.write(scene_code)
        output_path = self._render_video(scene_file, output_filename)
        return output_path
    
    def _escape_for_python(self, s: str, max_len: int = 500) -> str:
        """Escape string for Python code embedding"""
        if not s:
            return ""
        s = s[:max_len]
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        s = s.replace("'", "\\'")
        s = s.replace('\n', ' ')
        s = s.replace('\r', '')
        s = s.replace('\t', ' ')
        s = ''.join(c for c in s if c.isprintable() or c == ' ')
        return s
    
    def _extract_example_array(self, question: Question) -> str:
        """Try to extract an example array from the question"""
        # Common patterns for arrays in problem examples
        # Handle examples that might be dicts or strings
        examples_text = ""
        if question.examples:
            for ex in question.examples:
                if isinstance(ex, dict):
                    examples_text += " " + str(ex.get("input", "")) + " " + str(ex.get("output", ""))
                elif isinstance(ex, str):
                    examples_text += " " + ex
        
        text = question.description + " " + examples_text
        
        # Look for patterns like [1, 2, 3] or nums = [1, 2, 3]
        patterns = [
            r'\[[\d,\s-]+\]',
            r'nums\s*=\s*\[[\d,\s-]+\]',
            r'arr\s*=\s*\[[\d,\s-]+\]',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                # Extract just the array part
                arr_match = re.search(r'\[([\d,\s-]+)\]', match.group())
                if arr_match:
                    try:
                        arr_str = "[" + arr_match.group(1) + "]"
                        # Validate it's a valid list
                        arr = eval(arr_str)
                        if isinstance(arr, list) and len(arr) >= 2 and len(arr) <= 10:
                            return str(arr)
                    except:
                        pass
        
        # Default example array
        return "[3, 1, 4, 1, 5, 9, 2, 6]"
    
    def _detect_algorithm_type(self, analysis: Dict[str, Any], solution: Solution) -> str:
        """Detect algorithm type for visualization"""
        concept = (solution.concept + " " + solution.approach).lower()
        topics = [t.lower() for t in analysis.get("topics", [])]
        
        if any(x in concept for x in ["two pointer", "two-pointer"]):
            return "two_pointer"
        elif any(x in concept for x in ["sliding window"]):
            return "sliding_window"
        elif any(x in concept for x in ["binary search"]):
            return "binary_search"
        elif any(x in concept for x in ["hash", "dictionary", "map"]):
            return "hash_map"
        elif any(x in concept for x in ["dynamic", "dp", "memoization"]):
            return "dp"
        elif any(x in concept for x in ["stack"]):
            return "stack"
        elif any(x in concept for x in ["queue", "bfs"]):
            return "queue"
        elif any(x in concept for x in ["tree", "dfs"]):
            return "tree"
        elif any(x in concept for x in ["linked list"]):
            return "linked_list"
        elif any(x in concept for x in ["sort"]):
            return "sorting"
        elif any(x in concept for x in ["graph"]):
            return "graph"
        elif "array" in topics or "string" in topics:
            return "array"
        return "array"
    
    def _generate_animated_scene(
        self,
        question: Question,
        solution: Solution,
        analysis: Dict[str, Any]
    ) -> str:
        """Generate Manim scene with proper animations and visualizations"""
        
        title = self._escape_for_python(question.title, 100)
        concept = self._escape_for_python(solution.concept, 200)
        approach = self._escape_for_python(solution.approach, 300)
        time_comp = self._escape_for_python(solution.time_complexity, 50)
        space_comp = self._escape_for_python(solution.space_complexity, 50)
        
        # Get topics
        topics = analysis.get("topics", [])
        topics_str = ", ".join(str(t) for t in topics[:4])
        topics_str = self._escape_for_python(topics_str, 100)
        
        # Get example array
        example_arr = self._extract_example_array(question)
        
        # Detect algorithm type
        algo_type = self._detect_algorithm_type(analysis, solution)
        
        # Generate step-by-step as Python list
        steps = solution.step_by_step[:5] if solution.step_by_step else []
        steps_list = "[" + ", ".join(f'"{self._escape_for_python(str(s), 100)}"' for s in steps) + "]"
        
        # Prepare code lines (first 15 lines only)
        code_lines = solution.code.split('\n')[:15] if solution.code else ["# Solution code"]
        code_for_display = []
        for line in code_lines:
            clean_line = self._escape_for_python(line, 80)
            code_for_display.append(clean_line)
        code_list = "[" + ", ".join(f'"{line}"' for line in code_for_display) + "]"
        
        scene_code = f'''"""
Manim scene for DSA explanation video - Generated by Pragyan
Features: Animated data structures, algorithm visualization, professional graphics
"""

from manim import *
import textwrap

config.pixel_height = {self.config.pixel_height}
config.pixel_width = {self.config.pixel_width}
config.frame_rate = {self.config.fps}
config.background_color = "{self.config.background_color}"


class DSAExplanation(Scene):
    """Professional DSA explanation with visual animations"""
    
    def construct(self):
        # Data
        title = "{title}"
        concept = "{concept}"
        approach = "{approach}"
        time_complexity = "{time_comp}"
        space_complexity = "{space_comp}"
        topics = "{topics_str}"
        example_arr = {example_arr}
        algo_type = "{algo_type}"
        steps = {steps_list}
        code_lines = {code_list}
        
        # Run all scenes
        self.intro_scene(title, topics)
        self.concept_visual_scene(concept, algo_type)
        self.data_structure_scene(example_arr, algo_type)
        self.algorithm_walkthrough_scene(example_arr, algo_type, steps)
        self.code_scene(code_lines)
        self.complexity_visual_scene(time_complexity, space_complexity)
        self.outro_scene(title)
    
    def clear_all(self):
        """Clear all objects with fade"""
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
    
    def intro_scene(self, title: str, topics: str):
        """Animated intro with geometric elements"""
        # Background decoration
        circles = VGroup(*[
            Circle(radius=0.3 + i*0.2, color=BLUE, stroke_opacity=0.3 - i*0.05)
            for i in range(5)
        ]).shift(LEFT*5 + UP*2)
        
        squares = VGroup(*[
            Square(side_length=0.3 + i*0.2, color=GREEN, stroke_opacity=0.3 - i*0.05).rotate(i*PI/8)
            for i in range(5)
        ]).shift(RIGHT*5 + UP*2)
        
        self.play(
            *[Create(c, run_time=0.5) for c in circles],
            *[Create(s, run_time=0.5) for s in squares],
        )
        
        # Title with glow effect
        title_text = Text(title[:50], font_size=42, color=WHITE, weight=BOLD)
        title_text.to_edge(UP, buff=1.2)
        
        # Underline animation
        underline = Line(
            title_text.get_left() + DOWN*0.3,
            title_text.get_right() + DOWN*0.3,
            color=BLUE
        )
        
        self.play(Write(title_text), run_time=1.5)
        self.play(Create(underline), run_time=0.5)
        
        # Topics as badges
        if topics:
            topic_list = [t.strip() for t in topics.split(",")][:4]
            badges = VGroup()
            for i, topic in enumerate(topic_list):
                badge = VGroup(
                    RoundedRectangle(
                        width=len(topic)*0.15 + 0.6,
                        height=0.5,
                        corner_radius=0.2,
                        fill_color=BLUE_E,
                        fill_opacity=0.8,
                        stroke_color=BLUE
                    ),
                    Text(topic, font_size=18, color=WHITE)
                )
                badge[1].move_to(badge[0])
                badges.add(badge)
            
            badges.arrange(RIGHT, buff=0.3)
            badges.next_to(title_text, DOWN, buff=0.8)
            
            self.play(
                *[FadeIn(b, shift=UP*0.3) for b in badges],
                run_time=1
            )
        
        # DSA icon
        dsa_icon = self.create_dsa_icon().scale(0.8).shift(DOWN*1.5)
        self.play(GrowFromCenter(dsa_icon), run_time=1)
        
        self.wait(1.5)
        self.clear_all()
    
    def create_dsa_icon(self):
        """Create an animated DSA-themed icon"""
        # Tree structure
        nodes = VGroup()
        edges = VGroup()
        
        root = Circle(radius=0.25, color=GOLD, fill_opacity=0.8)
        left = Circle(radius=0.2, color=BLUE, fill_opacity=0.8).shift(LEFT*0.8 + DOWN*0.7)
        right = Circle(radius=0.2, color=GREEN, fill_opacity=0.8).shift(RIGHT*0.8 + DOWN*0.7)
        
        edge1 = Line(root.get_center(), left.get_center(), color=WHITE)
        edge2 = Line(root.get_center(), right.get_center(), color=WHITE)
        
        nodes.add(root, left, right)
        edges.add(edge1, edge2)
        
        return VGroup(edges, nodes)
    
    def concept_visual_scene(self, concept: str, algo_type: str):
        """Visual representation of the concept"""
        header = Text("Core Concept", font_size=36, color=ORANGE, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)
        
        # Concept in a styled box
        concept_short = concept[:100] + "..." if len(concept) > 100 else concept
        wrapped = "\\n".join(textwrap.wrap(concept_short, 40))
        
        concept_box = VGroup(
            RoundedRectangle(
                width=9, height=2.5,
                corner_radius=0.3,
                fill_color="#1a1a2e",
                fill_opacity=0.9,
                stroke_color=ORANGE,
                stroke_width=2
            ),
            Text(wrapped, font_size=22, color=WHITE)
        )
        concept_box[1].move_to(concept_box[0])
        concept_box.next_to(header, DOWN, buff=0.6)
        
        self.play(
            FadeIn(concept_box[0], scale=0.9),
            Write(concept_box[1]),
            run_time=1.5
        )
        
        # Algorithm type icon
        algo_visual = self.create_algo_icon(algo_type)
        algo_visual.scale(0.7).shift(DOWN*1.5)
        self.play(GrowFromCenter(algo_visual), run_time=1)
        
        self.wait(2)
        self.clear_all()
    
    def create_algo_icon(self, algo_type: str):
        """Create visual icon based on algorithm type"""
        if algo_type == "two_pointer":
            # Two arrows pointing at array
            arr = VGroup(*[
                Square(side_length=0.4, color=WHITE).shift(RIGHT*i*0.5)
                for i in range(5)
            ]).center()
            left_arrow = Arrow(arr[0].get_bottom() + DOWN*0.5, arr[0].get_bottom(), color=BLUE, buff=0.05)
            right_arrow = Arrow(arr[-1].get_bottom() + DOWN*0.5, arr[-1].get_bottom(), color=RED, buff=0.05)
            return VGroup(arr, left_arrow, right_arrow)
        
        elif algo_type == "sliding_window":
            arr = VGroup(*[
                Square(side_length=0.4, color=WHITE).shift(RIGHT*i*0.5)
                for i in range(6)
            ]).center()
            window = SurroundingRectangle(VGroup(arr[1], arr[2], arr[3]), color=YELLOW, buff=0.05)
            return VGroup(arr, window)
        
        elif algo_type == "binary_search":
            arr = VGroup(*[
                Square(side_length=0.4, color=WHITE).shift(RIGHT*i*0.5)
                for i in range(7)
            ]).center()
            mid_highlight = arr[3].copy().set_fill(GREEN, opacity=0.5)
            return VGroup(arr, mid_highlight)
        
        elif algo_type == "hash_map":
            boxes = VGroup()
            for i in range(4):
                box = Rectangle(width=1.5, height=0.4, color=TEAL).shift(DOWN*i*0.5)
                label = Text(f"key{i}", font_size=14, color=WHITE).move_to(box)
                boxes.add(VGroup(box, label))
            return boxes.center()
        
        elif algo_type == "stack":
            boxes = VGroup(*[
                Rectangle(width=1, height=0.4, color=PURPLE).shift(DOWN*i*0.5)
                for i in range(4)
            ]).center()
            return boxes
        
        elif algo_type == "dp":
            grid = VGroup()
            for i in range(3):
                for j in range(4):
                    cell = Square(side_length=0.4, color=GOLD).shift(RIGHT*j*0.45 + DOWN*i*0.45)
                    grid.add(cell)
            return grid.center()
        
        else:  # Default: array
            arr = VGroup(*[
                Square(side_length=0.5, color=BLUE).shift(RIGHT*i*0.55)
                for i in range(5)
            ]).center()
            return arr
    
    def data_structure_scene(self, arr: list, algo_type: str):
        """Visualize the data structure"""
        header = Text("Data Structure Visualization", font_size=32, color=GREEN, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)
        
        # Create array visualization
        array_viz = self.create_array_visualization(arr[:8])  # Limit to 8 elements
        array_viz.scale(0.9).next_to(header, DOWN, buff=1)
        
        self.play(
            *[GrowFromCenter(box) for box in array_viz[0]],
            run_time=1
        )
        self.play(
            *[Write(val) for val in array_viz[1]],
            run_time=0.8
        )
        self.play(
            *[FadeIn(idx) for idx in array_viz[2]],
            run_time=0.5
        )
        
        # Show array properties
        props = VGroup(
            Text(f"Length: {{len(arr)}}", font_size=20, color=YELLOW),
            Text(f"Type: Integer Array", font_size=20, color=YELLOW),
        ).arrange(RIGHT, buff=1).shift(DOWN*2)
        
        self.play(FadeIn(props), run_time=0.5)
        
        self.wait(2)
        self.clear_all()
    
    def create_array_visualization(self, arr: list):
        """Create a visual array with boxes, values, and indices"""
        boxes = VGroup()
        values = VGroup()
        indices = VGroup()
        
        n = len(arr)
        box_size = min(0.8, 6.0 / n)  # Scale boxes based on array size
        
        for i, val in enumerate(arr):
            # Box
            box = Square(
                side_length=box_size,
                color=BLUE,
                fill_opacity=0.2,
                stroke_width=2
            ).shift(RIGHT * i * (box_size + 0.1))
            boxes.add(box)
            
            # Value
            value = Text(str(val), font_size=int(20 * box_size), color=WHITE)
            value.move_to(box.get_center())
            values.add(value)
            
            # Index
            idx = Text(str(i), font_size=int(14 * box_size), color=GRAY)
            idx.next_to(box, DOWN, buff=0.15)
            indices.add(idx)
        
        group = VGroup(boxes, values, indices)
        group.center()
        return group
    
    def algorithm_walkthrough_scene(self, arr: list, algo_type: str, steps: list):
        """Animate the algorithm execution"""
        header = Text("Algorithm Walkthrough", font_size=32, color=PURPLE, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)
        
        arr = arr[:8]  # Limit array size
        
        if algo_type == "two_pointer":
            self.animate_two_pointer(arr, header)
        elif algo_type == "sliding_window":
            self.animate_sliding_window(arr, header)
        elif algo_type == "binary_search":
            self.animate_binary_search(sorted(arr), header)
        else:
            self.animate_generic_iteration(arr, header, steps)
        
        self.clear_all()
    
    def animate_two_pointer(self, arr: list, header):
        """Animate two-pointer technique"""
        array_viz = self.create_array_visualization(arr)
        array_viz.scale(0.8).next_to(header, DOWN, buff=0.8)
        
        boxes, values, indices = array_viz
        
        self.play(FadeIn(array_viz), run_time=0.8)
        
        # Create pointers
        left_ptr = Arrow(
            boxes[0].get_bottom() + DOWN*0.5,
            boxes[0].get_bottom(),
            color=BLUE, buff=0.05
        )
        right_ptr = Arrow(
            boxes[-1].get_bottom() + DOWN*0.5,
            boxes[-1].get_bottom(),
            color=RED, buff=0.05
        )
        
        left_label = Text("L", font_size=20, color=BLUE).next_to(left_ptr, DOWN, buff=0.1)
        right_label = Text("R", font_size=20, color=RED).next_to(right_ptr, DOWN, buff=0.1)
        
        self.play(
            GrowArrow(left_ptr), GrowArrow(right_ptr),
            Write(left_label), Write(right_label),
            run_time=0.8
        )
        
        # Animate pointer movement
        left_idx, right_idx = 0, len(arr) - 1
        
        for _ in range(min(3, len(arr)//2)):
            if left_idx >= right_idx:
                break
            
            # Highlight current elements
            self.play(
                boxes[left_idx].animate.set_fill(BLUE, opacity=0.5),
                boxes[right_idx].animate.set_fill(RED, opacity=0.5),
                run_time=0.5
            )
            
            self.wait(0.5)
            
            # Move pointers
            left_idx += 1
            right_idx -= 1
            
            if left_idx < right_idx:
                self.play(
                    left_ptr.animate.next_to(boxes[left_idx], DOWN, buff=0.05).shift(DOWN*0.5),
                    right_ptr.animate.next_to(boxes[right_idx], DOWN, buff=0.05).shift(DOWN*0.5),
                    run_time=0.5
                )
                left_label.next_to(left_ptr, DOWN, buff=0.1)
                right_label.next_to(right_ptr, DOWN, buff=0.1)
        
        # Success indicator
        check = Text("Pointers Met!", font_size=28, color=GREEN).shift(DOWN*2.5)
        self.play(Write(check), run_time=0.5)
        self.wait(1)
    
    def animate_sliding_window(self, arr: list, header):
        """Animate sliding window technique"""
        array_viz = self.create_array_visualization(arr)
        array_viz.scale(0.8).next_to(header, DOWN, buff=0.8)
        
        boxes, values, indices = array_viz
        
        self.play(FadeIn(array_viz), run_time=0.8)
        
        k = min(3, len(arr) - 1)  # Window size
        
        # Create window
        window = SurroundingRectangle(
            VGroup(*boxes[:k]),
            color=YELLOW,
            buff=0.05,
            stroke_width=3
        )
        window_label = Text(f"Window (k={{k}})", font_size=20, color=YELLOW)
        window_label.next_to(window, UP, buff=0.2)
        
        self.play(Create(window), Write(window_label), run_time=0.8)
        
        # Slide the window
        for i in range(min(len(arr) - k, 4)):
            if i > 0:
                new_window = SurroundingRectangle(
                    VGroup(*boxes[i:i+k]),
                    color=YELLOW,
                    buff=0.05,
                    stroke_width=3
                )
                self.play(
                    Transform(window, new_window),
                    window_label.animate.next_to(new_window, UP, buff=0.2),
                    run_time=0.5
                )
            
            # Highlight window elements
            self.play(
                *[boxes[j].animate.set_fill(YELLOW, opacity=0.3) for j in range(i, i+k)],
                run_time=0.3
            )
            self.wait(0.3)
            self.play(
                *[boxes[j].animate.set_fill(BLUE, opacity=0.2) for j in range(i, i+k)],
                run_time=0.2
            )
        
        self.wait(1)
    
    def animate_binary_search(self, arr: list, header):
        """Animate binary search"""
        arr = sorted(arr)
        array_viz = self.create_array_visualization(arr)
        array_viz.scale(0.8).next_to(header, DOWN, buff=0.8)
        
        boxes, values, indices = array_viz
        
        self.play(FadeIn(array_viz), run_time=0.8)
        
        # Show sorted indicator
        sorted_label = Text("Sorted Array", font_size=18, color=GREEN).next_to(array_viz, LEFT, buff=0.5)
        self.play(Write(sorted_label), run_time=0.3)
        
        left, right = 0, len(arr) - 1
        
        for _ in range(min(3, len(arr))):
            if left > right:
                break
            
            mid = (left + right) // 2
            
            # Highlight search range
            self.play(
                *[boxes[i].animate.set_fill(BLUE, opacity=0.3) for i in range(left, right+1)],
                run_time=0.3
            )
            
            # Highlight mid
            self.play(
                boxes[mid].animate.set_fill(GREEN, opacity=0.7),
                run_time=0.5
            )
            
            mid_label = Text("mid", font_size=16, color=GREEN).next_to(boxes[mid], UP, buff=0.2)
            self.play(Write(mid_label), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(mid_label), run_time=0.2)
            
            # Simulate moving left or right
            if mid > 0:
                left = mid + 1
            else:
                break
        
        self.wait(1)
    
    def animate_generic_iteration(self, arr: list, header, steps: list):
        """Generic iteration animation for other algorithms"""
        array_viz = self.create_array_visualization(arr)
        array_viz.scale(0.8).next_to(header, DOWN, buff=0.8)
        
        boxes, values, indices = array_viz
        
        self.play(FadeIn(array_viz), run_time=0.8)
        
        # Current pointer
        pointer = Arrow(
            boxes[0].get_top() + UP*0.5,
            boxes[0].get_top(),
            color=GREEN, buff=0.05
        )
        
        self.play(GrowArrow(pointer), run_time=0.5)
        
        # Iterate through array
        for i in range(min(len(arr), 5)):
            if i > 0:
                self.play(
                    pointer.animate.next_to(boxes[i], UP, buff=0.05).shift(UP*0.5),
                    run_time=0.3
                )
            
            self.play(
                boxes[i].animate.set_fill(GREEN, opacity=0.5),
                run_time=0.3
            )
            self.wait(0.2)
        
        # Show a step if available
        if steps:
            step_text = Text(
                steps[0][:60] + "..." if len(steps[0]) > 60 else steps[0],
                font_size=20,
                color=YELLOW
            ).shift(DOWN*2.5)
            self.play(Write(step_text), run_time=0.8)
        
        self.wait(1)
    
    def code_scene(self, code_lines: list):
        """Display code with animation"""
        header = Text("Solution Code", font_size=32, color=GREEN, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)
        
        # Create code display
        code_group = VGroup()
        
        for i, line in enumerate(code_lines[:12]):  # Limit lines
            # Line number
            line_num = Text(f"{{i+1:2d}}", font_size=14, color=GRAY)
            line_num.align_to(LEFT*6, LEFT)
            line_num.shift(DOWN * i * 0.35)
            
            # Code text
            code_text = Text(line[:60], font_size=14, color=WHITE, font="Monospace")
            code_text.next_to(line_num, RIGHT, buff=0.3)
            
            code_group.add(VGroup(line_num, code_text))
        
        code_group.center().shift(DOWN*0.5)
        
        # Background
        code_bg = RoundedRectangle(
            width=12, height=len(code_lines[:12]) * 0.35 + 0.6,
            corner_radius=0.2,
            fill_color="#1e1e1e",
            fill_opacity=0.95,
            stroke_color=GREEN,
            stroke_width=1
        ).move_to(code_group.get_center())
        
        self.play(FadeIn(code_bg), run_time=0.3)
        
        # Animate code lines appearing
        for line_group in code_group:
            self.play(Write(line_group), run_time=0.15)
        
        # Highlight effect
        highlight = SurroundingRectangle(code_bg, color=YELLOW, buff=0.1)
        self.play(Create(highlight), run_time=0.3)
        self.play(FadeOut(highlight), run_time=0.3)
        
        self.wait(2)
        self.clear_all()
    
    def complexity_visual_scene(self, time_comp: str, space_comp: str):
        """Visual complexity analysis with graphs"""
        header = Text("Complexity Analysis", font_size=32, color=RED, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.5)
        
        # Create complexity boxes with icons
        # Time complexity
        time_box = VGroup(
            RoundedRectangle(
                width=4.5, height=2.5,
                corner_radius=0.2,
                fill_color="#1a1a2e",
                fill_opacity=0.9,
                stroke_color=BLUE,
                stroke_width=2
            ),
            Text("Time", font_size=24, color=BLUE, weight=BOLD),
            Text(time_comp[:30], font_size=20, color=WHITE),
        )
        time_box[1].move_to(time_box[0].get_top() + DOWN*0.4)
        time_box[2].move_to(time_box[0].get_center() + DOWN*0.2)
        
        # Add a simple complexity curve
        time_curve = self.create_complexity_curve(time_comp).scale(0.4)
        time_curve.move_to(time_box[0].get_center() + DOWN*0.7)
        time_box.add(time_curve)
        time_box.shift(LEFT*3)
        
        # Space complexity
        space_box = VGroup(
            RoundedRectangle(
                width=4.5, height=2.5,
                corner_radius=0.2,
                fill_color="#1a1a2e",
                fill_opacity=0.9,
                stroke_color=GREEN,
                stroke_width=2
            ),
            Text("Space", font_size=24, color=GREEN, weight=BOLD),
            Text(space_comp[:30], font_size=20, color=WHITE),
        )
        space_box[1].move_to(space_box[0].get_top() + DOWN*0.4)
        space_box[2].move_to(space_box[0].get_center() + DOWN*0.2)
        
        space_curve = self.create_complexity_curve(space_comp).scale(0.4)
        space_curve.move_to(space_box[0].get_center() + DOWN*0.7)
        space_box.add(space_curve)
        space_box.shift(RIGHT*3)
        
        self.play(
            FadeIn(time_box, shift=RIGHT),
            FadeIn(space_box, shift=LEFT),
            run_time=1
        )
        
        self.wait(2)
        self.clear_all()
    
    def create_complexity_curve(self, complexity: str):
        """Create a visual curve representing complexity"""
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=2,
            axis_config={{"color": GRAY, "stroke_width": 1}}
        )
        
        complexity_lower = complexity.lower()
        
        if "1)" in complexity_lower or "constant" in complexity_lower:
            curve = axes.plot(lambda x: 1, color=GREEN)
        elif "log" in complexity_lower:
            curve = axes.plot(lambda x: 0.5 + 0.8*np.log(x + 1), color=BLUE)
        elif "n)" in complexity_lower and "n^2" not in complexity_lower and "n*" not in complexity_lower:
            curve = axes.plot(lambda x: x, color=YELLOW)
        elif "n log" in complexity_lower or "nlog" in complexity_lower:
            curve = axes.plot(lambda x: x * (0.3 + 0.2*np.log(x + 1)), color=ORANGE)
        elif "n^2" in complexity_lower or "n*n" in complexity_lower:
            curve = axes.plot(lambda x: 0.2 * x**2, color=RED)
        else:
            curve = axes.plot(lambda x: x, color=YELLOW)
        
        return VGroup(axes, curve)
    
    def outro_scene(self, title: str):
        """Professional outro"""
        # Animated circles
        circles = VGroup(*[
            Circle(radius=0.5 + i*0.3, color=GOLD, stroke_opacity=0.5 - i*0.1)
            for i in range(4)
        ])
        
        self.play(
            *[Create(c) for c in circles],
            run_time=1
        )
        
        # Success message
        success = Text("Solution Complete!", font_size=42, color=GOLD, weight=BOLD)
        success.shift(UP*0.5)
        
        self.play(
            circles.animate.scale(2).set_opacity(0),
            Write(success),
            run_time=1
        )
        
        # Problem title
        prob_title = Text(title[:40], font_size=24, color=WHITE)
        prob_title.next_to(success, DOWN, buff=0.5)
        self.play(FadeIn(prob_title), run_time=0.5)
        
        # Branding
        branding = Text("Generated by Pragyan", font_size=18, color=GRAY)
        branding.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(branding), run_time=0.3)
        
        self.wait(2)
        self.clear_all()
'''
        
        return scene_code
    
    def _render_video(self, scene_file: Path, output_filename: Optional[str] = None) -> Path:
        """Render the Manim scene to video"""
        quality_map = {
            "low_quality": "-ql",
            "medium_quality": "-qm",
            "high_quality": "-qh",
            "production_quality": "-qp",
        }
        quality_flag = quality_map.get(self.config.video_quality, "-qm")
        
        cmd = [
            "manim",
            quality_flag,
            str(scene_file),
            "DSAExplanation",
            "--media_dir", str(self._get_temp_dir() / "media"),
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(scene_file.parent),
                timeout=300
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                raise RuntimeError(f"Manim rendering failed: {error_msg}")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Video rendering timed out after 5 minutes")
        except FileNotFoundError:
            raise RuntimeError("Manim command not found. Make sure Manim is installed and in PATH.")
        
        media_dir = self._get_temp_dir() / "media" / "videos"
        video_files = list(media_dir.rglob("*.mp4"))
        
        if not video_files:
            raise RuntimeError("No video file was generated")
        
        rendered_video = max(video_files, key=lambda p: p.stat().st_mtime)
        
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"pragyan_dsa_solution_{timestamp}.mp4"
        
        output_path = self.config.output_dir / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rendered_video, output_path)
        self._cleanup_temp_dir()
        
        return output_path
    
    def generate_quick_preview(
        self,
        question: Question,
        solution: Solution,
        duration: int = 30
    ) -> Path:
        """Generate a quick preview video"""
        original_quality = self.config.video_quality
        self.config.video_quality = "low_quality"
        
        try:
            analysis = {"topics": [], "main_concept": solution.concept}
            return self.generate_video(
                question, solution, analysis, [],
                output_filename="preview.mp4"
            )
        finally:
            self.config.video_quality = original_quality


class SimpleVideoGenerator:
    """Fallback video generator using MoviePy"""
    
    def __init__(self, config: Optional[VideoConfig] = None):
        self.config = config or VideoConfig()
    
    def generate_slideshow(
        self,
        question: Question,
        solution: Solution,
        analysis: Dict[str, Any]
    ) -> Path:
        try:
            from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
        except ImportError:
            raise ImportError("MoviePy not installed. Install with: pip install moviepy")
        
        clips = []
        duration = 5
        bg_color = tuple(int(self.config.background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        for title, content in [
            (question.title, "DSA Problem Solution"),
            ("Concept", solution.concept),
            ("Approach", solution.approach[:300]),
            ("Complexity", f"Time: {solution.time_complexity}\\nSpace: {solution.space_complexity}"),
        ]:
            bg = ColorClip(
                size=(self.config.pixel_width, self.config.pixel_height),
                color=bg_color, duration=duration
            )
            title_clip = TextClip(
                title, fontsize=60, color='white', font='Arial-Bold',
                method='caption', size=(self.config.pixel_width - 100, None)
            ).set_position(('center', 100)).set_duration(duration)
            content_clip = TextClip(
                content, fontsize=36, color='lightgray', font='Arial',
                method='caption', size=(self.config.pixel_width - 150, None)
            ).set_position(('center', 'center')).set_duration(duration)
            clips.append(CompositeVideoClip([bg, title_clip, content_clip]))
        
        final_video = concatenate_videoclips(clips, method="compose")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.config.output_dir / f"pragyan_solution_{timestamp}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_video.write_videofile(str(output_path), fps=self.config.fps, codec="libx264", audio=False, verbose=False, logger=None)
        
        return output_path
