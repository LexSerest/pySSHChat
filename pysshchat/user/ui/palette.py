_palette = [
    ("divider", "black", "dark cyan", "standout"),
    ("text", "yellow", "default"),
    ("bold_text", "light gray", "default", "bold"),
    ("bold", "bold", ""),
    ("italics", "italics", ""),
    ("underline", "underline", ""),
    ("body", "text"),
    ("footer", "text"),
    ("header", "text"),
    ("list", "black", "light gray"),
    ("msg_info", "black", "dark cyan", "bold"),
    ("info", "default", "dark cyan", "bold"),
    ("title", "bold", "dark cyan", "bold"),
    ("body", "dark cyan", "", ""),
    ("msg_danger", "black", "dark red", "bold"),
    ("default", "", "", "")
]

for id in range(255):
    _palette.append(("h" + str(id), "", "", "", "h" + str(id), "default"))


def palette():
    return _palette

