import json
import plotly.graph_objects as go
from langchain_core.messages import HumanMessage

from db_client import log_usage

def extract_data_for_chart(text: str, llm, user_id: str = None):
    """
    Extracts numerical data from text to create a chart.
    Returns a JSON object with 'title', 'labels', 'values', 'type'.
    """
    prompt = (
        f"Analyze the following text and extract any significant numerical data suitable for a chart (e.g., market share, growth rates, revenue).\n\n"
        f"{text[:4000]}\n\n"
        "Return ONLY a valid JSON object with the following structure:\n"
        "{\n"
        '  "title": "Chart Title",\n'
        '  "labels": ["Label1", "Label2", ...],\n'
        '  "values": [10, 20, ...],\n'
        '  "type": "bar" (or "pie" or "line")\n'
        "}\n"
        "If no suitable data is found, return an empty JSON object: {}"
    )
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        
        # Log Usage
        if user_id:
            usage = response.response_metadata.get('token_usage', {})
            log_usage(user_id, "llama-3.3-70b", usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0))

        content = response.content.strip()
        # Clean up potential markdown code blocks
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"⚠️ Error extracting chart data: {e}")
        return {}

def create_chart(data: dict):
    """
    Generates a Plotly figure from the extracted data.
    """
    if not data or not data.get("values"):
        return None
        
    try:
        fig = go.Figure()
        
        if data.get("type") == "pie":
            fig.add_trace(go.Pie(labels=data["labels"], values=data["values"]))
        elif data.get("type") == "line":
             fig.add_trace(go.Scatter(x=data["labels"], y=data["values"], mode='lines+markers'))
        else: # Default to bar
            fig.add_trace(go.Bar(x=data["labels"], y=data["values"]))
            
        fig.update_layout(
            title=data.get("title", "Data Visualization"),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    except Exception as e:
        print(f"⚠️ Error creating chart: {e}")
        return None
