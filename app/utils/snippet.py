import re

def generate_snippet(query, document_content, max_length=150):
    """
    Finds the query terms in the document and returns a highlighted snippet.
    Falls back to the beginning of the text if no terms are found.
    """
    if not query or not document_content:
        return document_content[:max_length] + "..." if len(document_content) > max_length else document_content

    # Tokenize query, avoiding small stop words
    query_terms = [re.escape(term) for term in query.split() if len(term) > 2]
    
    if not query_terms:
        return document_content[:max_length] + "..." if len(document_content) > max_length else document_content

    pattern = re.compile(r'(' + '|'.join(query_terms) + r')', re.IGNORECASE)
    
    match = pattern.search(document_content)
    if not match:
        return document_content[:max_length] + "..." if len(document_content) > max_length else document_content
        
    start_pos = max(0, match.start() - 50)
    end_pos = min(len(document_content), match.end() + 100)
    
    snippet = document_content[start_pos:end_pos]
    if start_pos > 0:
        snippet = "..." + snippet
    if end_pos < len(document_content):
        snippet = snippet + "..."
        
    # Highlight
    highlighted = pattern.sub(r'<strong class="highlight">\1</strong>', snippet)
    
    return highlighted
