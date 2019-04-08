import requests
from django.shortcuts import render
import datetime
import time
from .models import GroupVkProfile


# Create your views here.

def main(request):
    title = 'Рабочее пространство'# Заголовок страницы
    content = {'title':title}
    return render(request, 'dataqueryapp/base.html', content)


def test(request):
    TOKEN = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
    VERSION = '5.92'
    offset = 0
    all_posts = []
    date_x = 1552250789
    total_posts_dict = []
    IDENTITY = 0
    title = "Поиск групп" # Заголовок страницы

    if request.POST:
        IDENTITY = '-{}'.format(request.POST.get('identity'))

    while True:
        r = requests.post('https://api.vk.com/method/wall.get', params={'owner_id': IDENTITY, 'access_token': TOKEN,
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

        data_set = {
            'id': post_id,
            'likes': post_likes,
            'date': post_date,
            'text': post_text,
            'comments': post_comments,
            'reposts': post_reposts
        }

        bd_group_profile = GroupVkProfile(posts_id=post_id, posts_likes=post_likes, posts_date=post_date,
                                          posts_comments=post_comments, posts_reposts=post_reposts)
        bd_group_profile.save()
        total_posts_dict.append(data_set)

    data = {'posts': total_posts_dict, 
            'title': title,
    }

    return render(request, 'dataqueryapp/test.html', context=data)


def similar_members(request):
    title = "Similar_members" # Заголовок страницы
    token = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
    groups_list = []
    version = '5.92'
    groups_data = {}  # {'identity1': {'photo' : 'http://', 'count': 12, 'members': [1, 2, 3, 4 ... n]}
    clock = 0
    idx_groups_data = 0
    total_data = {}  # {'groups': [{},{}], 'members': [{},{}...]} контекст для страницы
    groups = 0
    list_of_similar_members = []
    total_members = []
    

    if request.POST:
        groups = '{}'.format(request.POST.get('groups'))

    r = requests.post('https://api.vk.com/method/groups.getById', params={'group_ids': groups,
                                                                         'access_token': token,
                                                                         'v': version,
                                                                         'fields': 'members_count'})

    total_data['groups'] = r.json()['response']

    for group in total_data['groups']:
        groups_list.append(int(group['id']))

    time.sleep(1)

    for group in groups_list:
        groups_data['{}'.format(group)] = {'members': []}
        offset = 0
        while True:
            if clock % 3 == 0 and clock != 0:
                time.sleep(1)

            clock += 1

            r = requests.post('https://api.vk.com/method/execute',
                             params={'code': 'var offset = {};'.format(offset) +
                                             'var i = 0;'
                                             'var groupId = {};'.format(group) +
                                             'var members = null;'
                                             'var membersList = [];'
                                             'while (i < 25) {'
                                             'members = API.groups.getMembers({"group_id": groupId,'
                                             '"count" : 1000, "offset": offset}).items;'
                                             'membersList = membersList + members;'
                                             'i = i + 1;'
                                             'offset = offset + 1000;'
                                             '};'
                                             'return membersList;',

                                     'access_token': token,
                                     'v': version})

            members = r.json()['response']

            if len(members) == 0:
                break

            groups_data['{}'.format(group)]['members'].extend(members)

            offset += 25000

        # Делаем список пользователей для текущей группы словарем.
        groups_data['{}'.format(group)]['members'] = set(groups_data['{}'.format(group)]['members'])

        idx_groups_data += 1

    similar_members = list(
        groups_data['{}'.format(groups_list[0])]['members'] & groups_data['{}'.format(groups_list[1])]['members'])

    quantity_of_similar = len(similar_members)

    slices = quantity_of_similar//200 + 1

    # Создаем список из строк по 200 ids в каждой строке
    for i in range(0, slices):
        stroke = ','.join(map(str, similar_members[0:200]))
        list_of_similar_members.append(stroke)
        del similar_members[0:200]

    # Сохраняем в данные количество пересечений
    total_data['quantity_of_similar'] = quantity_of_similar

    for ids in list_of_similar_members:
        if clock % 3 == 0 and clock != 0:
            time.sleep(1)
        clock += 1

        r = requests.post('https://api.vk.com/method/users.get',
                          params={'user_ids': ids,
                                  'access_token': token,
                                  'v': version,
                                  'fields': 'connections, photo_200'})

        total_members.extend(r.json()['response'])

    total_data['members'] = total_members

    

    return render(request, 'dataqueryapp/similar_members.html', total_data)