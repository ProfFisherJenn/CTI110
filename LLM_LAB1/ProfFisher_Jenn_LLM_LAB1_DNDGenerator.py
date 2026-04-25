# LLM_LAB1
# Jennifer Fisher
# April, 25, 2026
# Application to assit user with selecting DND character attributes and determining character stats to produce a character sheet

import math

# ─────────────────────────────────────────────
#  D&D 5e DATA
# ─────────────────────────────────────────────

RACES = {
    "Human":        {"STR":1,"DEX":1,"CON":1,"INT":1,"WIS":1,"CHA":1, "traits":["Extra Language","Bonus Feat"]},
    "Elf":          {"DEX":2,"INT":1,                                   "traits":["Darkvision","Fey Ancestry","Trance"]},
    "High Elf":     {"DEX":2,"INT":1,                                   "traits":["Darkvision","Fey Ancestry","Cantrip","Extra Language"]},
    "Wood Elf":     {"DEX":2,"WIS":1,                                   "traits":["Darkvision","Fey Ancestry","Fleet of Foot","Mask of the Wild"]},
    "Dark Elf":     {"DEX":2,"CHA":1,                                   "traits":["Superior Darkvision","Fey Ancestry","Sunlight Sensitivity","Drow Magic"]},
    "Dwarf":        {"CON":2,                                           "traits":["Darkvision","Dwarven Resilience","Stonecunning"]},
    "Hill Dwarf":   {"CON":2,"WIS":1,                                   "traits":["Darkvision","Dwarven Resilience","Dwarven Toughness","Stonecunning"]},
    "Mountain Dwarf":{"STR":2,"CON":2,                                  "traits":["Darkvision","Dwarven Resilience","Dwarven Armor Training","Stonecunning"]},
    "Halfling":     {"DEX":2,                                           "traits":["Lucky","Brave","Halfling Nimbleness"]},
    "Lightfoot Halfling":{"DEX":2,"CHA":1,                              "traits":["Lucky","Brave","Halfling Nimbleness","Naturally Stealthy"]},
    "Stout Halfling":{"DEX":2,"CON":1,                                  "traits":["Lucky","Brave","Halfling Nimbleness","Stout Resilience"]},
    "Gnome":        {"INT":2,                                           "traits":["Darkvision","Gnome Cunning"]},
    "Forest Gnome": {"INT":2,"DEX":1,                                   "traits":["Darkvision","Gnome Cunning","Natural Illusionist","Speak with Small Beasts"]},
    "Rock Gnome":   {"INT":2,"CON":1,                                   "traits":["Darkvision","Gnome Cunning","Artificer's Lore","Tinker"]},
    "Half-Elf":     {"CHA":2,                                           "traits":["Darkvision","Fey Ancestry","Skill Versatility","Two free +1s (auto STR/CON)"], "extra":{"STR":1,"CON":1}},
    "Half-Orc":     {"STR":2,"CON":1,                                   "traits":["Darkvision","Menacing","Relentless Endurance","Savage Attacks"]},
    "Tiefling":     {"INT":1,"CHA":2,                                   "traits":["Darkvision","Hellish Resistance","Infernal Legacy"]},
    "Dragonborn":   {"STR":2,"CHA":1,                                   "traits":["Draconic Ancestry","Breath Weapon","Damage Resistance"]},
}

# Classes: valid races (None = any), hit die, primary ability, saves, skill count, skill pool
CLASSES = {
    "Barbarian": {
        "races": None,
        "hit_die": 12,
        "primary": ["STR"],
        "saves": ["STR","CON"],
        "skill_count": 2,
        "skills": ["Animal Handling","Athletics","Intimidation","Nature","Perception","Survival"],
    },
    "Bard": {
        "races": None,
        "hit_die": 8,
        "primary": ["CHA"],
        "saves": ["DEX","CHA"],
        "skill_count": 3,
        "skills": ["Any"],  # Bards get any 3
    },
    "Cleric": {
        "races": None,
        "hit_die": 8,
        "primary": ["WIS"],
        "saves": ["WIS","CHA"],
        "skill_count": 2,
        "skills": ["History","Insight","Medicine","Persuasion","Religion"],
    },
    "Druid": {
        "races": None,
        "hit_die": 8,
        "primary": ["WIS"],
        "saves": ["INT","WIS"],
        "skill_count": 2,
        "skills": ["Arcana","Animal Handling","Insight","Medicine","Nature","Perception","Religion","Survival"],
    },
    "Fighter": {
        "races": None,
        "hit_die": 10,
        "primary": ["STR","DEX"],
        "saves": ["STR","CON"],
        "skill_count": 2,
        "skills": ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"],
    },
    "Monk": {
        "races": None,
        "hit_die": 8,
        "primary": ["DEX","WIS"],
        "saves": ["STR","DEX"],
        "skill_count": 2,
        "skills": ["Acrobatics","Athletics","History","Insight","Religion","Stealth"],
    },
    "Paladin": {
        "races": None,
        "hit_die": 10,
        "primary": ["STR","CHA"],
        "saves": ["WIS","CHA"],
        "skill_count": 2,
        "skills": ["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"],
    },
    "Ranger": {
        "races": None,
        "hit_die": 10,
        "primary": ["DEX","WIS"],
        "saves": ["STR","DEX"],
        "skill_count": 3,
        "skills": ["Animal Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"],
    },
    "Rogue": {
        "races": None,
        "hit_die": 8,
        "primary": ["DEX"],
        "saves": ["DEX","INT"],
        "skill_count": 4,
        "skills": ["Acrobatics","Athletics","Deception","Insight","Intimidation","Investigation","Perception","Performance","Persuasion","Sleight of Hand","Stealth"],
    },
    "Sorcerer": {
        "races": ["Tiefling","Dragonborn","Half-Elf","Human","Dark Elf"],
        "hit_die": 6,
        "primary": ["CHA"],
        "saves": ["CON","CHA"],
        "skill_count": 2,
        "skills": ["Arcana","Deception","Insight","Intimidation","Persuasion","Religion"],
    },
    "Warlock": {
        "races": ["Tiefling","Half-Elf","Human","Dark Elf","Gnome","Forest Gnome"],
        "hit_die": 8,
        "primary": ["CHA"],
        "saves": ["WIS","CHA"],
        "skill_count": 2,
        "skills": ["Arcana","Deception","History","Intimidation","Investigation","Nature","Religion"],
    },
    "Wizard": {
        "races": None,
        "hit_die": 6,
        "primary": ["INT"],
        "saves": ["INT","WIS"],
        "skill_count": 2,
        "skills": ["Arcana","History","Insight","Investigation","Medicine","Religion"],
    },
}

BACKGROUNDS = {
    "Acolyte":       {"skills":["Insight","Religion"],        "trait":"Shelter of the Faithful"},
    "Charlatan":     {"skills":["Deception","Sleight of Hand"],"trait":"False Identity"},
    "Criminal":      {"skills":["Deception","Stealth"],       "trait":"Criminal Contact"},
    "Entertainer":   {"skills":["Acrobatics","Performance"],  "trait":"By Popular Demand"},
    "Folk Hero":     {"skills":["Animal Handling","Survival"],"trait":"Rustic Hospitality"},
    "Guild Artisan": {"skills":["Insight","Persuasion"],      "trait":"Guild Membership"},
    "Hermit":        {"skills":["Medicine","Religion"],       "trait":"Discovery"},
    "Noble":         {"skills":["History","Persuasion"],      "trait":"Position of Privilege"},
    "Outlander":     {"skills":["Athletics","Survival"],      "trait":"Wanderer"},
    "Sage":          {"skills":["Arcana","History"],          "trait":"Researcher"},
    "Sailor":        {"skills":["Athletics","Perception"],    "trait":"Ship's Passage"},
    "Soldier":       {"skills":["Athletics","Intimidation"],  "trait":"Military Rank"},
    "Urchin":        {"skills":["Sleight of Hand","Stealth"], "trait":"City Secrets"},
}

ALIGNMENTS = [
    "Lawful Good","Neutral Good","Chaotic Good",
    "Lawful Neutral","True Neutral","Chaotic Neutral",
    "Lawful Evil","Neutral Evil","Chaotic Evil",
]

STATS = ["STR","DEX","CON","INT","WIS","CHA"]
STAT_NAMES = {"STR":"Strength","DEX":"Dexterity","CON":"Constitution",
              "INT":"Intelligence","WIS":"Wisdom","CHA":"Charisma"}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def modifier(score):
    return math.floor((score - 10) / 2)

def mod_str(score):
    m = modifier(score)
    return f"+{m}" if m >= 0 else str(m)

def proficiency_bonus(level):
    return math.ceil(level / 4) + 1

def divider(char="═", width=55):
    print(char * width)

def section(title):
    divider()
    print(f"  {title}")
    divider()

def pick_from_list(items, prompt, label="Option"):
    print()
    for i, item in enumerate(items, 1):
        print(f"  [{i:>2}] {item}")
    print()
    while True:
        raw = input(f"  {prompt}: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return items[int(raw)-1]
        print(f"  ✖  Enter a number between 1 and {len(items)}.")

def pick_multiple(items, count, prompt):
    chosen = []
    available = list(items)
    print(f"\n  Choose {count} skill(s):")
    for pick_n in range(1, count+1):
        for i, s in enumerate(available, 1):
            print(f"  [{i:>2}] {s}")
        while True:
            raw = input(f"  Choice {pick_n}/{count}: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(available):
                chosen.append(available.pop(int(raw)-1))
                break
            print(f"  ✖  Enter a number between 1 and {len(available)}.")
    return chosen

def get_int(prompt, lo=None, hi=None):
    while True:
        raw = input(f"  {prompt}: ").strip()
        if raw.isdigit():
            val = int(raw)
            if (lo is None or val >= lo) and (hi is None or val <= hi):
                return val
        bounds = ""
        if lo is not None and hi is not None:
            bounds = f" ({lo}–{hi})"
        print(f"  ✖  Enter a valid integer{bounds}.")

# ─────────────────────────────────────────────
#  MAIN FLOW
# ─────────────────────────────────────────────

def main():
    print()
    divider("▓")
    print("  ⚔   D&D 5e CHARACTER CREATOR   ⚔")
    divider("▓")

    # ── RACE ──────────────────────────────────
    section("STEP 1 · SELECT YOUR RACE")
    race_list = sorted(RACES.keys())
    race = pick_from_list(race_list, "Enter race number")
    race_data = RACES[race]
    bonuses = {k:v for k,v in race_data.items() if k in STATS}
    if "extra" in race_data:
        for k,v in race_data["extra"].items():
            bonuses[k] = bonuses.get(k,0) + v

    print(f"\n  ✔  Race selected: {race}")
    if bonuses:
        bonus_str = ", ".join(f"{k} +{v}" for k,v in bonuses.items())
        print(f"     Racial bonuses: {bonus_str}")

    # ── CLASS ──────────────────────────────────
    section("STEP 2 · SELECT YOUR CLASS")
    valid_classes = [c for c,d in CLASSES.items()
                     if d["races"] is None or race in d["races"]]
    cls = pick_from_list(sorted(valid_classes), "Enter class number")
    cls_data = CLASSES[cls]
    print(f"\n  ✔  Class selected: {cls}")

    # ── LEVEL ──────────────────────────────────
    section("STEP 3 · CHARACTER LEVEL")
    level = get_int("Enter character level", 1, 20)
    prof_bonus = proficiency_bonus(level)
    print(f"\n  ✔  Level {level}  |  Proficiency Bonus: +{prof_bonus}")

    # ── NAME ───────────────────────────────────
    section("STEP 4 · CHARACTER NAME")
    while True:
        name = input("  Enter character name: ").strip()
        if name:
            break
        print("  ✖  Name cannot be blank.")
    print(f"\n  ✔  Name: {name}")

    # ── ALIGNMENT ──────────────────────────────
    section("STEP 5 · ALIGNMENT")
    alignment = pick_from_list(ALIGNMENTS, "Enter alignment number")
    print(f"\n  ✔  Alignment: {alignment}")

    # ── BACKGROUND ─────────────────────────────
    section("STEP 6 · BACKGROUND")
    bg_list = sorted(BACKGROUNDS.keys())
    background = pick_from_list(bg_list, "Enter background number")
    bg_data = BACKGROUNDS[background]
    print(f"\n  ✔  Background: {background}")
    print(f"     Skills granted: {', '.join(bg_data['skills'])}")
    print(f"     Feature: {bg_data['trait']}")

    # ── ABILITY SCORE ROLLS ────────────────────
    section("STEP 7 · ABILITY SCORE ROLLS")
    print("  Roll 4d6, drop lowest — enter your six scores.")
    print("  They will be assigned to stats in order:")
    print("  Strength · Dexterity · Constitution · Intelligence · Wisdom · Charisma\n")

    base_scores = {}
    rolled_scores = []
    for i, stat in enumerate(STATS, 1):
        full_name = STAT_NAMES[stat]
        score = get_int(f"Roll {i}/6 — {full_name} (score 3–18)", 3, 18)
        rolled_scores.append(score)

    print(f"\n  Rolls entered: {rolled_scores}")
    print("  Assigning to stats in order…")

    for stat, score in zip(STATS, rolled_scores):
        base_scores[stat] = score

    # Apply racial bonuses
    final_scores = {}
    for stat in STATS:
        final_scores[stat] = base_scores[stat] + bonuses.get(stat, 0)

    # ── SKILL PROFICIENCIES ────────────────────
    section("STEP 8 · SKILL PROFICIENCIES")
    skill_pool = cls_data["skills"]
    skill_count = cls_data["skill_count"]

    if "Any" in skill_pool:
        all_skills = sorted(set([s for bg in BACKGROUNDS.values() for s in bg["skills"]] +
            ["Acrobatics","Animal Handling","Arcana","Athletics","Deception","History",
             "Insight","Intimidation","Investigation","Medicine","Nature","Perception",
             "Performance","Persuasion","Religion","Sleight of Hand","Stealth","Survival"]))
        skill_pool = all_skills

    chosen_skills = pick_multiple(skill_pool, skill_count, "Choose class skill")

    # Add background skills (no duplication)
    all_proficiencies = list(dict.fromkeys(bg_data["skills"] + chosen_skills))
    print(f"\n  ✔  All skill proficiencies: {', '.join(all_proficiencies)}")

    # ── HP CALCULATION ─────────────────────────
    hit_die = cls_data["hit_die"]
    con_mod = modifier(final_scores["CON"])
    # Level 1: max hit die + CON mod. Additional levels: avg (rounded up) + CON mod each
    if level == 1:
        hp = hit_die + con_mod
    else:
        avg_per_level = math.ceil(hit_die / 2) + 1
        hp = hit_die + con_mod + (avg_per_level + con_mod) * (level - 1)
    hp = max(hp, 1)

    # ─────────────────────────────────────────
    #  SUMMARY REPORT
    # ─────────────────────────────────────────
    print()
    divider("▓")
    print("  ⚔   CHARACTER SHEET   ⚔")
    divider("▓")
    print(f"  Name:        {name}")
    print(f"  Race:        {race}")
    print(f"  Class:       {cls}  (Level {level})")
    print(f"  Alignment:   {alignment}")
    print(f"  Background:  {background}")
    print(f"  Feature:     {bg_data['trait']}")
    divider("─")
    print(f"  Hit Points:       {hp}  (d{hit_die} hit die)")
    print(f"  Proficiency Bonus: +{prof_bonus}")
    divider("─")
    print(f"  {'ABILITY':<14}  {'BASE':>4}  {'RACIAL':>6}  {'FINAL':>5}  {'MOD':>4}")
    print(f"  {'──────────────':<14}  {'────':>4}  {'──────':>6}  {'─────':>5}  {'───':>4}")
    for stat in STATS:
        base  = base_scores[stat]
        bonus = bonuses.get(stat, 0)
        final = final_scores[stat]
        mod   = mod_str(final)
        bonus_disp = f"+{bonus}" if bonus > 0 else ("—" if bonus == 0 else str(bonus))
        full_name = STAT_NAMES[stat]
        print(f"  {full_name:<14}  {base:>4}  {bonus_disp:>6}  {final:>5}  {mod:>4}")
    divider("─")
    print(f"  Racial Traits:")
    for trait in race_data.get("traits", []):
        print(f"    • {trait}")
    divider("─")
    print(f"  Class Saves:       {', '.join(STAT_NAMES[s] for s in cls_data['saves'])}")
    print(f"  Skill Proficiencies:")
    for sk in all_proficiencies:
        print(f"    • {sk}")
    divider("▓")
    print()

if __name__ == "__main__":
    main()
