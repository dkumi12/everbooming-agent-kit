import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class Context7Client:
    """
    Client for interacting with Context7 Documentation API.
    Fetches up-to-date technical documentation for frameworks and libraries.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CONTEXT7_API_KEY")
        self.base_url = "https://api.context7.com/v1"
        
        if not self.api_key:
            print("⚠️  Warning: Context7 API key not found. Live documentation will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
    
    def search_library(self, library_name: str) -> Dict[str, Any]:
        """
        Search for a library/framework in Context7.
        
        Args:
            library_name: Name of the library (e.g., "react", "nextjs", "fastapi")
            
        Returns:
            Library information including ID and available versions
        """
        if not self.enabled:
            return {"error": "Context7 client not enabled - missing API key"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                json={"query": library_name},
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to search library: {str(e)}"}
    
    def get_documentation(
        self, 
        library_id: str, 
        topic: Optional[str] = None,
        max_tokens: int = 3000
    ) -> Dict[str, Any]:
        """
        Fetch documentation for a specific library.
        
        Args:
            library_id: Context7 library ID (e.g., '/vercel/next.js')
            topic: Optional specific topic to focus on
            max_tokens: Maximum tokens of documentation to retrieve
            
        Returns:
            Documentation content and metadata
        """
        if not self.enabled:
            return {"error": "Context7 client not enabled - missing API key"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "library_id": library_id,
            "max_tokens": max_tokens
        }
        
        if topic:
            payload["topic"] = topic
        
        try:
            response = requests.post(
                f"{self.base_url}/docs",
                json=payload,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch documentation: {str(e)}"}
    
    def get_code_examples(self, library_id: str, query: str) -> Dict[str, Any]:
        """
        Get relevant code examples from documentation.
        
        Args:
            library_id: Context7 library ID
            query: What you're trying to accomplish
            
        Returns:
            Code examples and snippets
        """
        if not self.enabled:
            return {"error": "Context7 client not enabled - missing API key"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/examples",
                json={
                    "library_id": library_id,
                    "query": query
                },
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch code examples: {str(e)}"}


# Convenience function for agent use
def fetch_tech_docs(tech_stack: List[str], context: str = "") -> str:
    """
    Fetch documentation for multiple technologies.
    
    Args:
        tech_stack: List of technology names (e.g., ["react", "fastapi", "postgresql"])
        context: Optional context about what you're building
        
    Returns:
        Formatted documentation string for AI agent consumption
    """
    client = Context7Client()
    
    if not client.enabled:
        return "Context7 documentation unavailable - API key not configured."
    
    docs_output = []
    
    for tech in tech_stack:
        print(f"  📖 Fetching docs for: {tech}")
        
        # Search for library
        search_result = client.search_library(tech)
        
        if "error" in search_result:
            docs_output.append(f"## {tech}\n⚠️  Unavailable: {search_result['error']}\n")
            continue
        
        # Get first matching result
        if search_result.get("results"):
            library = search_result["results"][0]
            library_id = library.get("id")
            
            # Fetch documentation
            docs = client.get_documentation(library_id, topic=context)
            
            if "error" not in docs:
                content = docs.get('content', 'No content available')
                docs_output.append(f"## {tech}\n\n{content}\n")
                print(f"  ✅ Fetched {len(content)} characters for {tech}")
            else:
                docs_output.append(f"## {tech}\n⚠️  Error: {docs['error']}\n")
        else:
            docs_output.append(f"## {tech}\n⚠️  No documentation found\n")
    
    return "\n\n".join(docs_output)


if __name__ == "__main__":
    # Test the client
    print("Testing Context7 Client...")
    test_result = fetch_tech_docs(["react", "fastapi"], "Building a web application")
    print(test_result)
