import re
import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import os

class RufusScraper:
    def __init__(self, llm_model="gpt-3.5-turbo", max_depth=2, max_scrolls=5):
        self.visited_urls = set()
        self.max_depth = max_depth
        self.max_scrolls = max_scrolls  # Max scroll attempts
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0, openai_api_key=os.getenv('OPENAI_KEY'))

    def get_relevant_text(self, text, user_prompt):
        """ Uses LLM to filter relevant content based on user instructions. """
        prompt = PromptTemplate(
            input_variables=["text", "instruction"],
            template="""
            Extract only the most relevant data from the following webpage text:
            {text}

            The user is interested in: {instruction}

            Only return important details; remove irrelevant text.
            """
        )
        refined_text = self.llm.predict(prompt.format(text=text, instruction=user_prompt))
        return refined_text

    def extract_links(self, page_content, base_url):
        """ Extracts and resolves absolute links from the page. """
        soup = BeautifulSoup(page_content, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            full_url = urljoin(base_url, link["href"])
            if self.is_valid_url(full_url, base_url):
                links.add(full_url)
        return links

    def is_valid_url(self, url, base_url):
        """ Checks if URL is valid and belongs to the same domain. """
        return url.startswith(base_url) and url not in self.visited_urls

    def scroll_page(self, page):
        """ Scrolls the page down to load more content (for infinite scrolling). """
        last_height = 0
        for _ in range(self.max_scrolls):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # Allow time for content to load

            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                print("No more content loaded. Stopping scroll.")
                break
            last_height = new_height
            print("Scrolled to bottom, loading more content...")

    def scrape_page(self, page, url, user_prompt):
        """ Scrapes content from a single page, including infinite scroll handling. """
        try:
            page.goto(url, timeout=15000)
            page.wait_for_selector("body", timeout=5000)

            # Handle infinite scrolling
            self.scroll_page(page)

            soup = BeautifulSoup(page.content(), "html.parser")
            raw_text = soup.get_text(separator="\n", strip=True)

            # Use LLM to filter relevant content
            refined_text = self.get_relevant_text(raw_text, user_prompt)

            return refined_text, self.extract_links(page.content(), url)

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return "", set()

    def crawl(self, page, url, user_prompt, depth=0):
        """ Recursively crawls the website, following links up to max_depth. """
        if depth > self.max_depth or url in self.visited_urls:
            return

        print(f"[Crawling] Depth {depth}: {url}")
        self.visited_urls.add(url)

        content, links = self.scrape_page(page, url, user_prompt)

        if content:
            print(f"[Extracted Content from {url}]:\n{content}...\n")  # Truncated output

        for link in links:
            self.crawl(page, link, user_prompt, depth + 1)

    def run(self, start_url, user_prompt):
        """ Launches the scraper using Playwright. """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print(f"\nStarting Rufus AI Web Scraper on: {start_url}")
            self.crawl(page, start_url, user_prompt)

            browser.close()
            print("\nScraping Complete!")



# if __name__ == "__main__":
#     start_url = input("Enter the website URL: ").strip()
#     user_prompt = input("What specific information should be extracted? ").strip()

#     scraper = RufusScraper(max_depth=5, max_scrolls=10)
#     scraper.run(start_url, user_prompt)
