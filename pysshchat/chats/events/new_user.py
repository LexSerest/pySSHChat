import pysshchat.variables as variables


def new_user(user):
    for line in variables.history:
        user.local(line)
    user.local('', 'text.MOTD')
