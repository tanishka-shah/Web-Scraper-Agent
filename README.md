# Web-Scraper-Agent
The steps behind building this AI Agent would be as following:
1. Defines tools that structure the query, scrape the data, structure the output.
2. Structuring the query will help us understand what the user wants.
3. Design a scraper that handles links, nested pages, and dynamically-loaded content.
4. Design an extraction tool to extract informaation relevant to user's query
5. Design an output structuring tool to json (in the format of query, url, extracted conntent)
6. Using CrewAI, to define agents with the tasks and respective tools
7. The Crew will have: Scraper Agent, Extraction Agent, Output Agent


My progress: I was able to write a script for scraping. 

Challenges: 
1. I am pretty new to Agents and took some time to read and understand how to build them with available tools.
2. The scraping tool requires refinement and testing.
3. I am stuck at installing crewai and could not resolve it (will require some more time)
4. But I've written a demo file - crew_main.py to showcase how the crew can be defined.
   

