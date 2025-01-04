from typing import Dict, List, Tuple, Any
from langchain.graphs import StateGraph
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import ChatOpenAI
from ..scrapers.linkedin_scraper import LinkedInScraper
from ..scrapers.github_scraper import GitHubScraper
from ..scrapers.google_scraper import GoogleScraper
import json

class AITrendsScraper:
    def __init__(self, make_connector, llm: ChatOpenAI):
        self.make_connector = make_connector
        self.llm = llm
        self.linkedin_scraper = LinkedInScraper(make_connector)
        self.github_scraper = GitHubScraper(make_connector)
        self.google_scraper = GoogleScraper(make_connector)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(name="ai_trends_scraper")
        
        # Define nodes for each source
        workflow.add_node("linkedin_scrape", self._scrape_linkedin)
        workflow.add_node("github_scrape", self._scrape_github)
        workflow.add_node("google_scrape", self._scrape_google)
        workflow.add_node("analyze_results", self._analyze_results)
        
        # Define edges
        workflow.add_edge("linkedin_scrape", "github_scrape")
        workflow.add_edge("github_scrape", "google_scrape")
        workflow.add_edge("google_scrape", "analyze_results")
        
        # Set entry and exit points
        workflow.set_entry_point("linkedin_scrape")
        workflow.set_exit_point("analyze_results")
        
        return workflow

    async def _scrape_linkedin(self, state: Dict) -> Dict:
        results = await self.linkedin_scraper.scrape(state.get('params'))
        state['linkedin_data'] = results
        return state

    async def _scrape_github(self, state: Dict) -> Dict:
        results = await self.github_scraper.scrape(state.get('params'))
        state['github_data'] = results
        return state

    async def _scrape_google(self, state: Dict) -> Dict:
        results = await self.google_scraper.scrape(state.get('params'))
        state['google_data'] = results
        return state

    async def _analyze_results(self, state: Dict) -> Dict:
        combined_data = {
            'linkedin': state['linkedin_data'],
            'github': state['github_data'],
            'google': state['google_data']
        }
        
        analysis_prompt = HumanMessage(content=f"""
        Analyze the following data from different sources and identify the top 5 trending AI projects:
        {json.dumps(combined_data, indent=2)}
        
        Please consider:
        1. Project popularity and engagement metrics
        2. Innovation and technical significance
        3. Cross-platform presence
        4. Recent updates and activity
        
        Format the results as a JSON list with project details.
        """)
        
        response = await self.llm.ainvoke([analysis_prompt])
        state['analyzed_trends'] = json.loads(response.content)
        return state