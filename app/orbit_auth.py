from dash import html, dcc

def render_auth_view(mode="login"):
    """High-tech login/signup interface with pattern-matching triggers."""
    is_login = mode == "login"
    
    # Auth fields use static IDs for State capture, but actions use Pattern Matching
    auth_fields = [
        dcc.Input(placeholder="Uplink Identifier (Email)", className='orbit-input', id='auth-email', type='email'),
        dcc.Input(placeholder="Security Sequence (Password)", className='orbit-input', type='password', id='auth-pass'),
    ]
    
    if not is_login:
        auth_fields.append(dcc.Input(placeholder="Confirm Security Sequence", className='orbit-input', type='password', id='auth-pass-confirm'))

    return html.Div([
        html.Div([
            html.Div([
                html.H2("SECURE LOGIN" if is_login else "ACCESS GRANTED", 
                        style={'fontWeight': '900', 'fontSize': '2.5rem', 'marginBottom': '0.5rem', 'letterSpacing': '-2px'}),
                html.P("Enter planetary credentials to sync with Space42." if is_login 
                       else "Create a new biological identity in the network.",
                       style={'opacity': 0.6, 'marginBottom': '2.5rem'}),
                
                html.Div(auth_fields),
                
                # Using Pattern Matching for triggers
                html.Button("INITIALIZE ACCESS" if is_login else "CREATE IDENTITY", 
                            id={'type': 'auth-trigger', 'index': 'submit'}, className='btn-action', 
                            style={'width': '100%', 'marginTop': '1rem'}),
                
                html.Button("BYPASS TELEMETRY (TEST MODE)", 
                            id={'type': 'auth-trigger', 'index': 'test'}, 
                            style={'width': '100%', 'marginTop': '12px', 'background': 'rgba(255,255,255,0.05)', 
                                   'border': '1px solid rgba(255,255,255,0.1)', 'color': '#94a3b8', 
                                   'padding': '12px', 'borderRadius': '50px', 'fontSize': '0.7rem', 
                                   'fontWeight': '800', 'cursor': 'pointer', 'letterSpacing': '1px'}),

                html.Div([
                    html.P("New to the sector?" if is_login else "Already verified?", 
                           style={'fontSize': '0.85rem', 'opacity': 0.5, 'margin': 0}),
                    html.Button("Switch Mode", id={'type': 'auth-trigger', 'index': 'switch'},
                                style={'background': 'none', 'border': 'none', 'color': '#3b82f6', 
                                       'fontWeight': '700', 'cursor': 'pointer', 'fontSize': '0.85rem', 
                                       'textDecoration': 'underline'})
                ], style={'marginTop': '2.5rem', 'display': 'flex', 'gap': '10px', 'justifyContent': 'center', 'alignItems': 'center'})
                
            ], className='glass-panel', style={'maxWidth': '450px', 'width': '95%'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'minHeight': '80vh'})
    ], id='auth-container', className='animate-page')