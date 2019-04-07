import re
import requests
import time

from django.conf import settings
from mainapp.models import VkGroups


def sanitize_user_input(identity):
    if re.match(r'\d+', identity):  # number
        return identity

    elif re.match(r'public\d+', identity):
        number = identity.split('public')[1]
        return get_group_id_by_name(number)

    elif re.match(r'club\d+', identity):
        number = identity.split('club')[1]
        return get_group_id_by_name(number)

    elif re.match(r'[A-Za-z0-9~_.-]', identity):  # ascii
        return get_group_id_by_name(identity)


def get_group_id_by_name(group_name):
    try:
        vk_group_id = VkGroups.objects.filter(screen_name=group_name)[0].vk_group_id
        # FIXIT протестировать варианты формата group_ids
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
        for i in range(3):
            try:
                response = response.json()['response'][0]
                break
            except KeyError:
                time.sleep(1)

        group_id = VkGroups.create_new_group(response)
        return group_id

