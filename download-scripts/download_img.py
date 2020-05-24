import requests, json
import sys

def get(url, data):
    response = requests.get(url, params=data)
    return response.json()

def search(query):
    url = "https://yts.mx/api/v2/list_movies.json"
    data ={
        "query_term" : query,
        "limit" : 50,
        "quality" : "720p"
    }
    response = get(url, data)
    data = response['data']
    if response['status'] == "ok":
        if data['movie_count'] == 0:
            return 1
        else:
            return data['movies'][0]['medium_cover_image']
    else:
        return 1

print(search(sys.argv[1]))    
