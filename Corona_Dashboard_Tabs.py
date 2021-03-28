import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

yesterday = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')

#load latest total numbers
df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + yesterday + ".csv")

#delete columns not needed and rename the Country column
df = df.drop(['FIPS', 'Admin2', 'Last_Update', 'Lat', 'Long_'], axis=1)
df = df.rename(columns = {'Country_Region' : 'Country'})

#Combine countries which become the index
df = df.groupby('Country').sum()

#compute totals
df.loc['Total']= df.sum(numeric_only=True, axis=0)

#rename countries
df = df.T
df = df.rename(columns = {'US' : 'USA', 'Taiwan*' : 'Taiwan', 'United Kingdom': 'UK'})
df = df.T

#load time series for graphs
TS_c = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
TS_d = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
TS_r = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

#for dropdown graphs
TS_c = TS_c.groupby('Country/Region').sum()
TS_d = TS_d.groupby('Country/Region').sum()
TS_r = TS_r.groupby('Country/Region').sum()
TS_c = TS_c.drop(['Lat', 'Long'], axis=1)
TS_d = TS_d.drop(['Lat', 'Long'], axis=1)
TS_r = TS_r.drop(['Lat', 'Long'], axis=1)
TS_c = TS_c.T
TS_d = TS_d.T
TS_r = TS_r.T
TS_c = TS_c.rename(columns = {'US' : 'USA', 'Taiwan*' : 'Taiwan', 'United Kingdom': 'UK'})
TS_d = TS_d.rename(columns = {'US' : 'USA', 'Taiwan*' : 'Taiwan', 'United Kingdom': 'UK'})
TS_r = TS_r.rename(columns = {'US' : 'USA', 'Taiwan*' : 'Taiwan', 'United Kingdom': 'UK'})

#options for country dropdown
cols = TS_c.columns
options = [{'label' : i, 'value' : i} for i in cols]

################
#Portugal plots#
################
trace1 = go.Scatter(x = TS_c.index, y = TS_c['Portugal'], line=dict(width=3), name = 'Confirmed')
trace2 = go.Scatter(x = TS_d.index, y = TS_d['Portugal'], line=dict(width=3), name = 'Death')

#for graph new daily cases
y_pt = TS_c['Portugal'] - TS_c['Portugal'].shift(1)
trace3 = go.Bar(x = TS_c.index, y = y_pt, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_pt = y_pt.rolling(7).mean()
trace4 = go.Scatter(x = TS_c.index, y = ma7_cases_pt, name='7-day avg', line=dict(width=3))

#for graph new daily deaths
yd_pt = TS_d['Portugal'] - TS_d['Portugal'].shift(1)
trace5 = go.Bar(x = TS_c.index, y = yd_pt, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_pt = yd_pt.rolling(7).mean()
trace6 = go.Scatter(x = TS_c.index, y = ma7_deaths_pt, name='7-day avg', line=dict(width=3))

#Total Portugal cases
confirmed_pt = df.loc['Portugal']['Confirmed'].round().astype(int)
deaths_pt = df.loc['Portugal']['Deaths'].round().astype(int)
recovered_pt = df.loc['Portugal']['Recovered'].round().astype(int)
mortality_pt = (deaths_pt / confirmed_pt) * 100
active_pt = df.loc['Portugal']['Active'].round().astype(int)

#Portugal Cards
card_content1 = [
    dbc.CardHeader("Total Confirmed Cases - Portugal", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_pt:,}', className="card-title")
        ]
    ),
]
card_content2 = [
    dbc.CardHeader("Total Active Cases - Portugal", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{active_pt:,}', className="card-title")
        ]
    ),
]
card_content3 = [
    dbc.CardHeader("Total Recovered Cases - Portugal", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{recovered_pt:,}', className="card-title")
        ]
    ),
]
card_content4 = [
    dbc.CardHeader("Total Deaths - Portugal", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_pt:,}', className="card-title")
        ]
    ),
]
card_content5 = [
    dbc.CardHeader("Total Mortality Rate - Portugal", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_pt), className="card-title")
        ]
    ),
]

################
#Brazil plots#
################
trace7 = go.Scatter(x = TS_c.index, y = TS_c['Brazil'], line=dict(width=3), name = 'Confirmed')
trace8 = go.Scatter(x = TS_d.index, y = TS_d['Brazil'], line=dict(width=3), name = 'Death')

#for default graph new cases
y_brz = TS_c['Brazil'] - TS_c['Brazil'].shift(1)
trace9 = go.Bar(x = TS_c.index, y = y_brz, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_brz = y_brz.rolling(7).mean()
trace10 = go.Scatter(x = TS_c.index, y = ma7_cases_brz, name='7-day avg', line=dict(width=3))

#for default graph new deaths
yd_brz = TS_d['Brazil'] - TS_d['Brazil'].shift(1)
trace11 = go.Bar(x = TS_c.index, y = yd_brz, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_brz = yd_brz.rolling(7).mean()
trace12 = go.Scatter(x = TS_c.index, y = ma7_deaths_brz, name='7-day avg', line=dict(width=3))

#Total Brazil cases
confirmed_brz = df.loc['Brazil']['Confirmed'].round().astype(int)
deaths_brz = df.loc['Brazil']['Deaths'].round().astype(int)
recovered_brz = df.loc['Brazil']['Recovered'].round().astype(int)
mortality_brz = (deaths_brz / confirmed_brz) * 100
active_brz = df.loc['Brazil']['Active'].round().astype(int)

#Brazil Cards
card_content6 = [
    dbc.CardHeader("Total Confirmed Cases - Brazil", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_brz:,}', className="card-title")
        ]
    ),
]
card_content7 = [
    dbc.CardHeader("Total Active Cases - Brazil", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{active_brz:,}', className="card-title")
        ]
    ),
]
card_content8 = [
    dbc.CardHeader("Total Recovered Cases - Brazil", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{recovered_brz:,}', className="card-title")
        ]
    ),
]
card_content9 = [
    dbc.CardHeader("Total Deaths - Brazil", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_brz:,}', className="card-title")
        ]
    ),
]
card_content10 = [
    dbc.CardHeader("Total Mortality Rate - Brazil", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_brz), className="card-title")
        ]
    ),
]

################
#Germany plots#
################
trace13 = go.Scatter(x = TS_c.index, y = TS_c['Germany'], line=dict(width=3), name = 'Confirmed')
trace14 = go.Scatter(x = TS_d.index, y = TS_d['Germany'], line=dict(width=3), name = 'Death')

#for default graph new cases
y_ger = TS_c['Germany'] - TS_c['Germany'].shift(1)
trace15 = go.Bar(x = TS_c.index, y = y_ger, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_ger = y_ger.rolling(7).mean()
trace16 = go.Scatter(x = TS_c.index, y = ma7_cases_ger, name='7-day avg', line=dict(width=3))

#for default graph new deaths
yd_ger = TS_d['Germany'] - TS_d['Germany'].shift(1)
trace17 = go.Bar(x = TS_c.index, y = yd_ger, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_ger = yd_ger.rolling(7).mean()
trace18 = go.Scatter(x = TS_c.index, y = ma7_deaths_ger, name='7-day avg', line=dict(width=3))

#Total cases
confirmed_ger = df.loc['Germany']['Confirmed'].round().astype(int)
deaths_ger = df.loc['Germany']['Deaths'].round().astype(int)
recovered_ger = df.loc['Germany']['Recovered'].round().astype(int)
mortality_ger = (deaths_ger / confirmed_ger) * 100
active_ger = df.loc['Germany']['Active'].round().astype(int)

#Cards
card_content11 = [
    dbc.CardHeader("Total Confirmed Cases - Germany", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_ger:,}', className="card-title")
        ]
    ),
]
card_content12 = [
    dbc.CardHeader("Total Active Cases - Germany", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{active_ger:,}', className="card-title")
        ]
    ),
]
card_content13 = [
    dbc.CardHeader("Total Recovered Cases - Germany", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{recovered_ger:,}', className="card-title")
        ]
    ),
]
card_content14 = [
    dbc.CardHeader("Total Deaths - Germany", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_ger:,}', className="card-title")
        ]
    ),
]
card_content15 = [
    dbc.CardHeader("Total Mortality Rate - Germany", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_ger), className="card-title")
        ]
    ),
]

################
#Angola plots#
################
trace19 = go.Scatter(x = TS_c.index, y = TS_c['Angola'], line=dict(width=3), name = 'Confirmed')
trace20 = go.Scatter(x = TS_d.index, y = TS_d['Angola'], line=dict(width=3), name = 'Death')

#for default graph new cases
y_ang = TS_c['Angola'] - TS_c['Angola'].shift(1)
trace21 = go.Bar(x = TS_c.index, y = y_ang, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_ang = y_ang.rolling(7).mean()
trace22 = go.Scatter(x = TS_c.index, y = ma7_cases_ang, name='7-day avg', line=dict(width=3))

#for default graph new deaths
yd_ang = TS_d['Angola'] - TS_d['Angola'].shift(1)
trace23 = go.Bar(x = TS_c.index, y = yd_ang, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_ang = yd_ang.rolling(7).mean()
trace24 = go.Scatter(x = TS_c.index, y = ma7_deaths_ang, name='7-day avg', line=dict(width=3))

#Total cases
confirmed_ang = df.loc['Angola']['Confirmed'].round().astype(int)
deaths_ang = df.loc['Angola']['Deaths'].round().astype(int)
recovered_ang = df.loc['Angola']['Recovered'].round().astype(int)
mortality_ang = (deaths_ang / confirmed_ang) * 100
active_ang = df.loc['Angola']['Active'].round().astype(int)

#Cards
card_content16 = [
    dbc.CardHeader("Total Confirmed Cases - Angola", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_ang:,}', className="card-title")
        ]
    ),
]
card_content17 = [
    dbc.CardHeader("Total Active Cases - Angola", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{active_ang:,}', className="card-title")
        ]
    ),
]
card_content18 = [
    dbc.CardHeader("Total Recovered Cases - Angola", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{recovered_ang:,}', className="card-title")
        ]
    ),
]
card_content19 = [
    dbc.CardHeader("Total Deaths - Angola", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_ang:,}', className="card-title")
        ]
    ),
]
card_content20 = [
    dbc.CardHeader("Total Mortality Rate - Angola", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_ang), className="card-title")
        ]
    ),
]

################
#UK plots#
################
trace25 = go.Scatter(x = TS_c.index, y = TS_c['UK'], line=dict(width=3), name = 'Confirmed')
trace26 = go.Scatter(x = TS_d.index, y = TS_d['UK'], line=dict(width=3), name = 'Death')

#for default graph new cases
y_uk = TS_c['UK'] - TS_c['UK'].shift(1)
trace27 = go.Bar(x = TS_c.index, y = y_uk, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_uk = y_uk.rolling(7).mean()
trace28 = go.Scatter(x = TS_c.index, y = ma7_cases_uk, name='7-day avg', line=dict(width=3))

#for default graph new deaths
yd_uk = TS_d['UK'] - TS_d['UK'].shift(1)
trace29 = go.Bar(x = TS_c.index, y = yd_uk, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_uk = yd_uk.rolling(7).mean()
trace30 = go.Scatter(x = TS_c.index, y = ma7_deaths_uk, name='7-day avg', line=dict(width=3))

#Total cases
confirmed_uk = df.loc['UK']['Confirmed'].round().astype(int)
deaths_uk = df.loc['UK']['Deaths'].round().astype(int)
recovered_uk = df.loc['UK']['Recovered'].round().astype(int)
mortality_uk = (deaths_uk / confirmed_uk) * 100
active_uk = df.loc['UK']['Active'].round().astype(int)

#Cards
card_content21 = [
    dbc.CardHeader("Total Confirmed Cases - UK", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_uk:,}', className="card-title")
        ]
    ),
]
card_content22 = [
    dbc.CardHeader("Total Active Cases - UK", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{active_uk:,}', className="card-title")
        ]
    ),
]
card_content23 = [
    dbc.CardHeader("Total Recovered Cases - UK", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{recovered_uk:,}', className="card-title")
        ]
    ),
]
card_content24 = [
    dbc.CardHeader("Total Deaths - UK", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_uk:,}', className="card-title")
        ]
    ),
]
card_content25 = [
    dbc.CardHeader("Total Mortality Rate - UK", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_uk), className="card-title")
        ]
    ),
]

################
#USA plots#
################
trace31 = go.Scatter(x = TS_c.index, y = TS_c['USA'], line=dict(width=3), name = 'Confirmed')
trace32 = go.Scatter(x = TS_d.index, y = TS_d['USA'], line=dict(width=3), name = 'Death')

#for default graph new cases
y_usa = TS_c['USA'] - TS_c['USA'].shift(1)
trace33 = go.Bar(x = TS_c.index, y = y_usa, width=1, name = 'Daily')

#add a 7-day moving average curve to new cases
ma7_cases_usa = y_usa.rolling(7).mean()
trace34 = go.Scatter(x = TS_c.index, y = ma7_cases_usa, name='7-day avg', line=dict(width=3))

#for default graph new deaths
yd_usa = TS_d['USA'] - TS_d['USA'].shift(1)
trace35 = go.Bar(x = TS_c.index, y = yd_usa, width=1, name = 'Daily')

#add a 7-day moving average curve to new deaths
ma7_deaths_usa = yd_usa.rolling(7).mean()
trace36 = go.Scatter(x = TS_c.index, y = ma7_deaths_usa, name='7-day avg', line=dict(width=3))

#Total cases
confirmed_usa = df.loc['USA']['Confirmed'].round().astype(int)
deaths_usa = df.loc['USA']['Deaths'].round().astype(int)
#recovered_usa = df.loc['USA']['Recovered'].round().astype(int)
mortality_usa = (deaths_usa / confirmed_usa) * 100
#active_usa = df.loc['USA']['Active'].round().astype(int)

#Cards
card_content26 = [
    dbc.CardHeader("Total Confirmed Cases - USA", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_usa:,}', className="card-title")
        ]
    ),
]
card_content29 = [
    dbc.CardHeader("Total Deaths - USA", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_usa:,}', className="card-title")
        ]
    ),
]
card_content30 = [
    dbc.CardHeader("Total Mortality Rate - USA", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_usa), className="card-title")
        ]
    ),
]

################
#Global plots#
################

#Total cases
confirmed_global = df.loc['Total']['Confirmed'].round().astype(int)
deaths_global = df.loc['Total']['Deaths'].round().astype(int)
#recovered_global = df.loc['Total']['Recovered'].round().astype(int)
mortality_global = (deaths_global / confirmed_global) * 100
#active_global = df.loc['Total']['Active'].round().astype(int)

#Cards
card_content31 = [
    dbc.CardHeader("Total Confirmed Cases - Global", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{confirmed_global:,}', className="card-title")
        ]
    ),
]
card_content34 = [
    dbc.CardHeader("Total Deaths - Global", className="card-title"),
    dbc.CardBody(
        [
            html.H5(f'{deaths_global:,}', className="card-title")
        ]
    ),
]
card_content35 = [
    dbc.CardHeader("Total Mortality Rate - Global", className="card-title"),
    dbc.CardBody(
        [
            html.H5('{:.1f} %'.format(mortality_global), className="card-title")
        ]
    ),
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
                html.Div([
                    html.H1("Coronavirus Dashboard"),
                    html.H3('Last update: {}'.format(yesterday))
                        ], style={'textAlign' : 'center', 'border' : 'solid', 'backgroundColor' : 'silver'}
                        ),
                html.Hr(),
                html.Div([
                    dcc.Tabs([
                        dcc.Tab(label='Global', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content31, color="primary", inverse=True),
                                                dbc.Card(card_content34, color="danger", inverse=True),
                                                dbc.Card(card_content35, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 8, 'offset': 2}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                        ]),
                        dcc.Tab(label='United States', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content26, color="primary", inverse=True),
                                                dbc.Card(card_content29, color="danger", inverse=True),
                                                dbc.Card(card_content30, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 8, 'offset': 2}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace31],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - USA',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace33, trace34],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - USA',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace32],
                										'layout' : go.Layout(title = 'Cumulative Deaths - USA',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace35, trace36],
                										'layout' : go.Layout(title = 'Daily New Deaths - USA',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='United Kingdom', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content21, color="primary", inverse=True),
                                                dbc.Card(card_content22, color="warning", inverse=True),
                                                dbc.Card(card_content23, color="success", inverse=True),
                                                dbc.Card(card_content24, color="danger", inverse=True),
                                                dbc.Card(card_content25, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 12}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace25],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - UK',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace27, trace28],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - UK',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace26],
                										'layout' : go.Layout(title = 'Cumulative Deaths - UK',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace29, trace30],
                										'layout' : go.Layout(title = 'Daily New Deaths - UK',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='Portugal', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content1, color="primary", inverse=True),
                                                dbc.Card(card_content2, color="warning", inverse=True),
                                                dbc.Card(card_content3, color="success", inverse=True),
                                                dbc.Card(card_content4, color="danger", inverse=True),
                                                dbc.Card(card_content5, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 12}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace1],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - Portugal',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace3, trace4],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - Portugal',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace2],
                										'layout' : go.Layout(title = 'Cumulative Deaths - Portugal',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace5, trace6],
                										'layout' : go.Layout(title = 'Daily New Deaths - Portugal',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='Brazil', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content6, color="primary", inverse=True),
                                                dbc.Card(card_content7, color="warning", inverse=True),
                                                dbc.Card(card_content8, color="success", inverse=True),
                                                dbc.Card(card_content9, color="danger", inverse=True),
                                                dbc.Card(card_content10, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 12}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace7],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - Brazil',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace9, trace10],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - Brazil',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace8],
                										'layout' : go.Layout(title = 'Cumulative Deaths - Brazil',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace11, trace12],
                										'layout' : go.Layout(title = 'Daily New Deaths - Brazil',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='Germany', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content11, color="primary", inverse=True),
                                                dbc.Card(card_content12, color="warning", inverse=True),
                                                dbc.Card(card_content13, color="success", inverse=True),
                                                dbc.Card(card_content14, color="danger", inverse=True),
                                                dbc.Card(card_content15, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 12}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace13],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - Germany',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace15, trace16],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - Germany',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace14],
                										'layout' : go.Layout(title = 'Cumulative Deaths - Germany',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace17, trace18],
                										'layout' : go.Layout(title = 'Daily New Deaths - Germany',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='Angola', children=[
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.CardDeck([
                                                dbc.Card(card_content16, color="primary", inverse=True),
                                                dbc.Card(card_content17, color="warning", inverse=True),
                                                dbc.Card(card_content18, color="success", inverse=True),
                                                dbc.Card(card_content19, color="danger", inverse=True),
                                                dbc.Card(card_content20, color="secondary", inverse=True)],
                                                style={'textAlign' : 'center'}),
                                                width={"size": 12}),
                                ],
                                align='top',
                                ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace19],
                    										'layout' : go.Layout(title = 'Cumulative Confirmed Cases - Angola',
                                                            xaxis = dict(showgrid=False), title_font_size=24)
                    									}
                    						), md=6),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace21, trace22],
                    										'layout' : go.Layout(title = 'Daily New Confirmed Cases - Angola',
                                                            legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
                    						), md=6),
                                ],
                                align="top",
                            ),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace20],
                										'layout' : go.Layout(title = 'Cumulative Deaths - Angola',
                                                        xaxis = dict(showgrid=False), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                    dbc.Col(dcc.Graph(
                    							figure = {'data' : [trace23, trace24],
                										'layout' : go.Layout(title = 'Daily New Deaths - Angola',
                                                        legend=dict(x=0.1, y=0.9, font_size=16), title_font_size=24)
                    									}
						                              ), md=6
                                          ),
                                ],
                                align="top",
                            )
                        ]),
                        dcc.Tab(label='Choose a Country', children=[
                        ]),

                    ])
                ])
            ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
