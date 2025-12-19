"""
Advanced animation scenes for DSA visualizations using Manim
This module contains specialized scenes for different data structures and algorithms
"""

from typing import List, Dict, Any, Optional
import json


class AnimationTemplates:
    """
    Templates for common DSA animations
    These generate Manim code for specific algorithm visualizations
    """
    
    @staticmethod
    def array_visualization(arr: List[int], title: str = "Array") -> str:
        """Generate Manim code for array visualization"""
        arr_str = str(arr)
        return f'''
class ArrayScene(Scene):
    def construct(self):
        # Title
        title = Text("{title}", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Create array visualization
        arr = {arr_str}
        boxes = VGroup()
        values = VGroup()
        indices = VGroup()
        
        for i, val in enumerate(arr):
            box = Square(side_length=0.8, color=WHITE)
            box.shift(RIGHT * i * 0.9)
            boxes.add(box)
            
            value = Text(str(val), font_size=24, color=WHITE)
            value.move_to(box.get_center())
            values.add(value)
            
            idx = Text(str(i), font_size=18, color=GRAY)
            idx.next_to(box, DOWN, buff=0.2)
            indices.add(idx)
        
        array_group = VGroup(boxes, values, indices).center()
        
        self.play(Create(boxes), run_time=1)
        self.play(Write(values), run_time=0.8)
        self.play(Write(indices), run_time=0.5)
        self.wait(2)
'''

    @staticmethod
    def two_pointer_animation(arr: List[int]) -> str:
        """Generate Manim code for two-pointer technique visualization"""
        arr_str = str(arr)
        return f'''
class TwoPointerScene(Scene):
    def construct(self):
        # Title
        title = Text("Two Pointer Technique", font_size=36, color=GREEN).to_edge(UP)
        self.play(Write(title))
        
        arr = {arr_str}
        n = len(arr)
        
        # Create array
        boxes = VGroup()
        values = VGroup()
        
        for i, val in enumerate(arr):
            box = Square(side_length=0.7, color=WHITE)
            box.shift(RIGHT * i * 0.8)
            boxes.add(box)
            
            value = Text(str(val), font_size=20, color=WHITE)
            value.move_to(box.get_center())
            values.add(value)
        
        array_group = VGroup(boxes, values).center()
        self.play(Create(boxes), Write(values), run_time=1)
        
        # Create pointers
        left_ptr = Arrow(start=DOWN, end=UP, color=BLUE, buff=0.1).scale(0.5)
        right_ptr = Arrow(start=DOWN, end=UP, color=RED, buff=0.1).scale(0.5)
        
        left_label = Text("L", font_size=20, color=BLUE)
        right_label = Text("R", font_size=20, color=RED)
        
        left_ptr.next_to(boxes[0], DOWN, buff=0.3)
        right_ptr.next_to(boxes[-1], DOWN, buff=0.3)
        left_label.next_to(left_ptr, DOWN, buff=0.1)
        right_label.next_to(right_ptr, DOWN, buff=0.1)
        
        self.play(GrowArrow(left_ptr), GrowArrow(right_ptr))
        self.play(Write(left_label), Write(right_label))
        
        # Animate pointer movement
        left_idx, right_idx = 0, n - 1
        
        while left_idx < right_idx:
            self.wait(0.5)
            
            # Highlight current elements
            self.play(
                boxes[left_idx].animate.set_fill(BLUE, opacity=0.3),
                boxes[right_idx].animate.set_fill(RED, opacity=0.3),
                run_time=0.3
            )
            
            self.wait(0.5)
            
            # Move pointers
            left_idx += 1
            right_idx -= 1
            
            if left_idx < right_idx:
                self.play(
                    left_ptr.animate.next_to(boxes[left_idx], DOWN, buff=0.3),
                    right_ptr.animate.next_to(boxes[right_idx], DOWN, buff=0.3),
                    left_label.animate.next_to(left_ptr, DOWN, buff=0.1).set_opacity(0),
                    right_label.animate.next_to(right_ptr, DOWN, buff=0.1).set_opacity(0),
                    run_time=0.5
                )
                left_label.next_to(left_ptr, DOWN, buff=0.1)
                right_label.next_to(right_ptr, DOWN, buff=0.1)
        
        self.wait(1)
'''

    @staticmethod
    def sliding_window_animation(arr: List[int], k: int) -> str:
        """Generate Manim code for sliding window visualization"""
        arr_str = str(arr)
        return f'''
class SlidingWindowScene(Scene):
    def construct(self):
        # Title
        title = Text("Sliding Window", font_size=36, color=PURPLE).to_edge(UP)
        self.play(Write(title))
        
        arr = {arr_str}
        k = {k}  # Window size
        n = len(arr)
        
        # Create array
        boxes = VGroup()
        values = VGroup()
        
        for i, val in enumerate(arr):
            box = Square(side_length=0.7, color=WHITE)
            box.shift(RIGHT * i * 0.8)
            boxes.add(box)
            
            value = Text(str(val), font_size=20, color=WHITE)
            value.move_to(box.get_center())
            values.add(value)
        
        array_group = VGroup(boxes, values).center()
        self.play(Create(boxes), Write(values), run_time=1)
        
        # Create window rectangle
        window = SurroundingRectangle(
            VGroup(*boxes[:k]),
            color=YELLOW,
            buff=0.1
        )
        window_label = Text("Window", font_size=20, color=YELLOW)
        window_label.next_to(window, UP, buff=0.2)
        
        self.play(Create(window), Write(window_label))
        
        # Slide the window
        for i in range(n - k):
            self.wait(0.5)
            
            new_window = SurroundingRectangle(
                VGroup(*boxes[i+1:i+1+k]),
                color=YELLOW,
                buff=0.1
            )
            
            self.play(
                Transform(window, new_window),
                window_label.animate.next_to(new_window, UP, buff=0.2),
                run_time=0.5
            )
        
        self.wait(1)
'''

    @staticmethod
    def binary_search_animation(arr: List[int], target: int) -> str:
        """Generate Manim code for binary search visualization"""
        arr_str = str(arr)
        return f'''
class BinarySearchScene(Scene):
    def construct(self):
        # Title
        title = Text("Binary Search", font_size=36, color=ORANGE).to_edge(UP)
        self.play(Write(title))
        
        arr = {arr_str}
        target = {target}
        n = len(arr)
        
        # Target display
        target_text = Text(f"Target: {{target}}", font_size=24, color=YELLOW)
        target_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(target_text))
        
        # Create array
        boxes = VGroup()
        values = VGroup()
        
        for i, val in enumerate(arr):
            box = Square(side_length=0.7, color=WHITE)
            box.shift(RIGHT * i * 0.8)
            boxes.add(box)
            
            value = Text(str(val), font_size=20, color=WHITE)
            value.move_to(box.get_center())
            values.add(value)
        
        array_group = VGroup(boxes, values).center().shift(DOWN * 0.5)
        self.play(Create(boxes), Write(values), run_time=1)
        
        # Binary search animation
        left, right = 0, n - 1
        
        # Pointers
        l_ptr = Triangle(color=BLUE).scale(0.2).rotate(PI)
        r_ptr = Triangle(color=RED).scale(0.2).rotate(PI)
        m_ptr = Triangle(color=GREEN).scale(0.2).rotate(PI)
        
        l_ptr.next_to(boxes[left], DOWN, buff=0.3)
        r_ptr.next_to(boxes[right], DOWN, buff=0.3)
        
        self.play(GrowFromCenter(l_ptr), GrowFromCenter(r_ptr))
        
        while left <= right:
            mid = (left + right) // 2
            
            m_ptr.next_to(boxes[mid], DOWN, buff=0.5)
            
            self.play(
                GrowFromCenter(m_ptr) if left == 0 else m_ptr.animate.next_to(boxes[mid], DOWN, buff=0.5),
                boxes[mid].animate.set_fill(GREEN, opacity=0.3),
                run_time=0.5
            )
            
            # Status text
            status = Text(
                f"Checking index {{mid}}: {{arr[mid]}}",
                font_size=20,
                color=GREEN
            ).to_edge(DOWN)
            
            self.play(Write(status), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(status))
            
            if arr[mid] == target:
                # Found
                self.play(
                    boxes[mid].animate.set_fill(GREEN, opacity=0.7),
                    Flash(boxes[mid], color=GREEN),
                    run_time=0.5
                )
                found_text = Text("Found!", font_size=28, color=GREEN).to_edge(DOWN)
                self.play(Write(found_text))
                break
            elif arr[mid] < target:
                left = mid + 1
                self.play(
                    *[boxes[i].animate.set_fill(GRAY, opacity=0.3) for i in range(mid + 1)],
                    l_ptr.animate.next_to(boxes[left] if left < n else boxes[-1], DOWN, buff=0.3),
                    run_time=0.5
                )
            else:
                right = mid - 1
                self.play(
                    *[boxes[i].animate.set_fill(GRAY, opacity=0.3) for i in range(mid, n)],
                    r_ptr.animate.next_to(boxes[right] if right >= 0 else boxes[0], DOWN, buff=0.3),
                    run_time=0.5
                )
        
        self.wait(2)
'''

    @staticmethod
    def hash_map_animation() -> str:
        """Generate Manim code for hash map visualization"""
        return '''
class HashMapScene(Scene):
    def construct(self):
        # Title
        title = Text("Hash Map / Dictionary", font_size=36, color=TEAL).to_edge(UP)
        self.play(Write(title))
        
        # Create hash map buckets
        buckets = VGroup()
        bucket_size = 8
        
        for i in range(bucket_size):
            bucket = Rectangle(width=2, height=0.6, color=BLUE)
            bucket.shift(DOWN * i * 0.7)
            
            idx_label = Text(str(i), font_size=18, color=BLUE)
            idx_label.next_to(bucket, LEFT, buff=0.3)
            
            buckets.add(VGroup(bucket, idx_label))
        
        buckets.center()
        self.play(Create(buckets), run_time=1.5)
        
        # Insert elements
        elements = [("apple", 5), ("banana", 3), ("cherry", 7)]
        
        for key, value in elements:
            hash_val = hash(key) % bucket_size
            
            # Show hash calculation
            hash_text = Text(
                f"hash('{key}') % {bucket_size} = {hash_val}",
                font_size=20,
                color=YELLOW
            ).to_edge(DOWN)
            
            self.play(Write(hash_text))
            self.wait(0.5)
            
            # Insert into bucket
            entry = Text(f"{key}: {value}", font_size=16, color=WHITE)
            entry.move_to(buckets[hash_val][0].get_center())
            
            self.play(
                buckets[hash_val][0].animate.set_fill(TEAL, opacity=0.3),
                Write(entry),
                run_time=0.5
            )
            
            self.play(FadeOut(hash_text))
            self.wait(0.3)
        
        self.wait(2)
'''

    @staticmethod
    def recursion_tree_animation(n: int = 4) -> str:
        """Generate Manim code for recursion tree visualization"""
        return f'''
class RecursionTreeScene(Scene):
    def construct(self):
        # Title
        title = Text("Recursion Tree", font_size=36, color=RED).to_edge(UP)
        self.play(Write(title))
        
        # Create tree for fibonacci
        n = {n}
        
        # Root node
        root = Circle(radius=0.4, color=RED, fill_opacity=0.3)
        root_label = Text(f"fib({n})", font_size=18, color=WHITE)
        root_label.move_to(root.get_center())
        
        root_group = VGroup(root, root_label)
        root_group.to_edge(UP, buff=1.5)
        
        self.play(Create(root), Write(root_label))
        
        # Helper function to create children
        def create_node(val, parent_pos, direction):
            node = Circle(radius=0.35, color=RED, fill_opacity=0.3)
            label = Text(f"fib({{val}})", font_size=14, color=WHITE)
            label.move_to(node.get_center())
            
            offset = LEFT * 1.5 if direction == "left" else RIGHT * 1.5
            node.move_to(parent_pos + DOWN * 1 + offset)
            label.move_to(node.get_center())
            
            line = Line(parent_pos, node.get_center(), color=GRAY)
            
            return VGroup(node, label), line
        
        # Level 1
        left1, line1 = create_node(n-1, root.get_center(), "left")
        right1, line2 = create_node(n-2, root.get_center(), "right")
        
        self.play(Create(line1), Create(line2), run_time=0.5)
        self.play(Create(left1), Create(right1), run_time=0.5)
        
        # Level 2 (left subtree)
        if n - 1 >= 2:
            ll, l_line1 = create_node(n-2, left1[0].get_center(), "left")
            lr, l_line2 = create_node(n-3, left1[0].get_center(), "right")
            self.play(Create(l_line1), Create(l_line2), run_time=0.3)
            self.play(Create(ll), Create(lr), run_time=0.3)
        
        # Level 2 (right subtree)
        if n - 2 >= 2:
            rl, r_line1 = create_node(n-3, right1[0].get_center(), "left")
            rr, r_line2 = create_node(n-4, right1[0].get_center(), "right")
            self.play(Create(r_line1), Create(r_line2), run_time=0.3)
            self.play(Create(rl), Create(rr), run_time=0.3)
        
        self.wait(2)
'''

    @staticmethod
    def dp_table_animation(rows: int = 5, cols: int = 5) -> str:
        """Generate Manim code for DP table visualization"""
        return f'''
class DPTableScene(Scene):
    def construct(self):
        # Title
        title = Text("Dynamic Programming Table", font_size=36, color=GOLD).to_edge(UP)
        self.play(Write(title))
        
        rows, cols = {rows}, {cols}
        
        # Create grid
        grid = VGroup()
        cells = [[None for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                cell = Square(side_length=0.6, color=WHITE)
                cell.shift(RIGHT * j * 0.65 + DOWN * i * 0.65)
                cells[i][j] = cell
                grid.add(cell)
        
        grid.center()
        self.play(Create(grid), run_time=1)
        
        # Fill DP table (example: simple path counting)
        values = [[None for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                if i == 0 or j == 0:
                    val = 1
                else:
                    val = values[i-1][j] + values[i][j-1]
                
                values[i][j] = val
                
                text = Text(str(val), font_size=16, color=YELLOW)
                text.move_to(cells[i][j].get_center())
                
                self.play(
                    cells[i][j].animate.set_fill(GOLD, opacity=0.3),
                    Write(text),
                    run_time=0.15
                )
        
        self.wait(2)
'''

    @staticmethod
    def linked_list_animation() -> str:
        """Generate Manim code for linked list visualization"""
        return '''
class LinkedListScene(Scene):
    def construct(self):
        # Title
        title = Text("Linked List", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Create nodes
        values = [1, 2, 3, 4, 5]
        nodes = VGroup()
        arrows = VGroup()
        
        for i, val in enumerate(values):
            # Node box
            node = VGroup()
            data_box = Square(side_length=0.6, color=BLUE)
            next_box = Square(side_length=0.6, color=GRAY)
            next_box.next_to(data_box, RIGHT, buff=0)
            
            data_text = Text(str(val), font_size=20, color=WHITE)
            data_text.move_to(data_box.get_center())
            
            node.add(data_box, next_box, data_text)
            node.shift(RIGHT * i * 2)
            nodes.add(node)
            
            # Arrow to next node
            if i < len(values) - 1:
                arrow = Arrow(
                    start=next_box.get_right(),
                    end=next_box.get_right() + RIGHT * 0.8,
                    color=WHITE,
                    buff=0.1
                )
                arrows.add(arrow)
        
        # Add NULL at the end
        null_text = Text("NULL", font_size=18, color=RED)
        null_text.next_to(nodes[-1], RIGHT, buff=0.5)
        
        # Center everything
        all_elements = VGroup(nodes, arrows, null_text).center()
        
        # Animate creation
        for i, node in enumerate(nodes):
            self.play(Create(node), run_time=0.3)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.2)
        
        self.play(Write(null_text), run_time=0.3)
        
        # Head pointer
        head_label = Text("head", font_size=18, color=GREEN)
        head_arrow = Arrow(
            start=nodes[0].get_top() + UP * 0.5,
            end=nodes[0].get_top(),
            color=GREEN,
            buff=0.1
        )
        head_label.next_to(head_arrow, UP, buff=0.1)
        
        self.play(GrowArrow(head_arrow), Write(head_label))
        
        self.wait(2)
'''

    @staticmethod
    def stack_queue_animation() -> str:
        """Generate Manim code for stack and queue visualization"""
        return '''
class StackQueueScene(Scene):
    def construct(self):
        # Title
        title = Text("Stack vs Queue", font_size=36, color=PURPLE).to_edge(UP)
        self.play(Write(title))
        
        # Stack (left side)
        stack_title = Text("Stack (LIFO)", font_size=24, color=BLUE)
        stack_title.move_to(LEFT * 3.5 + UP * 2)
        
        stack_boxes = VGroup()
        stack_values = [1, 2, 3]
        
        for i, val in enumerate(stack_values):
            box = Rectangle(width=1.5, height=0.5, color=BLUE)
            box.shift(LEFT * 3.5 + DOWN * i * 0.6)
            
            text = Text(str(val), font_size=18, color=WHITE)
            text.move_to(box.get_center())
            
            stack_boxes.add(VGroup(box, text))
        
        # Queue (right side)
        queue_title = Text("Queue (FIFO)", font_size=24, color=GREEN)
        queue_title.move_to(RIGHT * 3 + UP * 2)
        
        queue_boxes = VGroup()
        queue_values = [1, 2, 3]
        
        for i, val in enumerate(queue_values):
            box = Rectangle(width=0.7, height=1, color=GREEN)
            box.shift(RIGHT * (1.5 + i * 0.8) + DOWN * 0.5)
            
            text = Text(str(val), font_size=18, color=WHITE)
            text.move_to(box.get_center())
            
            queue_boxes.add(VGroup(box, text))
        
        # Animate
        self.play(Write(stack_title), Write(queue_title))
        
        for sbox, qbox in zip(stack_boxes, queue_boxes):
            self.play(Create(sbox), Create(qbox), run_time=0.4)
        
        # Show operations
        # Push to stack
        new_stack = Rectangle(width=1.5, height=0.5, color=YELLOW, fill_opacity=0.3)
        new_stack.move_to(LEFT * 3.5 + UP * 1)
        new_text = Text("4", font_size=18, color=WHITE)
        new_text.move_to(new_stack.get_center())
        
        push_label = Text("push(4)", font_size=18, color=YELLOW)
        push_label.next_to(new_stack, LEFT, buff=0.3)
        
        self.play(Write(push_label))
        self.play(
            new_stack.animate.shift(DOWN * 1),
            new_text.animate.shift(DOWN * 1),
            run_time=0.5
        )
        
        # Enqueue
        new_queue = Rectangle(width=0.7, height=1, color=YELLOW, fill_opacity=0.3)
        new_queue.move_to(RIGHT * 5 + DOWN * 0.5)
        new_q_text = Text("4", font_size=18, color=WHITE)
        new_q_text.move_to(new_queue.get_center())
        
        enqueue_label = Text("enqueue(4)", font_size=18, color=YELLOW)
        enqueue_label.next_to(new_queue, RIGHT, buff=0.3)
        
        self.play(Write(enqueue_label))
        self.play(
            new_queue.animate.shift(LEFT * 0.8),
            new_q_text.animate.shift(LEFT * 0.8),
            run_time=0.5
        )
        
        self.wait(2)
'''


def get_animation_template(algorithm_type: str, **kwargs) -> Optional[str]:
    """
    Get the appropriate animation template for an algorithm
    
    Args:
        algorithm_type: Type of algorithm (e.g., "two_pointer", "binary_search")
        **kwargs: Additional parameters for the template
        
    Returns:
        Manim code string or None if no template found
    """
    templates = AnimationTemplates()
    
    template_map = {
        "array": templates.array_visualization,
        "two_pointer": templates.two_pointer_animation,
        "sliding_window": templates.sliding_window_animation,
        "binary_search": templates.binary_search_animation,
        "hash_map": templates.hash_map_animation,
        "recursion": templates.recursion_tree_animation,
        "dp": templates.dp_table_animation,
        "linked_list": templates.linked_list_animation,
        "stack_queue": templates.stack_queue_animation,
    }
    
    if algorithm_type in template_map:
        return template_map[algorithm_type](**kwargs)
    
    return None


def detect_algorithm_type(concept: str, topics: List[str]) -> str:
    """
    Detect the algorithm type from concept and topics
    
    Args:
        concept: Main concept string
        topics: List of topic tags
        
    Returns:
        Algorithm type string
    """
    concept_lower = concept.lower()
    topics_lower = [t.lower() for t in topics]
    
    # Check for specific patterns
    if "two pointer" in concept_lower or "two-pointer" in concept_lower:
        return "two_pointer"
    
    if "sliding window" in concept_lower:
        return "sliding_window"
    
    if "binary search" in concept_lower or "binary-search" in topics_lower:
        return "binary_search"
    
    if "hash" in concept_lower or "hashmap" in concept_lower or "dictionary" in concept_lower:
        return "hash_map"
    
    if "recursion" in concept_lower or "recursive" in concept_lower:
        return "recursion"
    
    if "dynamic programming" in concept_lower or "dp" in topics_lower:
        return "dp"
    
    if "linked list" in concept_lower:
        return "linked_list"
    
    if "stack" in concept_lower or "queue" in concept_lower:
        return "stack_queue"
    
    # Default to array for most problems
    if any(t in topics_lower for t in ["array", "string"]):
        return "array"
    
    return "array"  # Default
