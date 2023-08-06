import requests
import json
from github_skills.exceptions import RateLimitException


def get_skills(username):
    skills = {}
    resp = requests.get('https://api.github.com/users/' + username + '/repos')

    if resp.status_code != 200:
        raise RateLimitException(json.loads(resp.text)['message'])

    repos = json.loads(resp.text)
    count = 0

    for repo in filter(lambda x: x['language'] is not None, repos):
        skills[repo['language']] = 1 if repo['language'] not in skills else\
            skills[repo['language']] + 1

        count += 1

    return map(
        lambda x: {
            'language': x[0],
            'percentage': (float(x[1]) / float(count)) * 100
        },
        skills.items()
    )
