import gradio as gr

def create_sidebar_view():
    """
    Creates dynamic role-aware sidebars for Manager and Employee users.
    Returns the sidebar columns, navigation buttons, profile components, and logout buttons.
    """
    # 1. MANAGER SIDEBAR
    with gr.Column(visible=False, elem_classes=["sidebar-panel"], scale=1) as mgr_sidebar:
        gr.HTML("""
        <div class="sidebar-header">
            <div style="font-size: 20px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                <span>🏢</span> <span>HR Portal</span>
            </div>
            <div style="font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
                Management Suite
            </div>
        </div>
        """)

        mgr_profile_html = gr.HTML("""
        <div class="user-profile-card">
            <div style="font-size: 26px;">👨‍💼</div>
            <div>
                <div style="font-weight: 700; color: #0f172a; font-size: 14px;">Manager</div>
                <div style="margin-top: 3px;"><span class="role-badge-manager">MANAGER</span></div>
            </div>
        </div>
        """)

        gr.HTML('<div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin: 12px 0 6px 8px; letter-spacing: 0.05em;">Main Menu</div>')
        mgr_nav_dash = gr.Button("🏠  Dashboard", elem_classes=["sidebar-nav-btn"])
        mgr_nav_emps = gr.Button("👥  Employees", elem_classes=["sidebar-nav-btn"])
        mgr_nav_att = gr.Button("📊  Attendance", elem_classes=["sidebar-nav-btn"])
        mgr_nav_leaves = gr.Button("📝  Leave Management", elem_classes=["sidebar-nav-btn"])
        mgr_nav_agent = gr.Button("🤖  AI Leave Agent", elem_classes=["sidebar-nav-btn"])
        mgr_nav_analytics = gr.Button("📈  Analytics", elem_classes=["sidebar-nav-btn"])
        
        gr.HTML('<div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin: 16px 0 6px 8px; letter-spacing: 0.05em;">System &amp; Account</div>')
        mgr_nav_notif = gr.Button("🔔  Notifications", elem_classes=["sidebar-nav-btn"])
        mgr_nav_settings = gr.Button("⚙️  Settings", elem_classes=["sidebar-nav-btn"])
        mgr_nav_audit = gr.Button("📋  Audit Logs", elem_classes=["sidebar-nav-btn"])
        mgr_nav_profile = gr.Button("👤  My Profile", elem_classes=["sidebar-nav-btn"])
        
        mgr_logout_btn = gr.Button("🚪  Sign Out", elem_classes=["logout-button"])

    # 2. EMPLOYEE SIDEBAR
    with gr.Column(visible=False, elem_classes=["sidebar-panel"], scale=1) as emp_sidebar:
        gr.HTML("""
        <div class="sidebar-header">
            <div style="font-size: 20px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                <span>🏢</span> <span>HR Portal</span>
            </div>
            <div style="font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
                Employee Self-Service
            </div>
        </div>
        """)

        emp_profile_html = gr.HTML("""
        <div class="user-profile-card">
            <div style="font-size: 26px;">👨‍💻</div>
            <div>
                <div style="font-weight: 700; color: #0f172a; font-size: 14px;">Employee</div>
                <div style="margin-top: 3px;"><span class="role-badge-employee">EMPLOYEE</span></div>
            </div>
        </div>
        """)

        gr.HTML('<div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin: 12px 0 6px 8px; letter-spacing: 0.05em;">Employee Workspace</div>')
        emp_nav_dash = gr.Button("🏠  Dashboard", elem_classes=["sidebar-nav-btn"])
        emp_nav_att = gr.Button("📊  My Attendance", elem_classes=["sidebar-nav-btn"])
        emp_nav_apply = gr.Button("📝  Apply Leave", elem_classes=["sidebar-nav-btn"])
        emp_nav_hist = gr.Button("📋  My Leave History", elem_classes=["sidebar-nav-btn"])

        gr.HTML('<div style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin: 16px 0 6px 8px; letter-spacing: 0.05em;">Account</div>')
        emp_nav_notif = gr.Button("🔔  Notifications", elem_classes=["sidebar-nav-btn"])
        emp_nav_profile = gr.Button("👤  My Profile", elem_classes=["sidebar-nav-btn"])

        emp_logout_btn = gr.Button("🚪  Sign Out", elem_classes=["logout-button"])

    return (
        mgr_sidebar, mgr_profile_html, {
            "dash": mgr_nav_dash, "emps": mgr_nav_emps, "att": mgr_nav_att,
            "leaves": mgr_nav_leaves, "agent": mgr_nav_agent, "analytics": mgr_nav_analytics,
            "notif": mgr_nav_notif, "settings": mgr_nav_settings, "audit": mgr_nav_audit,
            "profile": mgr_nav_profile, "logout": mgr_logout_btn
        },
        emp_sidebar, emp_profile_html, {
            "dash": emp_nav_dash, "att": emp_nav_att, "apply": emp_nav_apply,
            "hist": emp_nav_hist, "notif": emp_nav_notif, "profile": emp_nav_profile,
            "logout": emp_logout_btn
        }
    )
