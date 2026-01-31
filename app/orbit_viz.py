import plotly.graph_objects as go

def get_orbit_gauge(score):
    """Creates the high-tech match score gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'font': {'color': 'white', 'size': 60, 'family': 'Space Grotesk'}},
        gauge={
            'axis': {'range': [0, 100], 'visible': False},
            'bar': {'color': "#3b82f6", 'thickness': 0.1},
            'bgcolor': "rgba(255,255,255,0.02)",
            'steps': [{'range': [0, score], 'color': "rgba(59, 130, 246, 0.2)"}],
            'threshold': {'line': {'color': "#3b82f6", 'width': 3}, 'thickness': 0.8, 'value': score}
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=20, r=20, t=20, b=20))
    return fig

def get_skill_matrix(values):
    """Creates the bar chart for candidate telemetry."""
    labels = ['LOGIC', 'MATH', 'CODE', 'SYSTEMS', 'PHYSICS']
    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker=dict(color='rgba(59, 130, 246, 0.5)', line=dict(color='#3b82f6', width=2))
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', family='Space Grotesk', size=10),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100]),
        xaxis=dict(showgrid=False),
        height=280, margin=dict(l=40, r=20, t=20, b=40)
    )
    return fig