import argparse
import asyncio
from typing import Dict, List, Any
from utils.make_connector import MakeComConnector
from analysis.trend_analyzer import AITrendsScraper
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

def parse_args():
    parser = argparse.ArgumentParser(description='AI Trends Scraper')
    parser.add_argument('--schedule', choices=['daily', 'weekly'], help='Run schedule')
    parser.add_argument('--topics', type=str, help='Comma-separated topics to search')
    parser.add_argument('--timeframe', type=str, help='Timeframe for search (e.g., 1w, 2w)')
    return parser.parse_args()

async def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_args()
    
    # Initialize components
    make_connector = MakeComConnector(
        webhook_urls={
            'linkedin': os.getenv('LINKEDIN_WEBHOOK_URL'),
            'github': os.getenv('GITHUB_WEBHOOK_URL'),
            'google': os.getenv('GOOGLE_WEBHOOK_URL')
        }
    )
    
    llm = ChatOpenAI(
        model='gpt-4',
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Create scraper instance
    scraper = AITrendsScraper(make_connector=make_connector, llm=llm)
    
    # Run the workflow
    initial_state = {
        'topics': args.topics.split(',') if args.topics else None,
        'timeframe': args.timeframe
    }
    
    final_state = await scraper.graph.arun(initial_state)
    
    # Print results
    print('\nTop 5 Trending AI Projects:')
    for idx, project in enumerate(final_state['analyzed_trends'], 1):
        print(f"\n{idx}. {project['name']}")
        print(f"Description: {project['description']}")
        print(f"Source(s): {', '.join(project['sources'])}")
        print(f"Metrics: {project['engagement_metrics']}")

if __name__ == '__main__':
    asyncio.run(main())