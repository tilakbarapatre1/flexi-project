import sqlite3
from datetime import date, timedelta
import pandas as pd
import gradio as gr

from backend.database import get_connection, init_db
from frontend.styles import SAAS_THEME_CSS
from frontend.components.login_view import create_login_view
from frontend.components.sidebar import create_sidebar_view

# Maintain conn alias
conn = get_connection

# Initialize database schema and rich demo workforce
init_db()

# ==============================================================================
# BACKEND BUSINESS FUNCTIONS (PRESERVED & EXPANDED)
# ==============================================================================

def mark_attendance(employee_id, status):
    if not employee_id:
        return "❌ Please login first."
    c = conn()
    c.execute("""INSERT INTO attendance(employee_id, att_date, status)
                 VALUES(?,?,?)
                 ON CONFLICT(employee_id, att_date) DO UPDATE SET status=excluded.status""",
              (int(employee_id), date.today().isoformat(), status))
    c.commit()
    c.close()
    return f"✅ Attendance recorded for today: **{status}**"

def employee_summary(employee_id):
    if not employee_id:
        return pd.DataFrame(), "Please login first."
    c = conn()
    rows = c.execute("""SELECT att_date, status FROM attendance
                       WHERE employee_id=? ORDER BY att_date DESC LIMIT 30""",
                    (int(employee_id),)).fetchall()
    bal = c.execute("SELECT leave_balance FROM employees WHERE employee_id=?",
                   (int(employee_id),)).fetchone()
    c.close()
    df = pd.DataFrame(rows, columns=["Date", "Status"])
    if df.empty:
        pct = 0
    else:
        pct = round((df.Status == "Present").mean() * 100, 1)
    balance_days = bal[0] if bal else 0
    return df, f"📈 **30-Day Attendance Rate:** {pct}%  |  🌴 **Available Leave Balance:** {balance_days} days"

def apply_leave(employee_id, start_date, end_date, leave_type, reason):
    if not employee_id:
        return "❌ Please login first."
    if not start_date or not end_date or not reason:
        return "❌ Please fill in all required fields."
    try:
        s = date.fromisoformat(start_date)
        e = date.fromisoformat(end_date)
        if e < s:
            return "❌ End date must be on or after start date."
    except Exception:
        return "❌ Dates must use standard YYYY-MM-DD format."
    days = (e - s).days + 1
    c = conn()
    bal = c.execute("SELECT leave_balance FROM employees WHERE employee_id=?",
                   (int(employee_id),)).fetchone()
    if not bal or bal[0] < days:
        c.close()
        return f"❌ Insufficient leave balance. You requested {days} day(s), but only have {bal[0] if bal else 0} day(s) available."
    c.execute("""INSERT INTO leaves(employee_id, start_date, end_date, leave_type, reason, applied_on)
                 VALUES(?,?,?,?,?,?)""",
              (int(employee_id), s.isoformat(), e.isoformat(), leave_type, reason, date.today().isoformat()))
    c.commit()
    c.close()
    return f"✅ Leave application submitted successfully for **{days} day(s)**. Current status: **Pending Manager Review**."

def my_leaves(employee_id):
    if not employee_id:
        return pd.DataFrame()
    c = conn()
    rows = c.execute("""SELECT leave_id, start_date, end_date, leave_type, reason, status, manager_comment
                       FROM leaves WHERE employee_id=? ORDER BY leave_id DESC""",
                    (int(employee_id),)).fetchall()
    c.close()
    return pd.DataFrame(rows, columns=["Leave ID", "Start Date", "End Date", "Type", "Reason", "Status", "Manager Comment"])

def all_employees():
    c = conn()
    rows = c.execute("""SELECT employee_id, name, email, department, role, leave_balance FROM employees
                       ORDER BY employee_id""").fetchall()
    c.close()
    return pd.DataFrame(rows, columns=["Employee ID", "Name", "Email", "Department", "Role", "Leave Balance (Days)"])

def all_attendance():
    c = conn()
    rows = c.execute("""SELECT e.name, e.department, a.att_date, a.status
                       FROM attendance a JOIN employees e ON e.employee_id=a.employee_id
                       ORDER BY a.att_date DESC, e.name ASC""").fetchall()
    c.close()
    return pd.DataFrame(rows, columns=["Employee Name", "Department", "Date", "Attendance Status"])

def pending_leaves():
    c = conn()
    rows = c.execute("""SELECT l.leave_id, e.name, e.department, l.start_date, l.end_date, l.leave_type, l.reason, l.status
                       FROM leaves l JOIN employees e ON e.employee_id=l.employee_id
                       ORDER BY l.leave_id DESC""").fetchall()
    c.close()
    return pd.DataFrame(rows, columns=["ID", "Employee Name", "Department", "Start Date", "End Date", "Leave Type", "Reason", "Status"])

def agent_analysis(leave_id):
    if not leave_id:
        return "⚠️ Please enter a valid Leave ID."
    c = conn()
    leave = c.execute("""SELECT l.employee_id, e.name, l.start_date, l.end_date, l.leave_type, l.reason, l.status, e.leave_balance
                        FROM leaves l JOIN employees e ON e.employee_id=l.employee_id
                        WHERE l.leave_id=?""", (int(leave_id),)).fetchone()
    rules = c.execute("SELECT min_attendance, max_consecutive, max_monthly_leave FROM rules WHERE id=1").fetchone()
    c.close()
    if not leave:
        return "❌ Leave ID not found in database."
    emp, name, s, e, lt, reason, status, balance = leave
    c = conn()
    att = c.execute("""SELECT status FROM attendance WHERE employee_id=?
                      AND att_date>=date('now','-29 day')""", (emp,)).fetchall()
    recent = c.execute("""SELECT COUNT(*) FROM leaves WHERE employee_id=?
                         AND start_date>=date('now','start of month')""", (emp,)).fetchone()[0]
    c.close()
    total = len(att)
    present = sum(x[0] == "Present" for x in att)
    pct = round(present / total * 100, 1) if total else 0
    days = (date.fromisoformat(e) - date.fromisoformat(s)).days + 1
    reasons = []
    if pct < rules[0]:
        reasons.append(f"30-day attendance ({pct}%) is below policy minimum ({rules[0]}%)")
    if days > rules[1]:
        reasons.append(f"requested duration ({days} days) exceeds maximum consecutive limit ({rules[1]} days)")
    if balance < days:
        reasons.append(f"available leave balance ({balance} days) is less than requested ({days} days)")
    if recent >= rules[2]:
        reasons.append(f"monthly leave requests ({recent}) reached policy limit ({rules[2]})")

    if reasons:
        rec = "⚠️ MANAGER REVIEW / REJECT"
        explanation = "; ".join(reasons) + "."
        status_box = f"<div style='background:#fffbeb;border:1px solid #fde68a;padding:12px;border-radius:8px;color:#92400e;font-weight:700;'>{rec}</div>"
    else:
        rec = "✅ RECOMMEND APPROVAL"
        explanation = "Attendance rate, leave balance, consecutive duration, and monthly quota all meet company guidelines."
        status_box = f"<div style='background:#f0fdf4;border:1px solid #bbf7d0;padding:12px;border-radius:8px;color:#166534;font-weight:700;'>{rec}</div>"

    return f"""### 🤖 AI Leave Agent Evaluation Report

**Employee:** {name} (ID: {emp})  
**Requested Period:** {s} to {e} (**{days} day(s)**)  
**Leave Type:** {lt}  
**Reason:** {reason}  

---
#### Policy Compliance Checklist
- **30-Day Attendance:** **{pct}%** (Policy Minimum: {rules[0]}%) {'✅' if pct>=rules[0] else '❌'}
- **Current Leave Balance:** **{balance} days** (Requested: {days} days) {'✅' if balance>=days else '❌'}
- **Consecutive Duration:** **{days} days** (Policy Maximum: {rules[1]} days) {'✅' if days<=rules[1] else '❌'}
- **Monthly Applications:** **{recent}** (Policy Maximum: {rules[2]}) {'✅' if recent<rules[2] else '❌'}

---
#### Agent Recommendation
{status_box}

**Summary:** {explanation}

> *Notice: This automated report is generated to assist decision-making. The manager retains final approval authority.*"""

def manager_decision(leave_id, decision, comment):
    if not leave_id:
        return "⚠️ Please enter a Leave ID."
    c = conn()
    row = c.execute("SELECT employee_id, start_date, end_date, status FROM leaves WHERE leave_id=?",
                   (int(leave_id),)).fetchone()
    if not row:
        c.close()
        return "❌ Leave application ID not found."
    if row[3] != "Pending":
        c.close()
        return f"⚠️ This leave application is already marked as **{row[3]}**."
    emp, s, e, _ = row
    days = (date.fromisoformat(e) - date.fromisoformat(s)).days + 1
    if decision == "Approved":
        bal = c.execute("SELECT leave_balance FROM employees WHERE employee_id=?", (emp,)).fetchone()[0]
        if bal < days:
            c.close()
            return f"❌ Cannot approve: Insufficient leave balance (Available: {bal}, Requested: {days})."
        c.execute("UPDATE employees SET leave_balance=leave_balance-? WHERE employee_id=?", (days, emp))
    c.execute("UPDATE leaves SET status=?, manager_comment=? WHERE leave_id=?",
              (decision, comment or "", int(leave_id)))
    c.commit()
    c.close()
    return f"✅ Leave #{leave_id} successfully marked as **{decision}**."

def create_employee(name, email, password, department):
    if not all([name, email, password, department]):
        return "⚠️ Please fill in all fields (Name, Email, Password, Department)."
    c = conn()
    try:
        c.execute("""INSERT INTO employees(name, email, password, department, role, leave_balance)
                     VALUES(?,?,?,?,?,?)""", (name.strip(), email.strip(), password.strip(), department.strip(), "employee", 12))
        c.commit()
        msg = f"✅ Employee **{name}** registered successfully with default 12 days leave balance."
    except sqlite3.IntegrityError:
        msg = "❌ An employee with this email already exists."
    c.close()
    return msg

# ==============================================================================
# AUTHENTICATION & SESSION CONTROLLERS
# ==============================================================================

def handle_login(email, password):
    if not email or not password:
        return (
            "❌ Please provide both email and password.",
            None, None, "", "",
            gr.update(visible=True),   # login_container
            gr.update(visible=False),  # app_shell
            gr.update(visible=False),  # mgr_sidebar
            gr.update(visible=False),  # emp_sidebar
            gr.update(visible=False),  # mgr_tabs
            gr.update(visible=False),  # emp_tabs
            gr.update(),               # mgr_profile_html
            gr.update()                # emp_profile_html
        )
    c = conn()
    row = c.execute("SELECT employee_id, name, role, email FROM employees WHERE email=? AND password=?",
                    (email.strip(), password.strip())).fetchone()
    c.close()
    if not row:
        return (
            "❌ Invalid email or password. Please try again.",
            None, None, "", "",
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(),
            gr.update()
        )
    uid, name, role, user_email = row
    is_mgr = (role == "manager")

    mgr_profile = f"""
    <div class="user-profile-card">
        <div style="font-size: 26px;">👨‍💼</div>
        <div style="overflow: hidden;">
            <div style="font-weight: 700; color: #0f172a; font-size: 14px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{name}</div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 4px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{user_email}</div>
            <div><span class="role-badge-manager">MANAGER</span></div>
        </div>
    </div>
    """

    emp_profile = f"""
    <div class="user-profile-card">
        <div style="font-size: 26px;">👨‍💻</div>
        <div style="overflow: hidden;">
            <div style="font-weight: 700; color: #0f172a; font-size: 14px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{name}</div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 4px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{user_email}</div>
            <div><span class="role-badge-employee">EMPLOYEE</span></div>
        </div>
    </div>
    """

    return (
        f"✅ Welcome, {name}!",
        uid, role, name, user_email,
        gr.update(visible=False),                              # login_container
        gr.update(visible=True),                               # app_shell
        gr.update(visible=is_mgr),                             # mgr_sidebar
        gr.update(visible=not is_mgr),                         # emp_sidebar
        gr.update(visible=is_mgr, selected="mgr_dash"),        # mgr_tabs
        gr.update(visible=not is_mgr, selected="emp_dash"),    # emp_tabs
        gr.update(value=mgr_profile),                          # mgr_profile_html
        gr.update(value=emp_profile)                           # emp_profile_html
    )

def handle_logout():
    return (
        "", None, None, "", "",
        gr.update(visible=True),   # login_container
        gr.update(visible=False),  # app_shell
        gr.update(visible=False),  # mgr_sidebar
        gr.update(visible=False),  # emp_sidebar
        gr.update(visible=False),  # mgr_tabs
        gr.update(visible=False)   # emp_tabs
    )

# ==============================================================================
# GRADIO APPLICATION SHELL (STAGE 1: MODERN LOGIN + ROLE-BASED SIDEBAR)
# ==============================================================================

with gr.Blocks(title="AI Employee Leave Automation", css=SAAS_THEME_CSS, theme=gr.themes.Base()) as demo:
    # App Session State
    user_id = gr.State(None)
    user_role = gr.State(None)
    user_name = gr.State("")
    user_email = gr.State("")

    # 1. LOGIN CONTAINER
    login_container, email_box, pass_box, login_action_btn, login_feedback = create_login_view()

    # 2. MAIN APPLICATION WORKSPACE (Hidden until login)
    with gr.Row(visible=False) as app_shell:
        # Sidebars
        mgr_sidebar, mgr_profile_html, mgr_nav, emp_sidebar, emp_profile_html, emp_nav = create_sidebar_view()

        # ======================================================================
        # MAIN CONTENT: MANAGER TABS
        # ======================================================================
        with gr.Tabs(elem_classes=["hidden-tabs", "main-view-panel"], visible=False) as mgr_tabs:
            # Tab 1: Dashboard
            with gr.Tab("Dashboard", id="mgr_dash"):
                gr.HTML("""
                <div class="page-header-title">Good morning, Manager 👋</div>
                <div class="page-header-subtitle">Here's your workforce overview for today.</div>
                """)
                with gr.Row():
                    gr.HTML("""
                    <div class="kpi-card" style="flex: 1;">
                        <div class="kpi-title">👥 Total Workforce</div>
                        <div class="kpi-value">22</div>
                        <div class="kpi-subtext">Active team members</div>
                    </div>
                    """)
                    gr.HTML("""
                    <div class="kpi-card" style="flex: 1;">
                        <div class="kpi-title">✅ Present Today</div>
                        <div class="kpi-value">19</div>
                        <div class="kpi-subtext">86.4% on-site / remote</div>
                    </div>
                    """)
                    gr.HTML("""
                    <div class="kpi-card" style="flex: 1;">
                        <div class="kpi-title">❌ Absent Today</div>
                        <div class="kpi-value">3</div>
                        <div class="kpi-subtext">Unplanned absences</div>
                    </div>
                    """)
                    gr.HTML("""
                    <div class="kpi-card" style="flex: 1;">
                        <div class="kpi-title">📝 Pending Leaves</div>
                        <div class="kpi-value">3</div>
                        <div class="kpi-subtext">Awaiting AI/Manager review</div>
                    </div>
                    """)
                gr.Markdown("---")
                gr.Markdown("### ⚡ Quick Shortcuts")
                with gr.Row():
                    quick_view_leaves = gr.Button("📝 Review Pending Leaves", variant="primary")
                    quick_view_emps = gr.Button("👥 Manage Employees", variant="secondary")
                    quick_view_agent = gr.Button("🤖 Open AI Leave Agent", variant="secondary")
                quick_view_leaves.click(lambda: gr.update(selected="mgr_leaves"), None, mgr_tabs)
                quick_view_emps.click(lambda: gr.update(selected="mgr_emps"), None, mgr_tabs)
                quick_view_agent.click(lambda: gr.update(selected="mgr_agent"), None, mgr_tabs)

            # Tab 2: Employees
            with gr.Tab("Employees", id="mgr_emps"):
                gr.HTML("""
                <div class="page-header-title">👥 Employee Directory &amp; Registration</div>
                <div class="page-header-subtitle">Manage company workforce and onboard new team members.</div>
                """)
                with gr.Accordion("➕ Register New Employee", open=False):
                    with gr.Row():
                        reg_name = gr.Textbox(label="Full Name", placeholder="e.g. Rahul Sharma")
                        reg_email = gr.Textbox(label="Work Email", placeholder="e.g. rahul.s@company.com")
                    with gr.Row():
                        reg_pwd = gr.Textbox(label="Password", type="password", placeholder="Assign initial password")
                        reg_dept = gr.Dropdown(["Engineering", "HR", "Finance", "Marketing", "Operations"], label="Department", value="Engineering")
                    reg_submit = gr.Button("Register Employee", variant="primary")
                    reg_out = gr.Markdown()
                    reg_submit.click(create_employee, [reg_name, reg_email, reg_pwd, reg_dept], reg_out)

                gr.Markdown("### All Employees")
                emps_refresh_btn = gr.Button("🔄 Refresh Employee List", size="sm")
                emps_df = gr.Dataframe(value=all_employees, interactive=False)
                emps_refresh_btn.click(all_employees, None, emps_df)

            # Tab 3: Attendance
            with gr.Tab("Attendance", id="mgr_att"):
                gr.HTML("""
                <div class="page-header-title">📊 Workforce Attendance Records</div>
                <div class="page-header-subtitle">Monitor daily attendance logs across all departments.</div>
                """)
                att_refresh_btn = gr.Button("🔄 Refresh Attendance Records", size="sm")
                all_att_df = gr.Dataframe(value=all_attendance, interactive=False)
                att_refresh_btn.click(all_attendance, None, all_att_df)

            # Tab 4: Leave Management
            with gr.Tab("Leaves", id="mgr_leaves"):
                gr.HTML("""
                <div class="page-header-title">📝 Leave Applications &amp; Decisions</div>
                <div class="page-header-subtitle">Review, analyze, and process leave requests.</div>
                """)
                leaves_refresh_btn = gr.Button("🔄 Refresh Leave Applications", size="sm")
                pending_leaves_df = gr.Dataframe(value=pending_leaves, interactive=False)
                leaves_refresh_btn.click(pending_leaves, None, pending_leaves_df)

                gr.Markdown("---")
                gr.Markdown("### ⚖️ Process Leave Application")
                with gr.Row():
                    mgr_lid_input = gr.Number(label="Leave Application ID", precision=0, value=1)
                    mgr_decision_choice = gr.Radio(["Approved", "Rejected"], value="Approved", label="Manager Decision")
                mgr_comment_input = gr.Textbox(label="Manager Comment / Notes", placeholder="e.g. Approved. Please ensure handover before leaving.")
                mgr_submit_decision_btn = gr.Button("Submit Manager Decision", variant="primary")
                mgr_decision_out = gr.Markdown()
                mgr_submit_decision_btn.click(
                    manager_decision,
                    [mgr_lid_input, mgr_decision_choice, mgr_comment_input],
                    mgr_decision_out
                ).then(pending_leaves, None, pending_leaves_df)

            # Tab 5: AI Leave Agent
            with gr.Tab("AI Agent", id="mgr_agent"):
                gr.HTML("""
                <div class="page-header-title">🤖 AI Leave Agent Recommendation Engine</div>
                <div class="page-header-subtitle">Automated policy checks, attendance thresholds, and leave duration evaluation.</div>
                """)
                with gr.Row():
                    agent_lid_input = gr.Number(label="Enter Leave ID to Analyze", precision=0, value=1)
                    agent_run_btn = gr.Button("Run AI Analysis 🚀", variant="primary")
                agent_report = gr.Markdown()
                agent_run_btn.click(agent_analysis, agent_lid_input, agent_report)

            # Tab 6: Analytics
            with gr.Tab("Analytics", id="mgr_analytics"):
                gr.HTML("""
                <div class="page-header-title">📈 Workforce Analytics &amp; Trends</div>
                <div class="page-header-subtitle">Comprehensive attendance and leave insights (Stage 7 preview).</div>
                """)
                gr.Info("Visual Plotly charts for attendance rate, department breakdown, and monthly leave patterns will be rendered here in Stage 7.")

            # Tab 7: Notifications
            with gr.Tab("Notifications", id="mgr_notif"):
                gr.HTML("""
                <div class="page-header-title">🔔 Notification Center</div>
                <div class="page-header-subtitle">Real-time alerts for leave submissions, approvals, and reminders.</div>
                """)
                gr.Markdown("""
                - 🔵 **New Leave Application:** Priya Patel submitted a 2-day Sick Leave request *(Today)*
                - 🟢 **Attendance Marked:** 19 team members marked attendance today *(Today)*
                - 🟡 **Policy Warning:** Deepak Pillai's attendance is nearing the 75% threshold *(Yesterday)*
                """)

            # Tab 8: Settings
            with gr.Tab("Settings", id="mgr_settings"):
                gr.HTML("""
                <div class="page-header-title">⚙️ Company Leave Policies &amp; Thresholds</div>
                <div class="page-header-subtitle">Configure company rules applied by the AI Leave Agent.</div>
                """)
                with gr.Row():
                    gr.Number(label="Minimum Attendance Rate (%)", value=75)
                    gr.Number(label="Max Consecutive Leave Days", value=3)
                    gr.Number(label="Max Monthly Applications", value=4)

            # Tab 9: Audit Logs
            with gr.Tab("Audit Logs", id="mgr_audit"):
                gr.HTML("""
                <div class="page-header-title">📋 System Audit Trail</div>
                <div class="page-header-subtitle">Tamper-evident logs of administrative actions, logins, and approvals.</div>
                """)
                gr.Markdown("""
                | Timestamp | User | Action | Status |
                |---|---|---|---|
                | Today, 09:15 | manager@company.com | Manager Login | Success |
                | Today, 09:20 | employee@company.com | Attendance Recorded | Success |
                | Yesterday, 16:45 | manager@company.com | Leave Approved (#3) | Success |
                """)

            # Tab 10: Profile
            with gr.Tab("Profile", id="mgr_profile"):
                gr.HTML("""
                <div class="page-header-title">👤 Manager Profile</div>
                <div class="page-header-subtitle">Account credentials and system privileges.</div>
                """)
                gr.Markdown("""
                - **Designation:** HR & Operations Director
                - **Role:** Manager (Super Administrator)
                - **Access:** Unrestricted Access to Workforce Logs, Approvals, & Policy Engines
                """)

        # ======================================================================
        # MAIN CONTENT: EMPLOYEE TABS
        # ======================================================================
        with gr.Tabs(elem_classes=["hidden-tabs", "main-view-panel"], visible=False) as emp_tabs:
            # Tab 1: Dashboard
            with gr.Tab("Dashboard", id="emp_dash"):
                gr.HTML("""
                <div class="page-header-title">Good morning 👋</div>
                <div class="page-header-subtitle">Here's your attendance and leave overview for today.</div>
                """)
                gr.Markdown("### 1. Mark Today's Attendance")
                with gr.Row():
                    emp_present_btn = gr.Button("✅ Mark Present", variant="primary", size="lg")
                    emp_absent_btn = gr.Button("❌ Mark Absent", variant="stop", size="lg")
                emp_mark_msg = gr.Markdown()
                emp_present_btn.click(lambda uid: mark_attendance(uid, "Present"), user_id, emp_mark_msg)
                emp_absent_btn.click(lambda uid: mark_attendance(uid, "Absent"), user_id, emp_mark_msg)

                gr.Markdown("---")
                gr.Markdown("### 2. My Summary & Quick Links")
                emp_dash_summary = gr.Markdown()
                emp_dash_refresh = gr.Button("🔄 Refresh Summary", size="sm")
                emp_dash_refresh.click(lambda uid: employee_summary(uid)[1], user_id, emp_dash_summary)

            # Tab 2: My Attendance
            with gr.Tab("Attendance", id="emp_att"):
                gr.HTML("""
                <div class="page-header-title">📊 My 30-Day Attendance Record</div>
                <div class="page-header-subtitle">Review your daily attendance history and compliance rate.</div>
                """)
                emp_att_refresh = gr.Button("🔄 Refresh Attendance Log", size="sm")
                emp_att_table = gr.Dataframe(interactive=False)
                emp_att_stat = gr.Markdown()
                emp_att_refresh.click(employee_summary, user_id, [emp_att_table, emp_att_stat])

            # Tab 3: Apply Leave
            with gr.Tab("Apply", id="emp_apply"):
                gr.HTML("""
                <div class="page-header-title">📝 Apply for Leave</div>
                <div class="page-header-subtitle">Submit a leave application for manager review and AI verification.</div>
                """)
                with gr.Row():
                    l_start = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="2026-10-01")
                    l_end = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="2026-10-03")
                l_type = gr.Dropdown(["Casual", "Sick", "Earned", "Personal"], value="Casual", label="Leave Type")
                l_reason = gr.Textbox(label="Reason for Leave", placeholder="Please provide brief details...")
                l_submit_btn = gr.Button("Submit Leave Application", variant="primary", size="lg")
                l_feedback = gr.Markdown()
                l_submit_btn.click(apply_leave, [user_id, l_start, l_end, l_type, l_reason], l_feedback)

            # Tab 4: My Leave History
            with gr.Tab("History", id="emp_hist"):
                gr.HTML("""
                <div class="page-header-title">📋 My Leave Applications History</div>
                <div class="page-header-subtitle">Check status, comments, and decision outcomes of your leave requests.</div>
                """)
                emp_leave_refresh = gr.Button("🔄 Refresh History", size="sm")
                emp_leave_table = gr.Dataframe(interactive=False)
                emp_leave_refresh.click(my_leaves, user_id, emp_leave_table)

            # Tab 5: Notifications
            with gr.Tab("Notifications", id="emp_notif"):
                gr.HTML("""
                <div class="page-header-title">🔔 My Notifications</div>
                <div class="page-header-subtitle">Updates regarding your leave submissions and attendance.</div>
                """)
                gr.Markdown("""
                - 🟢 **Leave Approved:** Your recent Casual Leave was approved by the manager.
                - ℹ️ **Attendance Reminder:** Remember to mark your attendance before 10:00 AM daily.
                """)

            # Tab 6: Profile
            with gr.Tab("Profile", id="emp_profile"):
                gr.HTML("""
                <div class="page-header-title">👤 Employee Profile</div>
                <div class="page-header-subtitle">Your workforce identity details.</div>
                """)
                gr.Markdown("""
                - **Role:** Regular Staff
                - **Default Quota:** 12 Annual Paid Leaves
                - **Policy Threshold:** Minimum 75% monthly attendance required
                """)

    # ==========================================================================
    # NAVIGATION BUTTON CLICK BINDINGS (SIDEBAR CONTROLLERS)
    # ==========================================================================

    # Manager Sidebar Actions
    mgr_nav["dash"].click(lambda: gr.update(selected="mgr_dash"), None, mgr_tabs)
    mgr_nav["emps"].click(lambda: gr.update(selected="mgr_emps"), None, mgr_tabs)
    mgr_nav["att"].click(lambda: gr.update(selected="mgr_att"), None, mgr_tabs)
    mgr_nav["leaves"].click(lambda: gr.update(selected="mgr_leaves"), None, mgr_tabs)
    mgr_nav["agent"].click(lambda: gr.update(selected="mgr_agent"), None, mgr_tabs)
    mgr_nav["analytics"].click(lambda: gr.update(selected="mgr_analytics"), None, mgr_tabs)
    mgr_nav["notif"].click(lambda: gr.update(selected="mgr_notif"), None, mgr_tabs)
    mgr_nav["settings"].click(lambda: gr.update(selected="mgr_settings"), None, mgr_tabs)
    mgr_nav["audit"].click(lambda: gr.update(selected="mgr_audit"), None, mgr_tabs)
    mgr_nav["profile"].click(lambda: gr.update(selected="mgr_profile"), None, mgr_tabs)

    # Employee Sidebar Actions
    emp_nav["dash"].click(lambda: gr.update(selected="emp_dash"), None, emp_tabs)
    emp_nav["att"].click(lambda: gr.update(selected="emp_att"), None, emp_tabs)
    emp_nav["apply"].click(lambda: gr.update(selected="emp_apply"), None, emp_tabs)
    emp_nav["hist"].click(lambda: gr.update(selected="emp_hist"), None, emp_tabs)
    emp_nav["notif"].click(lambda: gr.update(selected="emp_notif"), None, emp_tabs)
    emp_nav["profile"].click(lambda: gr.update(selected="emp_profile"), None, emp_tabs)

    # Login and Logout Handlers
    login_action_btn.click(
        handle_login,
        [email_box, pass_box],
        [
            login_feedback, user_id, user_role, user_name, user_email,
            login_container, app_shell,
            mgr_sidebar, emp_sidebar,
            mgr_tabs, emp_tabs,
            mgr_profile_html, emp_profile_html
        ]
    )

    mgr_nav["logout"].click(
        handle_logout,
        None,
        [
            login_feedback, user_id, user_role, user_name, user_email,
            login_container, app_shell,
            mgr_sidebar, emp_sidebar,
            mgr_tabs, emp_tabs
        ]
    )

    emp_nav["logout"].click(
        handle_logout,
        None,
        [
            login_feedback, user_id, user_role, user_name, user_email,
            login_container, app_shell,
            mgr_sidebar, emp_sidebar,
            mgr_tabs, emp_tabs
        ]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

