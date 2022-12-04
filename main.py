import json
import requests

url = 'https://reqres.in/api/users'


def get_users(page):
    headers = {
        'user-agent': 'AppleWebKit/537.36 (KHTML, like Gecko)'}
    r = requests.get(f'{url}?page={page}', headers=headers)
    return json.loads(r.text)['data']


def get_users_full_name_list(*args):
    try:
        id_from, id_to = args
    except ValueError:
        return []

    # see if we have to call both pages or just one of them is enough
    if id_to <= 6:
        users = get_users(page=1)
    elif id_from > 6:
        users = get_users(page=2)
    else:
        users = get_users(page=1) + get_users(page=2)

    # it'd be better to implement pagination and reading
    # "per_page", "total" and "total_pages" fields.
    # but given that exact values are specified as entry conditions
    # I didn't use this approach

    full_name = lambda x: f'{x["first_name"]} {x["last_name"]}'
    selected_users = []
    for user in users:
        if id_from <= user['id'] <= id_to:
            selected_users.append(user)
    return sorted(full_name(x) for x in selected_users)


print(get_users_full_name_list(0, 0))