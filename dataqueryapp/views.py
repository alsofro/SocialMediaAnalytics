import datetime
import requests
import time

from django.http import JsonResponse
from .models import GroupVkProfile
from authapp.models import SMAUserProfile
from mainapp.models import VkGroups
from django.conf import settings
from django.shortcuts import render
from dataqueryapp.utils import sanitize_user_input


def main(request):
    return render(request, 'dataqueryapp/base.html')


def test(request):
    token = SMAUserProfile.objects.get(pk=request.user.id).vk_access_token
    #token = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
    offset = 0
    all_posts = []
    date_x = 1552250789
    total_posts_dict = []
    identity = 0
    items_per_request = 100

    if request.POST:
        identity = sanitize_user_input(request.POST.get('identity'))
        #identity = '-{}'.format(identity)

    while True:
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'owner_id': identity,
                                 'access_token': token,
                                 'v': settings.VK_API_VERSION,
                                 'count': items_per_request,
                                 'offset': offset}
                         )
        response = r.json()
        if response.get('error'):
            if response['error'].get('error_code') == 5:
                print(response['error']['error_msg'])

        try:
            posts = response['response']['items']
        except KeyError:
            pass
            # TODO Show user that there is no such identity
            # Skip many try-excepts (break)
        if len(posts) == 0:
            pass
            # TODO Show user that there is no such identity
            # Skip many try-excepts (break)
        all_posts.extend(posts)
        oldest_post_date = posts[-1]['date']
        if oldest_post_date < date_x:
            break
        offset += items_per_request

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
        bd_group_profile = GroupVkProfile(posts_id=post_id,
                                          posts_likes=post_likes,
                                          posts_date=post_date,
                                          posts_text=post_text,
                                          posts_comments=post_comments,
                                          posts_reposts=post_reposts)
        bd_group_profile.save()
        total_posts_dict.append(data_set)

    data = {'posts': total_posts_dict}
    return render(request, 'dataqueryapp/test.html', context=data)


def similar_members(request):
    token = SMAUserProfile.objects.get(pk=request.user.id).vk_access_token
    #token = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
    groups_list = []
    groups_data = {}  # {'identity1': {'photo' : 'http://', 'count': 12, 'members': [1, 2, 3, 4 ... n]}
    clock = 0
    idx_groups_data = 0
    total_data = {}  # {'groups': [{},{}], 'members': [{},{}...]} контекст для страницы
    groups = 0
    list_of_similar_members = []
    total_members = []
    items_per_request = 1000

    if request.POST:
        groups = '{}'.format(request.POST.get('groups'))

    r = requests.get('https://api.vk.com/method/groups.getById',
                     params={'group_ids': groups,
                             'access_token': token,
                             'v': settings.VK_API_VERSION,
                             'fields': 'members_count'}
                     )


    total_data['groups'] = r.json()['response']
    for group in total_data['groups']:
        groups_list.append(int(group['id']))
    time.sleep(1)
    for group in groups_list:
        groups_data['{}'.format(group)] = {'members': []}
        offset = 0
        items_per_request = 1000
        items_per_request2 = 25000
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
                                     'v': settings.VK_API_VERSION})


            members = r.json()['response']
            if len(members) == 0:
                break
            groups_data['{}'.format(group)]['members'].extend(members)
            offset += items_per_request2

        # Делаем список пользователей для текущей группы словарем.
        groups_data['{}'.format(group)]['members'] = set(groups_data['{}'.format(group)]['members'])
        idx_groups_data += 1

    similar_members = list(
        groups_data['{}'.format(groups_list[0])]['members'] & groups_data['{}'.format(groups_list[1])]['members']
    )
    quantity_of_similar = len(similar_members)
    slices = quantity_of_similar//200 + 1

    # Создаем список из строк по 200 ids в каждой строке
    for _ in range(slices):
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
                                  'v': settings.VK_API_VERSION,
                                  'fields': 'connections, photo_200'})
        total_members.extend(r.json()['response'])

    total_data['members'] = total_members
    return render(request, 'dataqueryapp/similar_members.html', context=total_data)


def vk_groups_search(request):
    print("in da func >>>>>>>>>>>>>>>>>>>")
    print(request.POST)
    text_input = request.POST.get('text')
    result_groups = VkGroups.like_to_json(text_input)
    return JsonResponse({'data': result_groups})
