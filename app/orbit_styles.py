def get_orbit_css():
    """Consolidated cinematic CSS with animations, pill-nav, and dashboard styling."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --space-dark: #020617;
        --orbit-blue: #3b82f6;
        --orbit-purple: #8b5cf6;
        --orbit-cyan: #06b6d4;
        --orbit-red: #ef4444;
        --glass-bg: rgba(15, 23, 42, 0.7);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-main: #f8fafc;
        --text-dim: #94a3b8;
    }

    body {
        background-color: var(--space-dark) !important;
        color: var(--text-main) !important;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif !important;
        overflow-x: hidden;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }

    .animate-page {
        animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }

    .space-background {
        position: fixed; inset: 0;
        background: radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.1) 0%, transparent 45%),
                    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.1) 0%, transparent 45%);
        z-index: -2;
    }

    .star-layer {
        position: fixed; inset: 0;
        background-image: radial-gradient(#ffffff 1px, transparent 1px);
        background-size: 80px 80px;
        opacity: 0.1; z-index: -1;
    }

    /* Pill Navigation Bar */
    .nav-container {
        position: fixed; top: 25px; left: 0; right: 0;
        display: flex; justify-content: center; z-index: 9999;
        pointer-events: none;
    }

    .pill-nav {
        pointer-events: auto;
        display: flex; align-items: center;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        border-radius: 100px;
        padding: 8px 10px 8px 30px;
        gap: 15px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }

    .nav-item {
        color: var(--text-main); font-weight: 700; font-size: 0.8rem;
        text-transform: uppercase; letter-spacing: 1.5px;
        cursor: pointer; opacity: 0.6; transition: 0.3s;
        border: none; background: none; outline: none;
    }

    .nav-item:hover { opacity: 1; color: var(--orbit-blue); }

    .nav-auth-btn {
        background: linear-gradient(135deg, var(--orbit-blue), var(--orbit-purple));
        color: white; border: none; padding: 10px 25px; border-radius: 100px;
        font-weight: 800; font-size: 0.75rem; cursor: pointer;
        text-transform: uppercase; letter-spacing: 1px;
    }

    .brand-id {
        font-weight: 900; font-size: 1.1rem; letter-spacing: -1.5px;
        margin-right: 15px; border-right: 1px solid var(--glass-border);
        padding-right: 25px; cursor: pointer;
    }

    .glass-panel {
        background: var(--glass-bg); backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border); border-radius: 1.5rem;
        padding: 2rem; box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
        display: flex;
        flex-direction: column;
        /* Crucial fix for vertical expansion loop */
        min-height: 0; 
        max-height: 100%;
        overflow: hidden;
    }
    
    .glass-panel:hover {
        border-color: rgba(59, 130, 246, 0.3);
    }

    .orbit-input {
        background: rgba(255, 255, 255, 0.04); border: 1px solid var(--glass-border);
        border-radius: 1rem; padding: 1.1rem; color: white;
        width: 100%; margin-bottom: 1.2rem; outline: none; transition: 0.3s;
        box-sizing: border-box; /* Prevent padding from breaking width */
    }
    
    .orbit-input:focus {
        border-color: var(--orbit-blue);
        background: rgba(59, 130, 246, 0.05);
    }

    .btn-action {
        background: linear-gradient(135deg, var(--orbit-blue), var(--orbit-purple));
        color: white; border: none; padding: 1rem 2rem; border-radius: 100px;
        font-weight: 800; cursor: pointer; text-transform: uppercase;
        font-size: 0.8rem; letter-spacing: 1px; transition: 0.3s;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
    }
    
    .btn-action:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(59, 130, 246, 0.5);
    }

    /* AI FLOATING ACTION BUTTON (FAB) */
    .ai-fab {
        position: fixed;
        bottom: 40px;
        right: 40px;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--orbit-blue), var(--orbit-purple));
        border: none;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
        cursor: pointer;
        z-index: 9000;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: pulse-glow 3s infinite;
    }

    .ai-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6);
    }

    .terminal-window {
        background: #000; border: 1px solid var(--orbit-blue);
        border-radius: 1rem; font-family: 'JetBrains Mono', monospace;
        padding: 1.5rem; height: 350px; overflow-y: auto; color: var(--orbit-cyan);
    }

    .modal-overlay {
        position: fixed; inset: 0; z-index: 10000;
        background: rgba(0,0,0,0.85); backdrop-filter: blur(15px);
        display: flex; align-items: center; justify-content: center;
    }
    
    /* DASHBOARD GRID LAYOUT - CRITICAL FOR AESTHETICS */
    .widget-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
        width: 100%;
        align-items: start; /* Prevents stretching height infinitely */
    }

    .satellite-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--glass-border);
        padding: 2rem;
        border-radius: 1.5rem;
        transition: 0.3s;
    }
    
    .satellite-card:hover {
        background: rgba(255,255,255,0.06);
        transform: translateY(-5px);
    }
    
    .job-item {
        transition: 0.2s;
    }
    
    .job-item:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        padding-left: 15px !important;
    }
    
    /* Graph Container constraints */
    .graph-container {
        height: 300px;
        width: 100%;
        position: relative;
    }

    ._dash-loading { display: none; }
    """