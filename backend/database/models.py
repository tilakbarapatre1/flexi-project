from datetime import date, timedelta
from .connection import get_connection

def init_db():
    """Initializes the database schema and seeds initial demo data if needed."""
    c = get_connection()
    cur = c.cursor()

    # 1. Employees table
    cur.execute("""CREATE TABLE IF NOT EXISTS employees(
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        department TEXT,
        role TEXT DEFAULT 'employee',
        leave_balance INTEGER DEFAULT 12
    )""")

    # 2. Attendance table
    cur.execute("""CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        att_date TEXT,
        status TEXT,
        UNIQUE(employee_id, att_date)
    )""")

    # 3. Leave applications table
    cur.execute("""CREATE TABLE IF NOT EXISTS leaves(
        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        leave_type TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        manager_comment TEXT,
        applied_on TEXT
    )""")

    # 4. Company rules table
    cur.execute("""CREATE TABLE IF NOT EXISTS rules(
        id INTEGER PRIMARY KEY CHECK(id=1),
        min_attendance REAL DEFAULT 75,
        max_consecutive INTEGER DEFAULT 3,
        max_monthly_leave INTEGER DEFAULT 4
    )""")

    # 5. Notifications table (ready for future phases)
    cur.execute("""CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT
    )""")

    # 6. Audit logs table (ready for future phases)
    cur.execute("""CREATE TABLE IF NOT EXISTS audit_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        timestamp TEXT
    )""")

    # Default rule values
    cur.execute("INSERT OR IGNORE INTO rules(id) VALUES(1)")

    # Seed demo employees if not present or only initial 2
    cur.execute("SELECT COUNT(*) FROM employees")
    emp_count = cur.fetchone()[0]
    
    if emp_count == 0:
        cur.execute("""INSERT INTO employees(name,email,password,department,role,leave_balance)
                       VALUES(?,?,?,?,?,?)""",
                    ("Company Manager", "manager@company.com", "manager123", "HR", "manager", 0))
        cur.execute("""INSERT INTO employees(name,email,password,department,role,leave_balance)
                       VALUES(?,?,?,?,?,?)""",
                    ("Demo Employee", "employee@company.com", "employee123", "IT", "employee", 12))
        c.commit()

    # Expand demo workforce if only basic accounts exist (for presentation readiness)
    cur.execute("SELECT COUNT(*) FROM employees")
    if cur.fetchone()[0] <= 2:
        demo_staff = [
            ("Aarav Sharma", "aarav.sharma@company.com", "pass123", "Engineering", "employee", 10),
            ("Priya Patel", "priya.patel@company.com", "pass123", "Engineering", "employee", 8),
            ("Rohan Verma", "rohan.verma@company.com", "pass123", "Engineering", "employee", 12),
            ("Sneha Iyer", "sneha.iyer@company.com", "pass123", "Finance", "employee", 9),
            ("Vikram Singh", "vikram.singh@company.com", "pass123", "Finance", "employee", 11),
            ("Ananya Rao", "ananya.rao@company.com", "pass123", "Marketing", "employee", 7),
            ("Karan Kapoor", "karan.kapoor@company.com", "pass123", "Marketing", "employee", 14),
            ("Neha Gupta", "neha.gupta@company.com", "pass123", "Operations", "employee", 6),
            ("Aditya Joshi", "aditya.joshi@company.com", "pass123", "Operations", "employee", 12),
            ("Meera Nair", "meera.nair@company.com", "pass123", "HR", "employee", 11),
            ("Siddharth Roy", "siddharth.roy@company.com", "pass123", "Engineering", "employee", 5),
            ("Tanvi Deshmukh", "tanvi.deshmukh@company.com", "pass123", "Engineering", "employee", 10),
            ("Arjun Mehta", "arjun.mehta@company.com", "pass123", "Finance", "employee", 8),
            ("Pooja Choudhury", "pooja.c@company.com", "pass123", "Marketing", "employee", 13),
            ("Rishabh Malik", "rishabh.m@company.com", "pass123", "Operations", "employee", 10),
            ("Ishita Banerjee", "ishita.b@company.com", "pass123", "HR", "employee", 12),
            ("Deepak Pillai", "deepak.p@company.com", "pass123", "Engineering", "employee", 7),
            ("Ritu Saxena", "ritu.s@company.com", "pass123", "Finance", "employee", 9),
            ("Varun Bhatt", "varun.b@company.com", "pass123", "Operations", "employee", 11),
            ("Divya Kulkarni", "divya.k@company.com", "pass123", "Marketing", "employee", 10),
        ]
        for name, email, pw, dept, role, bal in demo_staff:
            cur.execute("""INSERT OR IGNORE INTO employees(name,email,password,department,role,leave_balance)
                           VALUES(?,?,?,?,?,?)""", (name, email, pw, dept, role, bal))
        c.commit()

        # Seed attendance for new staff over last 30 days
        start = date.today() - timedelta(days=29)
        cur.execute("SELECT employee_id FROM employees WHERE role='employee'")
        emp_ids = [r[0] for r in cur.fetchall()]
        for e_id in emp_ids:
            for i in range(30):
                d = start + timedelta(days=i)
                # Weekends or random distribution for realistic %
                status = "Absent" if (i + e_id) % 7 == 0 or (i * 3 + e_id) % 17 == 0 else "Present"
                cur.execute("""INSERT OR IGNORE INTO attendance(employee_id,att_date,status)
                               VALUES(?,?,?)""", (e_id, d.isoformat(), status))
        c.commit()

        # Seed realistic sample leaves
        today_iso = date.today().isoformat()
        sample_leaves = [
            (emp_ids[0], (date.today() + timedelta(days=3)).isoformat(), (date.today() + timedelta(days=5)).isoformat(), "Casual", "Family function", "Pending"),
            (emp_ids[1], (date.today() + timedelta(days=1)).isoformat(), (date.today() + timedelta(days=2)).isoformat(), "Sick", "Viral fever recovery", "Pending"),
            (emp_ids[2], (date.today() - timedelta(days=10)).isoformat(), (date.today() - timedelta(days=8)).isoformat(), "Earned", "Annual vacation", "Approved"),
            (emp_ids[3], (date.today() - timedelta(days=5)).isoformat(), (date.today() - timedelta(days=4)).isoformat(), "Personal", "Personal emergency", "Approved"),
            (emp_ids[4], (date.today() + timedelta(days=7)).isoformat(), (date.today() + timedelta(days=12)).isoformat(), "Casual", "Exceeds max consecutive limit", "Pending"),
        ]
        for e_id, s_d, e_d, l_t, r_s, stat in sample_leaves:
            cur.execute("""INSERT INTO leaves(employee_id,start_date,end_date,leave_type,reason,status,applied_on)
                           VALUES(?,?,?,?,?,?,?)""", (e_id, s_d, e_d, l_t, r_s, stat, today_iso))
        c.commit()

    # Seed 30 days of attendance for demo employee if not already seeded
    emp_row = cur.execute("SELECT employee_id FROM employees WHERE email=?",
                          ("employee@company.com",)).fetchone()
    if emp_row:
        emp_id = emp_row[0]
        att_count = cur.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=?", (emp_id,)).fetchone()[0]
        if att_count == 0:
            start = date.today() - timedelta(days=29)
            for i in range(30):
                d = start + timedelta(days=i)
                status = "Absent" if i in (4, 11, 20) else "Present"
                cur.execute("""INSERT OR IGNORE INTO attendance(employee_id,att_date,status)
                               VALUES(?,?,?)""", (emp_id, d.isoformat(), status))
            c.commit()

    c.close()
