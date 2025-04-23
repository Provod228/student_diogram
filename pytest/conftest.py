import pytest
import dash
import dash_bootstrap_components as dbc
import random
from dash import html
import requests
import time
import threading
import csv
import pandas
import os


@pytest.fixture(scope='function')
def test_url(request: None) -> str:
    return " http://127.0.0.1:8050"


@pytest.fixture(scope='session')
def test_dash_server() -> str:
    """Запускает Dash-сервер в отдельном потоке для тестирования"""
    app: dash.Dash = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])
    app.config.suppress_callback_exceptions = True
    app.layout = html.Div(children=[
        html.H1("Test App"),
    ])

    def run_server():
        app.run(debug=False, use_reloader=False)

    server_thread: threading.Thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    server_url: str = "http://127.0.0.1:8050/"
    max_attempts: int = 10
    for attempt in range(max_attempts):
        try:
            response: requests.get = requests.get(server_url, timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(0.5)
            if attempt == max_attempts - 1:
                pytest.fail("Не удалось запустить сервер Dash")

    yield server_url


@pytest.fixture(scope='function')
def test_data() -> pandas.read_csv:
    test_data: dict = {
        "test_student_id": [],
        "test_age": [],
        "test_gender": [],
        "test_study_hours_per_day": [],
        "test_social_media_hours": [],
        "test_netflix_hours": [],
        "test_part_time_job": [],
        "test_attendance_percentage": [],
        "test_sleep_hours": [],
        "test_diet_quality": [],
        "test_exercise_frequency": [],
        "test_parental_education_level": [],
        "test_internet_quality": [],
        "test_mental_health_rating": [],
        "test_extracurricular_participation": [],
        "test_exam_score": [],
    }
    random_count_objects: int = random.randint(0, 1002)
    for item in range(random_count_objects):
        test_data["test_student_id"].append(f"student_{item}")
        test_data["test_age"].append(random.randint(16, 25))
        test_data["test_gender"].append(random.choice(["Male", "Female", "Other"]))
        test_data["test_study_hours_per_day"].append(random.randint(0, 100) / 10)
        test_data["test_social_media_hours"].append(random.randint(0, 100) / 10)
        test_data["test_netflix_hours"].append(random.randint(0, 100) / 10)
        test_data["test_part_time_job"].append(random.choice(["Yes", "No"]))
        test_data["test_attendance_percentage"].append(random.randint(0, 1000) / 10)
        test_data["test_sleep_hours"].append(random.randint(0, 100) / 10)
        test_data["test_diet_quality"].append(random.choice(["Fair", "Good", "Poor"]))
        test_data["test_exercise_frequency"].append(random.randint(0, 10))
        test_data["test_parental_education_level"].append(random.choice(["High", "Middle", "Low"]))
        test_data["test_internet_quality"].append(random.choice(["Good", "Average", "Bad"]))
        test_data["test_mental_health_rating"].append(random.randint(0, 10))
        test_data["test_extracurricular_participation"].append(random.choice(["Yes", "No"]))
        test_data["test_exam_score"].append(random.randint(0, 1000) / 10)
    with open("test_file.csv", "a", newline="") as test_file_csv:
        writer: csv.DictWriter = csv.DictWriter(test_file_csv, fieldnames=test_data.keys())
        writer.writeheader()
        for i in range(len(test_data["test_student_id"])):
            row: dict = {k: test_data[k][i] for k in test_data.keys()}
            writer.writerow(row)
    test_data_student: pandas.read_csv = pandas.read_csv('test_file.csv')
    yield test_data_student
    os.remove("test_file.csv")

