import requests, json

def get(url, data):
    response = requests.get(url, params=data)
    return response.json()

def details(query):
    url = "https://yts.mx/api/v2/list_movies.json"
    data ={
        "query_term" : query,
        "limit" : 50
    }

    response = get(url, data)

    if response['status'] == "ok":
        data = response['data']
        if data['movie_count'] == 0:
            context = {
            "status" : "1"
        }
        else:
            movies = data['movies']
            context = {
                "status" : "0"
            }
            count = 0
            for i in movies:
                obj = {
                    "id" : i['id'],
                    "title" : i['title'],
                    "year" : i['year'],
                    "rating" : i['rating'],
                    "genres" : i['genres'],
                    "slug" : i['slug']
                }
                context[count] = obj
                count += 1
            return context

    