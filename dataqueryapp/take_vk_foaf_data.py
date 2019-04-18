import requests
import xmltodict


def get_vk_data(total_members):
    for member in total_members:
        try:
            identity = member['id']

            url = 'https://vk.com/foaf.php?id={}'.format(identity)

            r = requests.get(url).text

            parsed = xmltodict.parse(r)

            person = parsed['rdf:RDF']['foaf:Person']

            try:
                member['created'] = person['ya:created']['@dc:date'].replace("-", ".").replace("T", " ").replace(
                    "+03:00", "")
            except:
                member['created'] = False
            try:
                member['last_logged_in'] = person['ya:lastLoggedIn']['@dc:date'].replace("-", ".").replace("T",
                                                                                                           " ").replace(
                    "+03:00", "")
            except:
                member['last_logged_in'] = False
            try:
                member['friends'] = person['ya:friendsCount']
            except:
                member['friends'] = False
        except:
            member['created'] = False
            member['last_logged_in'] = False
            member['friends'] = False
