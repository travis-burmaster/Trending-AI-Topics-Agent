from typing import Dict, Any
import httpx
from datetime import datetime

class MakeComConnector:
    def __init__(self, webhook_urls: Dict[str, str]):
        self.webhook_urls = webhook_urls
        self.client = httpx.AsyncClient()
    
    async def trigger_scenario(self, source: str, params: Dict[str, Any]) -> Dict:
        """Trigger Make.com scenario for specific source"""
        if source not in self.webhook_urls:
            raise ValueError(f"Invalid source: {source}")
            
        webhook_url = self.webhook_urls[source]
        
        payload = {
            "source": source,
            "params": params,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = await self.client.post(webhook_url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Error triggering Make.com scenario: {str(e)}")
    
    async def close(self):
        await self.client.aclose()