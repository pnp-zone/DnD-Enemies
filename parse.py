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
        # Name
        self.name = re.compile(r"<h1>(.+)</h1>")

        # Description
        self.desc = re.compile(r"<p><em>"
                               r"(Medium|Large|Small|Huge|Tiny|Gargantuan|Diminutive|Colossal|Fine)"  # Size
                               r" ([\w ]+)"  # Race
                               r" ?(\(.*\))?"  # Subrace (optional)
                               r"(, [\w \-\(\)\%]+)"  # Alignment
                               r"</em></p>")

        # Hit Points
        self.hp = re.compile(r"<p><strong>Hit Points</strong> "
                             r"(\d+) "  # Average
                             r"\(([d\d +-]+)\)"  # Dice Expr
                             r"</p>")

        # Armor Class
        self.ac = re.compile(r"<p><strong>Armor Class</strong> "
                             r"(\d+)"  # Numeric value
                             r"(?: \((\d+ (?:with|while|in) [\w </>]+)\))?"  # Alternatives
                             r"(?: \(([\w ,+1</>]+)\))?"  # Types
                             r"</p>")

        # Ability Scores
        self.attr = re.compile(r"<li><strong>"
                               r"(\w\w\w)"  # Score name
                               r"</strong> "
                               r"(\d+)"  # Absolte value
                               r"\(([+-]\d+)\)"  # Modifier
                               r"</li>")

        # Skills
        self.skills = re.compile(r"<p><strong>Skills</strong>(.*)</p>")  # Outer container
        self.skill = re.compile(r"(\w+) "  # Name
                                r"([+-]\d+)")  # Modifier

        # Throws
        self.throws = re.compile(r"<p><strong>Saving Throws</strong>(.*)</p>")  # Outer container
        self.throw = re.compile(r"(\w\w\w) "  # Ability score
                                r"([+-]\d+)")  # Modifier

        # Senses
        self.senses = re.compile(r"<p><strong>Senses</strong> "
                                 r"(?:blindsight (\d+) ft\.(?: \(blind beyond this radius\))?, )?"
                                 r"(?:darkvision (\d+) ft\., )?"
                                 r"(?:truesight (\d+) ft\., )?"
                                 r"(?:tremorsense (\d+) ft\., )?"
                                 r"passive Perception (\d+)"
                                 r"</p>")

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
        name, = self.name.search(html).groups()
        size, race, subrace, alignment = self.desc.search(html).groups()
        hp_avg, hp_expr = self.hp.search(html).groups()
        ac, ac_alt, ac_types = self.ac.search(html).groups()
        attrs = self.attr.findall(html)

        skills = self.skills.search(html)
        if skills is not None:
            skills = self.skill.findall(skills.group(1))

        throws = self.throws.search(html)
        if throws is not None:
            throws = self.throw.findall(throws.group(1))

        blind, dark, true, tremor, passive = self.senses.search(html).groups()

        ####################
        # Create the sheet #
        ####################
        sheet = {
                    "name": name,
                    "size": size,
                    "race": race,
                    "subrace": subrace,
                    "alignment": alignment,
                    "hp": hp_expr,
                    "ac": int(ac),
                }
        for attr, val, mod in attrs:
            sheet[attr.lower()] = int(mod)

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

        senses_dict = {
                    "passive": passive,
                  }
        if dark:
            senses_dict["dakrvision"] = int(dark)
        if blind:
            senses_dict["blindsight"] = int(blind)
        if true:
            senses_dict["truesight"] = int(true)
        if tremor:
            senses_dict["tremorsense"] = int(tremor)
        sheet["senses"] = senses_dict

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
