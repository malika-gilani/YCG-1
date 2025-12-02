from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.testclient import TestClient
app = FastAPI()
API_KEY_NAME = "access-token"
API_KEY = "mysecret123"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
@app.get("/protected-data")
def protected_data(api_key: str = Depends(get_api_key)):
    return {"message": "This is protected data", "api_key": api_key}
@app.get("/public")
def public_endpoint():
    return {"message": "This is public data"}
client = TestClient(app)
def test_public_endpoint():
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "This is public data"}
def test_protected_endpoint_correct_key():
    response = client.get("/protected-data", headers={"access-token": API_KEY})
    assert response.status_code == 200
    assert response.json()["message"] == "This is protected data"
    assert response.json()["api_key"] == API_KEY
def test_protected_endpoint_wrong_key():
    response = client.get("/protected-data", headers={"access-token": "wrongkey"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate API key"}
if __name__ == "__main__":
    test_public_endpoint()
    test_protected_endpoint_correct_key()
    test_protected_endpoint_wrong_key()
    print("All tests passed ")
