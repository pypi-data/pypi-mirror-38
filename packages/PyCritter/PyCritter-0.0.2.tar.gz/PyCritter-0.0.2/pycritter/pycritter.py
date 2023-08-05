import requests

token = None
user_id = None


class APIError(Exception):
    pass


def error(res):
    if res.status_code is 200 or res.status_code is 201:
        pass
    else:
        raise APIError('Error {}. The server returned the following message:\n'
                       '{}'.format(res.status_code, res.text))
    return res.json()


def _url(path):
    return 'https://critterdb.com/api' + path


# Creatures
def get_creature(id):
    return error(requests.get(
        url=_url('/creatures/' + id),
        headers={'x-access-token': token}
    ))


def create_creature(creature):
    return error(requests.post(
        url=_url('/creatures'),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=creature
        ))


def update_creature(id, creature):
    return error(requests.put(
        url=_url('/creatures/' + id),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=creature
        ))


def delete_creature(id):
    return error(requests.delete(
        url=_url('/creatures/' + id),
        headers={'x-access-token': token}
    ))


# Bestiaries
def get_bestiary(id):
    return error(requests.get(
        url=_url('/bestiaries/' + id),
        headers={'x-access-token': token}
        ))


def get_bestiary_creatures(id):
    return error(requests.get(
        url=_url('/bestiaries/' + id + '/creatures'),
        headers={'x-access-token': token}
        ))


def create_bestiary(bestiary):
    """bestiary should be json with the following structure:
    {
        "name": "your string, required",
        "description": "your string, optional",
        "ownerId": "your userId string, required"
    }
    """
    return error(requests.post(
        url=_url('/bestiaries'),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=bestiary
        ))


def update_bestiary(id, bestiary):
    """bestiary should be JSON as returned by get_bestiary"""
    return error(requests.put(
        url=_url('/bestiaries/' + id),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=bestiary
        ))


def delete_bestiary(id):
    return error(requests.delete(
        url=_url('/bestiaries/' + id),
        headers={'x-access-token': token}
        ))


# Published bestiaries
def search_published(query, page=1):
    """query should be JSON with structure:
    {"name": "your search term"}
    """
    return error(requests.post(
        url=_url('publishedbestiaries/search/' + str(page)),
        body=query
    ))


def like(id):
    return error(requests.post(
        url=_url('publishedbestiaries/' + id + '/likes'),
        headers={'x-access-token': token}
    ))


def unlike(id):
    return error(requests.delete(
        url=_url('publishedbestiaries/' + id + '/likes'),
        headers={'x-access-token': token}
    ))


def favorite(id):
    return error(requests.post(
        url=_url('publishedbestiaries/' + id + '/favorites'),
        headers={'x-access-token': token}
    ))


def unfavorite(id):
    return error(requests.delete(
        url=_url('publishedbestiaries/' + id + '/favorites'),
        headers={'x-access-token': token}
    ))


def get_most_popular():
    return error(requests.get(
        url=_url('/publishedbestiaries/mostpopular')
    ))


def get_recent(page):
    return error(requests.get(
        url=_url('/publishedbestiaries/recent/' + str(page))
    ))


def get_popular(page):
    return error(requests.get(
        url=_url('/publishedbestiaries/popular/' + str(page))
    ))


def get_favorites(page):
    return error(requests.get(
        url=_url('/publishedbestiaries/favorites/' + str(page)),
        headers={'x-access-token': token}
    ))


def get_owned(page):
    return error(requests.get(
        url=_url('/publishedbestiaries/owned/' + str(page)),
        headers={'x-access-token': token}
    ))


def add_comment(id, comment):
    """{
        "text": "comment text",
        "author": "user id"
    }"""
    return error(requests.put(
        url=_url('/publishedbestiaries/' + id + '/comments'),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=comment
    ))


def update_comment(bestiary_id, comment_id, comment):
    return error(requests.put(
        url=_url('/publishedbestiaries/' + bestiary_id
                 + '/comments/' + comment_id),
        headers={'x-access-token': token},
        body=comment
        ))


def delete_comment(bestiary_id, comment_id):
    return error(requests.delete(
        url=_url('/publishedbestiaries/' + bestiary_id
                 + '/comments/' + comment_id),
        headers={'x-access-token': token}
        ))


def get_published_creatures(id, page):
    return error(requests.get(
        url=_url('/publishedbestiaries/' + id + '/creatures')
        ))


def delete_published_creatures(id):
    """Deletes ALL creatures from selected published bestiary."""
    return error(requests.delete(
        url=_url('/publishedbestiaries/' + id),
        headers={'x-access-token': token}
        ))


def get_published(id):
    return error(requests.get(
        url=_url('/publishedbestiaries/' + id)
        ))


def create_published(bestiary):
    return error(requests.post(
        url=_url('/publishedbestiaries'),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=bestiary
        ))


def update_published(id, bestiary):
    return error(requests.put(
        url=_url('/publishedbestiaries' + id),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        body=bestiary
        ))


def delete_published(id):
    return error(requests.delete(
        url=_url('/publishedbestiaries' + id),
        headers={'x-access-token': token}
        ))


# Users
def get_user_bestiaries():
    return error(requests.get(
        url=_url('/users/' + str(user_id) + '/bestiaries'),
        headers={'x-access-token': token}
        ))


def get_user_published(page):
    return error(requests.get(
        url=_url('/users/' + str(user_id) + '/publishedbestiaries/' + page)
        ))


def get_user_creatures(page):
    return error(requests.get(
        url=_url('/users/' + str(user_id) + '/creatures/' + page),
        headers={'x-access-token': token}
        ))


def get_public():
    return error(requests.get(
        url=_url('/users/' + str(user_id) + '/public'),
        headers={'x-access-token': token}
        ))


def search_public(user_dict):
    return error(requests.get(
        url=_url('/users/search'),
        headers={'x-access-token': token,
                 'Content-Type': 'application/json'},
        json=user_dict
        ))

# I'm going to leave user management alone for now. There aren't many legit
# reasons to create or delete users through the API (that I can think of).


# Authentication
def get_current_user():
    return error(requests.get(
        url=_url('/authenticate/user'),
        headers={'x-access-token': token}
    ))


def login(username, password, rememberme=False):
    global token, user_id
    auth_dict = {'username': username,
                 'password': password,
                 'rememberme': rememberme}
    res = requests.post(
        url=_url('/authenticate'),
        headers={'Content-Type': 'application/json'},
        json=auth_dict
    )
    if res.status_code is 200 or res.status_code is 201:
        token = res.text
        user_id = get_current_user()['_id']
        return token
    else:
        raise APIError('Error {}. The server returned the following message:\n'
                       '{}'.format(res.status_code, res.text))
        return False


# The revokeauthentication endpoint seems to only be to clear auth cookies.
def logout():
    res = requests.get(url=_url('/revokeauthentication'))
    if res.status_code is 200 or res.status_code is 201:
        pass
    else:
        raise APIError('Error {}. The server returned the following message:\n'
                       '{}'.format(res.status_code, res.text))


def set_token(new_token):
    global token, user_id
    token = new_token
    user_id = get_current_user()['_id']
