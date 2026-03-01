def test_login_page(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_register_and_login(client, db):
    # Register
    response = client.post(
        "/auth/register",
        data={
            "name": "Jane",
            "email": "jane@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Login
    response = client.post(
        "/auth/login",
        data={"email": "jane@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/auth/login" in response.location
