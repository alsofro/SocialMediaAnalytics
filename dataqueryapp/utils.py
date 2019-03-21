from django.conf import settings
from mainapp.models import VkGroups
import requests
import re


def sanitize_identity(identity):
    if re.match(r'\d+', identity):  # number
        return identity
    elif re.match(r'[A-Za-z0-9~_.-]', identity):  # ascii
        return get_group_id_by_name(identity)


def get_group_id_by_name(group_name):
    try:
        vk_group_id = VkGroups.objects.filter(screen_name=group_name)[0].vk_group_id
        return str(vk_group_id)
    except:
        # TODO token = request.user.vk_token
        token = '20b77cd4812b234c2d0f4d4a288bdf12809c0a76b5e7225d42c001829d355bcac63691196dbe0a6a83598'
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params={'group_ids': group_name,
                                        'access_token': token,
                                        'v': settings.VK_API_VERSION,
                                        'fields': 'description'}
                                )
        response = response.json()['response'][0]
        vk_group = VkGroups.objects.create(vk_group_id=int(response['id']))
        vk_group.name = response['name']
        vk_group.screen_name = response['screen_name']
        vk_group.is_closed = response['is_closed']
        vk_group.type = response['type']
        vk_group.description = response['description']
        vk_group.save()

        return response['id']

