import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html
import dash_bootstrap_components as dbc

df = pd.read_csv("data/new-neonatal-tetanas-with-continent.csv")
tetanus_deaths_by_age_gp = pd.read_csv("data/tetanus-deaths-by-age-group_mod.csv")
tetanus_deaths_by_age_gp = tetanus_deaths_by_age_gp.melt(id_vars=["Entity", 'Year', 'Code'],
                                                         var_name='Age Group',
                                                         value_name='Deaths')
who_vs_gbd = pd.read_csv("data/who-vs-gbd-incidence-of-tetanus_mod.csv")

content = """
        Tetanus is a bacterial infection that leads to painful muscle contractions, typically beginning in the jaw 
        and then progressing to the rest of the body. In recent years, tetanus has been fatal ‘in approximately 
        11% of reported cases’. Globally 38,000 people died from tetanus in 2017. Around half (49%) were younger 
        than five years old. This dashboard presents a global overview on tetanus and MNT, presenting data on cases and 
        deaths,and explaining transmission,prevention and the efforts to eliminate tetanus.
"""
heading_jumbotron = html.Div(
    dbc.Card(
        dbc.Container(
            children=[
                html.H1("Global Burden of Tetanus", className="display-3"),

                html.Hr(className="my-2"),
                html.P(
                    content
                ),
            ],
            fluid=True,
            className="py-3",
        )),
    className="p-3 bg-light rounded-3",
)

#
# collapse = html.Div(
#     [
#         dbc.Button(
#             "More facts about Tetanus",
#             id="collapse-button",
#             className="mb-3",
#             color="primary",
#             n_clicks=0,
#         ),
#         dbc.Collapse(
#             dbc.Card(dbc.CardBody("""
#             Tetanus is a disease caused by the toxin of a bacterium. There are two ways by which the disease can be contracted:
#             Tetanus can be contracted from dirt that enters through wounds, and can ultimately cause paralysis and death.
# When mothers or newborns contract tetanus through wounds during birth, this is called maternal/neonatal tetanus (MNT). It can be prevented by immunizing the mother who passes the immunity on to her newborn for a few days after birth.
#             """)),
#             id="collapse",
#             is_open=False,
#         ),
#     ]
# )

slider = html.Div(
    [
        dcc.Slider(id="year-slider",
                   min=df['Year'].min(),
                   max=df['Year'].max(),
                   step=1,
                   value=df['Year'].max(),
                   marks={
                       1974: {'label': '1974'},
                       1980: {'label': '1980'},
                       1985: {'label': '1985'},
                       1990: {'label': '1990'},
                       1995: {'label': '1995'},
                       2000: {'label': '2000'},
                       2005: {'label': '2005'},
                       2010: {'label': '2010'},
                       2015: {'label': '2015'},
                       2020: {'label': '2020'}
                   },
                   tooltip={"placement": "bottom", "always_visible": True},
                   included=False
                   ),
    ],
    className="mb-3",
)

slider_ui = html.Div(
    id="slider-container",
    children=[
        html.P(
            id="slider-text",
            children="Drag the slider to change the year:",
        ),
        slider,

    ]

)
continent_dropdown = html.Div(
    [
        dbc.Label("Choose a Continent", html_for="dropdown"),
        dcc.Dropdown(
            id="continent-dropdown",
            options=[{"label": i, "value": i} for i in df['Continent'].unique().tolist()],
            value="The World"
        ),
    ],
    className="mb-3",
)

country_dropdown = html.Div(
    [
        dbc.Label("Choose a Country", html_for="dropdown"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": i, "value": i} for i in df['Entity'].unique().tolist()],
            value="India"
        ),
    ],
    className="mb-3",
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['dbc.themes.BOOTSTRAP']


app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container(
    id='root',
    fluid=False,
    children=[
        dbc.Row(heading_jumbotron),
        html.Div(
            id='app-container',
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            children=[
                                slider_ui,
                                html.Div(
                                    id="map-container",
                                    children=[
                                        continent_dropdown,
                                        html.H4('Number of Reported Cases per million in The World',
                                                id='h3-country'),
                                        dcc.Graph(id='world-map'),
                                    ]

                                ),

                            ]

                        ),
                        dbc.Col(
                            html.Div(
                                id='graph-container',
                                children=[
                                    dbc.Row(country_dropdown),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                children=[
                                                    html.H4('Deaths from Tetanus in India', id='h1-country'),
                                                    dcc.Graph(id='tetanus-deaths-ts',
                                                              figure=dict(
                                                                  data=[dict(x=0, y=0)],
                                                                  layout=dict(
                                                                      paper_bgcolor="#F4F4F8",
                                                                      plot_bgcolor="#F4F4F8",
                                                                      autofill=True,
                                                                      margin=dict(t=75, r=50, b=100, l=50),
                                                                  )))
                                                ]),
                                            dbc.Col(
                                                children=[
                                                    html.H4('WHO vs. IHME incidence of tetanus, India',
                                                            id='h2-country'),
                                                    dcc.Graph(id='tetanus-incidence-ts',
                                                              figure=dict(
                                                                  data=[dict(x=0, y=0)],
                                                                  layout=dict(
                                                                      paper_bgcolor="#F4F4F8",
                                                                      plot_bgcolor="#F4F4F8",
                                                                      autofill=True,
                                                                      margin=dict(t=75, r=50, b=100, l=50),
                                                                  )))
                                                ]

                                            )
                                        ]

                                    ),
                                ]
                            ),
                        )]
                ),
            ])
    ])


@app.callback(
    Output('world-map', 'figure'),
    Input('continent-dropdown', 'value'),
    Input('year-slider', 'value'))
def update_figure(continent, selected_year):
    filtered_df = df.query("Year == @selected_year and Continent == @continent")

    fig = go.Figure(data=go.Choropleth(
        locations=filtered_df['Code'],
        z=filtered_df['Indicator:Neonatal tetanus - number of reported cases per million'],
        text=filtered_df['Entity'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.3,
        colorbar_title='Cases per million people'))
    fig.update_geos(fitbounds='locations')
    fig.update_layout(geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ), )

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('tetanus-deaths-ts', 'figure'),
    Input('country-dropdown', 'value'),
)
def update_figure(country):
    filtered_df = tetanus_deaths_by_age_gp.query("Entity == @country")
    filtered_df = filtered_df.sort_values('Year')

    # title = "Deaths from Tetanus in {}".format(country)
    fig = px.scatter(filtered_df,
                     x='Year',
                     y='Deaths',
                     color='Age Group')

    fig.update_traces(mode='lines+markers', marker=dict(size=3.8),
                      connectgaps=True)
    fig.update_xaxes(showgrid=False)
    fig.update_layout(transition_duration=500)

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )),
        yaxis=dict(
            showline=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )),
        plot_bgcolor='white',
        autosize=False,

    )

    return fig


@app.callback(
    Output('tetanus-incidence-ts', 'figure'),
    Input('country-dropdown', 'value'),
)
def update_figure(country):
    filtered_df = who_vs_gbd.query("Entity == @country")
    filtered_df = filtered_df.sort_values('Year')
    # title = "Deaths from Tetanus in {}".format(country)
    fig = px.scatter(filtered_df,
                     x='Year',
                     y='Cases',
                     color='Options')

    fig.update_traces(mode='lines+markers',
                      connectgaps=True)
    fig.update_xaxes(showgrid=False)
    fig.update_layout(transition_duration=500)
    fig.update_traces(mode='lines+markers', connectgaps=True, marker=dict(size=3.8))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )),
        yaxis=dict(
            showline=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )),
        plot_bgcolor='white',
        autosize=False,

    )

    return fig


@app.callback(Output('h1-country', 'children'),
              Input('country-dropdown', 'value'))
def update_h1(country):
    return "Deaths from Tetanus in {}".format(country)


@app.callback(Output('h2-country', 'children'),
              Input('country-dropdown', 'value'))
def update_h1(country):
    return "WHO vs. IHME incidence of tetanus, {}".format(country)


@app.callback(Output('h3-country', 'children'),
              Input('continent-dropdown', 'value'),
              Input('year-slider', 'value'))
def update_h1(country, year):
    return "Number of Reported Cases per million in {} ({})".format(country, year)


app.run_server(debug=True)  # Turn off reloader if inside Jupyter
