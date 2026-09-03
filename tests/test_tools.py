import pytest
from unittest.mock import patch, MagicMock
from app.tools.web_search import DuckDuckGoProvider

def test_duckduckgo_provider_success():
    provider = DuckDuckGoProvider()
    
    mock_results = [
        {"title": "Test Title", "href": "https://test.com", "body": "Test Snippet"},
        {"title": "Missing Href", "body": "Snippet 2"},
    ]
    
    # Mock DDGS text
    with patch("app.tools.web_search.DDGS") as mock_ddgs:
        mock_instance = MagicMock()
        mock_instance.text.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        
        results = provider.search("test query", max_results=2)
        
        assert len(results) == 2
        assert results[0]["title"] == "Test Title"
        assert results[0]["url"] == "https://test.com"
        assert results[0]["snippet"] == "Test Snippet"
        assert results[0]["source"] == "DuckDuckGo"
        
        assert results[1]["title"] == "Missing Href"
        assert results[1]["url"] == ""

def test_duckduckgo_provider_error():
    provider = DuckDuckGoProvider()
    
    with patch("app.tools.web_search.DDGS") as mock_ddgs:
        mock_instance = MagicMock()
        mock_instance.text.side_effect = Exception("API rate limit")
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        
        with pytest.raises(RuntimeError, match="Web search failed: API rate limit"):
            provider.search("test query")
