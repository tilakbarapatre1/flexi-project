import gradio as gr

def create_login_view():
    """Creates the modern SaaS login view card with branded header and demo logins."""
    with gr.Column(visible=True, elem_classes=["login-container"]) as login_container:
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 24px;">
            <div class="login-brand-icon">🏢</div>
            <h1 class="login-title">AI Employee Leave Automation</h1>
            <p class="login-subtitle">Smart Attendance &amp; Leave Management Platform</p>
        </div>
        """)

        email_input = gr.Textbox(
            label="Work Email",
            placeholder="e.g. manager@company.com or employee@company.com",
            value="manager@company.com",
            lines=1
        )
        password_input = gr.Textbox(
            label="Password",
            type="password",
            placeholder="••••••••",
            value="manager123",
            lines=1
        )
        
        login_btn = gr.Button("Sign In to Dashboard ➔", variant="primary", size="lg")
        login_msg = gr.Markdown()

        # Quick demo credentials section
        gr.HTML("""
        <div class="demo-credentials-box">
            <strong style="color: #0f172a; display: block; margin-bottom: 6px;">⚡ Quick Demo Accounts</strong>
            <div style="margin-bottom: 4px;">👔 <strong>Manager:</strong> <code>manager@company.com</code> | <code>manager123</code></div>
            <div>👤 <strong>Employee:</strong> <code>employee@company.com</code> | <code>employee123</code></div>
        </div>
        """)

        with gr.Row():
            quick_manager_btn = gr.Button("Fill Manager Demo", size="sm", variant="secondary")
            quick_employee_btn = gr.Button("Fill Employee Demo", size="sm", variant="secondary")

        # Quick fill handlers
        quick_manager_btn.click(
            lambda: ("manager@company.com", "manager123"),
            outputs=[email_input, password_input]
        )
        quick_employee_btn.click(
            lambda: ("employee@company.com", "employee123"),
            outputs=[email_input, password_input]
        )

    return login_container, email_input, password_input, login_btn, login_msg
