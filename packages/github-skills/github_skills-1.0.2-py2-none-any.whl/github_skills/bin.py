import sys
from tabulate import tabulate
from github_skills import get_skills
from github_skills.exceptions import RateLimitException


def run():
    if len(sys.argv) < 2:
        print('Usage: github-skills <username>')
        return

    try:
        skills = get_skills(sys.argv[1])
    except RateLimitException as e:
        print(e.message)
        return

    print(tabulate(
        [(s['language'], '{}%'.format(s['percentage'])) for s in skills],
        headers=['language', 'percentage']
    ))
