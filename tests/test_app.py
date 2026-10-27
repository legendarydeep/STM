"""
Automated Test Suite for TaskMate — Student Task Management System
Uses pytest and an isolated temporary SQLite database for regression safety.
"""

import os
import tempfile
import pytest
from app import create_app, get_db


@pytest.fixture
def app():
    """Create and configure a clean app instance with a temporary database for each test."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    test_app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret-key'
    })

    yield test_app

    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_home_page_loads(client):
    """Verify that the dashboard/home page loads with HTTP 200 and all metric cards."""
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "TaskMate" in html
    assert "Total Tasks" in html
    assert "Completed" in html
    assert "Pending" in html
    assert "Overdue" in html


def test_create_task(client, app):
    """Verify that a new task can be created via POST and appears in the database."""
    response = client.post('/tasks/new', data={
        'title': 'Operating Systems Assignment 1',
        'subject': 'Operating Systems',
        'description': 'Implement round robin scheduling algorithm in C',
        'priority': 'High',
        'due_date': '2026-11-05',
        'status': 'Pending'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Operating Systems Assignment 1" in html
    assert "created successfully" in html

    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE title = ?", ('Operating Systems Assignment 1',)).fetchone()
        assert task is not None
        assert task['subject'] == 'Operating Systems'
        assert task['priority'] == 'High'
        assert task['status'] == 'Pending'
        assert task['due_date'] == '2026-11-05'


def test_create_task_validation(client, app):
    """Verify server-side validation rejects empty titles with HTTP 400."""
    response = client.post('/tasks/new', data={
        'title': '   ',  # Empty or whitespace only
        'subject': 'Mathematics',
        'description': 'No title task',
        'priority': 'Medium',
        'due_date': '',
        'status': 'Pending'
    }, follow_redirects=True)

    assert response.status_code == 400
    html = response.get_data(as_text=True)
    assert "Task title is required." in html

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        assert count == 0


def test_update_task_status(client, app):
    """Verify task status can be updated from Pending to Completed."""
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, subject, status, priority) VALUES (?, ?, ?, ?)",
            ('Database Lab 3', 'Database Systems', 'Pending', 'Medium')
        )
        db.commit()
        task_id = cursor.lastrowid

    response = client.post(f'/tasks/{task_id}/status', data={
        'status': 'Completed'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['status'] == 'Completed'


def test_toggle_task(client, app):
    """Verify one-click checkbox toggle between Completed and Pending."""
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, status) VALUES ('Quick Toggle Task', 'Pending')"
        )
        db.commit()
        task_id = cursor.lastrowid

    # Toggle to Completed
    client.post(f'/tasks/{task_id}/toggle', follow_redirects=True)
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['status'] == 'Completed'

    # Toggle back to Pending
    client.post(f'/tasks/{task_id}/toggle', follow_redirects=True)
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['status'] == 'Pending'


def test_update_task_details(client, app):
    """Verify editing updates title, subject, description, priority, and date."""
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, subject, description, priority, status) VALUES (?, ?, ?, ?, ?)",
            ('Old Title', 'General', 'Old notes', 'Low', 'Pending')
        )
        db.commit()
        task_id = cursor.lastrowid

    response = client.post(f'/tasks/{task_id}/edit', data={
        'title': 'Revised Title for Seminar',
        'subject': 'Web Development',
        'description': 'Updated seminar slides',
        'priority': 'High',
        'due_date': '2026-11-10',
        'status': 'Pending'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['title'] == 'Revised Title for Seminar'
        assert task['subject'] == 'Web Development'
        assert task['description'] == 'Updated seminar slides'
        assert task['priority'] == 'High'


def test_delete_task(client, app):
    """Verify a task can be deleted successfully and is removed from the database."""
    with app.app_context():
        db = get_db()
        cursor = db.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", ('Task To Delete', 'Pending'))
        db.commit()
        task_id = cursor.lastrowid

    response = client.post(f'/tasks/{task_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "was deleted" in html

    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task is None


def test_dashboard_counts_calculation(client, app):
    """Verify dashboard metrics are computed accurately."""
    with app.app_context():
        db = get_db()
        # Insert 2 Pending (future due dates), 1 Completed, 1 Overdue (past due date)
        db.execute("INSERT INTO tasks (title, status, due_date) VALUES ('Task A', 'Pending', '2026-12-01')")
        db.execute("INSERT INTO tasks (title, status, due_date) VALUES ('Task B', 'Pending', '2026-12-02')")
        db.execute("INSERT INTO tasks (title, status, due_date) VALUES ('Task C', 'Completed', '2026-10-01')")
        db.execute("INSERT INTO tasks (title, status, due_date) VALUES ('Task D', 'Pending', '2020-01-01')") # Past date = Overdue
        db.commit()

    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Total Tasks" in html

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        assert count == 4


def test_task_filtering_and_tabs(client, app):
    """Verify tab filtering separates Pending and Completed tasks."""
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO tasks (title, status, subject) VALUES ('Active Homework', 'Pending', 'Mathematics')")
        db.execute("INSERT INTO tasks (title, status, subject) VALUES ('Done Project', 'Completed', 'Web Development')")
        db.commit()

    # Filter for Completed tab
    response = client.get('/tasks?tab=Completed')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Done Project" in html
    assert "Active Homework" not in html

    # Filter for Pending tab
    response_pending = client.get('/tasks?tab=Pending')
    assert response_pending.status_code == 200
    html_pending = response_pending.get_data(as_text=True)
    assert "Active Homework" in html_pending
    assert "Done Project" not in html_pending


def test_calendar_and_login_views(client):
    """Verify Calendar and Login pages render successfully with HTTP 200."""
    cal_res = client.get('/calendar')
    assert cal_res.status_code == 200
    assert "Calendar & Deadlines" in cal_res.get_data(as_text=True)

    login_res = client.get('/login')
    assert login_res.status_code == 200
    assert "TaskMate" in login_res.get_data(as_text=True)
    assert "Welcome Back!" in login_res.get_data(as_text=True)
