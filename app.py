import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
data_student = pandas.read_csv('student_habits_performance.csv')


avg_study_hours_by_age = data_student.groupby('age')[
    'study_hours_per_day'
    ].mean().reset_index()

job_counts = data_student['part_time_job'].value_counts().reset_index()
job_counts.columns = ['part_time_job', 'count']
job_counts['part_time_job'] = job_counts['part_time_job'].replace({
    'No': 'Студент не работает в свободное время', 'Yes': 'Студент работает в свободное время'
})

data_student['age_category'] = data_student['age'].apply(
    lambda x: 'Совершеннолетний' if int(x) >= 18 else 'Несовершеннолетний'
)
age_category_counts = data_student['age_category'].value_counts().reset_index()
age_category_counts.columns = ['age_category', 'count']

avg_study_mental_health_rating = data_student.groupby('age')['mental_health_rating'].mean().reset_index()
avg_study_exam_score = data_student['exam_score'].mean()
avg_study_attendance_percentage = data_student['attendance_percentage'].mean()

age_sort = data_student['age'].value_counts().reset_index()
age_sort.columns = ['age', 'count']

gender_sort = data_student['gender'].value_counts().reset_index()
gender_sort.columns = ['gender', 'count']

sort_parental_education_level = data_student["parental_education_level"].unique()
sort_parental_education_level = [level for level in sort_parental_education_level if isinstance(level, str)]

min_age = data_student['age'].min()
max_age = data_student['age'].max()


def filtered_data(min_age_input, max_age_input):
    return data_student[
        (data_student['age'] >= min_age_input) &
        (data_student['age'] <= max_age_input)
    ]


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


pie_graph_job_counts = px.pie(
    job_counts,
    values='count',
    names='part_time_job',
    title='Распределение студентов по наличию работы',
    hole=0.3,
    labels={"count": "количество"},
    hover_data={"part_time_job": False}
)

pie_graph_age_category_counts = px.pie(
    age_category_counts,
    values='count',
    names='age_category',
    title='Распределение студентов по совершенно летию',
    hole=0.3,
    labels={"count": "количество"},
    hover_data={"age_category": False}
)

pie_graph_gender_sort = px.pie(
    gender_sort,
    values='count',
    names='gender',
    title='Распределение студентов по полу',
    hole=0.3,
    labels={"count": "количество"},
    hover_data={"gender": False},
    color_discrete_sequence=["#4e73df", "#1cc88a", "#36b9cc"],
)

linear_graph_avg_study_mental_health_rating = px.line(
    avg_study_mental_health_rating,
    x="age",
    y="mental_health_rating",
    title="Среднее значение ментального здоровья по возрастам",
    labels={
        "study_hours_per_day": "Среднее значение ментального здоровья",
        "mental_health_rating": "Ментальное здоровье в баллах в среднем",
        "age": "Возраст"
    }
)

linear_graph_avg_study_mental_health_rating.update_traces(
    line_shape='spline',
    line=dict(width=3),
    mode='lines'
)

linear_graph_avg_study_mental_health_rating.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.8)'),
    plot_bgcolor='white',
    hovermode='x unified'
)


scatter_graph_social_media_hours_netflix_hours = px.scatter(
    data_student,
    x='social_media_hours',
    y='netflix_hours',
    color='age',
    title='Количество часов просмотра социальных сетей и Netflix',
    labels={
        "netflix_hours": "часы просмотра нетфликс",
        "social_media_hours": "часы прибывания в соц-сетях",
    },
)

make_subplots_graf = make_subplots(
        rows=2, cols=1,
        specs=[
            [{"type": "scatter"}],
            [{"type": "table"}]
        ],
        vertical_spacing=0.1,
        subplot_titles=("График зависимости", "Таблица данных"),
    )

make_subplots_graf.add_trace(
    go.Scatter(
        x=filtered_data(min_age, max_age)['social_media_hours'],
        y=filtered_data(min_age, max_age)['netflix_hours'],
        mode='markers',
        marker=dict(
            color=filtered_data(min_age, max_age)['age'],
            colorscale='Viridis',
            showscale=True
        ),
        text=filtered_data(min_age, max_age)['age'],
        name='Студенты'
    ),
    row=1, col=1,
)

make_subplots_graf.add_trace(
    go.Table(
            header=dict(
                values=[
                    "id",
                    "age",
                    "gender",
                    "part time job",
                    "social media hours",
                    "netflix hours",
                    "mental health rating",
                    "exam score",
                    "attendance percentage",
                    "sleep hours",
                    "study hours per day"
                    ],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[filtered_data(min_age, max_age).head(50)[k].tolist()
                        for k in filtered_data(min_age, max_age).head(50).columns
                        ],
                align="left"
            )
        ),
    row=2, col=1,
)

make_subplots_graf.update_layout(
    height=800,
    title_text=f'Данные студентов (возраст {min_age}-{max_age})',
    xaxis_title="Часы в социальных сетях",
    yaxis_title="Часы просмотра Netflix"
)

card1 = dbc.Card(
    dbc.CardBody([
        html.H1([html.I(className="bi bi-person-fill me-2"), "Кол. студентов"]),
        html.H3(data_student["attendance_percentage"].count()),
    ],),
    className="text-center m-4 bg-primary text-white",
)

card2 = dbc.Card(
    dbc.CardBody([
        html.H1([html.I(className="bi bi-bar-chart me-2"), "Средний бал студ."]),
        html.H3(avg_study_exam_score),
    ],),
    className="text-center m-4 bg-primary text-white",
)

card3 = dbc.Card(
    dbc.CardBody([
        html.H1([html.I(className="bi bi-building-check"), "Средний посещ. студ."]),
        html.H3(avg_study_attendance_percentage),
    ],),
    className="text-center m-4 bg-primary text-white",
)

age_filter = html.Div([
    html.Label('Фильтр по возрасту:'),
    dcc.RangeSlider(
        id='age-slider',
        min=min_age,
        max=max_age,
        value=[min_age, max_age],  
        marks={i: str(i) for i in range(int(min_age), int(max_age)+1)},
        step=1
    )
])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output(
        "page-content",
        "children",
        ),
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            html.H1("Добро пожаловать на главную страницу"),
            html.P(
                "Этот сайт создан для того, чтобы вы могли "
                "просмотреть и проанализировать данные о студентах"
                ),
            html.Div([
                html.Label('Фильтр по уровню образования родителей:'),
                dcc.Dropdown(
                    id='education-filter',
                    options=[
                        {'label': 'Все', 'value': 'all'},
                        *[{'label': level, 'value': level} for level in sort_parental_education_level]
                    ],
                    value='all',
                    clearable=False
                ),
                html.Button("Скачать отфильтрованные данные (.xlsx)", 
                            id="btn-download-education-filtered", 
                            className="btn btn-primary mt-2"),
                dcc.Download(id="download-education-filtered-xlsx")
            ], style={'marginBottom': '20px'}),
            html.Div([
                html.Button("Скачать все данные (.xlsx)", id="btn-download-all", className="btn btn-success"),
                dcc.Download(id="download-all-xlsx")
            ], style={'marginBottom': '20px'}),
            html.Div(
                id='dynamic-cards-container',
                children=[card1, card2, card3],
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'gap': '10px',
                    'marginBottom': '20px',
                    'justifyContent': 'space-between',
                }
            ),

            html.Div(
                id='dynamic-chart-container',
                children=[
                    dcc.Graph(
                        id="pie_graph_gender_sort",
                        figure=pie_graph_gender_sort,
                    ),
                ],
                style={
                    'width': '100%',
                    'marginTop': '20px',
                }
            ),
        ])
    elif pathname == "/page-1":
        return html.Div(children=[
            dcc.Graph(
                id='example-graph1',
                figure=linear_graph_avg_study_hours_by_age,
            ),
            dcc.Graph(
                id='example-graph4',
                figure=linear_graph_avg_study_mental_health_rating,
            ),
        ])
    elif pathname == "/page-2":
        return html.Div(children=[
            dcc.Graph(
                id='example-graph2',
                figure=pie_graph_job_counts,
            ),
            dcc.Graph(
                id='example-graph3',
                figure=pie_graph_age_category_counts,
            ),
        ])
    elif pathname == "/page-3":
        return html.Div([
            html.Label('Фильтр по возрасту:'),
            dcc.RangeSlider(
                id='age-slider',
                min=min_age,
                max=max_age,
                value=[min_age, max_age],
                marks={i: str(i) for i in range(int(min_age), int(max_age)+1)},
                step=1
            ),
            dcc.Graph(
                id='example-graph5',
                figure=make_subplots_graf,
            ),
            html.Div([
                html.Button("Скачать данные (.xlsx)", id="btn-download-filtered", className="btn btn-primary mt-3"),
                dcc.Download(id="download-filtered-xlsx")
            ], style={'marginTop': '20px'})
        ])
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    [Output('dynamic-cards-container', 'children'),
     Output('dynamic-chart-container', 'children')],
    [Input('education-filter', 'value')]
)
def update_home_content(education_level):
    if education_level == 'all':
        filtered_df = data_student
    else:
        filtered_df = data_student[data_student['parental_education_level'] == education_level]
    student_count = len(filtered_df)
    avg_exam_score = round(filtered_df['exam_score'].mean(), 2)
    avg_attendance = round(filtered_df['attendance_percentage'].mean(), 2)
    updated_card1 = dbc.Card(
        dbc.CardBody([
            html.H1([html.I(className="bi bi-person-fill me-2"), "Кол. студентов"]),
            html.H3(student_count),
        ],),
        className="text-center m-4 bg-primary text-white",
    )
    updated_card2 = dbc.Card(
        dbc.CardBody([
            html.H1([html.I(className="bi bi-bar-chart me-2"), "Средний бал студ."]),
            html.H3(avg_exam_score),
        ],),
        className="text-center m-4 bg-success text-white",
    )
    updated_card3 = dbc.Card(
        dbc.CardBody([
            html.H1([html.I(className="bi bi-building-check"), "Средний посещ. студ."]),
            html.H3(avg_attendance),
        ],),
        className="text-center m-4 bg-info text-white",
    )
    gender_counts = filtered_df['gender'].value_counts().reset_index()
    gender_counts.columns = ['gender', 'count']
    gender_mapping = {"Female": "Женский", "Male": "Мужской", "Other": "Другой"}
    gender_counts['gender'] = gender_counts['gender'].map(lambda x: gender_mapping.get(x, x))
    title = 'Распределение по полу'
    if education_level != 'all':
        title += f" (образование родителей: {education_level})"
    updated_pie_chart = px.pie(
        gender_counts,
        values='count',
        names='gender',
        title=title,
        color_discrete_sequence=["#4e73df", "#1cc88a", "#36b9cc"],
    )
    updated_cards = [updated_card1, updated_card2, updated_card3]
    updated_chart = dcc.Graph(
        id="pie_graph_gender_sort",
        figure=updated_pie_chart
    )
    return updated_cards, [updated_chart]


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
            marker=dict(
                color=filtered_data_update['age'],
                colorscale='Viridis',
                showscale=True
            ),
            text=filtered_data_update['age'],
            name='Студенты'
        ),
        row=1, col=1,
    )

    make_subplots_graf_updated.add_trace(
        go.Table(
            header=dict(
                values=list(filtered_data_update.columns),
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[
                    filtered_data_update.head(50)[k].tolist() for k in filtered_data_update.head(50).columns
                    ],
                align="left"
            )
        ),
        row=2, col=1,
    )

    make_subplots_graf_updated.update_layout(
        height=800,
        title_text=f'Данные студентов (возраст {age_range[0]}-{age_range[1]})',
        xaxis_title="Часы в социальных сетях",
        yaxis_title="Часы просмотра Netflix"
    )

    return make_subplots_graf_updated


@app.callback(
    Output("download-filtered-xlsx", "data"),
    Input("btn-download-filtered", "n_clicks"),
    State("age-slider", "value"),
    prevent_initial_call=True
)
def download_filtered_data(n_clicks, age_range):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    filtered_df = filtered_data(age_range[0], age_range[1])

    return dcc.send_data_frame(
        filtered_df.to_excel, 
        f"students_age_{age_range[0]}_to_{age_range[1]}.xlsx",
        sheet_name="Students",
        index=False
    )


@app.callback(
    Output("download-all-xlsx", "data"),
    Input("btn-download-all", "n_clicks"),
    prevent_initial_call=True
)
def download_all_data(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    return dcc.send_data_frame(
        data_student.to_excel,
        "all_students_data.xlsx",
        sheet_name="Students",
        index=False
    )


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


if __name__ == "__main__":
    app.run(debug=True)
