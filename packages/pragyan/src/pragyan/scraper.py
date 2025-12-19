"""
Web scraper module for extracting DSA questions from websites like LeetCode
Uses LangChain for intelligent web scraping
"""

import re
import time
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

from pragyan.models import Question


class QuestionScraper:
    """Scraper for extracting DSA questions from various sources"""
    
    SUPPORTED_SITES = {
        "leetcode.com": "leetcode",
        "www.leetcode.com": "leetcode",
        "hackerrank.com": "hackerrank",
        "www.hackerrank.com": "hackerrank",
        "codeforces.com": "codeforces",
        "www.codeforces.com": "codeforces",
        "geeksforgeeks.org": "gfg",
        "www.geeksforgeeks.org": "gfg",
        "practice.geeksforgeeks.org": "gfg",
    }
    
    def __init__(self):
        """Initialize the scraper"""
        self._driver = None
    
    def _get_driver(self):
        """Get or create Selenium WebDriver"""
        if self._driver is None:
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                
                service = Service(ChromeDriverManager().install())
                self._driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize WebDriver: {e}")
        
        return self._driver
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self._driver:
            self._driver.quit()
            self._driver = None
    
    def scrape_url(self, url: str) -> Question:
        """
        Scrape a question from a URL
        
        Args:
            url: URL of the problem page
            
        Returns:
            Question object with extracted information
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        site_type = self.SUPPORTED_SITES.get(domain)
        
        if site_type == "leetcode":
            return self._scrape_leetcode(url)
        elif site_type == "gfg":
            return self._scrape_gfg(url)
        elif site_type == "hackerrank":
            return self._scrape_hackerrank(url)
        elif site_type == "codeforces":
            return self._scrape_codeforces(url)
        else:
            # Try generic scraping with LangChain
            return self._scrape_generic(url)
    
    def _scrape_leetcode(self, url: str) -> Question:
        """Scrape a LeetCode problem"""
        try:
            from bs4 import BeautifulSoup
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            driver = self._get_driver()
            driver.get(url)
            
            # Wait for the content to load
            time.sleep(3)
            
            # Wait for the problem description to be present
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-track-load='description_content']"))
                )
            except:
                pass
            
            # Get page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract title
            title = ""
            title_elem = soup.find('div', {'data-cy': 'question-title'})
            if not title_elem:
                title_elem = soup.find('a', class_=re.compile(r'.*title.*', re.I))
            if not title_elem:
                # Try to extract from URL
                match = re.search(r'/problems/([^/]+)', url)
                if match:
                    title = match.group(1).replace('-', ' ').title()
            else:
                title = title_elem.get_text(strip=True)
            
            # Extract description
            description = ""
            desc_elem = soup.find('div', {'data-track-load': 'description_content'})
            if not desc_elem:
                desc_elem = soup.find('div', class_=re.compile(r'.*description.*', re.I))
            if desc_elem:
                description = desc_elem.get_text(separator='\n', strip=True)
            
            # Extract difficulty
            difficulty = None
            diff_elem = soup.find('div', class_=re.compile(r'.*(easy|medium|hard).*', re.I))
            if diff_elem:
                text = diff_elem.get_text(strip=True).lower()
                if 'easy' in text:
                    difficulty = 'Easy'
                elif 'medium' in text:
                    difficulty = 'Medium'
                elif 'hard' in text:
                    difficulty = 'Hard'
            
            # Extract examples
            examples = self._extract_examples(description)
            
            # Extract constraints
            constraints = self._extract_constraints(description)
            
            # Extract topics/tags
            topics = []
            topic_elems = soup.find_all('a', href=re.compile(r'/tag/'))
            for elem in topic_elems:
                topics.append(elem.get_text(strip=True))
            
            return Question(
                title=title,
                description=description,
                examples=examples,
                constraints=constraints,
                difficulty=difficulty,
                topics=topics,
                url=url,
                raw_text=description,
            )
            
        except Exception as e:
            # Fallback to LangChain scraping
            return self._scrape_with_langchain(url)
        finally:
            self._close_driver()
    
    def _scrape_gfg(self, url: str) -> Question:
        """Scrape a GeeksforGeeks problem"""
        try:
            from bs4 import BeautifulSoup
            import requests
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # Extract description
            description = ""
            problem_elem = soup.find('div', class_='problems_problem_content__Xm_eO')
            if not problem_elem:
                problem_elem = soup.find('article')
            if problem_elem:
                description = problem_elem.get_text(separator='\n', strip=True)
            
            examples = self._extract_examples(description)
            constraints = self._extract_constraints(description)
            
            return Question(
                title=title,
                description=description,
                examples=examples,
                constraints=constraints,
                url=url,
                raw_text=description,
            )
            
        except Exception as e:
            return self._scrape_with_langchain(url)
    
    def _scrape_hackerrank(self, url: str) -> Question:
        """Scrape a HackerRank problem"""
        return self._scrape_with_langchain(url)
    
    def _scrape_codeforces(self, url: str) -> Question:
        """Scrape a Codeforces problem"""
        try:
            from bs4 import BeautifulSoup
            import requests
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_elem = soup.find('div', class_='title')
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # Extract description
            description = ""
            problem_elem = soup.find('div', class_='problem-statement')
            if problem_elem:
                description = problem_elem.get_text(separator='\n', strip=True)
            
            examples = self._extract_examples(description)
            constraints = self._extract_constraints(description)
            
            return Question(
                title=title,
                description=description,
                examples=examples,
                constraints=constraints,
                url=url,
                raw_text=description,
            )
            
        except Exception as e:
            return self._scrape_with_langchain(url)
    
    def _scrape_generic(self, url: str) -> Question:
        """Generic scraping for unsupported sites"""
        return self._scrape_with_langchain(url)
    
    def _scrape_with_langchain(self, url: str) -> Question:
        """Use LangChain to scrape and understand the page content"""
        try:
            from langchain_community.document_loaders import WebBaseLoader
            
            loader = WebBaseLoader(url)
            documents = loader.load()
            
            if documents:
                content = documents[0].page_content
                
                # Try to extract title from content
                lines = content.split('\n')
                title = lines[0] if lines else "Unknown Problem"
                
                return Question(
                    title=title[:100],  # Limit title length
                    description=content,
                    examples=self._extract_examples(content),
                    constraints=self._extract_constraints(content),
                    url=url,
                    raw_text=content,
                )
            else:
                raise ValueError("No content found")
                
        except ImportError:
            raise ImportError("Please install langchain-community: pip install langchain-community")
        except Exception as e:
            # Last resort: use requests
            return self._scrape_with_requests(url)
    
    def _scrape_with_requests(self, url: str) -> Question:
        """Fallback scraping with requests and BeautifulSoup"""
        try:
            from bs4 import BeautifulSoup
            import requests
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for elem in soup(['script', 'style', 'nav', 'footer', 'header']):
                elem.decompose()
            
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Try to find title
            title = ""
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            return Question(
                title=title or "Problem",
                description=text[:5000],  # Limit description length
                examples=self._extract_examples(text),
                constraints=self._extract_constraints(text),
                url=url,
                raw_text=text,
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to scrape URL: {e}")
    
    def _extract_examples(self, text: str) -> List[Dict[str, Any]]:
        """Extract examples from problem description"""
        examples = []
        
        # Pattern for examples
        example_patterns = [
            r'Example\s*\d*:?\s*\n?\s*Input:?\s*(.+?)\s*Output:?\s*(.+?)(?:Explanation:?\s*(.+?))?(?=Example|\Z|Constraints)',
            r'Input:\s*(.+?)\s*Output:\s*(.+?)(?:Explanation:\s*(.+?))?(?=Input:|$)',
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                example = {
                    'input': match[0].strip() if match[0] else '',
                    'output': match[1].strip() if len(match) > 1 and match[1] else '',
                }
                if len(match) > 2 and match[2]:
                    example['explanation'] = match[2].strip()
                
                if example['input'] and example['output']:
                    examples.append(example)
            
            if examples:
                break
        
        return examples[:3]  # Return at most 3 examples
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract constraints from problem description"""
        constraints = []
        
        # Find constraints section
        constraint_match = re.search(r'Constraints?:?\s*(.+?)(?=Example|Follow|Note:|$)', text, re.DOTALL | re.IGNORECASE)
        
        if constraint_match:
            constraint_text = constraint_match.group(1)
            # Split by newlines or bullet points
            items = re.split(r'[\n•\-\*]', constraint_text)
            for item in items:
                item = item.strip()
                if item and len(item) > 3:
                    constraints.append(item)
        
        return constraints[:10]  # Return at most 10 constraints
    
    def parse_text_question(self, text: str) -> Question:
        """
        Parse a question from plain text input
        
        Args:
            text: Plain text description of the problem
            
        Returns:
            Question object
        """
        lines = text.strip().split('\n')
        
        # First non-empty line is usually the title
        title = ""
        description_start = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                title = line
                description_start = i + 1
                break
        
        # Rest is description
        description = '\n'.join(lines[description_start:]).strip()
        
        # If no clear title, use first sentence
        if not description:
            description = title
            title = title[:50] + "..." if len(title) > 50 else title
        
        return Question(
            title=title,
            description=description,
            examples=self._extract_examples(text),
            constraints=self._extract_constraints(text),
            raw_text=text,
        )
