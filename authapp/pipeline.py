
def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == "vk-oauth2":
        if 'first_name' in response.keys():
            user.smauserprofile.first_name = response['first_name']

        if 'last_name' in response.keys():
            user.smauserprofile.last_name = response['last_name']

        if 'access_token' in response.keys():
            user.smauserprofile.vk_access_token = response['access_token']

        user.save()

    return