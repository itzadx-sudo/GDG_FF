from dash import html, dcc
import orbit_viz

def render_user_dashboard(user):
    """The Cockpit: User-specific telemetry view."""
    if not user:
        return html.Div("Initializing telemetry stream...", style={'padding': '100px', 'textAlign': 'center'})

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4("ORBIT MATCH", style={'textAlign': 'center', 'fontSize': '0.7rem', 'letterSpacing': '2px', 'opacity': '0.5'}),
                    dcc.Graph(figure=orbit_viz.create_orbit_gauge(user['score']), config={'displayModeBar': False})
                ], className='glass-panel', style={'marginBottom': '2rem'}),
                
                html.Div([
                    html.H4("WEAKNESS DETECTED", style={'margin': 0, 'color': '#ef4444', 'fontSize': '1rem'}),
                    html.P(user['weakness'], style={'fontSize': '0.85rem', 'fontStyle': 'italic', 'margin': '15px 0'}),
                    html.Button("FIX SYSTEM", className='btn-action', id='btn-terminal-trigger', 
                                style={'width': '100%', 'background': '#ef4444'})
                ], className='glass-panel', style={'background': 'rgba(239, 68, 68, 0.05)', 'borderColor': 'rgba(239, 68, 68, 0.2)'})
            ], style={'width': '330px'}),
            
            html.Div([
                html.Div([
                    html.H3("TECHNICAL TELEMETRY", style={'marginTop': 0}),
                    dcc.Graph(figure=orbit_viz.create_telemetry_chart(user['matrix']), config={'displayModeBar': False})
                ], className='glass-panel', style={'height': '100%'})
            ], style={'flex': 1})
        ], style={'display': 'flex', 'gap': '2.5rem', 'padding': '4rem', 'maxWidth': '1300px', 'margin': '0 auto'})
    ], className='animate-page')