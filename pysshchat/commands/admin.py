from pysshchat.commands import register
from pysshchat.store import store


@register("info", is_admin=True)
def do_info(user, args):
    if len(args) != 1:
        return user.local("Use - /info <user nick>", off_formatting=True)

    find_user = store.users.get(args[0])

    if find_user:
        user.local("User: %s\n"
        "IP: %s\n"
        "Time connect: %s"
        % (find_user.username, find_user.ip, str(find_user.connected_date)[:19]), off_formatting=True)
    else:
        user.local("User is not found", off_formatting=True)


@register("kick", is_admin=True)
def do_kick(user, args):
    if len(args) != 1:
        return user.local("Use - /kick <user nick>", off_formatting=True)

    find_user = store.users.get(args[0])
    if find_user:
        find_user.exit()
    else:
        user.local("User is not found", off_formatting=True)


@register("ban", is_admin=True)
def do_ban(user, args):
    if len(args) != 1:
        return user.local("Use - /ban <user nick>", off_formatting=True)

    find_user = store.users.get(args[0])
    if find_user:
        store.bans[find_user.username] = find_user.ip
        find_user.exit()
    else:
        user.local("User is not found", off_formatting=True)


@register("unban", is_admin=True)
def do_unban(user, args):
    if len(args) != 1:
        return user.local("Use - /unban <user nick>", off_formatting=True)

    find_user = store.bans.get(args[0], False)

    if find_user:
        del store.bans[args[0]]
        user.local("User %s unban" % args[0], off_formatting=True)
    else:
        user.local("User is not found", off_formatting=True)