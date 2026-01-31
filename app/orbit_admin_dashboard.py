from dash import html

def render_admin_dashboard():
    """Mission Control: High-level overview for @space42.com staff."""
    # Mock data for demonstration
    pilots = [
        {"name": "Commander Shepard", "email": "n7@spectre.gov", "score": 98, "status": "READY"},
        {"name": "Ellen Ripley", "email": "ripley@weyland.corp", "score": 95, "status": "READY"},
        {"name": "Kari Byron", "email": "kari@space42.com", "score": 88, "status": "STAFF"}
    ]
    
    rows = [html.Tr([
        html.Td(p['name'], style={'padding': '15px'}),
        html.Td(p['email']),
        html.Td(f"{p['score']}%"),
        html.Td(p['status'], style={'color': '#10b981', 'fontWeight': '800'})
    ], style={'borderBottom': '1px solid rgba(255,255,255,0.05)'}) for p in pilots]

    return html.Div([
        html.Div([
            html.H2("MISSION CONTROL", style={'fontWeight': '900', 'fontSize': '2.5rem', 'marginBottom': '2rem'}),
            html.Div([
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("NAME"), html.Th("UPLINK"), html.Th("SCORE"), html.Th("STATUS")
                    ])),
                    html.Tbody(rows)
                ], style={'width': '100%', 'textAlign': 'left', 'borderCollapse': 'collapse'})
            ], className='glass-panel')
        ], style={'padding': '4rem 8%'})
    ], className='animate-page')