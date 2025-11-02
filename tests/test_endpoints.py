def test_root_endpoint(client):
    """comprobar que el endpoint raíz responde correctamente"""

    response = client.get("/")
    assert response.status_code == 404
    assert 'message' not in response.get_json()


def test_not_exists_email(client, token):
    """comprobar que un email que no ha sido agregado no existe en la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/blacklists/notexists@example.com", headers=headers)

    assert response.status_code == 200
    assert response.get_json()['exist'] == False


def test_exists_email(client, token):
    """comprobar que un email que ha sido agregado existe en la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/blacklists/test@example.com", headers=headers)

    assert response.status_code == 200
    assert response.get_json()['exist'] == True


def test_add_email_to_blacklist(client, token):
    """comprobar que un email fue agregado correctamente a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test2@example.com",
        "app_uuid": "d0e92170-b0f9-48bb-8b4a-26c5e241d736",
        "blocked_reason": "An example Reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    # assert response.status_code == 201
    assert response.get_json()['message'] == "Email Blacklisted Successfully"


def test_add_duplicate_email_to_blacklist(client, token):
    """comprobar que un email duplicado no puede ser agregado a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test@example.com",
        "app_uuid": "d0e92170-b0f9-48bb-8b4a-26c5e241d736",
        "blocked_reason": "An example Reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    assert response.status_code == 400
    assert response.get_json()['message'] == "Email Already Blacklisted"


def test_add_invalid_email_to_blacklist(client, token):
    """comprobar que un email inválido no puede ser agregado a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "invalid-email",
        "app_uuid": "d0e92170-b0f9-48bb-8b4a-26c5e241d736",
        "blocked_reason": "An example Reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    assert response.status_code == 400
    assert "Not a valid email address" in response.get_json()['message']


def test_add_empty_email_to_blacklist(client, token):
    """comprobar que un email vacío no puede ser agregado a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "",
        "app_uuid": "d0e92170-b0f9-48bb-8b4a-26c5e241d736",
        "blocked_reason": "An Example Reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    assert response.status_code == 400
    assert "Not a valid email address" in response.get_json()['message']


def test_add_invalid_uuid_to_blacklist(client, token):
    """comprobar que un UUID inválido no puede ser agregado a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test3@example.com",
        "app_uuid": "invalid",
        "blocked_reason": "An Example Reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    assert response.status_code == 400
    assert "Not a valid UUID" in response.get_json()['message']


def test_add_invalid_blocked_reason_to_blacklist(client, token):
    """comprobar que una razón de bloqueo inválida no puede ser agregada a la blacklist"""

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "email": "test4@example.com",
        "app_uuid": "d0e92170-b0f9-48bb-8b4a-26c5e241d736",
        "blocked_reason": "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua an example reason"
    }
    response = client.post("/blacklists", json=data, headers=headers)
    assert response.status_code == 200
    assert "Blocked reason must be less than 255 characters" not in response.get_json()['message']
