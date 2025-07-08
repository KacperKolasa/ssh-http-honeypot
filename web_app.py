# Import library dependencies.
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from pathlib import Path
from dotenv import load_dotenv
import os
from dashboard_data_parser import *
from honeypy import *

# Constants
base_dir = base_dir = Path(__file__).parent.parent
creds_audits_log_local_file_path = base_dir / 'ssh_honeypy' / 'log_files' / 'creds_audits.log'
cmd_audits_log_local_file_path = base_dir / 'ssh_honeypy' / 'log_files' / 'cmd_audits.log'
http_audits_log_local_file_path = base_dir / 'ssh_honeypy' / 'log_files' / 'http_audit.log'
# Load dotenv() to capture environment variable.
dotenv_path = Path('public.env')
load_dotenv(dotenv_path=dotenv_path)

# Pass log files to dataframe conversion
creds_audits_log_df = parse_creds_audits_log(creds_audits_log_local_file_path)
cmd_audits_log_df = parse_cmd_audits_log(cmd_audits_log_local_file_path)
http_audits_log_df = parse_http_audits_log(http_audits_log_local_file_path)

# Pass dataframes to top_10 calculator to get the top 10 values in the dataframe
top_ip_address = top_10_calculator(creds_audits_log_df, "ip_address")
top_usernames = top_10_calculator(creds_audits_log_df, "username")
top_passwords = top_10_calculator(creds_audits_log_df, "password")
top_cmds = top_10_calculator(cmd_audits_log_df, "Command")

top_http_ips       = top_10_calculator(http_audits_log_df, "ip_address")
top_http_usernames = top_10_calculator(http_audits_log_df, "username")
top_http_passwords = top_10_calculator(http_audits_log_df, "password")

# Pass IP address to calculate country code, then to the top_10 calculator
# get_ip_to_country = ip_to_country_code(creds_audits_log_df)
# top_country = top_10_calculator(get_ip_to_country, "Country_Code")

# Load the Cyborg theme from Python Dash Bootstrap
load_figure_template(["cyborg"])
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css")

# honeypot logo for dashboard
image = 'assets/images/honeypot-logo-white.png'

# Declare Dash App, apply CYBORG theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc_css])
# Provide web page title
app.title = "HONEYPOT"

# Set the value to True in (public.env) if you want country code lookup as default
country = os.getenv('COUNTRY')
# Function to get country code lookup if country = True
def country_lookup(country):
    if country == 'True':
        get_ip_to_country = ip_to_country_code(creds_audits_log_df)
        top_country = top_10_calculator(get_ip_to_country, "Country_Code")
        message = dbc.Col(dcc.Graph(figure=px.bar(top_country, x="Country_Code", y='count')), style={'width': '33%', 'display': 'inline-block'})
    else:
        message = "No Country Panel Defined"
    return message

# Generate tables using DBC (Dash Bootstrap Component) library
tables = html.Div([
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "IP Address", 'id': 'ip_address'}],
                    style_table={'width': '100%', 'color': 'black'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "Usernames", 'id': 'username'}],
                    style_table={'width': '100%'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),
        
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "Passwords", 'id': 'password'}],
                    style_table={'width': '100%','justifyContent': 'center'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),       
        ])
])
# Apply dark theme to the tables
apply_table_theme = html.Div(
    [tables],
    className="dbc"
)
# Define web application layout
app.layout = dbc.Container([
    html.Div([html.Img(src=image, style={'height': '25%', 'width': '25%'})], style={'textAlign': 'center'}, className='dbc'),
    # Row 1 - 3 Top 10 Dashboards, IP Address, Usernames, and Passwords
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(top_ip_address, x="ip_address", y='count')), width=4),
        dbc.Col(dcc.Graph(figure=px.bar(top_usernames, x='username', y='count')), width=4),
        dbc.Col(dcc.Graph(figure=px.bar(top_passwords, x='password', y='count')), ),
    ], align='center', class_name='mb-4'),

    # Row 2: Top 10 Commands + Country Codes
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(top_cmds, x='Command', y='count')), style={'width': '33%', 'display': 'inline-block'}),
        country_lookup(country)
    ], align='center', class_name='mb-4'),

    # Row 3: Top 10 HTTP honeypot stats
    html.Hr(),  # a separator line
    html.H3("HTTP Honeypot Top 10", style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(top_http_ips, x='ip_address', y='count')), width=4),
        dbc.Col(dcc.Graph(figure=px.bar(top_http_usernames, x='username', y='count')), width=4),
      dbc.Col(dcc.Graph(figure=px.bar(top_http_passwords, x='password', y='count')), width=4),
  ], align='center', class_name='mb-4'),

    # Table Titles
    html.Div([
        html.H3(
            "Intelligence Data", 
            style={'textAlign': 'center', "font-family": 'Consolas, sans-serif', 'font-weight': 'bold'}, 
        ),
        ]),
    # Row 3: Tables. Usernames, Passwords, and IP Addresses
    apply_table_theme    
])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

