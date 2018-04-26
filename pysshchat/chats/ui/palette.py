_palette = [
    ("divider", "black", "dark cyan", "standout"),
    ("text", "yellow", "default"),
    ("bold_text", "light gray", "default", "bold"),
    ("body", "text"),
    ("footer", "text"),
    ("header", "text"),
    ("list", "black", "light gray"),
    ("msg_info", "black", "dark cyan", "bold"),
    ("title", "bold", "dark cyan", "bold"),
    ("body", "dark cyan", "", ""),
    ("msg_danger", "black", "dark red", "bold"),
    ("admin", "", "", "bold", "h100", "default"),
    ("user", "", "", ""),
    ("default", "", "", "")
]

for id in range(255):
    _palette.append(("h" + str(id), "", "", "", "h" + str(id), "default"))


def palette():
    return _palette

