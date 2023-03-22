import pandas as pd
from dash import Dash, Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("data/new-neonatal-tetanas-with-continent.csv")
tetanus_deaths_by_age_gp = pd.read_csv("data/tetanus-deaths-by-age-group_mod.csv")
tetanus_deaths_by_age_gp = tetanus_deaths_by_age_gp.melt(id_vars=["Entity", 'Year', 'Code'],
                                                         var_name='Age Group',
                                                         value_name='Deaths')

who_vs_gbd = pd.read_csv("data/who-vs-gbd-incidence-of-tetanus_mod.csv")
custom_style_dict = {
    'background-color': '#f8f9fa',
    'padding': '15px',
    'margin': '20px',
    'border-radius': '3px',
    'box-shadow': '0px 0px 10px #ddd'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

content = """
        Tetanus is a bacterial infection that leads to painful muscle contractions, typically beginning in the jaw 
        and then progressing to the rest of the body. In recent years, tetanus has been fatal ‘in approximately 
        11% of reported cases’. Globally 38,000 people died from tetanus in 2017. Around half (49%) were younger 
        than five years old. This dashboard presents a global overview on tetanus and MNT, presenting data on cases and 
        deaths,and explaining transmission,prevention and the efforts to eliminate tetanus.
"""

heading_jumbotron = html.Div(
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
    ),
    className="p-3 bg-light rounded-3",
)

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

slider_ui = dbc.Card(
    dbc.Container(
        html.Div(
            id="slider-container",
            children=[
                html.P(
                    id="slider-text",
                    children="Drag the slider to change the year:",
                ),
                slider,

            ]

        ))
)

graph_dropdown = dbc.Card(
    dbc.Container(
        html.Div(
            [
                dbc.Label("Select a graph type", html_for="dropdown"),
                dcc.Dropdown(
                    id="graph-dropdown",
                    options=[
                        {"label": "Deaths from Tetanus", "value": "Deaths"},
                        {"label": "Incidence of Tetanus", "value": "Incidence"}
                    ],
                    value="Deaths"
                ),
            ],
            className="mb-3",
        )
    )
)

continent_dropdown = dbc.Card(
    dbc.Container(
        html.Div(
            [
                dbc.Label("Select a Continent", html_for="dropdown"),
                dcc.Dropdown(
                    id="continent-dropdown",
                    options=[{"label": i, "value": i} for i in sorted(df['Continent'].unique().tolist())],
                    value="The World"
                ),
            ],
            className="mb-3",
        )
    )
)

country_dropdown = html.Div(
    [
        dbc.Label("Select a Country from The World", html_for="dropdown", id='country-options'),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": i, "value": i} for i in df['Entity'].unique().tolist()],
            value="India"
        ),
    ],
    className="mb-3",
)

world_map_header = html.Div(html.H4('Number of Reported Cases per million in The World',
                                    id='world-map-heading'))
world_map_ui = dbc.Card(dbc.Container(html.Div([
    world_map_header,
    dcc.Graph(id='world-map',
              figure=dict(layout=dict(autosize=True)))
]), fluid=True))

graph_1_ui = dbc.Card(
    dbc.Container([
        country_dropdown,
        html.H4('Deaths from Tetanus in India', id='graph-1-heading'),
        dcc.Graph(id='tetanus-deaths-ts',
                  figure=dict(
                      data=[dict(x=0, y=0)],
                      layout=dict(
                          paper_bgcolor="#F4F4F8",
                          plot_bgcolor="#F4F4F8",
                          margin=dict(t=75, r=50, b=100, l=50),
                      )))
    ])
)

app.layout = dbc.Container([
    dbc.Row(heading_jumbotron,
            style={
                'background-color': '#f8f9fa',
                'padding': '15px',
                'margin': '20px',
                'border-radius': '3px',
                'box-shadow': '0px 0px 10px #ddd'
            }
            ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col(slider_ui),
                    dbc.Col(continent_dropdown, md=5)],
                    style={
                        'background-color': '#f8f9fa',
                        'padding': '15px',
                        'margin': '20px',
                        'border-radius': '3px',
                        'box-shadow': '0px 0px 10px #ddd'
                    }

                ),
                dbc.Row(world_map_ui,
                        style={
                            'background-color': '#f8f9fa',
                            'padding': '15px',
                            'margin': '20px',
                            'border-radius': '3px',
                            'box-shadow': '0px 0px 10px #ddd'
                        }
                        )
            ], md=6),
            dbc.Col([
                dbc.Row(graph_dropdown,
                        style=custom_style_dict
                        ),
                dbc.Row(graph_1_ui,
                        style=custom_style_dict),
            ])

        ], className="g-0"
    ),

], fluid=True)


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
        colorscale=[[0, 'rgb(201,83,35)'],
                    [0.2, 'rgb(224,113,49)'],
                    [0.4, 'rgb(238,147,79)'],
                    [0.6, 'rgb(246,210,168)'],
                    [0.8, 'rgb(250,231,209)'],
                    [1, 'rgb(251,251,225)']],
        autocolorscale=False,
        reversescale=True,
        colorbar_len=0.9,
        colorbar_orientation="h",
        marker_line_color='darkgray',
        marker_line_width=0.3,
        colorbar_title='Cases per million people',
    ))
    fig.update_geos(fitbounds='locations')
    fig.update_layout(geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'),
        height=600,
        width=600,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_traces(showscale=True)
    fig.update_coloraxes(colorbar_orientation="h")
    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('tetanus-deaths-ts', 'figure'),
    Input('graph-dropdown', 'value'),
    Input('country-dropdown', 'value'),
)
def update_figure(graph_name, country):
    if graph_name == 'Deaths':
        filtered_df = tetanus_deaths_by_age_gp.query("Entity == @country").sort_values('Year')
        fig = px.scatter(filtered_df,
                         x='Year',
                         y='Deaths',
                         color='Age Group')

        fig.update_traces(mode='lines+markers', marker=dict(size=3.8),
                          connectgaps=True)
        fig.update_xaxes(showgrid=False)
        fig.update_layout(transition_duration=500)

        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=1.1,
                xanchor="right",
                x=1.2
            ),
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
            autosize=True,

        )

        return fig
    else:
        filtered_df = who_vs_gbd.query("Entity == @country").sort_values('Year')
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
            legend=dict(
                yanchor="top",
                y=1.1,
                xanchor="right",
                x=1.2
            ),
            legend_title="",
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
            autosize=True,

        )

        return fig


@app.callback(Output('country-dropdown', 'options'),
              Input('continent-dropdown', 'value'))
def update_countries(continent):
    temp_df = df.copy()
    temp_df = temp_df.query('Continent == @continent')
    options = [{"label": i, "value": i} for i in temp_df['Entity'].unique().tolist()]
    return options


@app.callback(Output('world-map-heading', 'children'),
              Input('continent-dropdown', 'value'),
              Input('year-slider', 'value'))
def update_heading(country, year):
    return "Number of Reported Cases per million in {} ({})".format(country, year)


@app.callback(Output('graph-1-heading', 'children'),
              Input('country-dropdown', 'value'),
              Input('graph-dropdown', 'value'))
def update_heading(country, graph):
    if graph == 'Deaths':
        return "Deaths from Tetanus in {}".format(country)
    else:
        return "WHO vs. IHME incidence of tetanus, {}".format(country)


@app.callback(Output('country-options', 'children'),
              Input('continent-dropdown', 'value'))
def update_option_text(continent):
    return dbc.Label("Select a Country from {}".format(continent))


app.run_server(debug=True, port=4242)
