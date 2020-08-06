#!/usr/bin/env python3

import os
import json
import re

from sys import argv


class Parser:
    
    def __init__(self):
        """
        Initialize all patterns
        """
        self.main = re.compile(r""
                               r"<h1>(?P<name>.*)</h1>"
                               r"\n\n"
                               r"<p><em>"
                               r"(?P<size>Medium|Large|Small|Huge|Tiny|Gargantuan|Diminutive|Colossal|Fine) "
                               r"(?P<race>[\w]+|swarm of Tiny beasts) ?"
                               r"(?:\((?P<subrace>.*)\))?, "
                               r"(?P<alignment>[\w \-\(\)\%]+)"
                               r"</em></p>"
                               r"\n\n"
                               r"<hr>"
                               r"\n\n"
                               r"<p><strong>Armor Class</strong> "
                               r"(?P<ac>\d+) ?"
                               r"(?P<ac_alt>\((\d+ (?:with|while|in) [\w </>]+)\))? ?"
                               r"(?P<ac_types>\(([\w ,+1</>]+)\))?"
                               r"</p>"
                               r"\n\n"
                               r"<p><strong>Hit Points</strong> "
                               r"(?P<hp_avg>\d+) "
                               r"\((?P<hp_expr>[d\d +-]+)\)"
                               r"</p>"
                               r"\n\n"
                               r"<p><strong>Speed</strong> (?P<speed>.*)</p>"  # Need further matching
                               r"\n\n"
                               r"<hr>"
                               r"\n\n"
                               r"<ul class=\"monster-stats\">\n"
                               r"<li><strong>STR</strong> (?P<str>\d+) \((?P<str_mod>[+-]\d+)\)</li>\n"
                               r"<li><strong>DEX</strong> (?P<dex>\d+) \((?P<dex_mod>[+-]\d+)\)</li>\n"
                               r"<li><strong>CON</strong> (?P<con>\d+) \((?P<con_mod>[+-]\d+)\)</li>\n"
                               r"<li><strong>INT</strong> (?P<int>\d+) \((?P<int_mod>[+-]\d+)\)</li>\n"
                               r"<li><strong>WIS</strong> (?P<wis>\d+) \((?P<wis_mod>[+-]\d+)\)</li>\n"
                               r"<li><strong>CHA</strong> (?P<cha>\d+) \((?P<cha_mod>[+-]\d+)\)</li>\n"
                               r"</ul>"
                               r"\n\n"
                               r"<hr>"
                               r"(?:\n\n"
                               r"<p><strong>Saving Throws</strong> (?P<throws>.*)</p>)?"  # Need further matching
                               r"(?:\n\n"
                               r"<p><strong>Skills</strong> (?P<skills>.*)</p>)?"  # Need further matching
                               r"(?:\n\n"
                               r"<p><strong>Damage Vulnerabilities</strong> (?P<dmg_vul>.*)</p>)?"  # Need further matching
                               r"(?:\n\n"
                               r"<p><strong>Damage Resistances</strong> (?P<dmg_res>.*)</p>)?"  # Need further matching
                               r"(?:\n\n"
                               r"<p><strong>Damage Immunities</strong> (?P<dmg_imm>.*)</p>)?"  # Need further matching
                               r"(?:\n\n"
                               r"<p><strong>Condition Immunities</strong> (?P<cond_imm>.*)</p>)?"  # Need further matching
                               r"\n\n"
                               r"<p><strong>Senses</strong> "
                               r"(?:blindsight (?P<blindsight>\d+) ft\.(?: \(blind beyond this radius\))?, )?"
                               r"(?:darkvision (?P<darkvision>\d+) ft\., )?"
                               r"(?:truesight (?P<truesight>\d+) ft\., )?"
                               r"(?:tremorsense (?P<tremorsense>\d+) ft\., )?"
                               r"passive Perception (?P<passive_perception>\d+)"
                               r"</p>"
                               r"\n\n"
                               r"<p><strong>Languages</strong> (?P<languages>.*)</p>"  # Need further matching
                               r"\n\n"
                               r"<p><strong>Challenge</strong> "
                               r"(?P<cr>[\d/]+) "
                               r"\((?P<xp>[\d,]+) XP\)"
                               r"(?:.*)"  # Weird additions for only a few sheets
                               r"</p>"
                               r"\n\n"
                               r"<hr>"
                               r"\n\n"
                               r"")

        # Skills
        self.skill = re.compile(r"(\w+) "  # Name
                                r"([+-]\d+)")  # Modifier

        # Throws
        self.throw = re.compile(r"(\w\w\w) "  # Ability score
                                r"([+-]\d+)")  # Modifier

        # Languages
        self.language = re.compile(r"[\w '\.-]+")  # TODO get more structure from it
        
        #self.resistance = re.compile(r"(?:(?:slashing|piercing|bludgeoning|poison|acid|fire|cold|radiant|necrotic|lightning|thunder|force|psychic),? ?)*"
        #                             r"(?:;? ?bludgeoning, piercing, and slashing (?:damage )?"
        #                             r"from nonmagical attacks(?: that aren&#8217;t (?:silvered|adamantine))?)?"
        #                             r"(.*)")

    def parse(self, fname):
        #################################
        # Open and precut the html file #
        #################################
        with open(f"html/{fname}.html") as f:
            html = f.read()

        start = html.find(">", html.find("<section")) + 1
        end = html.find("</section>", start)

        html = html[start:end]

        ###############
        # Match regex #
        ###############
        sheet = self.main.search(html).groupdict()
        # print(sheet)
        # return

        if sheet["throws"] is not None:
            sheet["throws"] = dict(self.throw.findall(sheet["throws"]))

        if sheet["skills"] is not None:
            sheet["skills"] = dict(self.skill.findall(sheet["skills"]))

        sheet["languages"] = self.language.findall(sheet["languages"].replace("&#8217;", "'"))

        ##########################
        # Save the sheet as json #
        ##########################
        with open(f"sheets/{fname.replace('-', '_')}.json", "w") as f:
            json.dump(sheet, f, indent=4)


if __name__ == "__main__":
    if not os.path.isdir("sheets"):
        os.mkdir("sheets")

    if len(argv) > 1:
        files = argv[1:]
    else:
        with open("list") as f:
            files = f.read().splitlines()

    parser = Parser()

    for name in files:
        parser.parse(name)
