from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com',
        'rel': 'preconnect',
    },
    {
        'href': 'https://fonts.gstatic.com',
        'rel': 'preconnect',
        'crossorigin': 'crossorigin'
    },
    "https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap",
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("./merged.csv")
df.country = pd.Series(df.country, dtype='string')
df = df.loc[~(df['country'] == "World")]

fig1scatter = px.scatter(data_frame=df, x="country", y="prevelance", color="year")
fig2scatter = px.scatter(data_frame=df, x="country", y="suicide_rate", color="year")
fig3scatter = px.scatter(data_frame=df, x="country", y="anxiety_disorder", color="year")
fig4scatter = px.scatter(data_frame=df, x="country", y="eating_disorder", color="year")
fig5scatter = px.scatter(data_frame=df, x="country", y="drug_use_disorders", color="year")
fig6scatter = px.scatter(data_frame=df, x="country", y="bipolar_disorder", color="year")
fig7scatter = px.scatter(data_frame=df, x="country", y="alcohol_use_disorders ", color="year")

loc_df = pd.read_csv("./coordinates.csv")
loc_df.rename(columns={"entity":"country"}, inplace=True)
m_df = df.merge(loc_df, on="country")

# callbacks
@app.callback(
    Output('geo_scatter', 'figure'),
    Input('year-slider', 'value')
)
def update_figure(selected_year):
    fig = px.scatter_geo(
        data_frame=m_df[m_df['year'] == selected_year],
        lat="latitude",
        lon="longitude",
        size="population",
        color="suicide_rate",
        hover_name="country",
        hover_data=["prevalence_in_males", "prevalence_in_females", "prevelance"],
        height=500
    )
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('scatter-graph', 'figure'),
    Input('scatter-dropdown', 'value')
)
def update_scatter(selected_column):
    fig = px.scatter(data_frame=df, x="country", y=selected_column, log_y=True, color="year", hover_data=["year"])
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('bar-graph', 'figure'),
    Input('bar-dropdown-y', 'value'),
    Input('year-slider-bar', 'value'),
)
def update_bar(selected_column_y, selected_year):
    fig = px.bar(
            data_frame=df[df['year'] == selected_year],
            x="country",
            y=selected_column_y,
            color="country",
            hover_data=["year"]
        )
    fig.update_layout(showlegend=False)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('line-graph', 'figure'),
    Input('line-dropdown-y', 'value'),
    Input('line-dropdown-country', 'value'),
)
def update_line(selected_column_y, selected_country):
    fig = px.line(
            data_frame=df[df['country'] == selected_country],
            x="year",
            y=selected_column_y,
            log_y=True,
            # color="year",
            hover_data=["country"]
        )
    fig.update_layout(showlegend=False)
    fig.update_layout(transition_duration=500)
    return fig

# render
scatter_plot_comp = html.Div(
    className="scatter_plot_field",
    children=[
        html.Div([
            html.H4("Y: "),
            dcc.Dropdown(
                df.columns[2:],
                df.columns[2],
                id="scatter-dropdown",
            ),
        ], className="dropdown-field"),
        dcc.Graph(
            id='scatter-graph',
        ),
    ]
)
bar_plot_comp = html.Div(
    className="bar_plot_field",
    children=[
        html.Div([
            html.H4("Y: "),
            dcc.Dropdown(
                df.columns[2:],
                df.columns[2],
                id="bar-dropdown-y",
            ),
        ], className="dropdown-field"),
        html.Div([
            dcc.Slider(
                df['year'].min(),
                df['year'].max(),
                step=1,
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()},
                id='year-slider-bar'
            )
        ], className="slider-field"),
        dcc.Graph(
            id='bar-graph',
        ),
    ]
)
line_year_plot_comp = html.Div(
    className="line_plot_field",
    children=[
        html.Div([
            html.H4("Country: "),
            dcc.Dropdown(
                df.country.unique(),
                df.country.unique()[0],
                id='line-dropdown-country'
            )
        ], className="slider-field"),
        html.Div([
            html.H4("Y: "),
            dcc.Dropdown(
                df.columns[2:],
                df.columns[2],
                id="line-dropdown-y",
            ),
        ], className="dropdown-field"),
        dcc.Graph(
            id='line-graph',
        ),
    ]
)
geo_plot_comp = html.Div(
    className="geo_scatter_field",
    children=[
        dcc.Graph(
            id="geo_scatter",
        ),
        dcc.Slider(
            m_df['year'].min(),
            m_df['year'].max(),
            step=2,
            value=m_df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            id='year-slider'
        )
    ]
)

app.layout = html.Div(children=[
    html.H1(children='Mental Health/Depression/Suicides'),
    html.Div([
        scatter_plot_comp,
        bar_plot_comp,
        geo_plot_comp,
        line_year_plot_comp,
        html.Br(),
        html.Br()
    ])
], className="app_wrapper")

if __name__ == '__main__':
    app.run_server(debug=True)