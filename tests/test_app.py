def test_home(client):
    response = client.get("/")
    assert b"<title>Redirecting...</title>" in response.data