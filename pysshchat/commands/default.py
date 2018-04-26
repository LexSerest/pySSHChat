import pysshchat.variables as variables
from pysshchat.chats.commands import register


@register("help", "f1")
def do_help(user, args):
    user.local("text.help")


@register("color", "f2")
def do_color(user, args):
    user.change_color()


@register("me")
def do_me(user, args):
    user.send(" ".join(args), "plugins.me")


@register("quit")
def do_close(user, args):
    user.quit()
