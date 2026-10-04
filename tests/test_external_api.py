"""Tests for the OpenFoodFacts integration. Real HTTP calls are mocked."""
from unittest.mock import patch, Mock

from external_api import fetch_by_barcode, fetch_by_name, extract_fields


# fetch_by_barcode 
@patch("external_api.requests.get")
def test_fetch_by_barcode_success(mock_get):
    # Simulate a 200 response with a 'product' key
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Nutella", "brands": "Ferrero"},
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_barcode("3017620422003")
    assert result is not None
    assert result["product_name"] == "Nutella"


@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_barcode("0000000000000")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_barcode_network_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("connection failed")

    result = fetch_by_barcode("123")
    assert result is None


#fetch_by_name

@patch("external_api.requests.get")
def test_fetch_by_name_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {"product_name": "Almond Milk"},
            {"product_name": "Soy Milk"},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_name("milk")
    assert len(result) == 2
    assert result[0]["product_name"] == "Almond Milk"


@patch("external_api.requests.get")
def test_fetch_by_name_empty(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"products": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_by_name("xyzzy")
    assert result == []


#extract_fields 

def test_extract_fields_full():
    raw = {
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil",
    }
    result = extract_fields(raw)
    assert result == {
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil",
    }


def test_extract_fields_missing():
    result = extract_fields({})
    assert result["product_name"] == "Unknown"
    assert result["brands"] == "Unknown"
    assert result["ingredients_text"] == ""