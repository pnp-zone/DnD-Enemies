#!/usr/bin/env python3

import re


class Namespace:
    pass


pattern = Namespace()

pattern.name = re.compile(r"<h1>(.+)</h1>")
pattern.desc = re.compile(r"<p><em>"
                          r"(Medium|Large|Small|Huge|Tiny|Gargantuan|Diminutive|Colossal|Fine)"  # Size
                          r" ([\w ]+)"  # Race
                          r" ?(\(.*\))?"  # Subrace (optional)
                          r"(, [\w \-\(\)\%]+)"  # Alignment
                          r"</em></p>")
pattern.hp = re.compile(r"<p><strong>Hit Points</strong> (\d+) \(([d\d +-]+)\)</p>")
pattern.ac = re.compile(r"<p><strong>Armor Class</strong> (\d+)(.+)?</p>") # TODO make more specific
pattern.attr = re.compile(r"<li><strong>(\w\w\w)</strong> (\d+) \(([+-]\d+)\)</li>")
pattern.skills = re.compile(r"<p><strong>Skills</strong>(.*)</p>")
pattern.skill = re.compile(r"(\w+) ([+-]\d+)")
pattern.throws = re.compile(r"<p><strong>Saving Throws</strong>(.*)</p>")
pattern.throw = re.compile(r"(\w\w\w) ([+-]\d+)")

def get_section(fpath):
    with open(fpath) as f:
        html = f.read()

    start = html.find(">", html.find("<section")) + 1
    end = html.find("</section>", start)

    return html[start:end]

def parse(html):
    # Regex
    name = pattern.name.search(html).group(1)
    size, race, subrace, alignment = pattern.desc.search(html).groups()
    hp = pattern.hp.search(html)
    ac = pattern.ac.search(html)
    attrs = pattern.attr.findall(html)
    skills = pattern.skills.search(html)
    if skills is not None:
        skills = pattern.skill.findall(skills.group(1))
    throws = pattern.throws.search(html)
    if throws is not None:
        throws = pattern.throw.findall(throws.group(1))

    # Create sheet
    sheet = {
                "name": name,
                "size": size,
                "race": race,
                "subrace": subrace,
                "alignment": alignment,
                "hp": hp.group(2),
                "ac": int(ac.group(1)),
            }
    for attr in attrs:
        sheet[attr[0].lower()] = int(attr[2])

    if skills is not None:
        skill_dict = {}
        for skill, mod in skills:
            skill_dict[skill.lower()] = int(mod)
        sheet["skills"] = skill_dict

    if throws is not None:
        throws_dict = {}
        for throw, mod in throws:
            throws_dict[throw.lower()] = int(mod)
        sheet["saving_throws"] = throws_dict

    return sheet


if __name__ == "__main__":
    import sys, json, os

    if not os.path.isdir("sheets"):
        os.mkdir("sheets")

    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        with open("list") as f:
            files = f.read().splitlines()

    for name in files:
        html = get_section(f"html/{name}.html")
        sheet = parse(html)

        with open(f"sheets/{name.replace('-', '_')}.json", "w") as f:
            json.dump(sheet, f, indent=4)
