def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert 'message' in response.get_json()


def test_not_exists_email(client, token):

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/blacklists/notexists@example.com", headers=headers)

    assert response.status_code == 200
    assert response.get_json()['exist'] == False

def test_exists_email(client, token):

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/blacklists/test@example.com", headers=headers)

    assert response.status_code == 200
    assert response.get_json()['exist'] == True