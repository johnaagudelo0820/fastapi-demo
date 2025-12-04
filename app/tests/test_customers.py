from fastapi import status

def test_create_customer(client):
    response = client.post("/customers", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "description": "Customer description",
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_read_customer(client):
    response = client.post("/customers", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "description": "Customer description",
    })
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response = client.get(f"/customers/{customer_id}")
    assert response.json()["id"] == customer_id
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"
    assert response.json()["age"] == 30
    assert response.json()["description"] == "Customer description"
    assert response.status_code == status.HTTP_200_OK