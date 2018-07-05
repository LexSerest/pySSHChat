from pysshchat.commands import register
from pysshchat.store import store

@register("help", "f1")
def do_help(user, args):
    user.local("text.help")


@register("color", "f2")
def do_color(user, args):
    user.change_color()


@register("list", "f3")
def do_color(user, args):
    user.local("Online: " + ", ".join(store.users.keys()), off_formatting=True)


@register("me")
def do_me(user, args):
    user.send("plugins.me", " ".join(args))


@register("quit")
def do_close(user, args):
    user.exit()
