import dash
from dash import html, dcc, Input, Output, State, callback, ctx, ALL, MATCH
import dash_iconify as di
import sys
import os
import base64
import io

# --- CORE INTEGRATION ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from Core import database, vault
    # Initialize DB on startup
    database.init_db()
except ImportError:
    print("Warning: Core modules not found. Running in UI-only mode.")

# --- MODULE IMPORTS ---
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
    
    # Navigation Bar
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
    
    # Persistence Layer
    html.Div([
        html.Button(id={'type': 'auth-trigger', 'index': 'submit'}, style={'display':'none'}),
        html.Button(id={'type': 'auth-trigger', 'index': 'test'}, style={'display':'none'}),
        html.Button(id={'type': 'auth-trigger', 'index': 'switch'}, style={'display':'none'}),
        html.Button(id={'type': 'nav-trigger', 'index': 'hero'}, style={'display':'none'}),
        
        # Auth Inputs
        dcc.Input(id={'type': 'auth-input', 'index': 'email'}, value="", style={'display':'none'}),
        dcc.Input(id={'type': 'auth-input', 'index': 'pass'}, value="", style={'display':'none'}),
        dcc.Input(id={'type': 'auth-input', 'index': 'confirm'}, value="", style={'display':'none'}),
        
        html.Button(id='btn-submit-uplink', style={'display':'none'}),
        html.Button(id='btn-repair-trigger', style={'display':'none'}), # Trigger for Terminal
        html.Button(id='btn-ai-chat', style={'display':'none'}),
        html.Button(id='btn-close-modal', style={'display':'none'}),
        html.Button(id='btn-terminal-submit', style={'display':'none'}), # For Terminal Input
        
        html.Div(id={'type': 'apply-btn', 'index': 'init'}, style={'display':'none'})
    ]),

    # Main Dynamic Content Container
    html.Div(id='router-outlet'),
    
    # Modal Portal
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
    
    if isinstance(tid, dict) and tid.get('type') == 'auth-trigger':
        action = tid.get('index')
        
        # SWITCH MODE (Login <-> Signup)
        if action == 'switch':
            return 'auth', ('signup' if current_auth == 'login' else 'login'), dash.no_update
        
        # SUBMIT OR TEST
        if action == 'submit' or action == 'test':
            # Retrieve inputs (The 'ALL' pattern returns list, filter for non-empty or by index)
            email = next((v for v in auth_inputs if v and '@' in v), "")
            password = auth_inputs[1] if len(auth_inputs) > 1 else ""
            
            # --- BYPASS MODE ---
            if action == 'test':
                email = "guest.pilot@orbit.net" 
                user_data = orbit_logic.analyze_candidate("Guest Pilot", "Systems, Orbital Mechanics")
                return 'user-dashboard', 'login', user_data

            # --- REAL DB AUTHENTICATION ---
            if current_auth == 'login':
                user_record = database.login_user(email, password)
                if user_record:
                    is_admin = user_record.get('role') == 'COMMANDER' or email.lower().endswith("@space42.com")
                    user_data = {
                        "name": email.split('@')[0], 
                        "email": email, 
                        "score": user_record.get('match_score', 0),
                        "weakness": user_record.get('weakness_focus', 'None Detected'),
                        "matrix": [85, 90, 75, 80, 95] 
                    }
                    return ('admin-dashboard' if is_admin else 'user-dashboard'), 'login', user_data
                return dash.no_update, dash.no_update, dash.no_update

            elif current_auth == 'signup':
                if email and password:
                    database.add_candidate(email, password, "N/A", "N/A", "PILOT")
                    user_data = orbit_logic.analyze_candidate(email.split('@')[0], "General")
                    return 'user-dashboard', 'login', user_data

    # Nav Triggers
    if isinstance(tid, dict) and tid.get('type') == 'nav-trigger':
        if tid.get('index') == 'hero': return 'missions', 'login', dash.no_update

    # Navbar Links
    if isinstance(tid, dict) and tid.get('type') == 'nav-link':
        idx = tid.get('index')
        if idx == 'missions': return 'missions', 'login', dash.no_update
        if idx == 'fleet': return 'landing', 'login', dash.no_update
        if idx == 'auth': return 'auth', 'login', dash.no_update

    if tid == 'logo-home': 
        return 'landing', 'login', dash.no_update
    
    return dash.no_update, dash.no_update, dash.no_update


@callback(
    Output('modal-portal', 'children'),
    Output('nav-state', 'data', allow_duplicate=True),
    Output('user-store', 'data', allow_duplicate=True),
    Input({'type': 'apply-btn', 'index': ALL}, 'n_clicks'),
    Input('btn-submit-uplink', 'n_clicks'),
    Input('btn-ai-chat', 'n_clicks'),
    Input('btn-repair-trigger', 'n_clicks'), # TERMINAL TRIGGER
    Input('btn-close-modal', 'n_clicks'),
    Input('btn-terminal-submit', 'n_clicks'),
    State('uplink-upload', 'contents'),
    State('uplink-upload', 'filename'),
    State('reg-name', 'value'),
    State('reg-email', 'value'),
    State('terminal-input', 'value'),
    State('user-store', 'data'),
    prevent_initial_call=True
)
def handle_modal_system(apply_clicks, uplink_clicks, ai_clicks, repair_clicks, close_clicks, term_submit, 
                       file_content, file_name, reg_name, reg_email, term_input, user_data):
    
    tid = ctx.triggered_id

    # 1. Close Modal Logic
    if tid == 'btn-close-modal':
        return None, dash.no_update, dash.no_update

    # 2. AI Chat
    if tid == 'btn-ai-chat':
        return html.Div([
            html.Div([
                html.H3("AI FLIGHT COMPANION", style={'marginBottom': '1rem'}),
                html.Div("How can I assist with your mission parameters today?", 
                        style={'fontFamily': 'JetBrains Mono', 'color': '#94a3b8', 'marginBottom': '20px'}),
                dcc.Textarea(className='orbit-input', style={'height': '100px'}, placeholder="Enter query..."),
                html.Button("TRANSMIT", className='btn-action', style={'width': '100%'}),
                html.Button("CLOSE", id='btn-close-modal', 
                           style={'background': 'none', 'border': 'none', 'color': 'white', 'marginTop': '10px', 'width': '100%', 'cursor': 'pointer'})
            ], className='glass-panel', style={'maxWidth': '400px', 'width': '90%', 'position': 'relative', 'zIndex': '10001'})
        ], className='modal-overlay'), dash.no_update, dash.no_update

    # 3. Open Uplink Modal (Apply)
    if isinstance(tid, dict) and tid.get('type') == 'apply-btn':
        return html.Div([
            html.Div([
                html.H2("PERSONNEL UPLINK", style={'fontWeight':'900', 'marginBottom':'2rem'}),
                dcc.Input(id='reg-name', placeholder="Legal Identity", className='orbit-input'),
                dcc.Input(id='reg-email', placeholder="Secure Node (Email)", className='orbit-input'),
                
                # UPLOAD COMPONENT
                dcc.Upload(
                    id='uplink-upload',
                    children=html.Div([
                        di.DashIconify(icon="mdi:cloud-upload", width=40, color="#3b82f6"),
                        html.P("Drag Resume PDF or Click to Select", style={'marginTop': '10px', 'opacity': 0.7})
                    ]),
                    style={
                        'width': '100%', 'height': '120px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '15px',
                        'textAlign': 'center', 'margin': '20px 0', 'borderColor': 'rgba(255,255,255,0.2)',
                        'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center',
                        'cursor': 'pointer'
                    },
                    multiple=False
                ),
                
                html.Button("INITIATE SEQUENCE", id='btn-submit-uplink', className='btn-action', style={'width':'100%'}),
                html.Button("CANCEL", id='btn-close-modal', style={'width':'100%', 'marginTop':'10px', 'background':'none', 'border':'none', 'color':'#94a3b8', 'cursor':'pointer'})
            ], className='glass-panel', style={'maxWidth':'500px', 'width':'95%'})
        ], className='modal-overlay'), dash.no_update, dash.no_update

    # 4. Handle Uplink Submission (Redirect to Dashboard)
    if tid == 'btn-submit-uplink':
        # Simulate parsing delay or logic here
        # In real world: parse 'file_content' (base64) -> extract text -> orbit_logic.analyze()
        if reg_name:
            new_user = orbit_logic.analyze_candidate(reg_name, "Parsed Skills")
            # If DB is active, save here: database.add_candidate(reg_email, "temp123", file_name, "path", "PILOT")
            return None, 'user-dashboard', new_user
        return dash.no_update, dash.no_update, dash.no_update

    # 5. Handle Repair Trigger -> OPEN TERMINAL (The Boss Fight)
    if tid == 'btn-repair-trigger':
        return html.Div([
            html.Div([
                html.H3("SYSTEM DIAGNOSTIC TERMINAL", style={'fontFamily': 'JetBrains Mono', 'color': '#ef4444', 'marginBottom': '1rem'}),
                html.Div([
                    html.P("> ALERT: Satellite drift detected in Sector 7G.", style={'margin': '5px 0'}),
                    html.P("> PID Controller failing. P-gain is critically low.", style={'margin': '5px 0'}),
                    html.P("> Enter command to recalibrate:", style={'margin': '5px 0', 'color': '#3b82f6'}),
                ], style={'fontFamily': 'JetBrains Mono', 'fontSize': '0.9rem', 'color': '#10b981', 'marginBottom': '20px'}),
                
                dcc.Input(id='terminal-input', placeholder="root@orbit:~#", className='orbit-input', 
                         style={'fontFamily': 'JetBrains Mono', 'border': '1px solid #10b981', 'color': '#10b981'}),
                
                html.Button("EXECUTE", id='btn-terminal-submit', className='btn-action', 
                           style={'width': '100%', 'marginTop': '15px', 'background': '#10b981', 'color': 'black'}),
                html.Button("ABORT", id='btn-close-modal', style={'width':'100%', 'marginTop':'10px', 'background':'none', 'border':'none', 'color':'#ef4444', 'cursor':'pointer'})
            ], className='glass-panel', style={'maxWidth':'600px', 'width':'95%', 'background': 'black', 'border': '1px solid #ef4444'})
        ], className='modal-overlay'), dash.no_update, dash.no_update

    # 6. Handle Terminal Command Execution
    if tid == 'btn-terminal-submit':
        # Simple keyword check
        success = term_input and any(x in term_input.lower() for x in ['gain', 'pid', 'reset', 'calibrat'])
        
        result_color = "#10b981" if success else "#ef4444"
        result_msg = "> SUCCESS: P-Gain stabilized. Drift corrected." if success else "> ERROR: Command invalid. System critical."
        
        return html.Div([
            html.Div([
                html.H3("TERMINAL OUTPUT", style={'fontFamily': 'JetBrains Mono', 'color': result_color, 'marginBottom': '1rem'}),
                html.P(result_msg, style={'fontFamily': 'JetBrains Mono', 'color': 'white', 'fontSize': '1.1rem'}),
                html.Button("CLOSE TERMINAL", id='btn-close-modal', className='btn-action', style={'marginTop': '20px', 'width': '100%'})
            ], className='glass-panel', style={'maxWidth':'500px', 'width':'95%', 'textAlign': 'center'})
        ], className='modal-overlay'), dash.no_update, dash.no_update

    return None, dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run(debug=True, port=8051)