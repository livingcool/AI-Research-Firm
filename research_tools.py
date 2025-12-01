import requests
import os
import pymupdf4llm
import arxiv

def fetch_and_parse_rich_arxiv(arxiv_id: str, output_dir: str = "paper_content") -> tuple[str, str]:
    # Create specific directory for this paper
    paper_dir = os.path.join(output_dir, arxiv_id)
    os.makedirs(paper_dir, exist_ok=True)
    
    image_path = os.path.join(paper_dir, "images")
    os.makedirs(image_path, exist_ok=True)

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    pdf_path = os.path.join(paper_dir, f"{arxiv_id}.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"⬇️ Downloading paper {arxiv_id}...")
        response = requests.get(pdf_url)
        with open(pdf_path, "wb") as f:
            f.write(response.content)
    
    print("⚡ Parsing PDF layout...")
    md_text = pymupdf4llm.to_markdown(
        pdf_path,
        write_images=True,
        image_path=image_path,
        image_format="png"
    )
    
    # Save a visual copy for you to look at
    with open(os.path.join(paper_dir, f"{arxiv_id}_rich.md"), "w", encoding="utf-8") as f:
        f.write(md_text)
        
    return md_text, image_path

def search_arxiv(topic: str, max_results: int = 5):
    """
    Searches ArXiv for papers related to the topic.
    Returns a list of dictionaries with title, abstract, and id.
    """
    print(f"🔍 Searching ArXiv for: {topic}")
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "abstract": result.summary,
            "id": result.entry_id.split('/')[-1],
            "url": result.pdf_url
        })
    
    return results

def select_best_paper(topic: str, papers: list, llm):
    """
    Uses the LLM to select the most relevant paper from the list.
    """
    print("🤖 Selecting the best paper...")
    
    paper_summaries = "\n\n".join(
        [f"ID: {p['id']}\nTitle: {p['title']}\nAbstract: {p['abstract']}" for p in papers]
    )
    
    prompt = (
        f"I am researching '{topic}'. Here are 5 ArXiv papers:\n\n"
        f"{paper_summaries}\n\n"
        "Which one is the MOST relevant and interesting for this topic? "
        "Return ONLY the ID of the best paper. Nothing else."
    )
    
    response = llm.invoke(prompt)
    best_id = response.content.strip()
    
    # Simple cleanup in case the LLM is chatty
    for p in papers:
        if p['id'] in best_id:
            return p
            
    # Fallback: return the first one
    return papers[0]