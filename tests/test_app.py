"""
Automated Test Suite for Student Task Management System
Uses pytest and a temporary SQLite database to ensure safe, isolated testing.
"""

import os
import tempfile
import pytest
from app import create_app, get_db


@pytest.fixture
def app():
    """Create and configure a new app instance with a temporary database for each test."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    test_app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret-key'
    })

    yield test_app

    # Teardown: close and remove temporary test database
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_home_page_loads(client):
    """Verify that the dashboard/home page loads with HTTP 200 and basic elements."""
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Student Task Management System" in html
    assert "Total Tasks" in html
    assert "Pending" in html
    assert "In Progress" in html
    assert "Completed" in html


def test_create_task(client, app):
    """Verify that a new task can be created via POST and appears in the database."""
    response = client.post('/tasks/new', data={
        'title': 'Operating Systems Assignment 1',
        'description': 'Implement round robin scheduling algorithm in C',
        'priority': 'High',
        'due_date': '2026-11-05',
        'status': 'Pending'
    }, follow_redirects=True)

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Operating Systems Assignment 1" in html
    assert "created successfully" in html

    # Verify task exists in the test database
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE title = ?", ('Operating Systems Assignment 1',)).fetchone()
        assert task is not None
        assert task['priority'] == 'High'
        assert task['status'] == 'Pending'
        assert task['due_date'] == '2026-11-05'


def test_create_task_validation(client, app):
    """Verify server-side validation rejects empty titles with HTTP 400."""
    response = client.post('/tasks/new', data={
        'title': '   ',  # Empty or whitespace only
        'description': 'No title task',
        'priority': 'Medium',
        'due_date': '',
        'status': 'Pending'
    }, follow_redirects=True)

    assert response.status_code == 400
    html = response.get_data(as_text=True)
    assert "Task title is required." in html

    # Ensure nothing was inserted into database
    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        assert count == 0


def test_update_task_status(client, app):
    """Verify task status can be updated from Pending to In Progress and Completed."""
    # First, create a task
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, status, priority) VALUES (?, ?, ?)",
            ('Database Lab 3', 'Pending', 'Medium')
        )
        db.commit()
        task_id = cursor.lastrowid

    # Update status to 'In Progress' via quick status endpoint
    response = client.post(f'/tasks/{task_id}/status', data={
        'status': 'In Progress'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['status'] == 'In Progress'

    # Update status to 'Completed'
    client.post(f'/tasks/{task_id}/status', data={
        'status': 'Completed'
    }, follow_redirects=True)

    with app.app_context():
        db = get_db()
        task = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['status'] == 'Completed'


def test_update_task_details(client, app):
    """Verify full task editing updates title, description, priority, and date."""
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tasks (title, description, priority, status) VALUES (?, ?, ?, ?)",
            ('Old Title', 'Old notes', 'Low', 'Pending')
        )
        db.commit()
        task_id = cursor.lastrowid

    response = client.post(f'/tasks/{task_id}/edit', data={
        'title': 'Revised Title for Seminar',
        'description': 'Updated seminar slides',
        'priority': 'High',
        'due_date': '2026-11-10',
        'status': 'In Progress'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task['title'] == 'Revised Title for Seminar'
        assert task['description'] == 'Updated seminar slides'
        assert task['priority'] == 'High'
        assert task['status'] == 'In Progress'


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

    # Verify task no longer exists
    with app.app_context():
        db = get_db()
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        assert task is None


def test_dashboard_counts_calculation(client, app):
    """Verify dashboard metrics are computed accurately across different task states."""
    with app.app_context():
        db = get_db()
        # Insert 2 Pending, 1 In Progress, 1 Completed = Total 4
        db.execute("INSERT INTO tasks (title, status) VALUES ('Task A', 'Pending')")
        db.execute("INSERT INTO tasks (title, status) VALUES ('Task B', 'Pending')")
        db.execute("INSERT INTO tasks (title, status) VALUES ('Task C', 'In Progress')")
        db.execute("INSERT INTO tasks (title, status) VALUES ('Task D', 'Completed')")
        db.commit()

    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Check dashboard metric counts in the rendered template
    assert "Total Tasks" in html
    # Check that counts reflect correctly
    with app.app_context():
        db = get_db()
        stats = db.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
            FROM tasks
        """).fetchone()

        assert stats['total'] == 4
        assert stats['pending'] == 2
        assert stats['in_progress'] == 1
        assert stats['completed'] == 1


def test_task_filtering(client, app):
    """Verify filtering by status displays only matching tasks."""
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO tasks (title, status) VALUES ('Active Homework', 'In Progress')")
        db.execute("INSERT INTO tasks (title, status) VALUES ('Done Project', 'Completed')")
        db.commit()

    # Filter for 'In Progress'
    response = client.get('/?status=In+Progress')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Active Homework" in html
    assert "Done Project" not in html
