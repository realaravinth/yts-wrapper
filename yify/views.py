import os
import requests, json

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from bs4 import BeautifulSoup

from .models import Downloaded_movies, Downloading, Watch_history
    
def get(url, data):
    response = requests.get(url, params=data)
    return response.json()

def home(request, pageNum):
    url = "https://yts.mx/api/v2/list_movies.json"
    data = {
        "limit" : 15,
        "page" : pageNum,
        "quality" : "720p"
    }
    
    response = get(url, data)
    
    if response['status'] == "ok":
        data = response['data']
        data = data['movies']
        return render(request, "yts/home.html", {"movies" : data })
    else:
        raise Http404("Counldn't reach yts.mx, try reaching the site manually. If unreachable, contact admin")

def details(request,id):
    url = "https://yts.mx/api/v2/movie_details.json"
    data = {
        "movie_id" : id,
        "with_images" : "true",
    }

    response = get(url, data)
    
    if response['status'] == "ok":
        data = response['data']['movie']
        context = {
            "movie" : data,
            "magnet" : data['torrents'][0]['hash'],
            }
        return render(request, "yts/details.html", context )
    else:
        raise Http404("Counldn't reach yts.mx, try reaching the site manually. If unreachable, contact admin")

       
def search_bar(request):
    if request.POST.get('query'):
        return redirect(
            'search',
            query=request.POST.get('query')
        )
    else:
        raise Http404("Enter a search term")

def search(request, query):
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
            raise Http404("No results available, try IMDB codes for better results")
        else:
            return render(
            request, 
            "yts/search.html",
            {"movies" : data['movies']}
        )
    else:
        raise Http404("Counldn't reach yts.mx, try reaching the site manually. If unreachable, contact admin")

def check_local_avail(imdb):
    return Downloaded_movies.objects.all().filter(imdb_code=imdb).exists()

def check_download_queue(imdb):
    return Downloading.objects.all().filter(imdb_code=imdb).exists()

def check_user_downlads(username):
    return Downloading.objects.all().filter(download_by=username).exists()

def spawn_download_thread(t_hash, imdb):
    url = "'https://yts.mx/torrent/download/" + t_hash + "'"
    cmd = "/home/aravinth/moviesBatsense/download-scripts/download.sh" 
    md += " " + url + " " +  imdb + " " +  "&"
    #        os.run(cmd)

def create_downloading_record(username, yify_id, status):
    url = "https://yts.mx/api/v2/movie_details.json"
    data = {
        "movie_id" : yify_id,
        "with_images" : "true",
    }

    response = get(url, data)
    
    if response['status'] == "ok":
        movie = response['data']['movie']
        entry = Downloading.objects.create(
            download_by = username,
            title_long = movie['title_long'],
            year = movie['year'],
            yify_id = yify_id,
            imdb_code = movie['imdb_code'],
            genres = json.dumps(movie['genres']),
            rating = movie['rating'],
            description_intro = movie['description_intro'],
            yt_trailer_code = movie['yt_trailer_code'],
            size = movie['size'],
            runtime = movie['runtime'],
            progress = 'processing',
            downloading = status,
            img_url = movie['medium_cover_image']
            )
        entry.save()
    else:
        create_record(yify_id)

def check_num_downloads():
    if Downloading.objects.all().filter(downloading=True).count < 5:
        return True
    else:
        return False

def download(request, t_hash, imdb, yify_id):
    if check_local_avail(imdb):
        return redirect('stream',imdb_code=imdb)
    elif check_download_queue(imdb):
        return redirect('queue')
    else:
        if check_user_downlads(request.user.username):
            return render(request, 'yts/rate-limited.html', {'status':429})
        else:
            if check_num_downloads():
                spawn_download_thread(t_hash,imdb)
                create_downloading_record(
                    request.usern.username,
                    yify_id,
                    status=True
                )
            else:
                create_downloading_record(
                    request.usern.username,
                    yify_id,
                    status=True
                )
            return redirect('queue')

def queue(request):
    items = Downloading.objects.order_by('downloaded_on')
    return render(request, 'yts/queue.html', { "movies" : items })

def available(request):
    items = Downloaded_movies.order_by('downloaded_on')
    return render(request, 'yts/available.html', {"movies" : items})

def available_details(request, imdb):
    if Downloaded_movies.objects.all().filter(imdb_code=imdb).exists():
        movie = Downloaded_movies.objects.get(imdb_code=imdb)
        return render(request, 'yts/available_details.html', {'movie':movie})
    else:
        raise(Http404)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_history(title, username, ip_addr):
    activity = Watch_history.objects.create(
                    user = username,
                    ip = ip_addr,
                    title_long = title
               )
    activity.save()

def watch(request, imdb):
    if Downloaded_movies.objects.all().filter(imdb_code=imdb).exists():
        movie = Downloaded_movies.objects.get(imdb_code=imdb)
        log_history(
            movie.title_long,
            request.user.username,
            get_client_ip(request)
        )
        return render(request, 'yts/watch.html', {'movie':movie})
    else:
        raise(Http404)
