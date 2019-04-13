import requests
import xmltodict


def get_vk_data(total_members):
    for member in total_members:

        identity = member['id']

        url = 'https://vk.com/foaf.php?id={}'.format(identity)

        r = requests.get(url).text

        parsed = xmltodict.parse(r)

        person = parsed['rdf:RDF']['foaf:Person']

        member['status'] = person['foaf:weblog']['@dc:title']
        member['created'] = person['ya:created']['@dc:date'].replace("-", ".").replace("T", " | ").replace("+03:00", "")
        member['last_logged_in'] = person['ya:lastLoggedIn']['@dc:date'].replace("-", ".").replace("T", " | ").replace("+03:00", "")
        member['friends'] = person['ya:friendsCount']
        member['subscribers'] = person['ya:subscribersCount']
        member['location'] = person['ya:location']['@ya:city']
