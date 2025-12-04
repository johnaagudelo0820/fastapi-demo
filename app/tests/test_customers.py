from fastapi import status

def test_create_customer(client_fixture):
    response = client_fixture.post("/customers", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "description": "Customer description",
    })
    assert response.status_code == status.HTTP_201_CREATED