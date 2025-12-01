import os
from duckduckgo_search import DDGS
import newspaper
from langchain_core.messages import HumanMessage
import time
from db_client import log_usage

def search_market(topic: str, max_results: int = 5):
    """
    Searches DuckDuckGo for market news related to the topic.
    Includes retry logic and fallback to text search.
    """
    print(f"🔍 Searching Market News for: {topic}")
    results = []
    
    # Try 'news' backend first
    try:
        with DDGS() as ddgs:
            ddgs_gen = ddgs.news(topic, max_results=max_results)
            for r in ddgs_gen:
                results.append({
                    "title": r['title'],
                    "url": r['url'],
                    "source": r['source'],
                    "date": r['date']
                })
    except Exception as e:
        print(f"⚠️ News search failed: {e}. Retrying with text search...")
        time.sleep(2) # Wait a bit before retrying
        
        # Fallback to 'text' backend
        try:
            with DDGS() as ddgs:
                ddgs_gen = ddgs.text(topic, max_results=max_results)
                for r in ddgs_gen:
                    results.append({
                        "title": r['title'],
                        "url": r['href'],
                        "source": "Web Search", # Text search doesn't always have source
                        "date": "Recent" # Text search doesn't always have date
                    })
        except Exception as e2:
             print(f"❌ Market search completely failed: {e2}")
             
    return results

def get_article_content(url: str):
    """
    Downloads and parses the article content using newspaper3k.
    """
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        return {
            "text": article.text,
            "authors": article.authors,
            "publish_date": str(article.publish_date),
            "top_image": article.top_image
        }
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return None

def generate_market_report(topic: str, articles: list, llm, user_id: str = None):
    """
    Generates a strategic market report based on the fetched articles.
    """
    print("📊 Generating Market Report...")
    
    # Prepare context
    context = ""
    for i, art in enumerate(articles):
        content = get_article_content(art['url'])
        if content:
            context += f"\n--- Article {i+1}: {art['title']} ---\n"
            context += f"Source: {art['source']}\n"
            context += f"Content: {content['text'][:2000]}...\n" # Truncate to avoid token limits
    
    if not context:
        return "No valid articles found to generate a report."

    prompt = (
        f"You are a Senior Market Analyst. Analyze the following news articles about '{topic}'.\n\n"
        f"{context}\n\n"
        "Create a comprehensive Market Intelligence Report with the following sections:\n"
        "1. **Executive Summary**: High-level overview of the current situation.\n"
        "2. **Key Trends**: What are the emerging patterns?\n"
        "3. **Competitor Landscape**: Who are the key players mentioned?\n"
        "4. **SWOT Analysis**: Create a table of Strengths, Weaknesses, Opportunities, and Threats.\n"
        "5. **Strategic Outlook**: What should be the next steps?\n\n"
        "Format the output in clean Markdown."
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Log Usage
    if user_id:
        usage = response.response_metadata.get('token_usage', {})
        log_usage(user_id, "llama-3.3-70b", usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0))
        
    return response.content
