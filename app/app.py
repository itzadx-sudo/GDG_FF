import dash
from dash import html, dcc, Input, Output, State, callback, ctx, ALL, MATCH
import dash_iconify as di

# --- CORE IMPORTS ---
import orbit_styles
import orbit_logic
import orbit_viz
import orbit_auth
import orbit_user_dashboard
import orbit_admin_dashboard

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Orbit Recruit | Space42"

# Safely inject the CSS from the style module
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{orbit_styles.get_orbit_css()}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# --- Main Layout ---
app.layout = html.Div([
    dcc.Store(id='nav-state', data='landing'),
    dcc.Store(id='auth-mode', data='login'),
    dcc.Store(id='user-store'),
    dcc.Store(id='term-log', data=[]),
    
    html.Div(className='space-background'),
    html.Div(className='star-layer'),
    
    # Navigation Bar - All links converted to Pattern Matching to prevent "nonexistent" errors
    html.Nav([
        html.Div([
            html.Span("ORBIT", className='brand-id'),
            html.Span("RECRUIT", className='brand-id', style={'color': '#3b82f6', 'marginLeft': '-20px'}),
        ], style={'cursor': 'pointer'}, id='logo-home'),
        
        html.Div([
            html.Button("ACTIVE MISSIONS", id={'type': 'nav-link', 'index': 'missions'}, className='nav-item'),
            html.Button("THE FLEET", id={'type': 'nav-link', 'index': 'fleet'}, className='nav-item'),
            html.Button("SIGN IN", id={'type': 'nav-link', 'index': 'auth'}, className='nav-auth-btn', style={'marginLeft': '20px'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '15px'})
    ], className='navbar', style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '1rem 5%', 'background': 'rgba(2, 6, 23, 0.8)', 'backdropFilter': 'blur(15px)',
        'borderBottom': '1px solid rgba(255, 255, 255, 0.1)', 'position': 'sticky', 'top': 0, 'zIndex': 1000
    }),
    
    # Persistence Layer: Prevents "nonexistent object" errors by pre-registering IDs
    html.Div([
        # Hidden elements ensure Dash registers the callback signatures on boot
        html.Button(id={'type': 'auth-trigger', 'index': 'submit'}, style={'display':'none'}),
        html.Button(id={'type': 'auth-trigger', 'index': 'test'}, style={'display':'none'}),
        html.Button(id={'type': 'auth-trigger', 'index': 'switch'}, style={'display':'none'}),
        html.Button(id={'type': 'nav-trigger', 'index': 'hero'}, style={'display':'none'}),
        
        # Auth inputs are now pattern-matched to prevent errors when switching pages
        dcc.Input(id={'type': 'auth-input', 'index': 'email'}, value="", style={'display':'none'}),
        dcc.Input(id={'type': 'auth-input', 'index': 'pass'}, value="", style={'display':'none'}),
        
        html.Button(id='btn-submit-uplink', style={'display':'none'}),
        html.Button(id='btn-terminal-trigger', style={'display':'none'}),
        html.Div(id={'type': 'apply-btn', 'index': 'init'}, style={'display':'none'})
    ]),

    # Main Dynamic Content Container
    html.Div(id='router-outlet'),
    
    # Modal Portal for Uplink
    html.Div(id='modal-portal')

], id='app-root')

# --- Layout Renderers ---

def render_landing():
    fleet = orbit_logic.get_fleet()
    
    return html.Div([
        # Hero Section
        html.Div([
            html.Div([
                html.Span("ORBITAL INFRASTRUCTURE v4.0", style={'color': '#3b82f6', 'fontWeight': '800', 'letterSpacing': '4px', 'fontSize': '0.75rem'}),
                html.H1("ENGINEERING THE REACH OF HUMANITY.", 
                        style={'fontSize': '4rem', 'fontWeight': '900', 'lineHeight': '1.1', 'margin': '25px 0', 'letterSpacing': '-3px'}),
                html.P("Space42 is the global leader in autonomous satellite constellations and deep-space relay. Join the network that connects the modern universe.", 
                       style={'fontSize': '1.25rem', 'opacity': 0.6, 'maxWidth': '800px', 'lineHeight': '1.6', 'margin': '0 auto'}),
                # Navigation trigger for missions grid
                html.Button("EXPLORE ACTIVE MISSIONS", id={'type': 'nav-trigger', 'index': 'hero'}, className='btn-action', style={'marginTop': '50px', 'padding': '1.2rem 3.5rem'})
            ], style={'textAlign': 'center', 'padding': '80px 0'})
        ], className='animate-page'),

        # Fleet Section
        html.Div([
            html.H2("OUR CURRENT ASSETS", style={'textAlign': 'center', 'fontWeight': '900', 'marginBottom': '60px', 'fontSize': '2.5rem'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(di.DashIconify(icon="mdi:satellite-variant", width=35, color="#3b82f6"), style={'marginBottom': '15px'}),
                        html.H4(s['name'], style={'margin': '0 0 10px 0', 'fontWeight': '800'}),
                        html.P(s['type'], style={'opacity': 0.5, 'fontSize': '0.8rem'}),
                        html.Div([
                            html.Span(f"ALT: {s['alt']}", style={'fontWeight': '700', 'fontSize': '0.7rem'}),
                            html.Span(s['status'], style={'color': '#10b981', 'fontWeight': '900', 'fontSize': '0.7rem'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '30px', 'borderTop': '1px solid rgba(255,255,255,0.05)', 'paddingTop': '15px'})
                    ], className='satellite-card') for s in fleet
                ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '2.5rem'})
            ], className='glass-panel', style={'padding': '3rem', 'margin': '0 5%'})
        ], id='fleet-grid', className='animate-page', style={'paddingBottom': '100px'})
    ])

def render_missions_page():
    missions = orbit_logic.get_missions()
    return html.Div([
        html.Div([
            html.H2("OPEN ACTIVE MISSIONS", style={'textAlign': 'center', 'fontWeight': '900', 'marginBottom': '50px', 'fontSize': '2.5rem'}),
            html.Div([
                html.Div([
                    html.Span("MISSION STATUS: OPEN", style={'fontSize': '10px', 'fontWeight': '900', 'color': '#3b82f6', 'letterSpacing': '2px'}),
                    html.H3(m['title'], style={'margin': '1rem 0', 'fontSize': '1.6rem'}),
                    html.P(f"{m['dept']} | {m['loc']}", style={'color': '#94a3b8', 'fontSize': '0.85rem'}),
                    html.Button("INITIATE UPLINK", className='btn-action', style={'marginTop': '1.5rem', 'width': '100%'}, 
                                id={'type': 'apply-btn', 'index': m['id']})
                ], className='glass-panel', style={'padding': '2rem'}) for m in missions
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))', 'gap': '2.5rem', 'padding': '0 5%'})
        ], style={'padding': '80px 0'})
    ], className='animate-page')

# --- Callbacks ---

@callback(
    Output('router-outlet', 'children'),
    Input('nav-state', 'data'),
    Input('auth-mode', 'data'),
    State('user-store', 'data')
)
def router(state, auth_mode, user):
    if state == 'landing': return render_landing()
    if state == 'missions': return render_missions_page()
    if state == 'auth': return orbit_auth.render_auth_view(auth_mode)
    if state == 'admin-dashboard': return orbit_admin_dashboard.render_admin_dashboard()
    if state == 'user-dashboard': return orbit_user_dashboard.render_user_dashboard(user)
    return render_landing()

@callback(
    Output('nav-state', 'data'),
    Output('auth-mode', 'data'),
    Output('user-store', 'data'),
    Input('logo-home', 'n_clicks'),
    Input({'type': 'nav-link', 'index': ALL}, 'n_clicks'),
    Input({'type': 'nav-trigger', 'index': ALL}, 'n_clicks'),
    Input({'type': 'auth-trigger', 'index': ALL}, 'n_clicks'),
    State({'type': 'auth-input', 'index': ALL}, 'value'),
    State('auth-mode', 'data'),
    State('user-store', 'data'),
    prevent_initial_call=True
)
def handle_navigation(logo, nav_links, nav_triggers, auth_triggers, auth_inputs, current_auth, user_data):
    tid = ctx.triggered_id
    
    # 1. Handle Auth and Bypass Logic
    if isinstance(tid, dict) and tid.get('type') == 'auth-trigger':
        action = tid.get('index')
        
        if action == 'switch':
            return 'auth', ('signup' if current_auth == 'login' else 'login'), dash.no_update
        
        if action == 'submit' or action == 'test':
            # Extract email: find the first non-empty value in the pattern-matched list
            # (Matches both the dummy hidden input and the active auth input)
            email = next((v for v in auth_inputs if v), "")

            # Bypass Logic override
            if action == 'test':
                email = "commander@space42.com"
            
            is_admin = email.lower().endswith("@space42.com")
            
            # Generate session data if not exists
            if not user_data:
                user_data = orbit_logic.analyze_candidate("Authenticated Pilot", "Systems, Orbital Mechanics")
            
            return ('admin-dashboard' if is_admin else 'user-dashboard'), 'login', user_data

    # 2. Handle Navigation Triggers (Hero Buttons)
    if isinstance(tid, dict) and tid.get('type') == 'nav-trigger':
        if tid.get('index') == 'hero':
            return 'missions', 'login', dash.no_update

    # 3. Handle Navbar Link Clicks
    if isinstance(tid, dict) and tid.get('type') == 'nav-link':
        idx = tid.get('index')
        if idx == 'missions': return 'missions', 'login', dash.no_update
        if idx == 'fleet': return 'landing', 'login', dash.no_update
        if idx == 'auth': return 'auth', 'login', dash.no_update

    # 4. Handle Logo Home
    if tid == 'logo-home': 
        return 'landing', 'login', dash.no_update
    
    return dash.no_update, dash.no_update, dash.no_update

@callback(
    Output('modal-portal', 'children'),
    Input({'type': 'apply-btn', 'index': ALL}, 'n_clicks'),
    Input('btn-submit-uplink', 'n_clicks'),
    State('user-store', 'data'),
    prevent_initial_call=True
)
def handle_modal(apply_clicks, submit_clicks, user):
    if ctx.triggered_id == 'btn-submit-uplink' and user: return None
    if any(apply_clicks):
        return html.Div([
            html.Div([
                html.H2("PERSONNEL UPLINK", style={'fontWeight':'900', 'marginBottom':'2rem'}),
                dcc.Input(id='reg-name', placeholder="Legal Identity", className='orbit-input'),
                dcc.Input(id='reg-email', placeholder="Secure Node (Email)", className='orbit-input'),
                dcc.Textarea(id='reg-skills', placeholder="Paste Technical Telemetry...", className='orbit-input', style={'height':'120px'}),
                html.Button("SYNC DATA", id='btn-submit-uplink', className='btn-action', style={'width':'100%'})
            ], className='glass-panel', style={'maxWidth':'500px', 'width':'95%'})
        ], className='modal-overlay')
    return None

if __name__ == '__main__':
    app.run(debug=True, port=8051)