from github_skills import get_skills


def test_get_skills(username):
    skills = get_skills(username)

    assert isinstance(skills, list)
    assert reduce(lambda x, y: x + y, [s['percentage'] for s in skills])\
        == 100
