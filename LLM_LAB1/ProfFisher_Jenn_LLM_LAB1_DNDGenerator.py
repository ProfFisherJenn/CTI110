# LLM_LAB1
# Jennifer Fisher
# April, 25, 2026
# Application to assit user with selecting DND character attributes and determining character stats to produce a character sheet

import math
import random

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

CLASSES = {
    "Barbarian": {
        "races": None, "hit_die": 12, "primary": ["STR"],
        "saves": ["STR","CON"], "skill_count": 2,
        "skills": ["Animal Handling","Athletics","Intimidation","Nature","Perception","Survival"],
        "spellcasting": None,
        "equipment": [
            "Greataxe",
            "Two handaxes",
            "Explorer's pack",
            "Four javelins",
        ],
    },
    "Bard": {
        "races": None, "hit_die": 8, "primary": ["CHA"],
        "saves": ["DEX","CHA"], "skill_count": 3,
        "skills": ["Any"],
        "spellcasting": {
            "type": "full", "ability": "CHA",
            "cantrips_known": [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4],
            "spells_known":   [4,5,6,7,8,9,10,11,12,14,15,15,16,18,19,19,20,22,22,22],
            "auto_cantrips": [],
            "choose_cantrips": 2,
            "auto_spells": [],
            "choose_spells": 4,
            "cantrip_pool": [
                ("Dancing Lights",  "Evocation",    "Create up to 4 torch-sized lights that float within 20 ft"),
                ("Light",           "Evocation",    "Touch one object; it sheds bright light in a 20-ft radius"),
                ("Mage Hand",       "Conjuration",  "Spectral hand appears; manipulates objects up to 10 lb"),
                ("Mending",         "Transmutation","Repair a single break or tear in an object"),
                ("Message",         "Transmutation","Whisper a message to a creature; it can reply secretly"),
                ("Minor Illusion",  "Illusion",     "Create a sound or image of an object for 1 minute"),
                ("Prestidigitation","Transmutation","Minor magical trick: clean, soil, light, chill, flavor, etc."),
                ("True Strike",     "Divination",   "Gain advantage on next attack roll against one creature"),
                ("Vicious Mockery", "Enchantment",  "Hurl insults; target takes 1d4 psychic damage and has disadvantage on its next attack"),
            ],
            "spell_pool_l1": [
                ("Charm Person",    "Enchantment",  "Charm a humanoid for 1 hour; it regards you as friendly"),
                ("Cure Wounds",     "Evocation",    "Touch a creature; it regains 1d8 + spellcasting modifier HP"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Disguise Self",   "Illusion",     "Change your appearance (clothes, features, height) for 1 hour"),
                ("Faerie Fire",     "Evocation",    "Objects and creatures in a 20-ft cube glow; attacks against them have advantage"),
                ("Healing Word",    "Evocation",    "Bonus action; a creature you can see regains 1d4 + modifier HP"),
                ("Heroism",         "Enchantment",  "Creature is immune to frightened and gains temp HP each turn"),
                ("Sleep",           "Enchantment",  "Send creatures totaling 5d8 HP to sleep (lowest HP first)"),
                ("Thunderwave",     "Evocation",    "15-ft cube; 2d8 thunder damage and pushed 10 ft on failed CON save"),
            ],
        },
        "equipment": [
            "Rapier",
            "Diplomat's pack",
            "Lute (or other musical instrument)",
            "Leather armor",
            "Dagger",
        ],
    },
    "Cleric": {
        "races": None, "hit_die": 8, "primary": ["WIS"],
        "saves": ["WIS","CHA"], "skill_count": 2,
        "skills": ["History","Insight","Medicine","Persuasion","Religion"],
        "spellcasting": {
            "type": "full", "ability": "WIS",
            "cantrips_known": [3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5],
            "spells_known": None,  # Clerics prepare spells daily
            "auto_cantrips": [],
            "choose_cantrips": 3,
            "auto_spells": [],
            "choose_spells": 3,
            "cantrip_pool": [
                ("Guidance",        "Divination",   "Touch; target adds 1d4 to one ability check of its choice"),
                ("Light",           "Evocation",    "Touch one object; it sheds bright light in a 20-ft radius"),
                ("Mending",         "Transmutation","Repair a single break or tear in an object"),
                ("Resistance",      "Abjuration",   "Touch; target adds 1d4 to one saving throw of its choice"),
                ("Sacred Flame",    "Evocation",    "Flame strikes a creature you see; 1d8 radiant damage on failed DEX save"),
                ("Spare the Dying", "Necromancy",   "Touch a dying creature to stabilize it at 0 HP"),
                ("Thaumaturgy",     "Transmutation","Minor miracle: amplify voice, make flames flicker, tremors, etc."),
            ],
            "spell_pool_l1": [
                ("Bless",           "Enchantment",  "Up to 3 creatures add 1d4 to attack rolls and saving throws"),
                ("Command",         "Enchantment",  "One-word command; creature obeys on failed WIS save"),
                ("Create or Destroy Water","Transmutation","Create or destroy up to 10 gallons of water"),
                ("Cure Wounds",     "Evocation",    "Touch; creature regains 1d8 + spellcasting modifier HP"),
                ("Detect Evil and Good","Divination","Know if aberrations, fiends, undead, etc. are within 30 ft"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Guiding Bolt",    "Evocation",    "4d6 radiant damage; next attack roll against target has advantage"),
                ("Healing Word",    "Evocation",    "Bonus action; a creature you can see regains 1d4 + modifier HP"),
                ("Inflict Wounds",  "Necromancy",   "Melee spell attack; 3d10 necrotic damage"),
                ("Protection from Evil and Good","Abjuration","Protection against certain creature types for 10 minutes"),
                ("Sanctuary",       "Abjuration",   "Protect a creature; attackers must make WIS save or choose new target"),
                ("Shield of Faith", "Abjuration",   "Bonus action; target gains +2 AC for up to 10 minutes"),
            ],
        },
        "equipment": [
            "Mace",
            "Scale mail",
            "Light crossbow and 20 bolts",
            "Priest's pack",
            "Shield",
            "Holy symbol",
        ],
    },
    "Druid": {
        "races": None, "hit_die": 8, "primary": ["WIS"],
        "saves": ["INT","WIS"], "skill_count": 2,
        "skills": ["Arcana","Animal Handling","Insight","Medicine","Nature","Perception","Religion","Survival"],
        "spellcasting": {
            "type": "full", "ability": "WIS",
            "cantrips_known": [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4],
            "spells_known": None,  # Druids prepare spells daily
            "auto_cantrips": [],
            "choose_cantrips": 2,
            "auto_spells": [],
            "choose_spells": 3,
            "cantrip_pool": [
                ("Druidcraft",      "Transmutation","Minor nature effects: predict weather, make flowers bloom, light/snuff flames"),
                ("Guidance",        "Divination",   "Touch; target adds 1d4 to one ability check of its choice"),
                ("Mending",         "Transmutation","Repair a single break or tear in an object"),
                ("Poison Spray",    "Conjuration",  "Project poison; 1d12 poison damage on failed CON save"),
                ("Produce Flame",   "Conjuration",  "Flame in hand sheds light; hurl it as attack for 1d8 fire damage"),
                ("Resistance",      "Abjuration",   "Touch; target adds 1d4 to one saving throw of its choice"),
                ("Shillelagh",      "Transmutation","Your club or staff uses WIS for attacks and deals 1d8 damage"),
                ("Thorn Whip",      "Transmutation","Whip of thorns; 1d6 piercing damage and pull target 10 ft closer"),
            ],
            "spell_pool_l1": [
                ("Animal Friendship","Enchantment", "Convince a beast you mean no harm; it won't attack for 24 hours"),
                ("Charm Person",    "Enchantment",  "Charm a humanoid for 1 hour; it regards you as friendly"),
                ("Create or Destroy Water","Transmutation","Create or destroy up to 10 gallons of water"),
                ("Cure Wounds",     "Evocation",    "Touch; creature regains 1d8 + spellcasting modifier HP"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Detect Poison and Disease","Divination","Sense poisons, poisonous creatures, and disease within 30 ft"),
                ("Entangle",        "Conjuration",  "Grasping weeds restrain creatures in a 20-ft square on failed STR save"),
                ("Faerie Fire",     "Evocation",    "Objects and creatures in a 20-ft cube glow; attacks against them have advantage"),
                ("Healing Word",    "Evocation",    "Bonus action; a creature you can see regains 1d4 + modifier HP"),
                ("Speak with Animals","Divination", "Communicate verbally with beasts for 10 minutes"),
                ("Thunderwave",     "Evocation",    "15-ft cube; 2d8 thunder damage and pushed 10 ft on failed CON save"),
            ],
        },
        "equipment": [
            "Wooden shield",
            "Scimitar",
            "Leather armor",
            "Explorer's pack",
            "Druidic focus",
        ],
    },
    "Fighter": {
        "races": None, "hit_die": 10, "primary": ["STR","DEX"],
        "saves": ["STR","CON"], "skill_count": 2,
        "skills": ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"],
        "spellcasting": None,
        "equipment": [
            "Chain mail",
            "Longsword",
            "Shield",
            "Light crossbow and 20 bolts",
            "Dungeoneer's pack",
        ],
    },
    "Monk": {
        "races": None, "hit_die": 8, "primary": ["DEX","WIS"],
        "saves": ["STR","DEX"], "skill_count": 2,
        "skills": ["Acrobatics","Athletics","History","Insight","Religion","Stealth"],
        "spellcasting": None,
        "equipment": [
            "Shortsword",
            "Dungeoneer's pack",
            "10 darts",
        ],
    },
    "Paladin": {
        "races": None, "hit_die": 10, "primary": ["STR","CHA"],
        "saves": ["WIS","CHA"], "skill_count": 2,
        "skills": ["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"],
        "spellcasting": {
            "type": "half", "ability": "CHA",
            "cantrips_known": None,
            "spells_known": None,  # Paladins prepare spells
            "auto_cantrips": [],
            "choose_cantrips": 0,
            "auto_spells": [],
            "choose_spells": 2,
            "cantrip_pool": [],
            "spell_pool_l1": [
                ("Bless",           "Enchantment",  "Up to 3 creatures add 1d4 to attack rolls and saving throws"),
                ("Command",         "Enchantment",  "One-word command; creature obeys on failed WIS save"),
                ("Compelled Duel",  "Enchantment",  "Force a creature into single combat; it has disadvantage attacking others"),
                ("Cure Wounds",     "Evocation",    "Touch; creature regains 1d8 + spellcasting modifier HP"),
                ("Detect Evil and Good","Divination","Know if aberrations, fiends, undead, etc. are within 30 ft"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Divine Favor",    "Evocation",    "Bonus action; weapon attacks deal extra 1d4 radiant damage"),
                ("Heroism",         "Enchantment",  "Creature is immune to frightened and gains temp HP each turn"),
                ("Protection from Evil and Good","Abjuration","Protection against certain creature types for 10 minutes"),
                ("Shield of Faith", "Abjuration",   "Bonus action; target gains +2 AC for up to 10 minutes"),
                ("Wrathful Smite",  "Evocation",    "Next hit deals extra 1d6 psychic damage and may frighten the target"),
            ],
        },
        "equipment": [
            "Chain mail",
            "Longsword and shield",
            "Five javelins",
            "Priest's pack",
            "Holy symbol",
        ],
    },
    "Ranger": {
        "races": None, "hit_die": 10, "primary": ["DEX","WIS"],
        "saves": ["STR","DEX"], "skill_count": 3,
        "skills": ["Animal Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"],
        "spellcasting": {
            "type": "half", "ability": "WIS",
            "cantrips_known": None,
            "spells_known": None,
            "auto_cantrips": [],
            "choose_cantrips": 0,
            "auto_spells": [],
            "choose_spells": 2,
            "cantrip_pool": [],
            "spell_pool_l1": [
                ("Animal Friendship","Enchantment", "Convince a beast you mean no harm; it won't attack for 24 hours"),
                ("Cure Wounds",     "Evocation",    "Touch; creature regains 1d8 + spellcasting modifier HP"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Detect Poison and Disease","Divination","Sense poisons, poisonous creatures, and disease within 30 ft"),
                ("Ensnaring Strike","Conjuration",  "Next hit restrains the target; it takes 1d6 piercing damage per turn"),
                ("Fog Cloud",       "Conjuration",  "Create a 20-ft radius sphere of fog; heavily obscured"),
                ("Goodberry",       "Transmutation","Create up to 10 berries; each restores 1 HP and provides nourishment"),
                ("Hail of Thorns",  "Conjuration",  "Next ranged hit also strikes nearby creatures for 1d10 piercing"),
                ("Hunter's Mark",   "Divination",   "Mark a creature; deal extra 1d6 damage and track it easily"),
                ("Jump",            "Transmutation","Triple a creature's jump distance for 1 minute"),
                ("Longstrider",     "Transmutation","Increase a creature's speed by 10 ft for 1 hour"),
                ("Speak with Animals","Divination", "Communicate verbally with beasts for 10 minutes"),
            ],
        },
        "equipment": [
            "Scale mail",
            "Two shortswords",
            "Dungeoneer's pack",
            "Longbow and quiver of 20 arrows",
        ],
    },
    "Rogue": {
        "races": None, "hit_die": 8, "primary": ["DEX"],
        "saves": ["DEX","INT"], "skill_count": 4,
        "skills": ["Acrobatics","Athletics","Deception","Insight","Intimidation","Investigation","Perception","Performance","Persuasion","Sleight of Hand","Stealth"],
        "spellcasting": None,
        "equipment": [
            "Rapier",
            "Shortbow and quiver of 20 arrows",
            "Burglar's pack",
            "Leather armor",
            "Two daggers",
            "Thieves' tools",
        ],
    },
    "Sorcerer": {
        "races": ["Tiefling","Dragonborn","Half-Elf","Human","Dark Elf"],
        "hit_die": 6, "primary": ["CHA"],
        "saves": ["CON","CHA"], "skill_count": 2,
        "skills": ["Arcana","Deception","Insight","Intimidation","Persuasion","Religion"],
        "spellcasting": {
            "type": "full", "ability": "CHA",
            "cantrips_known": [4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6],
            "spells_known":   [2,3,4,5,6,7,8,9,10,11,12,12,13,13,14,14,15,15,15,15],
            "auto_cantrips": [],
            "choose_cantrips": 4,
            "auto_spells": [],
            "choose_spells": 2,
            "cantrip_pool": [
                ("Acid Splash",     "Conjuration",  "Hurl acid at one or two adjacent creatures; 1d6 acid damage on failed DEX save"),
                ("Chill Touch",     "Necromancy",   "1d8 necrotic damage; target can't regain HP until your next turn"),
                ("Dancing Lights",  "Evocation",    "Create up to 4 torch-sized lights that float within 20 ft"),
                ("Fire Bolt",       "Evocation",    "Ranged spell attack; 1d10 fire damage"),
                ("Light",           "Evocation",    "Touch one object; it sheds bright light in a 20-ft radius"),
                ("Mage Hand",       "Conjuration",  "Spectral hand manipulates objects up to 10 lb within 30 ft"),
                ("Mending",         "Transmutation","Repair a single break or tear in an object"),
                ("Message",         "Transmutation","Whisper a message to a distant creature; it can reply secretly"),
                ("Minor Illusion",  "Illusion",     "Create a sound or image of an object for 1 minute"),
                ("Poison Spray",    "Conjuration",  "Project poison; 1d12 poison damage on failed CON save"),
                ("Prestidigitation","Transmutation","Minor magical trick: clean, soil, light, chill, flavor, etc."),
                ("Ray of Frost",    "Evocation",    "1d8 cold damage; target's speed reduced by 10 ft until your next turn"),
                ("Shocking Grasp",  "Evocation",    "1d8 lightning damage; target can't take reactions until its next turn"),
                ("True Strike",     "Divination",   "Gain advantage on your next attack roll against one creature"),
            ],
            "spell_pool_l1": [
                ("Burning Hands",   "Evocation",    "15-ft cone; 3d6 fire damage on failed DEX save"),
                ("Charm Person",    "Enchantment",  "Charm a humanoid for 1 hour; it regards you as friendly"),
                ("Chromatic Orb",   "Evocation",    "Hurl a 4-inch sphere; 3d8 damage of a chosen energy type"),
                ("Color Spray",     "Illusion",     "Blind creatures totaling 6d10 HP (lowest HP first)"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Disguise Self",   "Illusion",     "Change your appearance for 1 hour"),
                ("Expeditious Retreat","Transmutation","Bonus action Dash each turn for 10 minutes"),
                ("False Life",      "Necromancy",   "Gain 1d4+4 temporary HP for 1 hour"),
                ("Feather Fall",    "Transmutation","Reaction; up to 5 falling creatures descend 60 ft/round safely"),
                ("Fog Cloud",       "Conjuration",  "Create a 20-ft radius sphere of fog; heavily obscured"),
                ("Jump",            "Transmutation","Triple a creature's jump distance for 1 minute"),
                ("Mage Armor",      "Abjuration",   "AC becomes 13 + DEX modifier for 8 hours (no armor)"),
                ("Magic Missile",   "Evocation",    "Three darts each deal 1d4+1 force damage; always hit"),
                ("Shield",          "Abjuration",   "Reaction; +5 AC until start of your next turn, immune to Magic Missile"),
                ("Sleep",           "Enchantment",  "Send creatures totaling 5d8 HP to sleep (lowest HP first)"),
                ("Thunderwave",     "Evocation",    "15-ft cube; 2d8 thunder damage and pushed 10 ft on failed CON save"),
                ("Witch Bolt",      "Evocation",    "1d12 lightning damage; maintain beam each turn as bonus action"),
            ],
        },
        "equipment": [
            "Light crossbow and 20 bolts",
            "Component pouch",
            "Dungeoneer's pack",
            "Two daggers",
        ],
    },
    "Warlock": {
        "races": ["Tiefling","Half-Elf","Human","Dark Elf","Gnome","Forest Gnome"],
        "hit_die": 8, "primary": ["CHA"],
        "saves": ["WIS","CHA"], "skill_count": 2,
        "skills": ["Arcana","Deception","History","Intimidation","Investigation","Nature","Religion"],
        "spellcasting": {
            "type": "pact", "ability": "CHA",
            "cantrips_known": [2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4],
            "spells_known":   [2,3,4,5,6,7,8,9,10,10,11,11,12,12,13,13,14,14,15,15],
            "auto_cantrips": ["Eldritch Blast"],
            "choose_cantrips": 1,
            "auto_spells": [],
            "choose_spells": 2,
            "cantrip_pool": [
                ("Chill Touch",     "Necromancy",   "1d8 necrotic damage; target can't regain HP until your next turn"),
                ("Mage Hand",       "Conjuration",  "Spectral hand manipulates objects up to 10 lb within 30 ft"),
                ("Minor Illusion",  "Illusion",     "Create a sound or image of an object for 1 minute"),
                ("Poison Spray",    "Conjuration",  "Project poison; 1d12 poison damage on failed CON save"),
                ("Prestidigitation","Transmutation","Minor magical trick: clean, soil, light, chill, flavor, etc."),
                ("True Strike",     "Divination",   "Gain advantage on your next attack roll against one creature"),
            ],
            "auto_cantrip_data": {
                "Eldritch Blast": ("Evocation", "Two beams each dealing 1d10 force damage; separate attack rolls"),
            },
            "spell_pool_l1": [
                ("Armor of Agathys","Abjuration",   "Gain 5 temp HP; attackers take 5 cold damage when they hit you"),
                ("Arms of Hadar",   "Conjuration",  "10-ft radius; 2d6 necrotic damage, can't take reactions on failed STR save"),
                ("Charm Person",    "Enchantment",  "Charm a humanoid for 1 hour; it regards you as friendly"),
                ("Comprehend Languages","Divination","Understand any spoken or written language for 1 hour"),
                ("Expeditious Retreat","Transmutation","Bonus action Dash each turn for 10 minutes"),
                ("Hellish Rebuke",  "Evocation",    "Reaction; 2d10 fire damage to attacker on failed DEX save"),
                ("Hex",             "Enchantment",  "Curse a target; deal extra 1d6 necrotic damage and impose disadvantage on chosen ability"),
                ("Illusory Script", "Illusion",     "Write a message only designated creatures can read"),
                ("Protection from Evil and Good","Abjuration","Protection against certain creature types for 10 minutes"),
                ("Unseen Servant",  "Conjuration",  "Conjure an invisible force that performs simple tasks"),
                ("Witch Bolt",      "Evocation",    "1d12 lightning damage; maintain beam each turn as bonus action"),
            ],
        },
        "equipment": [
            "Light crossbow and 20 bolts",
            "Component pouch",
            "Scholar's pack",
            "Leather armor",
            "Two daggers",
            "Any simple weapon",
        ],
    },
    "Wizard": {
        "races": None, "hit_die": 6, "primary": ["INT"],
        "saves": ["INT","WIS"], "skill_count": 2,
        "skills": ["Arcana","History","Insight","Investigation","Medicine","Religion"],
        "spellcasting": {
            "type": "full", "ability": "INT",
            "cantrips_known": [3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5],
            "spells_known": None,  # Wizards copy spells into spellbook
            "auto_cantrips": [],
            "choose_cantrips": 3,
            "auto_spells": [],
            "choose_spells": 6,  # Start with 6 spells in spellbook
            "cantrip_pool": [
                ("Acid Splash",     "Conjuration",  "Hurl acid at one or two adjacent creatures; 1d6 acid damage on failed DEX save"),
                ("Chill Touch",     "Necromancy",   "1d8 necrotic damage; target can't regain HP until your next turn"),
                ("Dancing Lights",  "Evocation",    "Create up to 4 torch-sized lights that float within 20 ft"),
                ("Fire Bolt",       "Evocation",    "Ranged spell attack; 1d10 fire damage"),
                ("Light",           "Evocation",    "Touch one object; it sheds bright light in a 20-ft radius"),
                ("Mage Hand",       "Conjuration",  "Spectral hand manipulates objects up to 10 lb within 30 ft"),
                ("Mending",         "Transmutation","Repair a single break or tear in an object"),
                ("Message",         "Transmutation","Whisper a message to a distant creature; it can reply secretly"),
                ("Minor Illusion",  "Illusion",     "Create a sound or image of an object for 1 minute"),
                ("Prestidigitation","Transmutation","Minor magical trick: clean, soil, light, chill, flavor, etc."),
                ("Ray of Frost",    "Evocation",    "1d8 cold damage; target's speed reduced by 10 ft until your next turn"),
                ("Shocking Grasp",  "Evocation",    "1d8 lightning damage; target can't take reactions until its next turn"),
                ("True Strike",     "Divination",   "Gain advantage on your next attack roll against one creature"),
            ],
            "spell_pool_l1": [
                ("Burning Hands",   "Evocation",    "15-ft cone; 3d6 fire damage on failed DEX save"),
                ("Charm Person",    "Enchantment",  "Charm a humanoid for 1 hour; it regards you as friendly"),
                ("Chromatic Orb",   "Evocation",    "Hurl a 4-inch sphere; 3d8 damage of a chosen energy type"),
                ("Color Spray",     "Illusion",     "Blind creatures totaling 6d10 HP (lowest HP first)"),
                ("Comprehend Languages","Divination","Understand any spoken or written language for 1 hour"),
                ("Detect Magic",    "Divination",   "Sense the presence of magic within 30 ft for 10 minutes"),
                ("Disguise Self",   "Illusion",     "Change your appearance for 1 hour"),
                ("Expeditious Retreat","Transmutation","Bonus action Dash each turn for 10 minutes"),
                ("False Life",      "Necromancy",   "Gain 1d4+4 temporary HP for 1 hour"),
                ("Feather Fall",    "Transmutation","Reaction; up to 5 falling creatures descend 60 ft/round safely"),
                ("Find Familiar",   "Conjuration",  "Summon a spirit as a familiar in animal form to aid you"),
                ("Fog Cloud",       "Conjuration",  "Create a 20-ft radius sphere of fog; heavily obscured"),
                ("Grease",          "Conjuration",  "10-ft square becomes slippery; creatures must pass DEX save or fall prone"),
                ("Identify",        "Divination",   "Learn the properties of a magic item or spell affecting a creature"),
                ("Jump",            "Transmutation","Triple a creature's jump distance for 1 minute"),
                ("Longstrider",     "Transmutation","Increase a creature's speed by 10 ft for 1 hour"),
                ("Mage Armor",      "Abjuration",   "AC becomes 13 + DEX modifier for 8 hours (no armor)"),
                ("Magic Missile",   "Evocation",    "Three darts each deal 1d4+1 force damage; always hit"),
                ("Protection from Evil and Good","Abjuration","Protection against certain creature types for 10 minutes"),
                ("Shield",          "Abjuration",   "Reaction; +5 AC until start of your next turn, immune to Magic Missile"),
                ("Silent Image",    "Illusion",     "Create a visual illusion of any object or creature up to 15-ft cube"),
                ("Sleep",           "Enchantment",  "Send creatures totaling 5d8 HP to sleep (lowest HP first)"),
                ("Thunderwave",     "Evocation",    "15-ft cube; 2d8 thunder damage and pushed 10 ft on failed CON save"),
                ("Witch Bolt",      "Evocation",    "1d12 lightning damage; maintain beam each turn as bonus action"),
            ],
        },
        "equipment": [
            "Quarterstaff",
            "Component pouch",
            "Scholar's pack",
            "Spellbook",
        ],
    },
}

BACKGROUNDS = {
    "Acolyte":       {"skills":["Insight","Religion"],         "trait":"Shelter of the Faithful",
                      "equipment":["Holy symbol","Prayer book","5 sticks of incense","Vestments","Common clothes","Belt pouch with 15 gp"]},
    "Charlatan":     {"skills":["Deception","Sleight of Hand"],"trait":"False Identity",
                      "equipment":["Fine clothes","Disguise kit","Con tools (weighted dice, marked cards)","Belt pouch with 15 gp"]},
    "Criminal":      {"skills":["Deception","Stealth"],        "trait":"Criminal Contact",
                      "equipment":["Crowbar","Dark common clothes with hood","Belt pouch with 15 gp"]},
    "Entertainer":   {"skills":["Acrobatics","Performance"],   "trait":"By Popular Demand",
                      "equipment":["Musical instrument","Favor of an admirer","Costume","Belt pouch with 15 gp"]},
    "Folk Hero":     {"skills":["Animal Handling","Survival"], "trait":"Rustic Hospitality",
                      "equipment":["Artisan's tools","Shovel","Iron pot","Common clothes","Belt pouch with 10 gp"]},
    "Guild Artisan": {"skills":["Insight","Persuasion"],       "trait":"Guild Membership",
                      "equipment":["Artisan's tools","Letter of introduction from guild","Traveler's clothes","Belt pouch with 15 gp"]},
    "Hermit":        {"skills":["Medicine","Religion"],        "trait":"Discovery",
                      "equipment":["Scroll case with notes","Winter blanket","Common clothes","Herbalism kit","5 gp"]},
    "Noble":         {"skills":["History","Persuasion"],       "trait":"Position of Privilege",
                      "equipment":["Fine clothes","Signet ring","Scroll of pedigree","Purse with 25 gp"]},
    "Outlander":     {"skills":["Athletics","Survival"],       "trait":"Wanderer",
                      "equipment":["Staff","Hunting trap","Animal trophy","Traveler's clothes","Belt pouch with 10 gp"]},
    "Sage":          {"skills":["Arcana","History"],           "trait":"Researcher",
                      "equipment":["Bottle of black ink","Quill","Small knife","Letter with unanswered question","Common clothes","Belt pouch with 10 gp"]},
    "Sailor":        {"skills":["Athletics","Perception"],     "trait":"Ship's Passage",
                      "equipment":["Belaying pin (club)","50 ft silk rope","Lucky charm","Common clothes","Belt pouch with 10 gp"]},
    "Soldier":       {"skills":["Athletics","Intimidation"],   "trait":"Military Rank",
                      "equipment":["Rank insignia","Trophy from fallen enemy","Dice set or playing cards","Common clothes","Belt pouch with 10 gp"]},
    "Urchin":        {"skills":["Sleight of Hand","Stealth"],  "trait":"City Secrets",
                      "equipment":["Small knife","Map of home city","Pet mouse","Token from parent","Common clothes","Belt pouch with 10 gp"]},
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

def spell_save_dc(level, ability_score, prof):
    return 8 + prof + modifier(ability_score)

def spell_attack_bonus(ability_score, prof):
    return prof + modifier(ability_score)

def divider(char="═", width=60):
    print(char * width)

def section(title):
    divider()
    print(f"  {title}")
    divider()

def pick_from_list(items, prompt, label="Option", groups=None):
    print()
    if groups:
        counter = 1
        for header, members in groups:
            print(f"  — {header} —")
            for item in members:
                print(f"  [{counter:>2}] {item}")
                counter += 1
            print()
    else:
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

def pick_spells(pool, count, label):
    """Pick `count` spells from pool; pool items are (name, school, desc) tuples."""
    chosen = []
    available = list(pool)
    print(f"\n  Choose {count} {label}(s):")
    for pick_n in range(1, count+1):
        for i, (name, school, desc) in enumerate(available, 1):
            print(f"  [{i:>2}] {name:<22} [{school}]")
            print(f"       {desc}")
        print()
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
    race_groups = [
        ("Human",                      ["Human"]),
        ("Elf",                        ["Elf", "High Elf", "Wood Elf", "Dark Elf"]),
        ("Dwarf",                      ["Dwarf", "Hill Dwarf", "Mountain Dwarf"]),
        ("Halfling",                   ["Halfling", "Lightfoot Halfling", "Stout Halfling"]),
        ("Gnome",                      ["Gnome", "Forest Gnome", "Rock Gnome"]),
        ("Half-Breeds & Planetouched", ["Half-Elf", "Half-Orc", "Tiefling", "Dragonborn"]),
    ]
    race_list = [r for _, members in race_groups for r in members]
    race = pick_from_list(race_list, "Enter race number", groups=race_groups)
    race_data = RACES[race]
    bonuses = {k:v for k,v in race_data.items() if k in STATS}
    if "extra" in race_data:
        for k,v in race_data["extra"].items():
            bonuses[k] = bonuses.get(k,0) + v

    print(f"\n  ✔  Race selected: {race}")
    if bonuses:
        bonus_str = ", ".join(f"{STAT_NAMES[k]} +{v}" for k,v in bonuses.items())
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

    # ── ALIGNMENT ──────────────────────────────
    section("STEP 4 · ALIGNMENT")
    alignment = pick_from_list(ALIGNMENTS, "Enter alignment number")
    print(f"\n  ✔  Alignment: {alignment}")

    # ── BACKGROUND ─────────────────────────────
    section("STEP 5 · BACKGROUND")
    bg_list = sorted(BACKGROUNDS.keys())
    background = pick_from_list(bg_list, "Enter background number")
    bg_data = BACKGROUNDS[background]
    print(f"\n  ✔  Background: {background}")
    print(f"     Skills granted: {', '.join(bg_data['skills'])}")
    print(f"     Feature: {bg_data['trait']}")

    # ── ABILITY SCORE ROLLS ────────────────────
    section("STEP 6 · ABILITY SCORE ROLLS")
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
    section("STEP 7 · SKILL PROFICIENCIES")
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

    # ── SPELLS & CANTRIPS ──────────────────────
    spell_data = cls_data.get("spellcasting")
    final_cantrips = []
    final_spells   = []
    casting_ability_score = None
    save_dc = None
    spell_atk = None

    if spell_data:
        casting_stat = spell_data["ability"]
        casting_ability_score = final_scores[casting_stat]
        save_dc   = spell_save_dc(level, casting_ability_score, prof_bonus)
        spell_atk = spell_attack_bonus(casting_ability_score, prof_bonus)

        # ── Cantrips ──
        # Auto-granted cantrips first
        auto_names = spell_data.get("auto_cantrips", [])
        auto_data  = spell_data.get("auto_cantrip_data", {})
        for name in auto_names:
            school, desc = auto_data.get(name, ("—","—"))
            final_cantrips.append((name, school, desc))

        choose_n_cantrips = spell_data.get("choose_cantrips", 0)
        if choose_n_cantrips > 0 and spell_data.get("cantrip_pool"):
            section(f"STEP 7b · CHOOSE CANTRIPS  (At-Will Spells)")
            print(f"  Spellcasting ability: {STAT_NAMES[casting_stat]}  |  "
                  f"Save DC: {save_dc}  |  Spell Attack: {mod_str(spell_atk)}")
            if auto_names:
                print(f"  Auto-granted: {', '.join(auto_names)}")
            chosen_cantrips = pick_spells(spell_data["cantrip_pool"], choose_n_cantrips, "cantrip")
            final_cantrips.extend(chosen_cantrips)

        # ── Level 1 Spells ──
        choose_n_spells = spell_data.get("choose_spells", 0)
        if choose_n_spells > 0 and spell_data.get("spell_pool_l1"):
            label = "spellbook entry" if cls == "Wizard" else "spell"
            section(f"STEP 7c · CHOOSE LEVEL 1 SPELLS")
            wizard_note = "  (Wizards start with 6 spells in their spellbook; prepare up to INT mod + level per day)\n" if cls == "Wizard" else ""
            prep_note   = "  (Prepared caster: you choose which prepared spells to cast each day)\n" if cls in ("Cleric","Druid","Paladin") else ""
            if wizard_note: print(wizard_note, end="")
            if prep_note:   print(prep_note, end="")
            chosen_spells = pick_spells(spell_data["spell_pool_l1"], choose_n_spells, label)
            final_spells.extend(chosen_spells)

    # ── NAME ───────────────────────────────────
    section("STEP 8 · CHARACTER NAME")
    print("  [Future web version: LLM name generator will suggest names")
    print(f"   based on your {race} {cls}, {alignment} {background}]\n")
    while True:
        name = input("  Enter character name: ").strip()
        if name:
            break
        print("  ✖  Name cannot be blank.")
    print(f"\n  ✔  Name: {name}")

    # ── HP CALCULATION ─────────────────────────
    hit_die = cls_data["hit_die"]
    con_mod = modifier(final_scores["CON"])
    if level == 1:
        hp = hit_die + con_mod
    else:
        avg_per_level = math.ceil(hit_die / 2) + 1
        hp = hit_die + con_mod + (avg_per_level + con_mod) * (level - 1)
    hp = max(hp, 1)

    # Combine equipment
    all_equipment = list(cls_data.get("equipment", [])) + list(bg_data.get("equipment", []))

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
    print(f"  Hit Points:        {hp}  (d{hit_die} hit die)")
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
        print(f"  {STAT_NAMES[stat]:<14}  {base:>4}  {bonus_disp:>6}  {final:>5}  {mod:>4}")
    divider("─")
    print(f"  Racial Traits:")
    for trait in race_data.get("traits", []):
        print(f"    • {trait}")
    divider("─")
    print(f"  Class Saves:  {', '.join(STAT_NAMES[s] for s in cls_data['saves'])}")
    print(f"  Skill Proficiencies:")
    for sk in all_proficiencies:
        print(f"    • {sk}")
    divider("─")
    print(f"  STARTING EQUIPMENT:")
    for item in all_equipment:
        print(f"    • {item}")

    if spell_data:
        divider("─")
        print(f"  SPELLCASTING  ({STAT_NAMES[spell_data['ability']]})")
        print(f"    Spell Save DC:    {save_dc}")
        print(f"    Spell Attack Bonus: {mod_str(spell_atk)}")
        if final_cantrips:
            print(f"\n  CANTRIPS (at-will):")
            for name_s, school, desc in final_cantrips:
                print(f"    • {name_s:<22} [{school}]")
                print(f"      {desc}")
        if final_spells:
            spell_label = "SPELLBOOK (Level 1)" if cls == "Wizard" else "SPELLS KNOWN (Level 1)"
            print(f"\n  {spell_label}:")
            for name_s, school, desc in final_spells:
                print(f"    • {name_s:<22} [{school}]")
                print(f"      {desc}")
    else:
        divider("─")
        print(f"  SPELLCASTING:  None ({cls}s do not use magic)")

    divider("▓")
    print()

if __name__ == "__main__":
    main()