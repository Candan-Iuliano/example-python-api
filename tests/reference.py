
import pytest

# Replace this import with the function you're testing
from app.example import validate_location


# 1. FIXTURE: reusable test data
@pytest.fixture
def sample_location():
    return {
        "name": "Boston",
        "latitude": 42.3601,
        "longitude": -71.0589
    }


# 2. BASIC TEST: verify expected output
def test_validate_location(sample_location):
    result = validate_location(sample_location)

    assert result == sample_location


# 3. INVALID INPUT: verify rejected data
def test_missing_name(sample_location):
    sample_location.pop("name")

    result = validate_location(sample_location)

    assert result is None


# 4. PARAMETRIZE: test multiple inputs with one function
@pytest.mark.parametrize(
    "latitude",
    [91, -91, 100, -100]
)
def test_invalid_latitude(sample_location, latitude):
    sample_location["latitude"] = latitude

    result = validate_location(sample_location)

    assert result is None


# 5. EXCEPTIONS: verify expected errors
def test_empty_results():
    results = []

    with pytest.raises(ValueError):
        calculate_average(results)


# 6. TEMPORARY FILE: test file operations
def test_save_and_load(tmp_path):
    file_path = tmp_path / "test.json"

    save_data({"name": "Boston"}, file_path)
    result = load_data(file_path)

    assert result == {"name": "Boston"}


# 7. DATABASE/API TEST: basic structure
def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "running"}
