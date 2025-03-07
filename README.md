# Web-Scraper-Agent
The steps behind building this AI Agent would be as following:
1. Defines tools that structure the query, scrape the data, structure the output.
2. Structuring the query will help us understand what the user wants.
3. Design a scraper that handles links, nested pages, and dynamically-loaded content.
4. Design an extraction tool to extract informaation relevant to user's query.
5. Design an output structuring tool to json (in the format of query, url, extracted conntent).
6. Using CrewAI, to define agents with the tasks and respective tools.
7. The Crew will have: Scraper Agent, Extraction Agent, Output Agent.


My progress: I was able to write a script for scraping. 


Challenges: 
1. I am pretty new to Agents and took some time to read and understand how to build them with available tools.
2. I am stuck at installing crewai and could not resolve it (will require some more time) but I've written a demo file - crew_main.py to showcase how the crew can be defined.
   

To do:
1. Refine and Test the scraping script
2. Add refined prompts for extraction and agents.
3. Write the extraction and output tools 
4. Define all agents with backstory, goal, role, tasks, tools
5. Make the API user friendly
6. Add proper documentation and docstrings
