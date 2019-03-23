
from authapp.models import UserProfile

def save_user_profile(backend, user, response, *args, **kwargs):
    #print(response)
    if backend.name == "vk-oauth2":
        if 'first_name' in response.keys():
            UserProfile.first_name = response['first_name']

        if 'last_name' in response.keys():
            UserProfile.last_name = response['last_name']

        if 'domain' in response.keys():
            UserProfile.vk_username = response['domain']

        if 'access_token' in response.keys():
            UserProfile.vk_access_token = response['access_token']

    return