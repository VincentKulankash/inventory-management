"""Tests for the CLI layer. HTTP calls are mocked. CLI tests mock requests so no server is needed:"""
from unittest.mock import patch, Mock
from io import StringIO

import cli


# view_all 
@patch("cli.requests.get")
def test_view_all_happy_path(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "product_name": "Milk", "brands": "Silk", "price": 4.99, "stock": 10}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    cli.view_all()
    captured = capsys.readouterr()
    assert "Milk" in captured.out
    assert "Silk" in captured.out


# add_item 

@patch("cli.requests.post")
@patch("builtins.input", side_effect=["Test Yogurt", "Chobani", "Cultured milk", "1.99", "8"])
def test_add_item_success(mock_input, mock_post, capsys):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 3}
    mock_post.return_value = mock_response

    cli.add_item()
    captured = capsys.readouterr()
    assert "[OK]" in captured.out
    assert "3" in captured.out


#  view_one 
@patch("cli.requests.get")
@patch("builtins.input", return_value="1")
def test_view_one_found(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1, "product_name": "Milk", "brands": "Silk",
        "ingredients_text": "", "price": 4.99, "stock": 10,
    }
    mock_get.return_value = mock_response

    cli.view_one()
    captured = capsys.readouterr()
    assert "Milk" in captured.out


@patch("cli.requests.get")
@patch("builtins.input", return_value="9999")
def test_view_one_missing(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Item 9999 not found"}
    mock_get.return_value = mock_response

    cli.view_one()
    captured = capsys.readouterr()
    assert "[ERROR]" in captured.out