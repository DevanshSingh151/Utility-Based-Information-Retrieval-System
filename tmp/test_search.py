import requests
import json
import time

def test_search():
    url = "http://localhost:5000/api/search"
    payload = {
        "query": "CPU architecture",
        "user_id": "test_user"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing search API (first request might trigger re-indexing)...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Search successful!")
            # print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception happened: {e}")

if __name__ == "__main__":
    # Wait for app to be ready
    time.sleep(2)
    test_search()
