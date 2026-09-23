from tavily import TavilyClient

class WebAgent:

    def __init__(self):
        self.client = TavilyClient(api_key="YOUR_API_KEY")

    def search(self, query):

        result = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        return result["results"]