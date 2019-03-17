import requests
from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
from .models import GroupVkProfile 


# Create your views here.

def main(request):
    
    return render(request, 'dataqueryapp/base.html')


def test(request):
    TOKEN = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
    VERSION = '5.92'
    offset = 0
    all_posts = []
    date_x = 1552250789
    total_posts_dict = []

    if request.POST:
        IDENTITY = '-{}'.format(request.POST.get('identity'))

    while True:
        r = requests.get('https://api.vk.com/method/wall.get', params={'owner_id': IDENTITY, 'access_token': TOKEN,
                                                                       'v': VERSION, 'count': 100, 'offset': offset})

        posts = r.json()['response']['items']

        all_posts.extend(posts)

        oldest_post_date = posts[-1]['date']

        if oldest_post_date < date_x:
            break

        offset += 100

    for post in all_posts:

        try:
            post_id = post['id']
        except:
            post_id = 0

        try:
            post_date = datetime.datetime.fromtimestamp(post['date']).strftime('%H:%M:%S %d-%m-%Y')
        except:
            post_date = 0

        try:
            post_text = post['text']
        except:
            post_text = 0

        try:
            post_likes = post['likes']['count']
        except:
            post_likes = 0

        try:
            post_comments = post['comments']['count']
        except:
            post_comments = 0

        try:
            post_reposts = post['reposts']['count']
        except:
            post_reposts = 0
        

        GroupVkProfile.objects.all()

        dataset = {
            'id': post_id,
            'likes': post_likes,
            'date': post_date,
            'text': post_text,
            'comments': post_comments,
            'reposts': post_reposts
        }
        
        bd_group_profile= GroupVkProfile(posts_id= post_id, posts_likes= post_likes, posts_date=post_date, posts_comments= post_comments, posts_reposts= post_reposts)
        bd_group_profile.save()
        total_posts_dict.append(dataset)

    data = {'posts': total_posts_dict}


    return render(request, 'dataqueryapp/test.html', context=data)
