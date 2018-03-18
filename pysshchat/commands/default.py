from pysshchat.chats.globals import users


@register('color', True)
def do_color(user, args):
    user.set_color()
    user.reset_input()


@register('help', True)
def do_help(user, args):
    user.local('', 'text.help')
    user.reset_input()


@register('list', True)
def do_list(user, args):
    user.local('', 'plugins.userlist', list=', '.join(list(users)))
    user.reset_input()


@register('me')
def do_me(user, args):
    user._send(' '.join(args), 'plugins.me')

@register('quit')
def do_close(user, args):
    user.close()