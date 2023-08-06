import requests
import json
from github_skills.exceptions import RateLimitException


def get_repos(username):
    page = 0
    repos = []

    while True:
        resp = requests.get(
            'https://api.github.com/users/' + username + '/repos?page={}'
            .format(page)
        )

        if resp.status_code != 200:
            raise RateLimitException(json.loads(resp.text)['message'])

        _repos = json.loads(resp.text)

        if _repos:
            [repos.append(r) for r in _repos]
            page += 1
        else:
            break

    return repos


def get_skills(username):
    skills = {}
    repos = get_repos(username)
    count = 0

    for repo in filter(lambda x: x['language'] is not None, repos):
        skills[repo['language']] = 1 if repo['language'] not in skills else\
            skills[repo['language']] + 1

        count += 1

    return sorted(
        map(
            lambda x: {
                'language': x[0],
                'percentage': (float(x[1]) / float(count)) * 100
            },
            skills.items()
        ),
        key=lambda x: x['percentage'],
        reverse=True
    )
