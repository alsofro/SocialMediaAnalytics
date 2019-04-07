from django.db.models import Q
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


"""
class VkUsers(models.Model):
    vk_user_id = models.PositiveIntegerField()
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    deactivated = models.CharField(max_length=8)
    is_closed = models.BooleanField(null=True)
    can_access_closed = models.BooleanField(null=True)
    about = models.CharField(max_length=40, null=True)
    activities = models.CharField(max_length=40, null=True)
    bdate = models.CharField(max_length=12, null=True)
    blacklisted = models.BooleanField(null=True)
    blacklisted_by_me = models.BooleanField(null=True)
    books = models.CharField(max_length=512, null=True)
    can_post = models.BooleanField(null=True)
    can_see_all_posts = models.BooleanField(null=True)
    can_see_audio = models.BooleanField(null=True)
    can_send_friend_request = models.BooleanField(null=True)
    can_write_private_message = models.BooleanField(null=True)
    career = JSONField(null=True)
    city = JSONField(null=True)
    common_count = models.PositiveIntegerField(null=True)
    connections = models.CharField(max_length=512, null=True)
    contacts = JSONField(null=True)
    counters = JSONField(null=True)
    country = JSONField(null=True)
    domain = models.CharField(max_length=12, null=True)
    education = JSONField(null=True)
    exports = models.CharField(max_length=128, null=True)
    followers_count = models.PositiveIntegerField(null=True)
    friend_status = models.PositiveIntegerField(null=True)
    games = models.CharField(max_length=512, null=True)
    has_mobile = models.BooleanField(null=True)
    has_photo = models.BooleanField(null=True)
    home_town = models.CharField(max_length=40, null=True)
    interests = models.CharField(max_length=512, null=True)
    is_favorite = models.BooleanField(null=True)
    is_friend = models.BooleanField(null=True)
    is_hidden_from_feed = models.BooleanField(null=True)
    last_seen = JSONField(null=True)
    lists = ArrayField(models.CharField(max_length=40, null=True))
    maiden_name = models.CharField(max_length=40, null=True)
    military = JSONField(null=True)
    movies = models.CharField(max_length=512, null=True)
    music = models.CharField(max_length=512, null=True)
    nickname = models.CharField(max_length=40, null=True)
    occupation = JSONField(null=True)
    online = models.BooleanField(null=True)
    personal = JSONField(null=True)
    photo_max_orig = models.CharField(max_length=128, null=True)
    quotes = models.CharField(max_length=512, null=True)
    relatives = JSONField(null=True)
    relation = models.PositiveIntegerField(null=True)
    schools = JSONField(null=True)
    screen_name = models.CharField(max_length=40, null=True)
    sex = models.BooleanField(null=True)
    site = models.CharField(max_length=40, null=True)
    status = models.CharField(max_length=40, null=True)
    timezone = models.PositiveIntegerField(null=True)
    trending = models.BooleanField(null=True)
    tv = models.CharField(max_length=40, null=True)
    universities = JSONField(null=True)
    verified = models.BooleanField(null=True)
    wall_default = models.CharField(max_length=40, null=True)
    #groups = models.ManyToManyField('VkGroups')
    #friends = models.ManyToManyField('VkUsers')
"""


class VkGroups(models.Model):
    vk_group_id = models.PositiveIntegerField()
    name = models.CharField(max_length=128, null=True)
    screen_name = models.CharField(max_length=20, null=True)
    is_closed = models.PositiveIntegerField(null=True)
    deactivated = models.CharField(max_length=8, null=True)
    is_admin = models.BooleanField(null=True)
    admin_level = models.PositiveIntegerField(null=True)
    is_member = models.BooleanField(null=True)
    invited_by = models.PositiveIntegerField(null=True)
    type = models.CharField(max_length=5, null=True)
    activity = models.CharField(max_length=128, null=True)
    age_limits = models.PositiveIntegerField(null=True)
    ban_info = JSONField(null=True)
    can_create_topic = models.BooleanField(null=True)
    can_message = models.BooleanField(null=True)
    can_post = models.BooleanField(null=True)
    can_see_all_posts = models.BooleanField(null=True)
    can_upload_doc = models.BooleanField(null=True)
    can_upload_video = models.BooleanField(null=True)
    city = JSONField(null=True)
    contacts = JSONField(null=True)
    counters = JSONField(null=True)
    country = JSONField(null=True)
    cover = JSONField(null=True)
    description = models.CharField(max_length=128, null=True)
    fixed_post = models.PositiveIntegerField(null=True)
    has_photo = models.BooleanField(null=True)
    is_favorite = models.BooleanField(null=True)
    is_hidden_from_feed = models.BooleanField(null=True)
    is_messages_blocked = models.BooleanField(null=True)
    links = JSONField(null=True)
    main_album_id = models.PositiveIntegerField(null=True)
    main_section = models.PositiveIntegerField(null=True)
    market = JSONField(null=True)
    member_status = models.PositiveIntegerField(null=True)
    members_count = models.PositiveIntegerField(null=True)
    place = JSONField(null=True)
    public_date_label = JSONField(null=True)
    site = models.CharField(max_length=64, null=True)
    start_date = models.CharField(max_length=10, null=True)
    finish_date = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=64, null=True)
    trending = models.BooleanField(null=True)
    verified = models.BooleanField(null=True)
    wall = models.PositiveIntegerField(null=True)
    wiki_page = models.CharField(max_length=40, null=True)
    #subscribers = models.ManyToManyField('VkUsers')
    @classmethod
    def like_to_json(cls, text_input):
        groups = []
        for group in VkGroups.objects.filter(
                        Q(name__contains=text_input) | Q(name__contains=text_input)
                        ).values():
            groups.append({
                'name': group['screen_name']
                #'description': group['description']
                #'name': group['name'],
            })
        return groups

    @classmethod
    def create_new_group(cls, group_json):
        vk_group = VkGroups.objects.create(vk_group_id=int(group_json['id']))
        vk_group.name = group_json['name']
        vk_group.screen_name = group_json['screen_name']
        vk_group.is_closed = group_json['is_closed']
        vk_group.type = group_json['type']
        vk_group.description = group_json['description']
        vk_group.save()

        return group_json['id']




class VkWalls(models.Model):
    vk_group_id = models.ForeignKey(VkGroups, on_delete=models.CASCADE) # ???
    wall_id = models.PositiveIntegerField(null=True)
    record_id = models.PositiveIntegerField(null=True)
    owner_id = models.PositiveIntegerField(null=True)
    from_id = models.PositiveIntegerField(null=True)
    date = models.PositiveIntegerField(null=True)
    text = models.TextField(null=True)
    reply_owner_id = models.PositiveIntegerField(null=True)
    reply_post_id = models.PositiveIntegerField(null=True)
    comments = models.PositiveIntegerField(null=True)
    likes = models.PositiveIntegerField(null=True)
    reposts = models.PositiveIntegerField(null=True)
    views = models.PositiveIntegerField(null=True)
    post_type = models.CharField(max_length=40, null=True)
    attachments = JSONField(null=True)
    geo = JSONField(null=True)
    signer_id = models.PositiveIntegerField(null=True)
    copy_history = JSONField(null=True)
    can_pin = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    can_edit = models.BooleanField(null=True)
    is_pinned = models.BooleanField(null=True)
    marked_as_ads = models.BooleanField(null=True)
    is_favorite = models.BooleanField(null=True)


"""

class VkComments(models.Model):
    comment_id = models.PositiveIntegerField(null=True)
    from_id = models.PositiveIntegerField(null=True)
    date = models.PositiveIntegerField(null=True)
    text = models.CharField(max_length=40, null=True)
    reply_to_user = models.PositiveIntegerField(null=True)
    reply_to_comment = models.PositiveIntegerField(null=True)
    attachments = JSONField(null=True)
    parents_stack = JSONField(null=True)
    thread = JSONField(null=True)
    # Связать со

"""
