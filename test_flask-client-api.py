import requests, pytest#, json

ENDPOINT = 'http://localhost:5000/'
ENDPOINT2='http://localhost:5000/metrics'
# url='http://localhost:5000/'


def test_call_api():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


def test_call_api_2():
    response = requests.get(ENDPOINT2)
    assert response.status_code == 200
    pass


def test_post_api():
    json_data={"firstname": "bonjour", "lastname": "Musie"}
    response = requests.post(ENDPOINT, json=json_data)
    assert response.status_code == 200
