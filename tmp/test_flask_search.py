import os
import sys
import json
from app import create_app

def test_flask_search():
    app = create_app()
    client = app.test_client()
    
    print("Sending search request via Flask test client...")
    response = client.post('/api/search', 
                            data=json.dumps({'query': 'CPU architecture', 'user_id': 'test_user'}),
                            content_type='application/json')
    
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print("Response data:")
        print(response.data.decode('utf-8'))
    else:
        print("Search successful!")
        # data = json.loads(response.data)
        # print(json.dumps(data, indent=2))

if __name__ == "__main__":
    os.environ['DATA_DIR'] = 'data'
    os.environ['INDEX_DIR'] = 'models'
    test_flask_search()
