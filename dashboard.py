import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('nirf_2025_combined.csv')
all_df = df.copy()
all_df['Category'] = 'All'
df = pd.concat([df, all_df])

# Initialize the Dash app
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app = dash_app.server

# --- App Layout ---
dash_app.layout = dbc.Container(fluid=True, children=[
    html.H1(
        "NIRF 2025 – Top 10 Dashboard",
        className="text-center text-primary mb-4"
    ),

    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Category", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': i, 'value': i} for i in df['Category'].unique()],
                value='All'
            )
        ], width=6),
        dbc.Col([
            html.Label("Region", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Region'].unique() if i != 'Other'],
                value='All'
            )
        ], width=6)
    ], className="mb-4"),

    # Summary Cards
    dbc.Row(id='summary-cards', className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='bar-chart')), width=12),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='pie-chart')), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='box-plot')), width=6),
    ])
])

# --- Callbacks ---
@dash_app.callback(
    [Output('summary-cards', 'children'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('box-plot', 'figure')],
    [Input('category-filter', 'value'),
     Input('region-filter', 'value')]
)
def update_dashboard(selected_category, selected_region):
    # Filter dataframe
    if selected_category == 'All':
        filtered_df = df[df['Category'] != 'All']
    else:
        filtered_df = df[df['Category'] == selected_category]

    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]

    # --- Summary Cards ---
    total_institutes = filtered_df['Name'].nunique()
    avg_score = filtered_df['Score'].mean() if not filtered_df.empty else 0
    
    summary_cards = [
        dbc.Col(dbc.Card([
            html.H4("Total Institutes", className="card-title"),
            html.H2(f"{total_institutes}", className="card-text"),
        ], body=True, color="light"), width=6),
        dbc.Col(dbc.Card([
            html.H4("Average Score", className="card-title"),
            html.H2(f"{avg_score:.2f}", className="card-text"),
        ], body=True, color="light"), width=6),
    ]

    # --- Bar Chart ---
    bar_fig = px.bar(
        filtered_df.sort_values('Score', ascending=False).head(10),
        x='Score',
        y='Name',
        orientation='h',
        title=f"Top 10 Institutes in {selected_category}",
        labels={'Name': 'Institute', 'Score': 'Score'},
        template='plotly_white'
    )
    bar_fig.update_layout(yaxis={'categoryorder':'total ascending'})

    # --- Pie Chart ---
    if selected_category == 'All':
        pie_df = df[df['Category'] != 'All']['Region'].value_counts().reset_index()
        pie_df.columns = ['Region', 'Count']
        pie_fig = px.pie(
            pie_df,
            names='Region',
            values='Count',
            title=f"Regional Distribution",
            template='plotly_white'
        )
    else:
        region_dist = df[df['Category'] == selected_category]['Region'].value_counts().reset_index()
        region_dist.columns = ['Region', 'Count']
        pie_fig = px.pie(
            region_dist,
            names='Region',
            values='Count',
            title=f"Regional Distribution for {selected_category}",
            template='plotly_white'
        )

    # --- Box Plot ---
    box_fig = px.box(
        filtered_df,
        x='Category',
        y='Score',
        title="Score Distribution by Category",
        template='plotly_white'
    )
    box_fig.update_xaxes(tickangle=45)

    return summary_cards, bar_fig, pie_fig, box_fig


if __name__ == '__main__':
    # app.run(debug=True) # For development
    from waitress import serve
    serve(dash_app.server, host='0.0.0.0', port=8050)