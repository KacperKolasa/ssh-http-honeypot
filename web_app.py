from pathlib import Path
import os
from dash import Dash, html, dcc, dash_table
import plotly.express as px
from dashboard_data_parser import *

# CONSTANTS & CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "honeypot" / "log_files"
CREDS_LOG = LOG_DIR / "creds_audits.log"
CMD_LOG = LOG_DIR / "cmd_audits.log"
HTTP_LOG = LOG_DIR / "http_audit.log"

# Load environment vars
from dotenv import load_dotenv
ENV_PATH = Path("public.env")
load_dotenv(dotenv_path=ENV_PATH)

COUNTRY_LOOKUP_ENABLED = os.getenv("COUNTRY", "False") == "True"

# DATA INGESTION
creds_df = parse_creds_audits_log(CREDS_LOG)
cmd_df   = parse_cmd_audits_log(CMD_LOG)
http_df  = parse_http_audits_log(HTTP_LOG)

# Pre-compute Top-10 lists
TOP_IP    = top_10_calculator(creds_df, "ip_address")
TOP_USERS = top_10_calculator(creds_df, "username")
TOP_PASS  = top_10_calculator(creds_df, "password")
TOP_CMDS  = top_10_calculator(cmd_df,   "Command")
TOP_HTTP_IPS   = top_10_calculator(http_df, "ip_address")
TOP_HTTP_USERS = top_10_calculator(http_df, "username")
TOP_HTTP_PASS  = top_10_calculator(http_df, "password")

if COUNTRY_LOOKUP_ENABLED:
    country_df = ip_to_country_code(creds_df)
    TOP_COUNTRY = top_10_calculator(country_df, "Country_Code")
else:
    TOP_COUNTRY = None

# INITIALISE DASH
app = Dash(__name__, assets_folder="assets")
app.title = "HONEYPOT"

# HELPER COMPONENTS

def bar_graph(df, x_col: str, y_col: str = "count") -> dcc.Graph:
    fig = px.bar(df, x=x_col, y=y_col)
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    return dcc.Graph(
        figure=fig,
        className="graph-item",
        style={"height": "350px"}
    )


def build_table(df, column_name: str, column_id: str, *, rows: int = 10) -> dash_table.DataTable:
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": column_name, "id": column_id}],
        page_size=rows,
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#1e1e1e",
            "color": "var(--accent)",
            "fontWeight": "bold",
            "textAlign": "left"
        },
        style_cell={
            "backgroundColor": "#1e1e1e",
            "color": "var(--fg)",
            "textAlign": "left",
            "whiteSpace": "normal",
            "height": "auto"
        },
    )

# LAYOUT
app.layout = html.Div(
    className="container",
    children=[
        html.Img(src="assets/images/honeypot-logo-white.png", className="logo"),
        html.H2("SSH Honeypot Top 10", className="section-title"),
        html.Div([
            html.Div(bar_graph(TOP_IP, "ip_address"), className="grid-item"),
            html.Div(bar_graph(TOP_USERS, "username"),   className="grid-item"),
            html.Div(bar_graph(TOP_PASS, "password"),   className="grid-item"),
        ], className="graphs-grid"),

        html.Div([
            html.Div(bar_graph(TOP_CMDS, "Command"), className="grid-item"),
            html.Div(
                bar_graph(TOP_COUNTRY, "Country_Code") if TOP_COUNTRY is not None else html.Div("Country disabled", className="disabled"),
                className="grid-item"
            ),
        ], className="graphs-grid"),

        html.Hr(),
        html.H2("HTTP Honeypot Top 10", className="section-title"),
        html.Div([
            html.Div(bar_graph(TOP_HTTP_IPS,   "ip_address"), className="grid-item"),
            html.Div(bar_graph(TOP_HTTP_USERS, "username"),   className="grid-item"),
            html.Div(bar_graph(TOP_HTTP_PASS,  "password"),   className="grid-item"),
        ], className="graphs-grid"),

        html.H2("Intelligence Data", className="section-title"),
        html.Div([
            html.Div(build_table(creds_df, "IP Address", "ip_address"), className="table-item"),
            html.Div(build_table(creds_df, "Usernames",  "username"),   className="table-item"),
            html.Div(build_table(creds_df, "Passwords",  "password"),   className="table-item"),
        ], className="tables-grid"),
    ]
)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")