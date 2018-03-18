from ..globals import get_history


def new_user(user):
    for line in get_history():
        user.local(line)
    user.local('', 'text.MOTD')
