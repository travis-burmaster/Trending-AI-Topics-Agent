# Trending AI Topics Agent

An automated agent that scrapes and analyzes trending AI projects using LangGraph and Make.com integration. This tool aggregates information from LinkedIn, GitHub, and Google to identify and analyze the top trending AI projects on a weekly basis.

## Features

- Multi-source data collection (LinkedIn, GitHub, Google)
- Automated workflow using LangGraph
- Make.com integration for reliable web scraping
- AI-powered analysis of trending projects
- Weekly automated reports

## Prerequisites

- Python 3.8+
- Make.com account
- API access tokens for:
  - LinkedIn API
  - GitHub API
  - Google Custom Search API
- OpenAI API key for GPT-4 access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/travis-burmaster/Trending-AI-Topics-Agent.git
cd Trending-AI-Topics-Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

## Usage

1. Run the agent:
```bash
python main.py
```

2. For scheduled execution:
```bash
python main.py --schedule weekly
```

3. Customize search parameters:
```bash
python main.py --topics "machine learning, computer vision" --timeframe "2w"
```