import pytest
from flask import Flask
import main

def test_load_and_parse_md():
    # Arrange
    filename = "test.md"
    expected_html = "<h1>Test</h1>\n"
    
    # Act
    result = main.load_and_parse_md(filename)
    
    # Assert
    assert result == expected_html

def test_dynamic_route():
    # Arrange
    filename = "test.md"
    expected_html = "<h1>Test</h1>\n"
    app = Flask(__name__)
    
    # Act
    with app.test_client() as client:
        response = client.get(f'/{filename}')
    
    # Assert
    assert response.data.decode() == expected_html
