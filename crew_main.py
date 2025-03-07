from crewai import Agent, Task, Crew
from langchain.tools import Tool
from Rufus import RufusScraper

scraper_tool = Tool(
    name="Web Scraper",
    func=RufusScraper().scrape,
    description="Scrapes a website for relevant content based on user instructions."
)
# Define AI Agent
scraper_agent = Agent(
    role="Web Crawler",
    goal="Extract relevant content from websites as per user instructions.",
    tools=[scraper_tool],
    verbose=True,
    allow_delegation=False
)

# Define Task for the Agent
scrape_task = Task(
    description="Scrape {url} for {instruction} and return structured data.",
    agent=scraper_agent
)

# Create Crew with AI Agents
crew = Crew(
    agents=[scraper_agent],
    tasks=[scrape_task]
)

# Execute the AI Agent Task
def run_scraper(url, instruction):
    result = crew.kickoff(inputs={"url": url, "instruction": instruction})
    print("Scraped Data:", result)
    return result
