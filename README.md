##### Обзор проекта
Анализ данных студента - это сайт с визуальными диаграммами по студентам, с возможностью интерактивного взаимодействия и скачивания как всех данных так и отобранных данных

1. Python - используется как основной язык программирования 
2. Dash — это Python-фреймворк с открытым исходным кодом используемый в этом проекте, предназначенный для создания веб-приложений для визуализации данных

### Структура проекта

Этот проект имеет следующую структуру:

- `bank_project/` (Корневая директория проекта) 
	- `.venv/` (Виртуальное окружение Python)
	- `pytest/` (Директория с тестами pytest) 
		- `conftest.py` (Файл конфигурации pytest) 
		- `test.py` (Файл с тестовыми функциями) 
	- `app.py` (Основной файл приложения Python) 
	- `requirements.txt` (Файл со списком зависимостей проекта) 
	- `student_habits_performance.csv` (CSV файл с данными о студентах)
#### `app.py` - основной файл проекта

Создание Dash приложения

```
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])  
app.config.suppress_callback_exceptions = True
```

Получение и обработка данных csv с помощью библиотеки pandas

```
data_student = pandas.read_csv('student_habits_performance.csv')  

avg_study_hours_by_age = data_student.groupby('age')[  
    'study_hours_per_day'  
    ].mean().reset_index()  

job_counts = data_student['part_time_job'].value_counts().reset_index()  
job_counts.columns = ['part_time_job', 'count']  
job_counts['part_time_job'] = job_counts['part_time_job'].replace({  
    'No': 'Студент не работает в свободное время', 'Yes': 'Студент работает в свободное время'  
})
```

Функция для фильтрации по возрасту для графиков

```
def filtered_data(min_age_input, max_age_input):  
    return data_student[  
        (data_student['age'] >= min_age_input) &  
        (data_student['age'] <= max_age_input)  
    ]
```

Отрисовка графиков с помощью plotly

```
linear_graph_avg_study_hours_by_age = px.line(  
    avg_study_hours_by_age,  
    x="age",  
    y="study_hours_per_day",  
    title="Среднее количество часов учебы по возрастам",  
    labels={"study_hours_per_day": "Среднее кол-во часов учебы", "age": "Возраст"}  
)  
  
linear_graph_avg_study_hours_by_age.update_traces(  
    line_shape='spline',  
    line=dict(width=3),  
    mode='lines',  
)  
  
linear_graph_avg_study_hours_by_age.update_layout(  
    xaxis=dict(showgrid=False),  
    yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),  
    plot_bgcolor='white',  
    hovermode='x unified',  
)
```

Сайт панель сайта

```
sidebar = html.Div(  
    [  
        html.H2("Sidebar", className="display-4"),  
        html.Hr(),  
        dbc.Nav(  
            [  
                dbc.NavLink("Главная страница", href="/", active="exact"),  
                dbc.NavLink("Линейные диаграммы", href="/page-1", active="exact"),  
                dbc.NavLink("Круговые диаграммы", href="/page-2", active="exact"),  
                dbc.NavLink("Динамические диаграммы", href="/page-3", active="exact"),  
            ],  
            vertical=True,  
            pills=True,  
        ),  
    ],  
    style=SIDEBAR_STYLE,  
)
```

Обновление графика через callback сайта

```
@app.callback(  
    Output('example-graph5', 'figure'),  
    [Input('age-slider', 'value')]  
)  
def update_graph_by_age(age_range):  
    filtered_data_update = filtered_data(age_range[0], age_range[1])  
    make_subplots_graf_updated = make_subplots(  
        rows=2, cols=1,  
        specs=[  
            [{"type": "scatter"}],  
            [{"type": "table"}]  
        ],  
        vertical_spacing=0.1,  
        subplot_titles=("График зависимости", "Таблица данных"),  
    )  
  
    make_subplots_graf_updated.add_trace(  
        go.Scatter(  
            x=filtered_data_update['social_media_hours'],  
            y=filtered_data_update['netflix_hours'],  
            mode='markers',
			...
```

Скачивание данных в формате .xlsx

```
@app.callback(  
    Output("download-education-filtered-xlsx", "data"),  
    Input("btn-download-education-filtered", "n_clicks"),  
    State("education-filter", "value"),  
    prevent_initial_call=True  
)  
def download_education_filtered_data(n_clicks, education_level):  
    if n_clicks is None:  
        raise dash.exceptions.PreventUpdate  
  
    if education_level == 'all':  
        filtered_df = data_student  
        filename = "all_students_data.xlsx"  
    else:  
        filtered_df = data_student[data_student['parental_education_level'] == education_level]  
        safe_filename = str(education_level).replace(" ", "_").replace("/", "_")  
        filename = f"students_education_{safe_filename}.xlsx"  
  
    return dcc.send_data_frame(  
        filtered_df.to_excel,  
        filename,  
        sheet_name="Students",  
        index=False  
    )
```

**Основные функции:**
 - Запуск сайта
 - Работа с данными через csv файл
 - Отрисовка и компоновка графиков
 - Обновление интерактивные графики
 - Скачивание данных через .xlsx


#### Pytest - файл с тестами

##### `conftest.py` - директории файл конфигурации pytest и подготовкой данных для тестов

Один из примеров фикстуры которую можно применить по несколько раз для разных тестов
```
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
```

##### `test.py` - файл со всеми тестами

Один из примеров теста, где проверяться валидность всех сгенерированных данных через фикстуру, под данные студентов

```
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
```

**Основные функции:**
 - Авто тесты проверяют минимальную работоспособность проекта

### Запуск проекта на своем устройстве
1. Проект разрабатывался на python версии 3.13 и рекомендуется использовать её
2. Установите виртуальное окружение python
```
python3.13 -m venv .venv
```
3. Клонируйте проект с репозитории
```
git clone https://github.com/Provod228/student_diogram.git
```
4. Активируйте виртуальное окружение и скачайте все зависимости c requirements.txt
```
pip install -r requirements.txt
```
5. Запустите сам проект через консоль
```
python app.py
```
6. Для запуска самих тестов нужно перейти в папку с тестами и запустить следующую команду
```
cd pytest
pytest test.py
```

### **Минимальные требования к приложению были решены**
1. **Структура проекта**  
- ✅Основной файл приложения app.py написан на Python. 
- ✅Файл со списком зависимостей requirements.txt содержится в проекте.  
- ✅Файлы с данными, с Kaggle храниться в проекте формата csv.
    

2. **Пользовательский интерфейс (UI)**  


- ✅**Боковая панель (sidebar panel):** для навигации по разным разделам дашборд.
    
- ✅**Интерактивный график:** 1 график на 'Главная страница', а 2 график в кладке 'Динамические диаграммы ' .
    
- ✅**Интерактивная таблица:** только в кладке 'Динамические диаграммы '.
    
- ✅**Карточка (card):** элемент интерфейса для отображения ключевых статистических расположены на главной странице.
    
- ✅**Кнопка для скачивания данных:** так же находиться на главной странице и в кладке 'Динамические диаграммы', реализован в формате .xlsx с возможностью скачивания фильтрованных данных .
    

3. **Анализ данных**
    

- ✅Представлены, линейные, круговые, текстовые, табличные диаграммы.
    
- ✅Визуализируйте данные по фильтру возраста и образования родителей.
    

4. **Интерактивность и демонстрация 
    
    - ✅Предоставлена возможность фильтровать данные.
        
    - ✅Графики, таблица, карточки меняются динамически по фильтру.
