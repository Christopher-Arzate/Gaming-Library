
# Import packages

from dash import  html, dcc, Output, Input
import pandas as pd
import dash
import plotly.express as px
import dash_bootstrap_components as dbc


# Incorporate data
library=pd.read_csv('Assets/library.csv')


#General Statistics
avg_game= library['price'].mean()
unique_game= len(library['title'].unique())
library.head()

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout= dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Library Gameboard"), width=15,className="text-center my-5")
    ]),
    # General Statistics
    dbc.Row([
        dbc.Col(html.Div(f"Average Price of Games: {avg_game:,.2f}",className="text-center my-3"), width=7),
        dbc.Col(html.Div(f"Unique Games in my Library: {unique_game}",className="text-center my-3"),width=7)
    ],className="mb-5"),
    
    #Histograms of price based on the games and Dicount rates
    dbc.Row([
        dbc.Col([
           dcc.Graph(figure=px.histogram(library, x='storeName', y='savings', histfunc='avg'))],width=6),
        dbc.Col([dcc.Graph(figure=px.histogram(library, x='Time', y='savings', histfunc='avg'))],width=6)   
    ]),
    
    # Discount per Game 
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Discount by Store",className='Discount-title'),
                    dcc.Dropdown(
                        id="game-filter",
                        options=[{'label':game,"value":game} for game in library['title'].unique()],
                        value=None,
                        placeholder="Select a Game"
                    ),
                    dcc.Graph(id="discount-distribution") 
                    
                ])
            ])
        ],width=12)
    ]),
    # Discount over Tme
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     html.H4("Discounts over time",className='Time-title'),
                    dcc.Dropdown(
                        id="game-filters",
                        options=[{'label':game,"value":game} for game in library['title'].unique()],
                        value=None,
                        placeholder="Select a Game"
                    ),
                    dcc.Graph(id="Time-distribution")  
                ])
            ])
        ], width=12)
    ])   
])


# Create the Callbacks
@app.callback(
    Output("discount-distribution","figure"),
    Input("game-filter","value")
)
def update_distrbutions(selected_game):
    if selected_game:
        filtered_df=library[library['title']==selected_game]
    else:
        filtered_df=library
        
        
    if filtered_df.empty:
        return {}
    
    fig=px.histogram(
        filtered_df,
        x="savings",
        nbins=10,
        title="Discount Distribution by Game"
    )
    
    return fig

@app.callback(
    Output("Time-distribution","figure"),
    Input("game-filters","value")
)
def update_distrbution(selected_game):
    if selected_game:
        filtered_df=library[library['title']==selected_game]
    else:
        filtered_df=library
    trend_df= filtered_df.groupby('Time')['savings'].mean().reset_index()   
        
    if filtered_df.empty:
        return {}
    
    fig=px.line(
        trend_df,
        x="Time",
        y='savings',
        title="Discount Distribution by Game"
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)