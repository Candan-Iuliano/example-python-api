from insert_locations import validate_location
import pytest


@pytest.fixture
def sample_location():
    test = {
    "name": "Boston",
    "latitude": 42.3601,
    "longitude": -71.0589,
    "description": "Capital of Massachusetts"
    }

    return [test]

def test_validate_location(sample_location):
    
    assert sample_location == validate_location(sample_location)

def test_invalid_location(sample_location):
        sample_location[0].pop("latitude")
        assert validate_location(sample_location) == []

def test_invalid_location(sample_location):
        sample_location[0].pop("longtitude")
        assert validate_location(sample_location) == []

def test_invalid_latitude(sample_location):
        sample_location[0]["latitude"] = 100
        assert validate_location(sample_location) == []

def test_invalid_longitude(sample_location):
        sample_location[0]["longitude"] = -200
        assert validate_location(sample_location) == []

def test_invalid_longitude(sample_location):
        sample_location[0]["name"] = ""
        assert validate_location(sample_location) == []

def test_invalid_longitude(sample_location):
        sample_location[0]["longitude"] = "200"
        assert validate_location(sample_location) == []

def test_invalid_longitude(sample_location):
        sample_location[0]["latitude"] = "200"
        assert validate_location(sample_location) == []