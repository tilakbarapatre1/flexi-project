"""Modern HR SaaS CSS Design System for Gradio."""

SAAS_THEME_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --font-sans: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --primary-blue: #1d4ed8;
    --primary-hover: #1e40af;
    --primary-light: #eff6ff;
    --primary-border: #bfdbfe;
    --slate-900: #0f172a;
    --slate-800: #1e293b;
    --slate-700: #334155;
    --slate-600: #475569;
    --slate-500: #64748b;
    --slate-400: #94a3b8;
    --slate-200: #e2e8f0;
    --slate-100: #f1f5f9;
    --slate-50: #f8fafc;
    --success-green: #15803d;
    --success-bg: #f0fdf4;
    --warning-amber: #b45309;
    --warning-bg: #fffbeb;
    --danger-red: #b91c1c;
    --danger-bg: #fef2f2;
}

/* Global Font & Resets */
body, .gradio-container {
    font-family: var(--font-sans) !important;
    background-color: #f8fafc !important;
    color: var(--slate-800) !important;
}

/* Login Screen Styling */
.login-container {
    max-width: 460px !important;
    margin: 40px auto !important;
    padding: 32px 36px !important;
    background: #ffffff !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04) !important;
    border: 1px solid #e2e8f0 !important;
}

.login-brand-icon {
    font-size: 38px;
    margin-bottom: 8px;
    display: inline-block;
}

.login-title {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin: 0 0 6px 0 !important;
    letter-spacing: -0.02em !important;
}

.login-subtitle {
    font-size: 14px !important;
    color: #64748b !important;
    margin-bottom: 24px !important;
    font-weight: 500 !important;
}

.demo-credentials-box {
    background: #f1f5f9;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 20px;
    border: 1px dashed #cbd5e1;
    font-size: 13px;
    color: #334155;
}

/* Hide default Gradio tab buttons for custom sidebar navigation */
.hidden-tabs > div[role="tablist"],
.hidden-tabs > .tab-nav {
    display: none !important;
}
.hidden-tabs {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
}

/* Sidebar & App Layout */
.sidebar-panel {
    flex: 1 1 260px !important;
    max-width: 280px !important;
    min-width: 240px !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    padding: 20px 16px !important;
    min-height: 820px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03) !important;
}

.sidebar-header {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid #f1f5f9;
}

.user-profile-card {
    background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.role-badge-manager {
    background-color: #dbeafe;
    color: #1e40af;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 3px 8px;
    border-radius: 9999px;
    display: inline-block;
}

.role-badge-employee {
    background-color: #dcfce7;
    color: #166534;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 3px 8px;
    border-radius: 9999px;
    display: inline-block;
}

/* Navigation buttons in sidebar */
.sidebar-nav-btn {
    text-align: left !important;
    justify-content: flex-start !important;
    border: none !important;
    background: transparent !important;
    color: #475569 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
    transition: all 0.15s ease-in-out !important;
}

.sidebar-nav-btn:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    transform: translateX(2px);
}

.sidebar-nav-btn-active {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
    font-weight: 700 !important;
    border-left: 3px solid #1d4ed8 !important;
}

.logout-button {
    background: #fff1f2 !important;
    color: #be123c !important;
    border: 1px solid #fecdd3 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    margin-top: 20px !important;
    transition: background 0.15s !important;
}

.logout-button:hover {
    background: #ffe4e6 !important;
}

/* Main Content Workspace */
.main-view-panel {
    flex: 4 1 0% !important;
    min-width: 0 !important;
    background: #ffffff !important;
    border-radius: 16px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 28px 32px !important;
    min-height: 820px !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03) !important;
}

.page-header-title {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin: 0 0 4px 0 !important;
    letter-spacing: -0.02em !important;
}

.page-header-subtitle {
    font-size: 14px !important;
    color: #64748b !important;
    margin-bottom: 24px !important;
}

/* Modern KPI Cards */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.08);
}

.kpi-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
}

.kpi-subtext {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
}

/* Status Badges */
.badge-approved {
    background: #dcfce7;
    color: #166534;
    padding: 3px 10px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 12px;
}

.badge-pending {
    background: #fef3c7;
    color: #92400e;
    padding: 3px 10px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 12px;
}

.badge-rejected {
    background: #fee2e2;
    color: #991b1b;
    padding: 3px 10px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 12px;
}
"""
