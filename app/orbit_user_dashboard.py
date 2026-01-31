from dash import html, dcc
import dash_iconify as di
import orbit_viz

def render_user_dashboard(user):
    """The Cockpit: Enhanced telemetry view with Widgets and AI Fab."""
    if not user:
        return html.Div("Initializing telemetry stream...", style={'padding': '100px', 'textAlign': 'center'})

    # Added IDs to jobs to support clickable callbacks
    jobs = [
        {"id": "job-101", "title": "Exo-Miner V", "loc": "Asteroid Belt", "pay": "4,500 CR", "type": "Engineering"},
        {"id": "job-102", "title": "Void Sentinel", "loc": "Deep Field", "pay": "8,200 CR", "type": "Security"},
        {"id": "job-103", "title": "Relay Tech", "loc": "Lagrange Pt 4", "pay": "6,000 CR", "type": "Ops"}
    ]

    return html.Div([
        # 1. Floating AI Chat Button
        html.Button([
            di.DashIconify(icon="mdi:robot-outline", width=35, color="white")
        ], className='ai-fab', id='btn-ai-chat'),

        # 2. Header
        html.Div([
            html.H1(f"WELCOME BACK, {user.get('name', 'PILOT').upper()}", 
                   style={'fontWeight': '900', 'letterSpacing': '-2px', 'marginBottom': '0.5rem'}),
            html.P("ORBITAL UPLINK ESTABLISHED. SYSTEMS NOMINAL.", style={'opacity': 0.6, 'fontFamily': 'JetBrains Mono'})
        ], style={'marginBottom': '3rem', 'borderBottom': '1px solid rgba(255,255,255,0.1)', 'paddingBottom': '2rem'}),

        # 3. Main Widget Grid
        html.Div([
            # Column 1: Match Protocol
            html.Div([
                html.H4("MATCH PROTOCOL", style={'textAlign': 'center', 'letterSpacing': '2px', 'opacity': '0.7'}),
                # WRAPPED IN CONTAINER TO FIX EXPANSION
                html.Div([
                    dcc.Graph(figure=orbit_viz.get_orbit_gauge(user['score']), config={'displayModeBar': False, 'responsive': True}, style={'height': '100%'})
                ], className='graph-container'),
                
                html.Div([
                    html.Button("UPDATE BIO-DATA", className='btn-action', style={'width': '100%', 'marginTop': '1rem'})
                ], style={'marginTop': '2rem'})
            ], className='glass-panel'),

            # Column 2: Telemetry
            html.Div([
                html.Div([
                    html.H3("TECHNICAL TELEMETRY", style={'marginTop': 0}),
                    # WRAPPED IN CONTAINER
                    html.Div([
                        dcc.Graph(figure=orbit_viz.get_skill_matrix(user['matrix']), config={'displayModeBar': False, 'responsive': True}, style={'height': '100%'})
                    ], className='graph-container')
                ], className='glass-panel', style={'marginBottom': '2rem'}),

                # System Health
                html.Div([
                    html.Div([
                        di.DashIconify(icon="mdi:heart-pulse", width=25, color="#10b981"),
                        html.Span("LIFE SUPPORT: 98%", style={'fontWeight': 'bold', 'color': '#10b981'})
                    ], style={'display': 'flex', 'gap': '10px', 'alignItems': 'center', 'marginBottom': '10px'}),
                    html.Div([
                        di.DashIconify(icon="mdi:shield-check", width=25, color="#3b82f6"),
                        html.Span("HULL INTEGRITY: 100%", style={'fontWeight': 'bold', 'color': '#3b82f6'})
                    ], style={'display': 'flex', 'gap': '10px', 'alignItems': 'center'})
                ], className='glass-panel')
            ]),

            # Column 3: Alerts & Jobs
            html.Div([
                # System Alert (Updated to Critical Weakness Narrative)
                html.Div([
                    html.Div([
                        di.DashIconify(icon="mdi:alert-octagon", width=20, color="#ef4444"),
                        html.H4("CRITICAL WEAKNESS DETECTED", style={'margin': 0, 'color': '#ef4444', 'fontSize': '0.9rem', 'letterSpacing': '1px'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '15px'}),
                    
                    html.P([
                        "Diagnostic Scan indicates failure in: ",
                        html.Span(user['weakness'], style={'color': 'white', 'fontWeight': 'bold', 'textDecoration': 'underline'})
                    ], style={'fontSize': '0.9rem', 'fontFamily': 'JetBrains Mono', 'lineHeight': '1.6', 'color': '#94a3b8'}),
                    
                    html.Button("INITIATE REPAIR SEQUENCE", className='btn-action', id='btn-repair-trigger', 
                                style={'width': '100%', 'marginTop': '15px', 'background': 'linear-gradient(45deg, #ef4444, #b91c1c)', 'boxShadow': '0 0 15px rgba(239, 68, 68, 0.4)'})
                ], className='glass-panel', style={'background': 'rgba(239, 68, 68, 0.05)', 'borderColor': 'rgba(239, 68, 68, 0.3)'}),

                # Active Contracts Widget
                html.Div([
                    html.Div([
                        html.H4("AVAILABLE CONTRACTS", style={'margin': 0, 'fontSize': '0.9rem', 'letterSpacing': '1px'}),
                        html.Span("LIVE FEED", style={'fontSize': '0.6rem', 'background': '#10b981', 'color': 'black', 'padding': '2px 6px', 'borderRadius': '4px', 'fontWeight': 'bold'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '15px'}),
                    
                    # Job List - Now Interactive Buttons
                    html.Div([
                        html.Button([
                            html.Div([
                                html.Span(job['title'], style={'fontWeight': '700', 'display': 'block', 'textAlign': 'left'}),
                                html.Span(f"{job['loc']} • {job['type']}", style={'fontSize': '0.75rem', 'opacity': 0.6, 'textAlign': 'left', 'display': 'block'})
                            ]),
                            html.Span(job['pay'], style={'color': '#fbbf24', 'fontWeight': 'bold', 'fontFamily': 'JetBrains Mono', 'fontSize': '0.8rem'})
                        ], id={'type': 'job-card', 'index': job['id']}, className='job-item', style={
                            'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                            'padding': '12px 10px', 'border': 'none', 'background': 'transparent', 'width': '100%',
                            'borderBottom': '1px solid rgba(255,255,255,0.05)',
                            'borderRadius': '8px', 'marginBottom': '5px', 'cursor': 'pointer'
                        }) for job in jobs
                    ]),
                    
                    html.Button("VIEW ALL CONTRACTS", style={
                        'width': '100%', 'marginTop': '15px', 'background': 'none', 'border': '1px solid rgba(255,255,255,0.2)',
                        'color': 'white', 'padding': '8px', 'borderRadius': '8px', 'cursor': 'pointer', 'fontSize': '0.7rem'
                    })
                ], className='glass-panel', style={'marginTop': '2rem'})
            ])
        ], className='widget-grid')

    ], className='animate-page', style={'padding': '2rem 5%', 'maxWidth': '1600px', 'margin': '0 auto'})