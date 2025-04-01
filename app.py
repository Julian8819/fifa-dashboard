#Link: https://fifa-dashboard-i77y.onrender.com

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import os

#Create the dataset
data = {
    'Year': [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998,
             2002, 2006, 2010, 2014, 2018, 2022],
    'Winner': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'Germany', 'Brazil', 'Brazil', 'England',
               'Brazil', 'Germany', 'Argentina', 'Italy', 'Argentina', 'Germany', 'Brazil', 'France',
               'Brazil', 'Italy', 'Spain', 'Germany', 'France', 'Argentina'],
    'RunnerUp': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 'Czechoslovakia', 'West Germany',
                 'Italy', 'Netherlands', 'Netherlands', 'West Germany', 'West Germany', 'Argentina', 'Italy', 'Brazil',
                 'Germany', 'France', 'Netherlands', 'Argentina', 'Croatia', 'France']
}

df = pd.DataFrame(data)

# Normalize "West Germany" → "Germany"
df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['RunnerUp'] = df['RunnerUp'].replace({'West Germany': 'Germany'})

# Get list of countries with win counts
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Add ISO-3 country codes for mapping
country_codes = {
    'Uruguay': 'URY', 'Italy': 'ITA', 'Germany': 'DEU', 'Brazil': 'BRA',
    'England': 'GBR', 'Argentina': 'ARG', 'France': 'FRA', 'Spain': 'ESP',
    'Croatia': 'HRV', 'Sweden': 'SWE', 'Netherlands': 'NLD',
    'Czechoslovakia': 'CZE', 'Hungary': 'HUN'
}
win_counts['ISO'] = win_counts['Country'].map(country_codes)

#Create Dash App
app = dash.Dash(__name__)
app.title = "FIFA World Cup Dashboard"

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1('🏆 FIFA World Cup Dashboard', style={'color': 'red'}),
    
    html.H2('World Cup Winning Countries Map', style={'color': 'red'}),
    dcc.Graph(id='choropleth',
              figure=px.choropleth(win_counts,
                        locations='ISO',
                        color='Wins',
                        hover_name='Country',
                        color_continuous_scale='Reds',
                        title='Countries with FIFA World Cup Wins',
                        projection='natural earth',
                        locationmode='ISO-3',
                        scope='world')),

    html.Br(),
    html.H2('Select a Country to View Wins', style={'color': 'red'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'].unique())],
        placeholder='Select a country'
    ),
    html.Div(id='country-output', style={'color': 'red', 'fontSize': 20, 'marginTop': '10px'}),

    html.Br(),
    html.H2('Select a Year to View Final Match Info', style={'color': 'red'}),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'])],
        placeholder='Select a year'
    ),
    html.Div(id='match-output', style={'color': 'red', 'fontSize': 20, 'marginTop': '10px'})
])

#Callbacks for interactivity
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    if selected_country:
        wins = win_counts.loc[win_counts['Country'] == selected_country, 'Wins'].values[0]
        return f"{selected_country} has won the World Cup {wins} time(s)."
    return ""

@app.callback(
    Output('match-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_match_output(selected_year):
    if selected_year:
        row = df[df['Year'] == selected_year].iloc[0]
        return f"In {selected_year}, the winner was {row['Winner']} and the runner-up was {row['RunnerUp']}."
    return ""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
