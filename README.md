# Employee Leave Automation

A modern, Python-based employee attendance and leave management system featuring an **AI-assisted Leave Recommendation Agent**.

---

## 📌 Project Description

**Employee Leave Automation** simplifies the workplace leave management lifecycle. It allows employees to mark daily attendance, track their leave records, and apply for leaves seamlessly. Managers get an administrative dashboard to monitor workforce attendance, configure leave policies, review pending applications, and leverage an **AI Leave Agent** that evaluates leave requests against historical attendance patterns and company rules to provide smart recommendations.

---

## 🌟 Main Features

### 👔 Manager Dashboard
- **Manager Authentication**: Secure login for authorized managers.
- **Employee Registration**: Easily onboard new team members with specific departments and roles.
- **Employee Monitoring**: View and manage the complete employee roster and profiles.
- **Attendance Monitoring**: Real-time overview of workforce attendance and trends.
- **Leave Application Monitoring**: Centralized queue for all submitted leave requests.
- **Approve / Reject Leave**: Take quick action on leave applications with custom manager remarks.
- **Company Leave Policies**: Configure minimum attendance rates, maximum consecutive leave days, and monthly limits.
- **AI Leave Recommendation**: Instant rule-based AI recommendations on whether to approve or review a leave request.
- **Interactive Analytics**: Visual charts powered by Plotly for attendance distribution and leave patterns.
- **System Notifications**: Stay informed about new requests and status updates.
- **Audit Logs**: Transparent record of critical actions taken across the system.

### 👤 Employee Portal
- **Employee Authentication**: Dedicated portal login for employees.
- **Daily Attendance Marking**: Mark daily presence with a single click.
- **Last 30 Days Attendance**: Visual attendance log displaying Present/Absent history.
- **Leave Application**: Submit leave requests with specific date ranges, leave types, and reasons.
- **Leave Balance Tracking**: Real-time tracker of remaining paid leave quota.
- **Leave History**: Historical log of all past leave applications.
- **Application Status**: Check approval status (`Pending`, `Approved`, `Rejected`) and manager comments.
- **Notifications**: Instant feedback when leave applications are reviewed.

---

## 🤖 AI Leave Agent

The **AI Leave Agent** assists managers by analyzing key factors before a leave decision is made:

### What the AI Agent Gathers:
1. **Employee Information** (Name, role, department)
2. **Last 30 Days Attendance History** (Attendance percentage and consistency)
3. **Current Leave Balance** (Available days vs. requested days)
4. **Previous Leave History** (Past leave frequency and patterns)
5. **Company Leave Rules** (Minimum attendance threshold, maximum consecutive days, monthly leave limits)

### How It Works:
The agent evaluates these factors against the organization's policies and produces an actionable recommendation (e.g., `RECOMMEND APPROVAL` or `FLAG FOR REVIEW`) along with an explanation of its reasoning.

> [!IMPORTANT]
> **Human-in-the-Loop Decision Making**:
> The AI recommendation is an advisory tool designed to help managers make informed decisions quickly. It **does NOT replace the manager's final judgment and authority**. The manager always has the final say to approve or reject any application.

---

## 🛠️ Technology Stack

- **Python 3.10+**: Core programming language.
- **Gradio**: Interactive web interface and UI components.
- **SQLite**: Lightweight, zero-configuration relational database.
- **Pandas**: Efficient data manipulation and processing.
- **Plotly**: Dynamic, interactive charts and visual analytics.
- **AI Leave Agent**: Intelligent policy and attendance evaluation engine.

---

## 🚀 How to Run

Follow these simple, beginner-friendly steps to run the application locally:

### 1. Clone or Navigate to the Project Directory
Open your terminal or command prompt:
```bash
cd employee_leave_automation
```

### 2. Install Required Dependencies
Run the following command to install the required Python packages:
```bash
python -m pip install -r requirements.txt
```

### 3. Launch the Application
Start the application with:
```bash
python app.py
```

### 4. Open in Your Browser
Once launched, Gradio will display a local URL in your terminal:
```text
Running on local URL: http://127.0.0.1:7860
```
Open **`http://127.0.0.1:7860`** in any web browser to use the application.

---

## 🔑 Demo Login Information

The application automatically initializes the SQLite database with safe demo accounts on first run:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Manager** | `manager@company.com` | `manager123` |
| **Employee** | `employee@company.com` | `employee123` |

*(Note: These are pre-configured demo test credentials intended solely for testing and demonstrations.)*

---

## 📂 Project Structure

```text
employee_leave_automation/
├── app.py                     # Main application entry point & AI Agent engine
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation & guide
├── .gitignore                 # Files excluded from version control
├── backend/
│   ├── __init__.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py      # SQLite connection utilities
│       └── models.py          # Database schema & automatic demo seeder
└── frontend/
    ├── __init__.py
    ├── styles.py              # CSS styles & visual theme
    └── components/
        ├── __init__.py
        ├── login_view.py      # Login page component
        └── sidebar.py        # Navigation sidebar component
```
