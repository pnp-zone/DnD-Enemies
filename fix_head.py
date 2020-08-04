#!/usr/bin/env python3

template = """
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{}</title>
    <link rel="shortcut icon" href="static/images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="static/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="static/index.css">
    <script src="static/jquery.js"></script>
    <script src="static/bootstrap.js"></script>
    <script src="static/index.js"></script>
    <script src="static/spells.js"></script>
    <script src="static/monsters.js"></script>
    <script src="static/magicitems.js"></script>
</head>
"""

def fix_head(fpath):
    with open(fpath) as f:
        html = f.read()

    start = html.find("<head>")
    end = html.find("</head>", start) + len("</head>")

    pre = html[:start]
    head = html[start:end]
    post = html[end:]

    start = head.find("<title>") + len("<title>")
    end = head.find("</title>", start)

    title = head[start:end]
    head = template.format(title)

    with open(fpath, "w") as f:
        f.write(pre + head + post)

if __name__ == "__main__":
    import sys
    fix_head(sys.argv[1])
