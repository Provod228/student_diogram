import pytest
import requests
from requests.exceptions import RequestException
import pandas


# Запусекать, только если запущен сервер в ручную
@pytest.mark.parametrize("endpoint", [
    '',
    '/page-1',
    '/page-2',
    '/page-3',
])
def test_endpoints(test_url: str, endpoint: str) -> None:
    url: str = test_url + endpoint
    try:
        response: requests.Response = requests.get(url)
        assert response.status_code == 200
    except RequestException as e:
        assert False, f"Request failed: {e}"


# Можно через фабрику сделать, но это займет много времени
@pytest.mark.parametrize(
    "test_data_key, test_data_type",
    [
        ["test_student_id", str],
        ["test_gender", str],
        ["test_age", int],
        ["test_study_hours_per_day", float],
        ["test_social_media_hours", float],
        ["test_netflix_hours", float],
        ["test_part_time_job", str],
        ["test_attendance_percentage", float],
        ["test_diet_quality", str],
        ["test_exercise_frequency", int],
        ["test_parental_education_level", str],
        ["test_internet_quality", str],
        ["test_mental_health_rating", int],
        ["test_extracurricular_participation", str],
        ["test_exam_score", float],
    ],
)
def test_data_base(test_data: pandas.read_csv, test_data_key: str, test_data_type: type) -> None:
    for item in test_data[test_data_key]:
        assert isinstance(item, test_data_type)


# Проверяет работу сервера
def test_app_start(test_dash_server: str) -> None:
    response: requests.Response = requests.get(test_dash_server)
    assert response.status_code == 200
