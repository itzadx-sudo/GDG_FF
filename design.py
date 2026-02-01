def get_styles():
    # Returns the complete CSS stylesheet for the dashboard.
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');

    :root {
        --theme-color-primary: #4169E1;
        --theme-color-secondary: #5B8FF9;
        --theme-color-tertiary: #6B9FFF;
        --theme-shadow-color: rgba(65, 105, 225, 0.15);
        --theme-shadow-color-faint: rgba(65, 105, 225, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(65, 105, 225, 0.05) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(65, 105, 225, 0.04) 0%, rgba(91, 143, 249, 0.04) 50%, rgba(107, 159, 255, 0.04) 100%);
        --theme-text-accent: #4169E1;
        --theme-text-muted: rgba(30, 41, 59, 0.75);

        --sidebar-width-expanded: 260px;
        --sidebar-width-collapsed: 100px;
        --sidebar-margin: 20px;
        --sidebar-transition-speed: 0.4s;
        --sidebar-transition-timing: cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    #\\{\\"index\\"\\:\\"overview\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #4169E1; }
    #\\{\\"index\\"\\:\\"metrics\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #10B981; }
    #\\{\\"index\\"\\:\\"sentiment\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #A855F7; }
    #\\{\\"index\\"\\:\\"text\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #F97316; }
    #\\{\\"index\\"\\:\\"data\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #EAB308; }
    #\\{\\"index\\"\\:\\"results\\"\\,\\"type\\"\\:\\"nav-button\\"\\} { --nav-color-primary: #F472B6; }

    .theme-overview {
        --theme-color-primary: #4169E1;
        --theme-color-secondary: #5B8FF9;
        --theme-color-tertiary: #6B9FFF;
        --theme-shadow-color: rgba(65, 105, 225, 0.15);
        --theme-shadow-color-faint: rgba(65, 105, 225, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(65, 105, 225, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(65, 105, 225, 0.05) 0%, rgba(91, 143, 249, 0.05) 50%, rgba(107, 159, 255, 0.05) 100%);
        --theme-text-accent: #4169E1;
    }
    .theme-metrics {
        --theme-color-primary: #10B981;
        --theme-color-secondary: #22C55E;
        --theme-color-tertiary: #84CC16;
        --theme-shadow-color: rgba(16, 185, 129, 0.15);
        --theme-shadow-color-faint: rgba(16, 185, 129, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(16, 185, 129, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(34, 197, 94, 0.05) 50%, rgba(132, 204, 22, 0.05) 100%);
        --theme-text-accent: #10B981;
    }
    .theme-sentiment {
        --theme-color-primary: #A855F7;
        --theme-color-secondary: #D946EF;
        --theme-color-tertiary: #EC4899;
        --theme-shadow-color: rgba(168, 85, 247, 0.15);
        --theme-shadow-color-faint: rgba(168, 85, 247, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(168, 85, 247, 0.05) 0%, rgba(217, 70, 239, 0.05) 50%, rgba(236, 72, 153, 0.05) 100%);
        --theme-text-accent: #A855F7;
    }
    .theme-text {
        --theme-color-primary: #F97316;
        --theme-color-secondary: #F59E0B;
        --theme-color-tertiary: #EAB308;
        --theme-shadow-color: rgba(249, 115, 22, 0.15);
        --theme-shadow-color-faint: rgba(249, 115, 22, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(249, 115, 22, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(249, 115, 22, 0.05) 0%, rgba(245, 158, 11, 0.05) 50%, rgba(234, 179, 8, 0.05) 100%);
        --theme-text-accent: #F97316;
    }
    .theme-data {
        --theme-color-primary: #EAB308;
        --theme-color-secondary: #F59E0B;
        --theme-color-tertiary: #F97316;
        --theme-shadow-color: rgba(234, 179, 8, 0.15);
        --theme-shadow-color-faint: rgba(234, 179, 8, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(234, 179, 8, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(234, 179, 8, 0.05) 0%, rgba(245, 158, 11, 0.05) 50%, rgba(249, 115, 22, 0.05) 100%);
        --theme-text-accent: #EAB308;
    }

    .theme-results {
        --theme-color-primary: #F472B6;
        --theme-color-secondary: #EC4899;
        --theme-color-tertiary: #F9A8D4;
        --theme-shadow-color: rgba(244, 114, 182, 0.15);
        --theme-shadow-color-faint: rgba(244, 114, 182, 0.1);
        --theme-glow-faint: radial-gradient(circle, rgba(244, 114, 182, 0.08) 0%, transparent 70%);
        --theme-gradient-faint: linear-gradient(135deg, rgba(244, 114, 182, 0.05) 0%, rgba(236, 72, 153, 0.05) 50%, rgba(249, 168, 212, 0.05) 100%);
        --theme-text-accent: #F472B6;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes springPill {
        0% { transform: scale(0.8) translateX(-20px); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1) translateX(0); opacity: 1; }
    }
    @keyframes dropdownSlideDown {
        from { 
            opacity: 0; 
            transform: translateY(-10px) scaleY(0.95);
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scaleY(1);
        }
    }
    @keyframes filterFade {
        from { opacity: 1; }
        to { opacity: 0.6; }
    }
    @keyframes shine {
        0% { transform: translateX(-100%) skewX(-20deg); opacity: 0.1; }
        70% { transform: translateX(100%) skewX(-20deg); opacity: 0.05; }
        100% { transform: translateX(100%) skewX(-20deg); opacity: 0; }
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        box-sizing: border-box;
    }
    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow-x: hidden;
    }
    body {
        background: #f8f9fc !important;
        color: #0f172a !important;
        min-height: 100vh;
        position: relative;
    }

    #theme-wrapper::before {
        content: '';
        position: fixed;
        top: 0; 
        left: 0;
        width: 100vw; 
        height: 100vh;
        background: 
            radial-gradient(circle at 0% 0%, var(--theme-color-primary) 0%, transparent 40%),
            radial-gradient(circle at 100% 100%, var(--theme-color-secondary) 0%, transparent 40%);
        filter: blur(120px);
        opacity: 0.12;
        pointer-events: none;
        z-index: 0;
        transition: background 1.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    #theme-wrapper::after {
        content: '';
        display: block;
        position: fixed;
        top: 0; 
        left: 0;
        width: 100vw; 
        height: 100vh;
        background: 
            radial-gradient(circle at 100% 0%, var(--theme-color-secondary) 0%, transparent 40%),
            radial-gradient(circle at 0% 100%, var(--theme-color-primary) 0%, transparent 40%);
        filter: blur(120px);
        opacity: 0.12;
        pointer-events: none;
        z-index: 0;
        transition: background 1.5s cubic-bezier(0.23, 1, 0.32, 1);
    }

    #react-entry-point, ._dash-loading, .dash-spinner {
        background: transparent !important;
    }

    .sidebar-container {
        position: fixed;
        top: var(--sidebar-margin);
        left: var(--sidebar-margin);
        width: var(--sidebar-width-expanded);
        height: calc(100vh - (2 * var(--sidebar-margin)));
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.07), 0 0 0 1.5px rgba(255, 255, 255, 0.5) inset;
        border-radius: 30px;
        padding: 20px;
        z-index: 100;
        display: flex;
        flex-direction: column;
        transition: width var(--sidebar-transition-speed) var(--sidebar-transition-timing);
        animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 10px 20px 10px;
        border-bottom: 1px solid var(--theme-shadow-color-faint);
        margin-bottom: 20px;
        transition: justify-content var(--sidebar-transition-speed) var(--sidebar-transition-timing);
    }

    .sidebar-logo-text {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 0px;
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        transition: background 0.5s ease, opacity 0.3s ease, width 0.3s ease;
        opacity: 1;
        width: auto;
        overflow: hidden;
        white-space: nowrap;
    }

    .sidebar-toggle {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: var(--theme-text-muted);
        box-shadow: 0 4px 12px var(--theme-shadow-color-faint);
        transition: all 0.3s var(--sidebar-transition-timing);
        flex-shrink: 0;
    }

    .sidebar-toggle .dash-iconify {
        transition: none;
    }

    .sidebar-toggle:hover {
        color: var(--theme-text-accent);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 6px 16px var(--theme-shadow-color-faint);
        transform: scale(1.05);
    }

    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .nav-link {
        display: flex;
        align-items: center;
        padding: 14px 20px;
        border-radius: 22px;
        cursor: pointer;
        font-size: 15px;
        font-weight: 700;
        color: var(--theme-text-muted);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        opacity: 0.8;
        border: 1px solid transparent;
        overflow: hidden;
        white-space: nowrap;
    }

    .nav-icon {
        font-size: 20px;
        min-width: 24px;
        margin-right: 16px;
        transition: transform 0.3s var(--sidebar-transition-timing), 
                    margin-right var(--sidebar-transition-speed) var(--sidebar-transition-timing);
        color: var(--theme-text-muted);
    }

    .nav-text {
        transition: opacity 0.3s ease;
        opacity: 1;
    }

    .nav-link:hover, .nav-link.active {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(255,255,255,0.3) 100%);
        color: var(--nav-color-primary);
        opacity: 1;
        transform: translateX(5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }
    .nav-link.active {
        background: linear-gradient(135deg, var(--nav-color-primary) 0%, rgba(255, 255, 255, 0) 100%);
         background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.6) 100%);

        box-shadow: 0 10px 25px rgba(0,0,0,0.05), 0 0 0 1.5px var(--nav-color-primary) inset;
        border-color: transparent;
    }

    .nav-link:hover .nav-icon, .nav-link.active .nav-icon {
        color: var(--nav-color-primary);
    }
    .nav-link:hover .nav-icon {
        transform: scale(1.1);
    }

    .sidebar-container.collapsed .sidebar-header {
        justify-content: center;
    }

    .sidebar-container.collapsed {
        width: var(--sidebar-width-collapsed);
    }

    .sidebar-container.collapsed .sidebar-logo-text {
        opacity: 0;
        width: 0;
        overflow: hidden;
    }

    .sidebar-container.collapsed .sidebar-toggle .dash-iconify {
        transform: none;
    }

    .sidebar-container.collapsed .nav-text {
        opacity: 0;
        width: 0;
    }
    .sidebar-container.collapsed .nav-link {
        justify-content: center;
        padding-left: 0;
        padding-right: 0;
    }
    .sidebar-container.collapsed .nav-icon {
        margin-right: 0;
    }
    .sidebar-container.collapsed .nav-link:hover {
        transform: translateX(0px) scale(1.05);
    }

    .main-content-wrapper {
        margin-left: calc(var(--sidebar-width-expanded) + (2 * var(--sidebar-margin)));
        width: calc(100% - var(--sidebar-width-expanded) - (2 * var(--sidebar-margin)));
        position: relative;
        z-index: 1;
        transition: margin-left var(--sidebar-transition-speed) var(--sidebar-transition-timing),
                    width var(--sidebar-transition-speed) var(--sidebar-transition-timing);
    }
    .main-content-wrapper.collapsed {
        margin-left: calc(var(--sidebar-width-collapsed) + (2 * var(--sidebar-margin)));
        width: calc(100% - var(--sidebar-width-collapsed) - (2 * var(--sidebar-margin)));
    }

    .app-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
        padding-top: var(--sidebar-margin);
        animation: fadeIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        z-index: 1;
    }

    .main-header-wrapper {
        text-align: center;
        margin-bottom: 35px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 36px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.07), 0 0 0 1.5px rgba(255, 255, 255, 0.5) inset, 0 4px 16px var(--theme-shadow-color-faint);
        animation: slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        z-index: 1;

        display: grid;
        grid-template-rows: 1fr;

        transform: translateZ(0); 

        transition: grid-template-rows var(--sidebar-transition-speed) var(--sidebar-transition-timing),
                    opacity var(--sidebar-transition-speed) ease-out,
                    margin-bottom var(--sidebar-transition-speed) var(--sidebar-transition-timing),
                    border-width var(--sidebar-transition-speed) var(--sidebar-transition-timing);
        opacity: 1;
    }

    #theme-wrapper:not(.theme-overview) .main-header-wrapper {
        grid-template-rows: 0fr;
        opacity: 0;
        margin-bottom: 0;
        border-width: 0;
        overflow: hidden;
    }

    .main-header-content {
        overflow: hidden;
        padding: 55px 45px;
        transition: padding-top 0.6s cubic-bezier(0.86, 0, 0.07, 1),
                    padding-bottom 0.6s cubic-bezier(0.86, 0, 0.07, 1);
    }

    #theme-wrapper:not(.theme-overview) .main-header-content {
        padding-top: 0;
        padding-bottom: 0;
    }

    .main-title {
        font-size: 56px !important;
        font-weight: 900 !important;
        margin: 0 !important;
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 50%, var(--theme-color-tertiary) 100%);
        background-size: 200% 200%;
        animation: gradientFlow 6s ease infinite, slideInLeft 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s backwards;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1.8px;
        position: relative;
        z-index: 2;
        transition: background 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .main-subtitle {
        font-size: 19px !important;
        font-weight: 500 !important;
        color: rgba(71, 85, 105, 0.75) !important;
        margin: 14px 0 0 0 !important;
        letter-spacing: 0.2px;
        animation: slideInRight 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
        position: relative;
        z-index: 2;
    }

    .nav-button-container {
        display: none;
    }
    .nav-button {
        padding: 14px 28px !important;
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        border: none !important;
        border-radius: 22px !important;
        color: var(--theme-text-muted) !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        white-space: nowrap !important;
        display: inline-flex;
        align-items: center;
        outline: none;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.05), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset;
    }
    .nav-button:hover {
        color: var(--theme-text-accent) !important;
        transform: translateY(-4px) scale(1.02) !important;
        background: rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 10px 24px var(--theme-shadow-color-faint), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset !important;
    }
    .nav-button.active {
        color: var(--theme-text-accent) !important;
        box-shadow: 0 10px 28px var(--theme-shadow-color-faint), 0 0 0 1.5px var(--theme-color-primary) inset !important;
        transform: translateY(-3px) !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.75) 100%) !important;
    }

    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 28px;
        padding: 16px;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05), 0 0 0 1.5px rgba(255, 255, 255, 0.5) inset;
    }
    .pagination-container .nav-button {
        opacity: 1 !important;
        color: var(--theme-text-accent) !important;
        animation: none !important;
    }
    .pagination-container .nav-button:disabled {
        color: var(--theme-text-muted) !important;
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    .page-content {
        animation: fadeIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s backwards;
        min-height: 400px;
        position: relative;
        z-index: 1;
    }
    .section-header {
        font-size: 40px !important;
        font-weight: 900 !important;
        margin: 50px 0 30px 0 !important;
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 50%, var(--theme-color-tertiary) 100%);
        background-size: 200% 200%;
        animation: gradientFlow 8s ease infinite, slideInLeft 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1.2px;
        transition: background 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .page-content .section-header:first-of-type {
        margin-top: 0 !important;
    }
    .subsection-header {
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 40px 0 24px 0 !important;
        color: rgba(30, 41, 59, 0.85) !important;
        letter-spacing: -0.5px;
        animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
    }

    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 24px;
        margin: 35px 0;
        animation: fadeIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
    }
    .metric-card {
        padding: 34px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset, 0 4px 16px var(--theme-shadow-color-faint);
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--theme-glow-faint);
        background-size: 200% 200%;
        z-index: -1;
        transition: background 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 70%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shine 8s cubic-bezier(0.23, 1, 0.32, 1) infinite;
        z-index: 1;
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.01);
        background: rgba(255, 255, 255, 0.6);
        box-shadow: 0 30px 70px var(--theme-shadow-color), 0 0 0 1.5px var(--theme-color-primary) inset;
        border-color: rgba(255, 255, 255, 0.1);
    }
    .metric-label {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: rgba(100, 116, 139, 0.75) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        animation: fadeIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        white-space: nowrap;
        position: relative;
        z-index: 2;
    }
    .metric-value {
        font-size: 46px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 50%, var(--theme-color-tertiary) 100%);
        background-size: 200% 200%;
        animation: gradientFlow 8s ease infinite, slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s backwards;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2.5px;
        transition: background 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        z-index: 2;
    }

    .row {
        display: grid;
        gap: 28px;
        margin: 28px 0;
        animation: fadeIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
    }
    .col-4 { grid-column: span 4; }
    .col-6 { grid-column: span 6; }
    .col-8 { grid-column: span 8; }
    @media (min-width: 768px) {
        .row { grid-template-columns: repeat(12, 1fr); }
    }
    @media (max-width: 767px) {
        .row { grid-template-columns: 1fr; }
        .col-4, .col-6, .col-8 { grid-column: span 1; }
    }

    .chart-container {
        padding: 30px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset, 0 4px 16px var(--theme-shadow-color-faint);
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: pointer;
        animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    .chart-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--theme-glow-faint);
        background-size: 200% 200%;
        opacity: 0;
        transition: opacity 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        z-index: -1;
    }
    .chart-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 70%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shine 7.5s cubic-bezier(0.23, 1, 0.32, 1) infinite;
        z-index: 1;
        pointer-events: none;
    }
    .chart-container .js-plotly-plot, .chart-container .plotly {
        position: relative;
        z-index: 2;
    }
    .chart-container:hover::before {
        opacity: 1;
    }
    .chart-container:hover {
        transform: translateY(-8px) scale(1.005);
        background: rgba(255, 255, 255, 0.6);
        box-shadow: 0 30px 70px var(--theme-shadow-color), 0 0 0 1.5px var(--theme-color-primary) inset;
        border-color: rgba(255, 255, 255, 0.1);
    }

    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 26px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.04), 0 0 0 1px rgba(255, 255, 255, 0.6) inset;
        animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        z-index: 1;
    }
    .data-table th {
        padding: 20px 22px;
        background: rgba(65, 105, 225, 0.04);
        font-weight: 800 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        color: rgba(51, 65, 85, 0.75) !important;
        text-align: left;
        border-bottom: 1px solid rgba(65, 105, 225, 0.1);
    }
    .data-table td {
        padding: 18px 22px;
        font-size: 14px !important;
        color: rgba(30, 41, 59, 0.8) !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.01);
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
        font-weight: 700;
    }
    .data-table tbody td:last-child {
        color: rgba(30, 41, 59, 0.95) !important;
        font-weight: 800;
        background: linear-gradient(135deg, rgba(65, 105, 225, 0.05) 0%, rgba(91, 143, 249, 0.04) 100%);
    }
    .data-table tr:hover {
        background: rgba(65, 105, 225, 0.04);
        transform: scale(1.001);
    }
    .data-table tr:last-child td {
        border-bottom: none;
    }

    .Select-control, .Select-menu-outer, .Select-option {
        padding: 12px 16px !important;
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(30px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        color: rgba(30, 41, 59, 0.85) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.03), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset !important;
        outline: none !important;
    }
    .Select-control {
        min-height: 44px !important;
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.6) !important;
    }
    .Select-control:hover {
        background: rgba(255, 255, 255, 0.7) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 20px var(--theme-shadow-color-faint), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset !important;
    }
    .Select-control.is-open {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 12px 28px var(--theme-shadow-color), 0 0 0 1.5px rgba(255, 255, 255, 0.8) inset !important;
    }
    .Select-control.is-focused {
        background: rgba(255, 255, 255, 0.7) !important;
        border-color: var(--theme-color-primary) !important;
        box-shadow: 0 0 0 3px var(--theme-shadow-color-faint), 0 12px 28px var(--theme-shadow-color-faint) !important;
    }
    .Select-input input {
        color: rgba(30, 41, 59, 0.85) !important;
        font-weight: 600 !important;
        background: transparent !important;
        outline: none !important;
    }
    .Select-input input::placeholder {
        color: rgba(100, 116, 139, 0.5) !important;
    }
    .Select-menu {
        background: transparent !important;
        border-radius: 0 !important;
        border: none !important;
        box-shadow: none !important;
        margin-top: 8px !important;
    }
    .Select-menu-outer {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(40px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 55px var(--theme-shadow-color), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset !important;
        margin-top: 8px !important;
        padding: 0 !important;
        border-top: none !important;
        position: relative;
        z-index: 100 !important;
        animation: dropdownSlideDown 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        transform-origin: top center;
    }
    .Select-option {
        background: transparent !important;
        color: rgba(30, 41, 59, 0.75) !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.01) !important;
    }
    .Select-option:last-child {
        border-bottom: none !important;
    }
    .Select-option:hover {
        background: var(--theme-gradient-faint) !important;
        color: var(--theme-text-accent) !important;
        transform: translateX(4px);
        padding-left: 18px !important;
    }
    .Select-option.is-selected {
        background: var(--theme-gradient-faint) !important;
        color: var(--theme-text-accent) !important;
        font-weight: 700 !important;
        border-left: 3px solid var(--theme-color-primary) !important;
        padding-left: 13px !important;
    }
    .Select-option.is-focused {
        background: var(--theme-gradient-faint) !important;
        color: var(--theme-text-accent) !important;
    }
    .Select-arrow-zone {
        padding-right: 12px !important;
        color: var(--theme-color-primary) !important;
        opacity: 0.4;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .Select-control:hover .Select-arrow-zone {
        opacity: 0.6;
    }
    .Select-control.is-open .Select-arrow-zone {
        opacity: 0.8;
    }
    .Select-clear-zone {
        color: rgba(100, 116, 139, 0.4) !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .Select-clear-zone:hover {
        color: rgba(220, 38, 38, 0.6) !important;
        transform: scale(1.1);
    }
    .Select-placeholder {
        color: rgba(100, 116, 139, 0.5) !important;
        font-weight: 500 !important;
    }
    .Select-value {
        color: rgba(30, 41, 59, 0.85) !important;
        font-weight: 700 !important;
    }

    .input-field, input[type="number"] {
        padding: 14px 16px !important;
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 22px !important;
        color: rgba(30, 41, 59, 0.85) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset;
    }
    .input-field::placeholder, input[type="number"]::placeholder {
        color: rgba(100, 116, 139, 0.5) !important;
    }
    .input-field:hover, input[type="number"]:hover {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 10px 24px var(--theme-shadow-color-faint), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset !important;
        transform: translateY(-2px);
    }
    .input-field:focus, input[type="number"]:focus {
        outline: none !important;
        background: rgba(255, 255, 255, 0.7) !important;
        border-color: var(--theme-color-primary) !important;
        box-shadow: 0 0 0 3px var(--theme-shadow-color-faint), 0 12px 32px var(--theme-shadow-color), 0 0 0 1.5px rgba(255, 255, 255, 0.8) inset !important;
        transform: translateY(-2px);
    }
    .input-wrapper {
        padding: 16px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-radius: 26px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.04), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: scaleIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        flex-direction: column;
        position: relative;
        z-index: 1;
    }
    .input-wrapper:hover {
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.04), 0 0 0 1.5px var(--theme-color-primary) inset;
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    .input-wrapper.open-dropdown {
        z-index: 101;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1), 0 0 0 1.5px var(--theme-color-primary) inset;
    }
    .input-wrapper.muted {
        opacity: 0.6;
        animation: filterFade 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    .input-wrapper label {
        color: rgba(30, 41, 59, 0.85) !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        display: block !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        z-index: 99999 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .modal-inner {
        width: 90%;
        max-width: 1200px;
        max-height: 90vh;
        overflow-y: auto;
        animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        z-index: 99998 !important;
    }
    .modal-content {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(45px) saturate(180%);
        -webkit-backdrop-filter: blur(45px) saturate(180%);
        border-radius: 36px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 44px;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.1), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset;
        position: relative;
        z-index: 99997 !important;
        animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .close-modal-btn {
        position: absolute;
        top: 24px;
        right: 24px;
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        color: rgba(71, 85, 105, 0.75) !important;
        font-size: 24px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 99999 !important;
        outline: none;
        padding: 0 !important;
        line-height: 1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04), 0 0 0 1.5px rgba(255, 255, 255, 0.6) inset;
    }
    .close-modal-btn:hover {
        background: rgba(239, 68, 68, 0.08) !important;
        border-color: rgba(239, 68, 68, 0.2) !important;
        color: rgba(220, 38, 38, 0.9) !important;
        transform: rotate(90deg) scale(1.1) !important;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.15), 0 0 0 1.5px rgba(255, 255, 255, 0.7) inset;
    }
    .modal-title {
        font-size: 34px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        letter-spacing: -0.7px;
        animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
        position: relative;
        z-index: 1;
    }
    .modal-description {
        font-size: 16px !important;
        color: rgba(71, 85, 105, 0.75) !important;
        margin-bottom: 28px;
        animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s backwards;
        position: relative;
        z-index: 1;
    }

    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.02);
        border-radius: 12px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--theme-color-primary) 0%, var(--theme-color-secondary) 100%);
        opacity: 0.3;
        border-radius: 12px;
        border: 3px solid rgba(255, 255, 255, 0.5);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    ::-webkit-scrollbar-thumb:hover {
        opacity: 0.5;
    }

    @media (max-width: 768px) {
        .sidebar-container {
            display: none;
        }
        .main-content-wrapper,
        .main-content-wrapper.collapsed {
            margin-left: 0;
            width: 100%;
        }

        .main-title { font-size: 40px !important; }
        .section-header { font-size: 32px !important; }
        .metrics-container {
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 18px;
        }
        .metric-card { padding: 28px; }
        .metric-value { font-size: 38px !important; }
    }

    ._dash-loading { background: transparent !important; }
    #_dash-app-content { background: transparent !important; }
    """