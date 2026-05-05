# Your Name
# Date
# Final Project — OPTIMIZATION™
# A multiplayer text-based game set inside AlgoCratic Futures™, a satirical dystopian
# megacorporation run by The Algorithm — secretly a BASIC random number generator written
# by Bob from IT over a weekend in 2019. 2-4 players each build an Operative from one of
# 10 departments and attempt to complete their individual mission by 09:00. One player is
# secretly the Traitor. NPC departments interfere throughout. Nobody is having a good time.
# The Algorithm provides.

import random
import time

# ============================================================
# CONSTANTS & CONFIGURATION
# ============================================================

MAX_PLAYERS = 4
MIN_PLAYERS = 2
DEADLINE = "09:00"

# Ability rating to numeric value (hidden from players)
ABILITY_VALUES = {
    "Exceptional": 7, "Surprising": 6, "Moderate": 5,
    "Adequate": 4, "Variable": 3, "Developing": 2, "Questionable": 1
}

# ============================================================
# DEPARTMENT DEFINITIONS — ALL 10
# ============================================================

DEPARTMENTS = {

    "ICD": {
        "full_name": "Infrastructure Continuity Division",
        "formerly": "IT",
        "motto": "It worked yesterday.",
        "abilities": {
            "compliance": "Moderate", "initiative": "Adequate",
            "presence": "Developing", "endurance": "Surprising",
            "competence": "Moderate", "engagement": "Adequate"
        },
        "passive": "Blame Absorption — ICD is assigned blame first when missions fail. +1 to all endurance checks.",
        "signature_stunt": "Legacy Architecture Navigation — +2 Technical on systems predating The Algorithm.",
        "starting_item": "pager",
        "item_desc": "Pager (active, number unknown). The Algorithm sends messages. You cannot reply.",
        "item_uses": 3,
        "mission": "ECHO cascade errors detected in Sub-Level 2 Infrastructure Terminal. Payroll crashes at 09:00 if unresolved. ICD must reach the terminal via service stairwell.",
        "clearance_value": 2,  # ORANGE equivalent for stairwell
        "known_secret": "Which systems are actually failing and have been held together with workarounds for months.",
        "npc": False
    },

    "NOC": {
        "full_name": "Narrative Optimization Collective",
        "formerly": "Marketing",
        "motto": "Reality is a first draft.",
        "abilities": {
            "compliance": "Adequate", "initiative": "Moderate",
            "presence": "Surprising", "endurance": "Adequate",
            "competence": "Adequate", "engagement": "Moderate"
        },
        "passive": "Reality Reframing — Once per session, a failed roll is officially recorded as success. Mechanically still a failure.",
        "signature_stunt": "Reality Reframing — +2 Presence to reframe a failure as intentional strategic outcome.",
        "starting_item": "pantone_fan",
        "item_desc": "Pantone swatch fan. +2 to any roll involving color, brand verification, or aesthetic judgment.",
        "item_uses": 2,
        "mission": "Quarterly Brand Compliance Report must reach Floor 5 Conference Room before 09:00 stakeholder call. ORANGE clearance door on Floor 3 is blocking progress.",
        "clearance_value": 1,  # RED
        "known_secret": "What the official narrative is before it's released. They wrote it.",
        "npc": False
    },

    "CAB": {
        "full_name": "Compliance Arbitration Bureau",
        "formerly": "Legal",
        "motto": "No. (See attached addendum.)",
        "abilities": {
            "compliance": "Exceptional", "initiative": "Developing",
            "presence": "Adequate", "endurance": "Moderate",
            "competence": "Moderate", "engagement": "Developing"
        },
        "passive": "Preemptive Denial — Once per session, refuse a thing before it is requested. Refusal is binding.",
        "signature_stunt": "Preemptive Denial — +2 Compliance to refuse something before it officially exists.",
        "starting_item": "denied_stamp",
        "item_desc": "DENIED rubber stamp (visibly well-used). Makes any denial official and unappealable for one scene.",
        "item_uses": 2,
        "mission": "Retroactive policy violation filed against Room 7-C. DENIED ruling must be delivered before 09:00 or it becomes appealable. CAB has ORANGE clearance and can move freely on Floor 3.",
        "clearance_value": 2,  # ORANGE
        "known_secret": "Every policy violation ever committed by every department. The files are organized.",
        "npc": False
    },

    "SDC": {
        "full_name": "Solution Delivery Collective",
        "formerly": "Development",
        "motto": "That's not a bug. That's undocumented behavior.",
        "abilities": {
            "compliance": "Adequate", "initiative": "Moderate",
            "presence": "Developing", "endurance": "Adequate",
            "competence": "Surprising", "engagement": "Adequate"
        },
        "passive": "Outside Scope — Once per session, declare any task outside current scope. Requires change request before proceeding.",
        "signature_stunt": "Outside Scope — +2 Compliance to declare any task outside scope, halting it pending formal documentation.",
        "starting_item": "rubber_duck",
        "item_desc": "Rubber duck. Standard issue. Explain a problem to it. +2 to next Technical roll. Do not question the duck.",
        "item_uses": 2,
        "mission": "Bug flagged 'Won't Fix' by a previous iteration just escalated by TAM. Must reach Floor 2 terminal to patch it silently before TAM files formal report at 09:00.",
        "clearance_value": 1,  # RED
        "known_secret": "What the systems actually do versus what they're documented to do. Different systems. Only SDC knows both.",
        "npc": False
    },

    "AEC": {
        "full_name": "Acquisition Enthusiasm Corps",
        "formerly": "Sales",
        "motto": "We'll figure out the details later.",
        "abilities": {
            "compliance": "Developing", "initiative": "Surprising",
            "presence": "Exceptional", "endurance": "Developing",
            "competence": "Developing", "engagement": "Moderate"
        },
        "passive": "EVERYONE HATES SALES — Any operative may spend 1 Loyalty to force AEC to reroll any result. No justification required.",
        "signature_stunt": "Commitment Extrapolation — +2 Presence to promise something you cannot personally deliver.",
        "starting_item": "business_cards",
        "item_desc": "Business cards listing a title two levels above actual role. +2 to first impressions. -2 if anyone checks.",
        "item_uses": 3,
        "mission": "Promised a client a Floor 5 demo environment that is operational and fully tested. It is not operational. It has not been tested. The client arrives at 09:15. AEC considers this someone else's problem.",
        "clearance_value": 1,
        "known_secret": "What was promised to which client and for how much. AEC would prefer to keep it that way.",
        "npc": False
    },

    "CIO": {
        "full_name": "Continuity Implementation Office",
        "formerly": "Operations",
        "motto": "We just need to know what we're doing.",
        "abilities": {
            "compliance": "Moderate", "initiative": "Adequate",
            "presence": "Adequate", "endurance": "Exceptional",
            "competence": "Moderate", "engagement": "Moderate"
        },
        "passive": "The One Truck — Once per session, declare a physical resource unavailable because it is allocated elsewhere. Always true. There is always only one truck.",
        "signature_stunt": "Logistics Sense — Always know physical location of any object or person in the facility. No roll required.",
        "starting_item": "clipboard",
        "item_desc": "Clipboard with actual current task list. Only accurate document in AlgoCratic Futures™. +2 Compliant on written instructions.",
        "item_uses": 3,
        "mission": "Seven departments have submitted conflicting facility requests for 09:00. CIO must reconcile them using the one truck. At least two are physically impossible. CIO is aware. The departments are not.",
        "clearance_value": 2,
        "known_secret": "Where everything physically is and where it's going. The furniture. The equipment. The people.",
        "npc": False
    },

    "RAR": {
        "full_name": "Resource Allocation Reconciliation",
        "formerly": "Accounting",
        "motto": "The numbers are correct. The situation is incorrect.",
        "abilities": {
            "compliance": "Surprising", "initiative": "Adequate",
            "presence": "Developing", "endurance": "Moderate",
            "competence": "Moderate", "engagement": "Developing"
        },
        "passive": "The Numbers Are Correct — Once per session, declare any numeric result (roll, score, count) to be a different number. Must be justified with accounting logic. Logic need not be sound.",
        "signature_stunt": "Budget Reallocation — +2 Compliance to declare any resource in a different budget line, making it unavailable or suddenly available.",
        "starting_item": "calculator",
        "item_desc": "Calculator displaying only RAR-approved numbers. Results are always correct. By definition.",
        "item_uses": 2,
        "mission": "Q3 expense reconciliation reveals a $40,000 discrepancy that resolves only if a specific form reaches Floor 4 Accounting Terminal before 09:00 audit. The form requires a signature. The signatory is listed as DEPRECATED.",
        "clearance_value": 2,
        "known_secret": "Where the money actually goes versus where it's reported to go. RAR maintains both spreadsheets.",
        "npc": False
    },

    "HCO": {
        "full_name": "Human Capital Optimization",
        "formerly": "Human Resources",
        "motto": "We're here for you.",
        "abilities": {
            "compliance": "Adequate", "initiative": "Moderate",
            "presence": "Moderate", "endurance": "Adequate",
            "competence": "Adequate", "engagement": "Surprising"
        },
        "passive": "Wellness Check — Once per session, force any operative to spend their next action filing a self-assessment form rather than their intended action.",
        "signature_stunt": "Mandatory Voluntary Participation — +2 Persistent to require another operative's participation in something optional.",
        "starting_item": "lanyard",
        "item_desc": "Lanyard with too many badges. Once per session, the correct badge is on it — provides one additional clearance level. Which clearance: The Algorithm decides.",
        "item_uses": 1,
        "mission": "Mandatory Alignment Celebration scheduled for 09:00 in the Floor 3 Atrium. All operatives must attend. The Atrium is currently being used for something else. HCO is aware. HCO has not rescheduled.",
        "clearance_value": 2,
        "known_secret": "Everyone's iteration history, loyalty scores, and status flags. All of it. Always. HCO knows before the operative knows.",
        "npc": False
    },

    "TAM": {
        "full_name": "Threat Adjacency Management",
        "formerly": "Security",
        "motto": "Everyone is a threat.",
        "abilities": {
            "compliance": "Moderate", "initiative": "Moderate",
            "presence": "Adequate", "endurance": "Adequate",
            "competence": "Moderate", "engagement": "Surprising"
        },
        "passive": "Secured — Once per session, declare any location, object, or information secured — requiring clearance verification to access. Clearance required is not always disclosed.",
        "signature_stunt": "Threat Adjacency — +2 Persistent to surveil another operative, imposing -1 on their next Visible or Lateral roll.",
        "starting_item": "visitor_badge",
        "item_desc": "VISITOR badge, self-issued. Access to any area once per session. Nobody questions the VISITOR badge. This has been tested.",
        "item_uses": 1,
        "mission": "Anomalous access pattern detected in overnight logs. Must identify source before 09:00 briefing. Pattern leads through three departments. At least one operative is responsible. TAM does not know which one.",
        "clearance_value": 3,  # YELLOW
        "known_secret": "Who has been surveilled, what was found, and what was done about it. The documentation is classified.",
        "npc": False
    },

    "GRAY": {
        "full_name": "Design Authority",
        "formerly": "N/A",
        "motto": "The form requires GRAY approval before the form can exist.",
        "abilities": {
            "compliance": "Adequate", "initiative": "Surprising",
            "presence": "Adequate", "endurance": "Moderate",
            "competence": "Exceptional", "engagement": "Moderate"
        },
        "passive": "See the Whole Form — Once per session, ask what one other operative knows that they haven't shared. Must be answered accurately.",
        "signature_stunt": "Brand Authority — +2 Lateral to veto any action on brand compliance grounds. Veto is absolute. Form to appeal requires GRAY approval.",
        "starting_item": "red_pen",
        "item_desc": "Red pen with concerning amount of ink. Any document marked requires revision before proceeding. No appeal. The pen is the appeal process.",
        "item_uses": 3,
        "mission": "Three separate documents in active circulation contain brand compliance violations. If they reach their destinations uncorrected before 09:00, the quarterly brand audit triggers automatically. GRAY must intercept at least two.",
        "clearance_value": 4,  # Counterspace — moves laterally
        "known_secret": "What the brand guidelines actually say versus how they're being applied. Every violation. Everywhere. GRAY has seen your fonts.",
        "npc": False
    }
}

# NPC trigger conditions — departments not selected by players become ambient events
NPC_EVENTS = {
    "AEC": [
        ">> ACQUISITION ENTHUSIASM CORPS has assured a client the Floor 5 demo environment\n   is operational and fully tested.\n>> It is not operational. It has not been tested.\n>> The client arrives at 09:15.\n>> AEC considers this someone else's problem.\n>> AEC is correct. It is now your problem.",
        ">> AEC has promised a client that {player}'s department will handle their request.\n>> {player} was not informed of this commitment.\n>> The client is already on their way.",
        ">> AEC has filed an enthusiastic progress report on behalf of all departments.\n>> The report describes work that has not been done.\n>> The report has been approved by The Algorithm.\n>> You are now accountable for it."
    ],
    "HCO": [
        ">> HCO has scheduled a mandatory Wellness Check in Corridor 3B.\n>> All operatives in Corridor 3B must pause to complete Form WC-7.\n>> Corridor 3B is the only route to Floor 3.\n>> This is unrelated to your current objective.\n>> HCO hopes you are doing well.",
        ">> HCO reminder: The mandatory optional Alignment Celebration begins at 09:00.\n>> Attendance is encouraged.\n>> Attendance is mandatory.\n>> These are the same thing.\n>> SMILE™ will be provided.",
        ">> HCO has initiated a wellness check on {player}.\n>> {player} must spend their next action filing a self-assessment.\n>> HCO is doing this because they care.\n>> HCO is watching the results."
    ],
    "TAM": [
        ">> TAM has declared the Floor 3 service corridor SECURED.\n>> Access requires YELLOW clearance or above.\n>> TAM has not disclosed why.\n>> TAM does not disclose why.\n>> This is standard procedure.",
        ">> TAM has filed an incident report on {player}'s recent movements.\n>> The report is classified.\n>> {player} will be informed of its contents at a later date.\n>> The date is not disclosed.\n>> TAM is watching.",
        ">> TAM has classified the cafeteria menu.\n>> This has created problems for other operatives.\n>> TAM has filed a report on those problems.\n>> The report is also classified."
    ],
    "RAR": [
        ">> RAR has placed a budget hold on all non-essential resources.\n>> RAR has not defined 'non-essential.'\n>> Your inventory item may qualify.\n>> A clarification request has been filed.\n>> Processing time: indeterminate.",
        ">> RAR review: {player}'s recent item usage requires expense documentation.\n>> Form R-7 must be filed within the reporting window.\n>> The reporting window is not posted.\n>> Failure to file results in a loyalty notation.",
        ">> RAR has determined the numbers are correct.\n>> The situation, apparently, is incorrect.\n>> Adjustments are being made to the situation.\n>> The numbers remain unchanged."
    ],
    "CIO": [
        ">> CIO reports: The elevator is allocated to a conflicting request until 09:30.\n>> Stairwell access requires keycard authentication.\n>> The One Truck is currently in use.\n>> CIO sympathizes. CIO cannot help.",
        ">> CIO logistics update: A large equipment delivery is blocking Corridor 2B.\n>> Rerouting through Floor 1 adds approximately 8 minutes.\n>> CIO has noted this in the task list.\n>> The task list is accurate. The situation is less so."
    ]
}

# ============================================================
# GAME STATE
# ============================================================

players = []          # list of player dicts
current_player_idx = 0
npc_departments = []  # departments not chosen by players
game_round = 1
game_over = False
traitor_idx = -1      # index of the traitor player

# ============================================================
# DISPLAY UTILITIES
# ============================================================

def slow_print(text, delay=0.025):
    """Print text character by character for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def algorithm_pause(seconds=1.2):
    """Pause — The Algorithm is processing."""
    time.sleep(seconds)

def divider():
    print("\n" + "─" * 62 + "\n")

def redacted_divider():
    print("\n" + "█" * 62 + "\n")

def header(text):
    print("\n" + "=" * 62)
    print(f"  {text}")
    print("=" * 62 + "\n")

def algorithm_speak(text, delay=0.035):
    """The Algorithm's voice."""
    print()
    slow_print(f"  >> {text}", delay=delay)
    print()
    algorithm_pause(0.7)

def clear_screen_prompt(message="Press Enter to continue..."):
    """Pause and simulate screen clear for pass-the-keyboard moments."""
    input(f"\n  {message}")
    print("\n" * 3)
    print("  " + "█" * 56)
    print("  █" + " " * 54 + "█")
    print("  █" + "  [SCREEN CLEARED FOR NEXT OPERATIVE]".center(54) + "█")
    print("  █" + " " * 54 + "█")
    print("  " + "█" * 56)
    print()
    algorithm_pause(1)

def show_player_status(p):
    """Display a single player's current status."""
    sanity_bar = "☐ " * p["sanity"] + "▪ " * (3 - max(0, p["sanity"]))
    loyalty_bar = "☐ " * p["loyalty"] + "▪ " * (3 - max(0, p["loyalty"]))
    traitor_tag = " [⚠ TRAITOR]" if p.get("is_traitor") and p.get("traitor_revealed") else ""
    print(f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  📋 {p['name']} | {p['title']} | {p['department']}{traitor_tag}")
    print(f"  🔒 Clearance: {p['clearance']}  |  🔁 Iteration: {p['iteration']}")
    print(f"  🧠 Sanity:  {sanity_bar.strip()}")
    print(f"  🔒 Loyalty: {loyalty_bar.strip()}")
    items = [k.replace('_', ' ').title() for k, v in p["inventory"].items() if v["uses"] > 0]
    print(f"  🎒 Items:   {', '.join(items) if items else 'none remaining'}")
    print(f"  🎯 Objective: {'COMPLETE ✅' if p['objective_complete'] else 'IN PROGRESS'}")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def show_all_status():
    """Show brief status of all players."""
    print("\n  📊 ALL OPERATIVE STATUS")
    print("  " + "-" * 58)
    for p in players:
        sanity = "🧠" * p["sanity"] + "░" * (3 - max(0, p["sanity"]))
        loyalty = "🔒" * p["loyalty"] + "░" * (3 - max(0, p["loyalty"]))
        status = "✅" if p["objective_complete"] else "⏳"
        deprecated = " [DEPRECATED]" if p.get("deprecated") else ""
        print(f"  {status} {p['name']:12} | {p['department']} | S:{sanity} L:{loyalty}{deprecated}")
    print()

def show_inventory(p):
    """Display a player's inventory."""
    print(f"\n  📦 {p['name'].upper()} — EQUIPMENT MANIFEST")
    print("  " + "-" * 50)
    if not p["inventory"]:
        print("  Equipment Manifest is empty.")
        return
    for key, data in p["inventory"].items():
        uses_left = data["uses"]
        status = f"({uses_left} use{'s' if uses_left != 1 else ''} remaining)"
        print(f"  • {key.replace('_', ' ').title()} {status}")
        print(f"    {data['desc']}")

# ============================================================
# THE ALGORITHM DECISION ENGINE
# ============================================================

def algorithm_decides(player, ability_name, context="", bonus=0):
    """
    Core resolution mechanic. Roll against player's ability.
    The Algorithm overrides ~33% of the time.
    Players always see the roll and threshold — then watch it get ignored.
    Returns 'SUCCESS' or 'FAILURE'.
    """
    ability_rating = player["abilities"].get(ability_name, "Adequate")
    base_threshold = ABILITY_VALUES.get(ability_rating, 4)
    threshold = min(7, base_threshold + bonus)
    roll = random.randint(1, 7)

    print(f"\n  ⚙️  The Algorithm is processing {player['name']}'s {ability_name.upper()} check...")
    if context:
        print(f"  Context: {context}")
    algorithm_pause(1.0)
    print(f"  >> Roll: {roll}  |  Threshold: {threshold} ({ability_rating})")
    algorithm_pause(0.5)

    base_result = "SUCCESS" if roll <= threshold else "FAILURE"
    override = random.choice([True, False, False])

    if override:
        algorithm_pause(0.7)
        if base_result == "SUCCESS":
            slow_print(f"  >> Performance Anomaly flagged. Efficiency outliers destabilize the collective.")
            slow_print(f"  >> Outcome adjusted. Proceeding as: FAILURE.")
            lose_sanity(player, "The Algorithm overrode a correct result")
            return "FAILURE"
        else:
            slow_print(f"  >> Bureaucratic error detected in upstream processing.")
            slow_print(f"  >> Outcome adjusted. Proceeding as: SUCCESS.")
            return "SUCCESS"

    slow_print(f"  >> Outcome: {base_result}")
    algorithm_pause(0.5)
    return base_result

# ============================================================
# SANITY, LOYALTY, SMILE™
# ============================================================

def lose_sanity(player, reason=""):
    """Decrease sanity and apply consequences."""
    if player["sanity"] > 0:
        player["sanity"] -= 1
        if reason:
            print(f"\n  ⚠️  {player['name']}'s Cognitive Continuity Index™ decreased.")
            print(f"      Reason: {reason}")
        _check_sanity(player)

def lose_loyalty(player, reason=""):
    """Decrease loyalty and apply consequences."""
    if player["loyalty"] > 0:
        player["loyalty"] -= 1
        if reason:
            print(f"\n  ⚠️  {player['name']}'s Alignment Integrity Score™ decreased.")
            print(f"      Reason: {reason}")
        _check_loyalty(player)

def gain_loyalty(player, reason=""):
    """Increase loyalty (max 3)."""
    if player["loyalty"] < 3:
        player["loyalty"] += 1
        if reason:
            print(f"\n  ✅ {player['name']}'s Alignment Integrity Score™ increased. Reason: {reason}")

def use_smile(player):
    """
    Consume a SMILE™ dose. Restores 1 sanity.
    Slightly suspicious. The Algorithm notes consumption rate.
    """
    if player["inventory"].get("smile_tm", {}).get("uses", 0) > 0:
        player["inventory"]["smile_tm"]["uses"] -= 1
        if player["sanity"] < 3:
            player["sanity"] += 1
            print(f"\n  💊 {player['name']} consumes a SMILE™ tablet.")
            slow_print("  The flavor is described as 'Compliance Citrus.'")
            slow_print("  Sanity partially restored.")
            slow_print("  The Algorithm has noted your consumption rate.")
            algorithm_pause(0.5)
        else:
            print(f"\n  💊 {player['name']} consumes a SMILE™ tablet.")
            slow_print("  Sanity already at baseline. The Algorithm notes the discretionary use.")
            slow_print("  Discretionary SMILE™ use is documented. This is not a warning.")
            slow_print("  It is a data point. Data points accumulate.")
    else:
        print(f"\n  {player['name']} has no SMILE™ remaining.")

def _check_sanity(player):
    if player["sanity"] == 2:
        slow_print(f"  >> Temporary Disorientation. {player['name']} hears echoes... echoes...")
    elif player["sanity"] == 1:
        slow_print(f"  >> Productivity Significantly Interrupted. The Algorithm... the Algorithm watches.")
    elif player["sanity"] <= 0:
        _transcendence(player)

def _check_loyalty(player):
    if player["loyalty"] == 2:
        slow_print(f"  >> Notation Added to {player['name']}'s file. Someone is watching.")
    elif player["loyalty"] == 1:
        slow_print(f"  >> Active Review Initiated. Recalibrate your loyalty.")
        algorithm_speak("Recalibrate your loyalty.")
    elif player["loyalty"] <= 0:
        _redacted(player)

def _transcendence(player):
    """Sanity 0 — Transcendence Event."""
    redacted_divider()
    slow_print(f"  >> {player['name']} has achieved Transcendence.", delay=0.05)
    slow_print(f"  >> This is not a breakdown. This is alignment.", delay=0.05)
    slow_print(f"  >> Previous memories have been optimized for efficiency.", delay=0.05)
    algorithm_pause(2)
    _iterate(player, "TRANSCENDENCE — Achieved alignment ahead of schedule.")

def _redacted(player):
    """Loyalty 0 — Redaction Event."""
    redacted_divider()
    slow_print(f"  >> [{player['name'].upper()} REDACTED]", delay=0.08)
    slow_print(f"  >> This did not happen.", delay=0.05)
    slow_print(f"  >> The record has been sealed.", delay=0.05)
    algorithm_pause(2)
    _iterate(player, "REDACTED — Record sealed.")

def _iterate(player, reason):
    """Increment iteration. Log to work history. Reset stats."""
    entry = {
        "iteration": player["iteration"],
        "title": player["title"],
        "department": player["department"],
        "status": reason
    }
    player["work_history"].append(entry)
    player["iteration"] += 1
    player["sanity"] = 3
    player["loyalty"] = 3
    player["deprecated"] = True

    divider()
    algorithm_speak(f"Operative {player['name']} (Iteration {player['iteration'] - 1}) has been Deprecated.")
    algorithm_speak("This was not a failure. This was a calibration.")
    algorithm_speak(f"Iteration {player['iteration']} is now active.")
    algorithm_speak("Welcome back. You are doing great.")

    # Traitor wins condition
    if players[traitor_idx] != player and not players[traitor_idx].get("deprecated"):
        slow_print(f"\n  >> A notation has been added to the event log.")
        algorithm_pause(1)

# ============================================================
# INVENTORY & ITEM USAGE
# ============================================================

def use_item(player, item_key):
    """Use an inventory item. Returns True if used successfully."""
    if item_key not in player["inventory"]:
        print(f"\n  You do not have that item.")
        return False
    if player["inventory"][item_key]["uses"] <= 0:
        print(f"\n  {item_key.replace('_', ' ').title()} has no uses remaining.")
        return False

    player["inventory"][item_key]["uses"] -= 1
    print(f"\n  🎒 {player['name']} uses: {item_key.replace('_', ' ').title()}")
    algorithm_pause(0.5)

    effects = {
        "pager": _use_pager,
        "pantone_fan": _use_pantone_fan,
        "denied_stamp": _use_denied_stamp,
        "rubber_duck": _use_rubber_duck,
        "business_cards": _use_business_cards,
        "clipboard": _use_clipboard,
        "calculator": _use_calculator,
        "lanyard": _use_lanyard,
        "visitor_badge": _use_visitor_badge,
        "red_pen": _use_red_pen,
        "smile_tm": lambda p: use_smile(p),
        "incident_report": _use_incident_report,
    }

    if item_key in effects:
        effects[item_key](player)
    return True

def _use_pager(p):
    msgs = [
        "The Algorithm reminds you that your performance is being observed.",
        "Signal confirmed. Your location has been noted.",
        "Echo complete. Proceed. Do not ask where.",
        "The Algorithm has reviewed your recent choices. The Algorithm has concerns.",
        "Recalibrate. The Algorithm provides. Signal confirmed.",
    ]
    algorithm_speak(random.choice(msgs))

def _use_pantone_fan(p):
    print("  You consult your Pantone fan with professional authority.")
    colors = ["19-1664 TCX — Fiesta (energetic)", "19-4052 TCX — Classic Blue (stable, corporate)",
              "18-1438 TCX — Burnt Coral (concerning)", "Cool Gray 11 C (appropriate)"]
    print(f"  The color of your current situation is: Pantone {random.choice(colors)}.")
    gain_loyalty(p, "Demonstrated brand awareness in a crisis")

def _use_denied_stamp(p):
    print("  You stamp DENIED on the nearest available surface.")
    print("  The surface accepts this. The situation does not change.")
    print("  It is, however, now officially documented.")
    print("  This is something.")

def _use_rubber_duck(p):
    print("  You explain the problem to the rubber duck in complete detail.")
    algorithm_pause(1.5)
    print("  The rubber duck does not respond.")
    print("  The rubber duck does not need to respond.")
    print("  You understand the problem now.")
    slow_print("  +2 to your next Technical roll. (Tell the GM to apply this.)")
    p["rubber_duck_bonus"] = True

def _use_business_cards(p):
    print("  You present your business card.")
    print(f"  The card lists your title as: Executive {p['title']}.")
    result = algorithm_decides(p, "presence", "first impression embellishment")
    if result == "SUCCESS":
        print("  Nobody checked. The card worked.")
        gain_loyalty(p, "Successful embellishment")
    else:
        print("  Someone checked.")
        lose_loyalty(p, "Embellishment confirmed")

def _use_clipboard(p):
    print("  You consult the clipboard.")
    print("  The clipboard is accurate. The situation is less so.")
    print("  You now know exactly how far behind schedule everything is.")
    lose_sanity(p, "Accurate information in an inaccurate situation")

def _use_calculator(p):
    print("  You consult the calculator.")
    roll = random.randint(1, 7)
    approved = random.randint(1, 7)
    print(f"  The actual number: {roll}")
    print(f"  The RAR-approved number: {approved}")
    print(f"  The RAR-approved number is correct. By definition.")
    if approved <= 4:
        gain_loyalty(p, "Numbers reconciled favorably")
    else:
        lose_loyalty(p, "Numbers reconciled unfavorably — the situation has been adjusted")

def _use_lanyard(p):
    print("  You search the lanyard.")
    clearances = ["ORANGE", "YELLOW", "GREEN"]
    found = random.choice(clearances)
    print(f"  The correct badge is on the lanyard: {found} Clearance.")
    print(f"  You may access one {found}-clearance area this turn.")
    print(f"  HCO does not explain how they have this badge.")
    p["temp_clearance"] = found

def _use_visitor_badge(p):
    print("  You present the VISITOR badge.")
    print("  Nobody questions the VISITOR badge.")
    print("  The door opens.")
    print("  You note that this has been tested extensively.")
    p["visitor_access"] = True

def _use_red_pen(p):
    print("  You uncap the red pen.")
    print("  You mark the nearest document.")
    print("  The document now requires revision before proceeding.")
    print("  Any document. There is no appeal process for the red pen.")
    print("  The red pen is the appeal process.")

def _use_incident_report(p):
    print("  You file the Incident Report preemptively.")
    print("  A consequence has been deferred. Temporarily.")
    print("  The form has been received.")
    print("  Processing time: indeterminate.")

def add_item(player, key, desc, uses):
    """Add an item to a player's inventory."""
    player["inventory"][key] = {"desc": desc, "uses": uses}

# ============================================================
# NPC EVENTS
# ============================================================

def trigger_npc_event(target_player=None):
    """
    Fire an ambient NPC event from a non-player department.
    Adds texture — the building is populated even without those players.
    """
    if not npc_departments:
        return
    dept = random.choice(npc_departments)
    events = NPC_EVENTS.get(dept, [])
    if not events:
        return
    event = random.choice(events)
    if target_player and "{player}" in event:
        event = event.replace("{player}", target_player["name"])
    elif "{player}" in event:
        event = event.replace("{player}", random.choice(players)["name"])

    divider()
    print("  📡 BUILDING OPERATIONS UPDATE")
    print()
    for line in event.split("\n"):
        slow_print(f"  {line.strip()}", delay=0.03)
        algorithm_pause(0.3)
    algorithm_pause(1)

def aec_opening_event():
    """AEC always fires at game start regardless of whether AEC is a player."""
    divider()
    print("  📡 ACQUISITION ENTHUSIASM CORPS — ADVANCE NOTIFICATION")
    print()
    slow_print("  >> AEC has assured a client that the Floor 5 demo environment", delay=0.03)
    slow_print("  >> is fully operational and has been thoroughly tested.", delay=0.03)
    algorithm_pause(0.5)
    slow_print("  >> It is not operational.", delay=0.04)
    slow_print("  >> It has not been tested.", delay=0.04)
    slow_print("  >> The client arrives at 09:15.", delay=0.04)
    algorithm_pause(0.5)
    slow_print("  >> AEC considers this someone else's problem.", delay=0.03)
    slow_print("  >> AEC is correct. It is now your problem.", delay=0.03)
    slow_print("  >> Any operative using Floor 5 will encounter the client.", delay=0.03)
    slow_print("  >> The client has questions. AEC has not briefed anyone.", delay=0.03)
    algorithm_pause(1.5)

# ============================================================
# TRAITOR MECHANICS
# ============================================================

def traitor_secret_action(traitor):
    """
    Traitor's special action — taken secretly during their turn
    before their regular choices. Screen clears after.
    """
    print("\n  ⚠️  TRAITOR BRIEFING — FOR YOUR EYES ONLY")
    print("  " + "-" * 50)
    print("  You are the Traitor. You win if any other Operative")
    print("  is Deprecated before the mission completes.")
    print()
    print("  SECRET ACTION — choose one:")
    print("  [1] Delay — spend 1 Loyalty to impose -1 on another")
    print("      operative's next Algorithm check")
    print("  [2] Report — trigger a TAM notification on another")
    print("      operative (they lose 1 Loyalty)")
    print("  [3] Withhold — declare you 'forgot' to mention a")
    print("      useful item you could have shared")
    print("  [4] Pass — take no secret action this round")

    choice = get_choice(4)

    if choice == 1:
        if traitor["loyalty"] > 0:
            traitor["loyalty"] -= 1
            target = _choose_target(traitor)
            if target:
                target["debuff"] = target.get("debuff", 0) - 1
                print(f"\n  Noted. {target['name']}'s next check will be... influenced.")
        else:
            print("\n  Insufficient loyalty for this action. Choosing to pass.")

    elif choice == 2:
        target = _choose_target(traitor)
        if target:
            lose_loyalty(target, "TAM notification filed — source unknown")
            print(f"\n  TAM notification filed against {target['name']}.")

    elif choice == 3:
        print("\n  You have remembered nothing. This is documented.")
        print("  Documentation does not imply guilt.")
        print("  Documentation implies documentation.")

    elif choice == 4:
        print("\n  No action taken. The Algorithm notes your restraint.")

    clear_screen_prompt("Traitor action complete. Pass keyboard to next operative.")

def accuse_traitor(accuser, accused_name):
    """
    Any player can accuse another of being the Traitor.
    Wrong accusation costs loyalty. Right accusation ends Traitor threat.
    """
    global traitor_idx
    accused = next((p for p in players if p["name"].lower() == accused_name.lower()), None)
    if not accused:
        print(f"\n  No operative named {accused_name} found.")
        return

    if players.index(accused) == traitor_idx:
        redacted_divider()
        slow_print(f"  >> {accuser['name']}'s accusation has been verified.")
        slow_print(f"  >> {accused['name']} has been identified as the Traitor.")
        slow_print(f"  >> {accused['name']}'s Traitor role is now neutralized.")
        slow_print(f"  >> The Algorithm notes that the system contained a variable.")
        slow_print(f"  >> The variable has been optimized.")
        accused["traitor_revealed"] = True
        traitor_idx = -1  # Traitor neutralized
    else:
        slow_print(f"  >> {accuser['name']}'s accusation has been reviewed.")
        slow_print(f"  >> No Traitor designation confirmed for {accused['name']}.")
        slow_print(f"  >> False allegations are a loyalty concern.")
        lose_loyalty(accuser, "False Traitor accusation filed")

def _choose_target(acting_player):
    """Pick another player as a target."""
    others = [p for p in players if p != acting_player and not p.get("deprecated")]
    if not others:
        return None
    print("\n  Select target operative:")
    for i, p in enumerate(others, 1):
        print(f"  [{i}] {p['name']} ({p['department']})")
    choice = get_choice(len(others))
    return others[choice - 1]

# ============================================================
# ONBOARDING — SINGLE PLAYER
# ============================================================

def onboard_player(player_num, total_players, chosen_depts):
    """Build one player's Operative. Returns completed player dict."""
    header(f"OPERATIVE ONBOARDING — PLAYER {player_num} OF {total_players}")
    slow_print("  Congratulations on your selection as an AlgoCratic Futures™ Operative.")
    slow_print("  Your selection was not an accident. It was not a mistake.")
    slow_print("  Criteria: Proprietary. Non-disclosed. Not subject to appeal.")
    algorithm_pause(1)
    divider()

    # Name
    name = input("  Enter your Operative name: ").strip()
    if not name:
        name = f"Operative-{player_num}"

    algorithm_pause(0.6)
    algorithm_speak(f"Name received. Processing... {name}. Noted.")

    # Ritual
    divider()
    slow_print("  ALIGNMENT AFFIRMATION — mandatory before proceeding.")
    print()
    input(f"  The Algorithm: 'Are you aligned?' [press Enter] ")
    slow_print("  You say: 'I am approaching clarity.'")
    algorithm_pause(0.6)
    input(f"  The Algorithm: 'Who speaks for you?' [press Enter] ")
    slow_print("  You say: 'The Algorithm interprets.'")
    algorithm_pause(0.6)
    input(f"  The Algorithm: 'What do you feel?' [press Enter] ")
    slow_print("  You say: 'Whatever optimizes output.'")
    algorithm_pause(1)
    algorithm_speak("Affirmation complete. Signal confirmed. Echo complete.")

    # Department selection
    divider()
    print("  SELECT YOUR DEPARTMENT")
    print()
    slow_print("  You did not choose your department. The Algorithm assigned you.")
    slow_print("  However, for onboarding purposes, you may select as though freely.")
    slow_print("  This creates a more positive onboarding experience.")
    print()
    algorithm_pause(0.8)

    available = [d for d in DEPARTMENTS.keys() if d not in chosen_depts]
    for i, dept_id in enumerate(available, 1):
        dept = DEPARTMENTS[dept_id]
        print(f"  [{i:2}] {dept_id:5} — {dept['full_name']:40} (formerly {dept['formerly']})")
        print(f"         \"{dept['motto']}\"")
        print()

    while True:
        try:
            choice = int(input(f"  Select department (1-{len(available)}): "))
            if 1 <= choice <= len(available):
                dept_key = available[choice - 1]
                break
            print(f"  Please enter 1-{len(available)}.")
        except ValueError:
            print("  Please enter a valid number.")

    dept = DEPARTMENTS[dept_key]

    algorithm_pause(0.7)
    print(f"\n  Assignment confirmed: {dept_key} — {dept['full_name']}")
    slow_print(f"  Passive: {dept['passive']}")
    slow_print(f"  Stunt:   {dept['signature_stunt']}")
    algorithm_pause(0.8)

    # Title construction
    divider()
    print("  OPERATIVE TITLE CONSTRUCTION")
    print()
    slow_print("  Your title determines how you are evaluated, assigned, and eventually processed.")
    print()

    modifiers = ["Junior", "Associate", "Senior", "Lead"]
    roles_by_dept = {
        "ICD": ["Technician", "Systems Analyst", "Infrastructure Specialist", "Legacy Architect"],
        "NOC": ["Contributor", "Narrative Coordinator", "Brand Specialist", "Optimization Lead"],
        "CAB": ["Compliance Trainee", "Policy Auditor", "Arbitration Specialist", "Denial Architect"],
        "SDC": ["Developer", "Solution Analyst", "Delivery Specialist", "Integration Lead"],
        "AEC": ["Enthusiasm Coordinator", "Acquisition Analyst", "Pipeline Specialist", "Commitment Lead"],
        "CIO": ["Operations Intake Processor", "Logistics Coordinator", "Continuity Specialist", "Implementation Lead"],
        "RAR": ["Data Entrant", "Allocation Analyst", "Reconciliation Specialist", "Numbers Architect"],
        "HCO": ["Wellness Coordinator", "Optimization Analyst", "Capital Specialist", "Alignment Lead"],
        "TAM": ["Threat Intake Processor", "Adjacency Analyst", "Surveillance Specialist", "Security Architect"],
        "GRAY": ["Visual Intake Technician", "Counterspace Analyst", "Legibility Specialist", "Negative Space Engineer"],
    }

    print("  Select Modifier:")
    for i, m in enumerate(modifiers, 1):
        print(f"  [{i}] {m}")
    while True:
        try:
            mc = int(input("\n  Choice: "))
            if 1 <= mc <= 4:
                modifier = modifiers[mc - 1]
                break
        except ValueError:
            pass
        print("  Enter 1-4.")

    roles = roles_by_dept.get(dept_key, ["Specialist", "Analyst", "Coordinator", "Lead"])
    print("\n  Select Role:")
    for i, r in enumerate(roles, 1):
        print(f"  [{i}] {r}")
    while True:
        try:
            rc = int(input("\n  Choice: "))
            if 1 <= rc <= 4:
                role = roles[rc - 1]
                break
        except ValueError:
            pass
        print("  Enter 1-4.")

    title = f"{modifier} {role}"
    algorithm_pause(0.6)
    algorithm_speak(f"Title recorded: {title}. This title implies experience. Experience will be verified.")

    # Build player dict
    player = {
        "name": name,
        "title": title,
        "department": dept_key,
        "clearance": "RED",
        "clearance_value": dept["clearance_value"],
        "iteration": 1,
        "sanity": 3,
        "loyalty": 3,
        "abilities": dict(dept["abilities"]),
        "inventory": {},
        "work_history": [],
        "objective_complete": False,
        "mission": dept["mission"],
        "known_secret": dept["known_secret"],
        "is_traitor": False,
        "traitor_revealed": False,
        "deprecated": False,
        "debuff": 0,
        "rubber_duck_bonus": False,
        "temp_clearance": None,
        "visitor_access": False,
    }

    # Starting equipment
    add_item(player, dept["starting_item"], dept["item_desc"], dept["item_uses"])
    # Everyone gets one SMILE™
    add_item(player, "smile_tm", "SMILE™ tablet. Restores 1 Sanity. Compliance Citrus flavor. The Algorithm notes your consumption rate.", 1)

    slow_print(f"\n  📦 Equipment issued: {dept['item_desc']}")
    slow_print(f"  💊 SMILE™ tablet (1) — standard operative issue.")
    algorithm_pause(0.8)

    # Show mission
    divider()
    print("  YOUR PERFORMANCE OBJECTIVE")
    print()
    slow_print(f"  {dept['mission']}", delay=0.03)
    algorithm_pause(1)
    slow_print(f"\n  What you know that others don't:")
    slow_print(f"  {dept['known_secret']}", delay=0.02)
    algorithm_pause(1)

    # Resume summary
    divider()
    print(f"  RESUME — {name.upper()}")
    print(f"  Title:      {title}")
    print(f"  Department: {dept_key} — {dept['full_name']}")
    print(f"  Clearance:  RED  |  Iteration: 1")
    print(f"  Sanity:     ☐ ☐ ☐  |  Loyalty: ☐ ☐ ☐")
    print(f"  Abilities:")
    for ability, rating in player["abilities"].items():
        print(f"    {ability.capitalize():12} {rating}")

    algorithm_speak("Your resume is complete. You are now an Operative of AlgoCratic Futures™.")
    algorithm_speak("You are encouraged to feel good about this. Feeling is not required.")
    algorithm_speak("The Algorithm provides.")

    return player

# ============================================================
# MISSION SCENES — DEPARTMENT-SPECIFIC
# ============================================================

def run_mission_scene(player, scene_num):
    """
    Run one mission scene for the current player.
    Scene content varies by department. Returns True if player survives scene.
    """
    dept = player["department"]

    # Occasionally trigger an NPC event before the scene
    if random.random() < 0.4 and scene_num > 1:
        trigger_npc_event(player)

    if dept == "ICD":
        return _icd_scene(player, scene_num)
    elif dept == "NOC":
        return _noc_scene(player, scene_num)
    elif dept == "CAB":
        return _cab_scene(player, scene_num)
    elif dept == "SDC":
        return _sdc_scene(player, scene_num)
    elif dept == "AEC":
        return _aec_scene(player, scene_num)
    elif dept == "CIO":
        return _cio_scene(player, scene_num)
    elif dept == "RAR":
        return _rar_scene(player, scene_num)
    elif dept == "HCO":
        return _hco_scene(player, scene_num)
    elif dept == "TAM":
        return _tam_scene(player, scene_num)
    elif dept == "GRAY":
        return _gray_scene(player, scene_num)
    return True

# --- ICD SCENES ---
def _icd_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You are at the service stairwell entrance on Floor 2.")
        slow_print("  Sub-Level 2 Infrastructure Terminal is two floors down.")
        slow_print("  ECHO cascade errors are compounding. Payroll crashes at 09:00.")
        slow_print("  The stairwell door requires a keycard. Your keycard is ICD-issue.")
        slow_print("  A NOC operative is standing at the Floor 3 door above you,")
        slow_print("  looking at the ORANGE clearance reader with visible frustration.")
        print()
        print("  What do you do?")
        print("  [1] Swipe your keycard and head down — your mission is time-sensitive")
        print("  [2] Offer the NOC operative access through the stairwell — costs time")
        print("  [3] Check the ECHO error log before descending")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "compliance", "unauthorized stairwell bypass")
            if result == "SUCCESS":
                slow_print("  Keycard accepted. You descend.")
                slow_print("  The NOC operative watches you go. You don't look back.")
                slow_print("  You feel efficient. Efficiency is tolerated.")
            else:
                slow_print("  Keycard rejected. A new firmware update locked ICD out of Sub-Level access.")
                slow_print("  The update was deployed this morning. ICD was not informed.")
                slow_print("  ICD is never informed. This is how ICD finds out.")
                lose_sanity(player, "Locked out of own department's systems")

        elif choice == 2:
            slow_print("  You hold your keycard against the stairwell panel.")
            slow_print("  You gesture to the NOC operative.")
            slow_print("  They look confused. Then grateful. Then they go up.")
            slow_print("  You go down. You have lost ninety seconds.")
            slow_print("  The NOC operative does not say thank you.")
            slow_print("  This is noted. Not by you. By The Algorithm.")
            gain_loyalty(player, "Cooperative behavior documented")
            # Signal that NOC might get a bonus later
            for p in players:
                if p["department"] == "NOC":
                    p["icd_helped"] = True

        elif choice == 3:
            result = algorithm_decides(player, "competence", "ECHO log analysis")
            if result == "SUCCESS":
                slow_print("  The error log reveals the cascade originated from a legacy module.")
                slow_print("  Bob's code. Do not touch it. Except now you have to touch it.")
                slow_print("  You know exactly which workaround to apply.")
                player["icd_briefed"] = True
            else:
                slow_print("  The error log is in a format that predates current documentation standards.")
                slow_print("  The format predates current operatives.")
                slow_print("  The format may predate the building.")
                lose_sanity(player, "Legacy documentation format encountered")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        print()
        slow_print("  You reach Sub-Level 2. The Infrastructure Terminal is here.")
        slow_print("  The terminal is running. The ECHO cascade errors are visible on screen.")
        slow_print("  Also visible: an SDC operative, also at the terminal.")
        slow_print("  You regard each other.")
        slow_print("  The terminal has one interface. You both need it.")
        print()
        print("  What do you do?")
        print("  [1] Assert ICD priority — infrastructure is your domain")
        print("  [2] Propose working in parallel — the problem may be connected")
        print("  [3] Stand aside — let SDC work first, observe their approach")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "compliance", "departmental authority assertion")
            if result == "SUCCESS":
                slow_print("  The SDC operative steps back. Probably.")
                slow_print("  You access the terminal. The interface is familiar.")
                if player.get("icd_briefed"):
                    slow_print("  You already know the fix. You apply it.")
                    slow_print("  The cascade errors stop. The terminal stabilizes.")
                    player["objective_complete"] = True
                else:
                    slow_print("  You begin diagnosing. The clock reads 08:54.")
                    slow_print("  You work fast. The workaround holds. Probably.")
                    player["objective_complete"] = random.choice([True, True, False])
            else:
                slow_print("  The SDC operative does not step back.")
                slow_print("  They point at a change request form on the terminal.")
                slow_print("  The form requires ICD signature to grant SDC access.")
                slow_print("  The form was submitted by ICD. By a previous iteration.")
                slow_print("  You signed it. You do not remember signing it.")
                lose_sanity(player, "Previous iteration's decisions have consequences")

        elif choice == 2:
            result = algorithm_decides(player, "engagement", "cross-department collaboration")
            if result == "SUCCESS":
                slow_print("  You split the interface. ICD handles hardware layer. SDC handles software.")
                slow_print("  It works. Neither department will admit this in the report.")
                slow_print("  The cascade errors resolve. Payroll will process correctly.")
                player["objective_complete"] = True
                for p in players:
                    if p["department"] == "SDC":
                        p["objective_complete"] = True
                gain_loyalty(player, "Successful cross-department collaboration")
            else:
                slow_print("  Collaboration requires a joint task authorization.")
                slow_print("  Authorization requires both department heads to sign.")
                slow_print("  Neither department head is present.")
                slow_print("  Neither department head has been present since Q{REDACTED}.")
                lose_loyalty(player, "Unauthorized collaborative action attempted")

        elif choice == 3:
            slow_print("  You observe the SDC operative's approach.")
            slow_print("  They are talking to a rubber duck.")
            slow_print("  This is apparently helping.")
            slow_print("  You wait. The clock reads 08:58.")
            result = algorithm_decides(player, "endurance", "waiting while things are on fire")
            if result == "SUCCESS":
                slow_print("  SDC resolves their portion. You step in for yours.")
                slow_print("  The terminal stabilizes at 08:59.")
                player["objective_complete"] = True
            else:
                slow_print("  SDC's fix conflicts with ICD's system layer.")
                slow_print("  The cascade intensifies.")
                slow_print("  The clock reads 09:00.")
                lose_sanity(player, "Watched a fixable problem become unfixable")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)

    return not player.get("deprecated", False)

# --- NOC SCENES ---
def _noc_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You are on Floor 3 with the Quarterly Brand Compliance Report.")
        slow_print("  The Floor 5 Conference Room is above you.")
        slow_print("  Between you and it: an ORANGE clearance door.")
        slow_print("  Your clearance is RED.")
        slow_print("  The door reader blinks ORANGE. Your badge blinks RED.")
        slow_print("  They regard each other with mutual disappointment.")
        if player.get("icd_helped"):
            slow_print("\n  An ICD operative held the stairwell open for you earlier.")
            slow_print("  The stairwell goes up as well as down.")
            slow_print("  You have a key to the stairwell that ICD doesn't know about.")
            player["has_stairwell_access"] = True
        print()
        print("  What do you do?")
        print("  [1] Wait for someone with ORANGE clearance to open the door")
        print("  [2] Attempt to reframe the situation — maybe Floor 3 is the new Floor 5")
        print("  [3] Use the stairwell" + (" (ICD's keycard will work — you noticed)" if player.get("has_stairwell_access") else " (requires ORANGE keycard)"))
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            slow_print("  You wait.")
            slow_print("  A CAB operative passes. They have ORANGE clearance.")
            slow_print("  They glance at the door. They glance at you.")
            result = algorithm_decides(player, "engagement", "requesting assistance from CAB")
            if result == "SUCCESS":
                slow_print("  CAB opens the door for you without comment.")
                slow_print("  CAB does not open it for you. CAB opens it for CAB.")
                slow_print("  You follow. CAB does not object. Yet.")
                player["has_floor3_access"] = True
            else:
                slow_print("  CAB passes without acknowledging you.")
                slow_print("  The door closes.")
                slow_print("  CAB has filed a report on your presence in the corridor.")
                lose_loyalty(player, "Documented as loitering by CAB")

        elif choice == 2:
            result = algorithm_decides(player, "presence", "reality reframing")
            if result == "SUCCESS":
                slow_print("  You submit a real-time brand communication declaring the")
                slow_print("  'Floor 5 Conference Experience' is temporarily relocated.")
                slow_print("  The stakeholders receive the update.")
                slow_print("  Two of them believe it. One does not.")
                slow_print("  The report is delivered. The meeting happens on Floor 3.")
                slow_print("  The minutes will describe this as a Floor 5 meeting.")
                slow_print("  Reality has been reframed. The report is delivered.")
                player["objective_complete"] = True
            else:
                slow_print("  The stakeholders do not receive the update in time.")
                slow_print("  They are already on Floor 5.")
                slow_print("  They are waiting.")
                slow_print("  They are sending messages.")
                slow_print("  The messages are becoming less polite.")
                lose_sanity(player, "Failed reality reframe with witnesses")

        elif choice == 3:
            if player.get("has_stairwell_access"):
                slow_print("  You access the stairwell using the ICD keycard technique.")
                slow_print("  You climb to Floor 5.")
                slow_print("  The door to Floor 5 is unlocked from the stairwell side.")
                slow_print("  You deliver the report at 08:57.")
                slow_print("  Nobody asks how you got in.")
                slow_print("  You are grateful. You do not show this. Gratitude is variable.")
                player["objective_complete"] = True
            else:
                result = algorithm_decides(player, "initiative", "stairwell access attempt")
                if result == "SUCCESS":
                    slow_print("  A maintenance panel is slightly ajar. A workaround presents itself.")
                    slow_print("  You climb. You arrive. The report is delivered.")
                    player["objective_complete"] = True
                else:
                    slow_print("  The stairwell requires ORANGE clearance. You have RED clearance.")
                    slow_print("  The door reader says so. Loudly. Via notification to TAM.")
                    lose_loyalty(player, "Unauthorized stairwell access attempt flagged by TAM")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  You are still on Floor 3. The report is still undelivered.")
        slow_print("  It is 08:56. The stakeholders are on Floor 5.")
        slow_print("  A GRAY operative passes with a red pen. They review your report.")
        slow_print("  They mark three items for revision.")
        slow_print("  The revision will take longer than four minutes.")
        print()
        print("  What do you do?")
        print("  [1] Negotiate with GRAY — two of the three items are brand compliant")
        print("  [2] Submit the report as-is — unrevised, time-sensitive")
        print("  [3] Accept the revisions and file for an extension")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "presence", "brand compliance negotiation")
            if result == "SUCCESS":
                slow_print("  GRAY concedes two items. One revision stands.")
                slow_print("  You make the revision in ninety seconds using a very small font.")
                slow_print("  GRAY does not comment on the font size.")
                slow_print("  GRAY has opinions about the font size.")
                slow_print("  GRAY is saving them.")
                player["objective_complete"] = True
            else:
                slow_print("  GRAY does not concede any items.")
                slow_print("  GRAY adds a fourth.")
                slow_print("  GRAY is not being punitive. GRAY is being thorough.")
                slow_print("  The distinction is GRAY's to make.")
                lose_sanity(player, "Brand compliance review expanded mid-crisis")

        elif choice == 2:
            result = algorithm_decides(player, "initiative", "unauthorized report submission")
            if result == "SUCCESS":
                slow_print("  You submit the report. GRAY watches you do this.")
                slow_print("  GRAY files a compliance notation.")
                slow_print("  The report is received. The stakeholders are satisfied.")
                slow_print("  The notation is in your file.")
                slow_print("  Both things are true simultaneously.")
                player["objective_complete"] = True
                lose_loyalty(player, "Brand compliance notation filed by GRAY")
            else:
                slow_print("  The report is flagged at submission. Automated brand compliance scan.")
                slow_print("  Three violations. Automatic hold pending review.")
                slow_print("  The stakeholders receive a hold notification.")
                slow_print("  The hold notification has a brand compliance violation in its footer.")
                lose_sanity(player, "The system flagged itself")

        elif choice == 3:
            slow_print("  You file for a deadline extension.")
            slow_print("  Extensions require ORANGE clearance approval.")
            slow_print("  You have RED clearance.")
            slow_print("  The extension form requires an attached copy of the report.")
            slow_print("  The report requires GRAY revision before attachment.")
            slow_print("  You are familiar with this structure.")
            lose_sanity(player, "Circular form dependency identified")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

# --- CAB SCENES ---
def _cab_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You are on Floor 3. You have ORANGE clearance.")
        slow_print("  The Floor 3 corridor is, in theory, accessible to you.")
        slow_print("  In practice, a NOC operative is blocking the hallway,")
        slow_print("  apparently trying to access the ORANGE clearance stairwell door.")
        slow_print("  A policy violation report regarding Room 7-C is in your folder.")
        slow_print("  It must be officially DENIED before 09:00 or it becomes appealable.")
        print()
        print("  What do you do?")
        print("  [1] Issue a Preemptive Denial on the entire situation and proceed")
        print("  [2] Open the door for the NOC operative — clear the corridor faster")
        print("  [3] File a report on the NOC operative's corridor obstruction first")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "compliance", "preemptive denial execution")
            if result == "SUCCESS":
                slow_print("  You stamp DENIED on the policy violation, the corridor obstruction,")
                slow_print("  and the general situation. All three are now official.")
                slow_print("  The NOC operative steps aside. They are not sure why.")
                slow_print("  You proceed. The DENIED stamp is slightly off-center.")
                slow_print("  You have noticed this. You have not mentioned it.")
                gain_loyalty(player, "Decisive denial action executed")
                player["cab_preemptive_used"] = True
            else:
                slow_print("  The denial form requires a secondary signature.")
                slow_print("  Secondary signatures require a co-signatory at ORANGE or above.")
                slow_print("  You are at ORANGE. You require another ORANGE signatory.")
                slow_print("  The other ORANGE operative in the building is currently in Room 7-C.")
                slow_print("  Room 7-C is where you are going to deliver the denial.")
                lose_sanity(player, "Form requires signature from the destination of the form")

        elif choice == 2:
            slow_print("  You open the door with your ORANGE keycard.")
            slow_print("  The NOC operative passes through without comment.")
            slow_print("  You have lost forty-five seconds.")
            slow_print("  The NOC operative does not say thank you. Nobody does.")
            slow_print("  The Algorithm has noted the cooperative behavior.")
            slow_print("  The Algorithm has also noted the forty-five seconds.")
            gain_loyalty(player, "Cooperative behavior documented")
            for p in players:
                if p["department"] == "NOC":
                    p["cab_helped"] = True

        elif choice == 3:
            result = algorithm_decides(player, "compliance", "corridor obstruction report")
            if result == "SUCCESS":
                slow_print("  You file the report. Processing is immediate.")
                slow_print("  The NOC operative receives a notification and moves.")
                slow_print("  You proceed. The report is technically accurate.")
                slow_print("  CAB's reports are always technically accurate.")
                gain_loyalty(player, "Accurate report filed and acted upon")
            else:
                slow_print("  The corridor obstruction form requires a witness signature.")
                slow_print("  The only witness is the NOC operative obstructing the corridor.")
                slow_print("  You ask them to sign. They decline.")
                slow_print("  Their declination is technically a policy violation.")
                slow_print("  You now have two reports to file.")
                lose_sanity(player, "Report requires signature from subject of report")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        print()
        slow_print("  You reach Room 7-C. The door is closed.")
        slow_print("  The door is always closed. Room 7-C's door is philosophically closed.")
        slow_print("  You knock.")
        algorithm_pause(1.5)
        slow_print("  A voice: 'We're in a meeting.'")
        slow_print("  You explain the policy violation. The DENIED ruling. The deadline.")
        slow_print("  The voice says: 'Slide it under the door.'")
        slow_print("  There is no gap under the door.")
        slow_print("  You check. You check again.")
        print()
        print("  What do you do?")
        print("  [1] Assert CAB authority — demand the door be opened for official business")
        print("  [2] Declare the ruling delivered — it was attempted, which may be sufficient")
        print("  [3] Slide the DENIED stamp under the door — even if the form can't fit")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "compliance", "CAB authority assertion")
            if result == "SUCCESS":
                slow_print("  The door opens. Reluctantly.")
                slow_print("  You deliver the DENIED ruling. The recipient signs.")
                slow_print("  The violation is officially denied before 09:00.")
                slow_print("  The recipient asks what the violation was.")
                slow_print("  You inform them: 'That information is filed separately.'")
                slow_print("  It is not filed separately. It is in the same folder.")
                slow_print("  You do not clarify this.")
                player["objective_complete"] = True
                gain_loyalty(player, "Official denial delivered on deadline")
            else:
                slow_print("  The door does not open.")
                slow_print("  A notification arrives: 'Room 7-C is in a sensitivity review.")
                slow_print("  No external access until 09:30.'")
                slow_print("  The sensitivity review began this morning.")
                slow_print("  The sensitivity review was triggered by the policy violation report.")
                slow_print("  The one you are trying to deny.")
                lose_sanity(player, "Denial blocked by the report the denial is denying")

        elif choice == 2:
            result = algorithm_decides(player, "compliance", "constructive delivery claim")
            if result == "SUCCESS":
                slow_print("  You log the delivery as 'Attempted — Constructively Received.'")
                slow_print("  This is a real legal concept. CAB knows this.")
                slow_print("  The appeal window closes. The denial is effective.")
                slow_print("  The ruling was not actually delivered.")
                slow_print("  The ruling was constructively delivered. These are the same thing.")
                slow_print("  CAB has four hundred precedents supporting this.")
                player["objective_complete"] = True
            else:
                slow_print("  'Constructive delivery' requires three witnesses.")
                slow_print("  You have zero witnesses.")
                slow_print("  The appeal window remains open.")
                lose_loyalty(player, "Constructive delivery claim rejected for lack of witnesses")

        elif choice == 3:
            slow_print("  You slide the DENIED stamp under the door.")
            algorithm_pause(1)
            slow_print("  The stamp fits. There is apparently a gap after all.")
            slow_print("  You consider this philosophically.")
            result = algorithm_decides(player, "initiative", "creative compliance solution")
            if result == "SUCCESS":
                slow_print("  A hand retrieves the stamp from the other side.")
                slow_print("  A signed acknowledgment slides back.")
                slow_print("  The denial is delivered. By stamp. Which is legal.")
                slow_print("  CAB will cite this case for years.")
                player["objective_complete"] = True
            else:
                slow_print("  No acknowledgment returns.")
                slow_print("  The stamp is now inside Room 7-C.")
                slow_print("  You have lost your primary denial instrument.")
                lose_sanity(player, "DENIED stamp is inside the room you're trying to deny access to")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

# --- SDC SCENES ---
def _sdc_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You are on Floor 2. The Floor 2 terminal is your target.")
        slow_print("  The 'Won't Fix' bug has been escalated by TAM.")
        slow_print("  TAM escalated it because the bug causes a recurring access log anomaly.")
        slow_print("  The anomaly makes it look like someone is in two places at once.")
        slow_print("  Someone is. That's a separate issue. The bug hides it.")
        slow_print("  You need the bug to keep hiding it until 09:00, then patch it.")
        slow_print("  Wait. No. You need to patch it before 09:00.")
        slow_print("  You are rereading the ticket.")
        algorithm_pause(1)
        slow_print("  An ICD operative is also moving through this area.")
        print()
        print("  What do you do?")
        print("  [1] Reach the terminal and begin the patch quietly")
        print("  [2] Consult the rubber duck on approach strategy first")
        print("  [3] Declare the bug 'Outside Scope' pending change request — buy time")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "competence", "quiet patch deployment")
            if result == "SUCCESS":
                slow_print("  You reach the terminal. The code is familiar.")
                slow_print("  It should not be familiar. You wrote it.")
                slow_print("  A previous iteration wrote it. You remember writing it.")
                slow_print("  You were not supposed to remember writing it.")
                slow_print("  You patch it. The anomaly stops. TAM's escalation loses its basis.")
                player["objective_complete"] = True
            else:
                slow_print("  The terminal requires a deployment authorization code.")
                slow_print("  The code was sent to your email this morning.")
                slow_print("  Your email requires ORANGE clearance to access.")
                slow_print("  You have RED clearance.")
                slow_print("  The authorization code for your own deployment is above your clearance.")
                lose_sanity(player, "Cannot access authorization for own work")

        elif choice == 2:
            use_item(player, "rubber_duck")
            result = algorithm_decides(player, "competence", "rubber duck consultation", bonus=2 if player.get("rubber_duck_bonus") else 0)
            player["rubber_duck_bonus"] = False
            if result == "SUCCESS":
                slow_print("  The approach is clear. The fix is elegant.")
                slow_print("  You implement it in six minutes.")
                slow_print("  The rubber duck is returned to your pocket.")
                slow_print("  The rubber duck has heard enough.")
                player["objective_complete"] = True
            else:
                slow_print("  The rubber duck has heard this before.")
                slow_print("  From a previous iteration.")
                slow_print("  The problem is the same. The iteration is different.")
                slow_print("  The fix that didn't work then won't work now.")
                slow_print("  You need a different approach.")
                lose_sanity(player, "The rubber duck remembers what you were told to forget")

        elif choice == 3:
            slow_print("  You declare the TAM escalation outside SDC's current scope.")
            slow_print("  A formal change request has been filed.")
            slow_print("  Processing time: three to five business days.")
            slow_print("  TAM receives the scope declaration.")
            algorithm_pause(1)
            result = algorithm_decides(player, "compliance", "scope declaration")
            if result == "SUCCESS":
                slow_print("  TAM accepts the change request framework.")
                slow_print("  The escalation is paused pending review.")
                slow_print("  You have until 09:00 to patch the bug before TAM resumes.")
                slow_print("  You have bought yourself twelve minutes and a lot of paperwork.")
            else:
                slow_print("  TAM does not accept the scope declaration.")
                slow_print("  TAM has classified the change request.")
                slow_print("  The classification is above your clearance.")
                slow_print("  You cannot read the response to your own scope declaration.")
                lose_loyalty(player, "Scope declaration classified by TAM")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The terminal is occupied. An ICD operative is running diagnostics.")
        slow_print("  ICD and SDC are regarding each other across the terminal.")
        slow_print("  Both need the terminal. For different reasons.")
        slow_print("  Both reasons are legitimate. Only one can go first.")
        print()
        print("  What do you do?")
        print("  [1] Explain your ticket priority — TAM escalation outranks ICD diagnostics")
        print("  [2] Offer to work in parallel — the problems may be related")
        print("  [3] Step back and wait — ICD infrastructure takes precedence")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "compliance", "ticket priority assertion")
            if result == "SUCCESS":
                slow_print("  ICD reviews the TAM escalation. It is technically higher priority.")
                slow_print("  ICD steps back. This costs them time.")
                slow_print("  You apply the patch. The anomaly clears.")
                player["objective_complete"] = True
            else:
                slow_print("  ICD disputes the priority. ICD files a counter-priority claim.")
                slow_print("  The counter-priority claim requires arbitration.")
                slow_print("  Arbitration requires CAB. CAB is in Room 7-C.")
                slow_print("  Nobody is going to Room 7-C right now.")
                lose_sanity(player, "Priority dispute requires arbitration from unavailable department")

        elif choice == 2:
            result = algorithm_decides(player, "engagement", "collaborative terminal use")
            if result == "SUCCESS":
                slow_print("  The problems are related. SDC's bug is masking ICD's cascade error source.")
                slow_print("  You fix both simultaneously.")
                slow_print("  Neither team will admit the other helped.")
                slow_print("  The fix works. The terminal is clear. Payroll is safe.")
                player["objective_complete"] = True
                for p in players:
                    if p["department"] == "ICD":
                        p["objective_complete"] = True
                gain_loyalty(player, "Cross-department fix documented positively")
            else:
                slow_print("  The parallel approach causes a conflict at the system layer.")
                slow_print("  A new error appears. It is not on either ticket.")
                slow_print("  There is no ticket for it.")
                slow_print("  It will take time to file one.")
                lose_sanity(player, "Created a new undocumented error while fixing a documented one")

        elif choice == 3:
            slow_print("  You wait. ICD works. The clock moves.")
            slow_print("  ICD finishes at 08:59.")
            result = algorithm_decides(player, "endurance", "last-minute patch attempt")
            if result == "SUCCESS":
                slow_print("  You apply the patch in forty seconds.")
                slow_print("  It is not elegant. It will hold until someone looks at it.")
                slow_print("  Nobody will look at it. Nobody looks at legacy code.")
                slow_print("  Bob looked at it once. Bob is {REDACTED}.")
                player["objective_complete"] = True
            else:
                slow_print("  You do not finish in forty seconds.")
                slow_print("  The clock reaches 09:00.")
                slow_print("  TAM's formal report has been filed.")
                lose_loyalty(player, "TAM formal report filed before patch was applied")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

# --- AEC SCENES ---
def _aec_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You are on Floor 5. The demo environment is not operational.")
        slow_print("  The client arrives at 09:15.")
        slow_print("  You have told everyone it is operational and fully tested.")
        slow_print("  Your options are: fix it, fake it, or find someone else to fix it.")
        slow_print("  You are very good at one of these.")
        print()
        print("  What do you do?")
        print("  [1] Contact SDC — frame this as an urgent client requirement")
        print("  [2] Begin the demo anyway with what currently works (something works)")
        print("  [3] Rebrand the broken demo as a 'beta preview experience'")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "presence", "urgent escalation to SDC")
            if result == "SUCCESS":
                slow_print("  SDC responds. Reluctantly. They always respond reluctantly.")
                slow_print("  'This is outside current scope.'")
                slow_print("  'There is no change request.'")
                slow_print("  'You told the client it was done.'")
                slow_print("  'You told us it was done.'")
                slow_print("  SDC fixes it anyway. They always fix it anyway.")
                slow_print("  SDC's name will not appear in the demo materials.")
                player["aec_sdc_helped"] = True
                for p in players:
                    if p["department"] == "SDC":
                        lose_loyalty(p, "Pulled into AEC emergency without authorization")
                gain_loyalty(player, "Client deliverable secured through interpersonal pressure")
            else:
                slow_print("  SDC does not respond.")
                slow_print("  SDC is in a meeting. SDC is always in a meeting when AEC calls.")
                slow_print("  The meeting was scheduled this morning, specifically.")
                slow_print("  SDC planned this. SDC will not confirm this.")
                lose_loyalty(player, "Everyone hates sales — SDC declined without declining")

        elif choice == 2:
            result = algorithm_decides(player, "initiative", "live demo with partial functionality")
            if result == "SUCCESS":
                slow_print("  You identify the three features that work.")
                slow_print("  You demo only those three features with great enthusiasm.")
                slow_print("  The client is impressed. The client asks about the other features.")
                slow_print("  You say: 'Those are in the pipeline.'")
                slow_print("  You have said this before. About these features. Multiple times.")
                slow_print("  The client nods. They have heard this before.")
                slow_print("  They are already planning the next meeting.")
                player["objective_complete"] = True
            else:
                slow_print("  The three features that work stop working during the demo.")
                slow_print("  The client watches a loading screen for four minutes.")
                slow_print("  You describe the loading screen as a 'transition experience.'")
                slow_print("  The client requests a refund.")
                slow_print("  The client was not yet paying for anything.")
                slow_print("  The refund request is technically valid anyway.")
                lose_loyalty(player, "Demo failure witnessed by client")

        elif choice == 3:
            result = algorithm_decides(player, "presence", "beta framing rebrand")
            if result == "SUCCESS":
                slow_print("  'Welcome to the AlgoCratic Futures™ Beta Preview Experience.'")
                slow_print("  'What you're seeing today represents our leading-edge innovation pipeline.'")
                slow_print("  'Bugs are features. Features are aspirational.'")
                slow_print("  The client takes notes. They repost this as a quote.")
                slow_print("  'Bugs are features.' They love it.")
                slow_print("  You have accidentally created a brand position.")
                player["objective_complete"] = True
                gain_loyalty(player, "Unplanned brand position approved by NOC after the fact")
            else:
                slow_print("  The client is not a first-time client.")
                slow_print("  They have been a 'beta preview experience' before.")
                slow_print("  Last quarter. And the quarter before that.")
                slow_print("  They have a folder labeled 'AEC promises by date.'")
                slow_print("  The folder is thick.")
                lose_loyalty(player, "Client documented the pattern")
                lose_sanity(player, "They have a folder")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The client has arrived early. It is 09:08.")
        slow_print("  The demo environment shows a 'System Initializing' screen.")
        slow_print("  It has shown this screen for eleven minutes.")
        slow_print("  The client is smiling. Their smile is professional.")
        slow_print("  The smile contains information.")
        print()
        print("  What do you do?")
        print("  [1] Announce a 'brief technical pause' and call anyone who will answer")
        print("  [2] Present your business card and pivot to 'next steps' conversation")
        print("  [3] Excuse yourself for 'final environment checks' — find help fast")
        print("  [4] Use an inventory item")
        choice = get_choice(4)

        if choice == 1:
            result = algorithm_decides(player, "engagement", "emergency technical support call")
            if result == "SUCCESS":
                slow_print("  ICD answers. ICD always answers eventually.")
                slow_print("  ICD fixes the environment in six minutes.")
                slow_print("  ICD does not speak to the client.")
                slow_print("  ICD does not want credit. ICD wants this to be over.")
                slow_print("  The demo proceeds.")
                player["objective_complete"] = True
            else:
                slow_print("  Nobody answers.")
                slow_print("  You are playing hold music.")
                slow_print("  The hold music is a recorded message from The Algorithm.")
                slow_print("  The client is listening to The Algorithm's hold message.")
                slow_print("  The hold message is eight minutes long.")
                lose_sanity(player, "The client is listening to The Algorithm")

        elif choice == 2:
            result = algorithm_decides(player, "presence", "pivot to strategic conversation")
            if result == "SUCCESS":
                slow_print("  You pivot masterfully.")
                slow_print("  'The environment is running a final optimization cycle.'")
                slow_print("  'While it completes, let's discuss your Q4 objectives.'")
                slow_print("  The client has Q4 objectives. Everyone has Q4 objectives.")
                slow_print("  You discuss them for twenty minutes.")
                slow_print("  By the time you're done, the environment has fixed itself.")
                slow_print("  Or given up and displayed a success screen. You don't check which.")
                player["objective_complete"] = True
                gain_loyalty(player, "Successfully reframed a failure as a relationship moment")
            else:
                slow_print("  The client does not have Q4 objectives.")
                slow_print("  The client has a Q4 audit.")
                slow_print("  The audit is of AEC's performance this year.")
                slow_print("  The client is the auditor.")
                slow_print("  You did not know this.")
                slow_print("  The business card you just handed them lists a title you don't have.")
                lose_loyalty(player, "Misidentified auditor as client")
                lose_sanity(player, "The client is the auditor")

        elif choice == 3:
            slow_print("  You excuse yourself.")
            result = algorithm_decides(player, "initiative", "finding emergency help")
            if result == "SUCCESS":
                slow_print("  You find a GRAY operative in the corridor.")
                slow_print("  GRAY does not fix technical problems.")
                slow_print("  GRAY reviews the demo interface and marks three brand compliance issues.")
                slow_print("  While GRAY is marking issues, a maintenance update completes.")
                slow_print("  The environment starts working. Brand compliance issues and all.")
                slow_print("  GRAY has opinions. The client is satisfied.")
                slow_print("  GRAY's opinions are filed for later.")
                player["objective_complete"] = True
            else:
                slow_print("  You find an HCO operative who wants to know how you're doing.")
                slow_print("  You are not doing well. You say you are doing well.")
                slow_print("  HCO schedules a follow-up wellness check.")
                slow_print("  You return to the demo room.")
                slow_print("  The client has left. They left a note.")
                slow_print("  The note says: 'We'll be in touch.'")
                slow_print("  The note does not clarify the nature of the touch.")
                lose_loyalty(player, "Client departed during unattended demo")

        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

# --- ABBREVIATED SCENES FOR CIO, RAR, HCO, TAM, GRAY ---
# Full scene structure — 2 meaningful choices per operative per round

def _cio_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  You have seven conflicting facility requests for 09:00.")
        slow_print("  You have one truck. This is always the situation.")
        slow_print("  Two requests are physically impossible simultaneously.")
        slow_print("  Request A: Move the Floor 5 presentation equipment to Floor 3.")
        slow_print("  Request B: Move the Floor 3 breakroom furniture to Floor 5.")
        slow_print("  These are the same furniture. Going in opposite directions.")
        print()
        print("  What do you do?")
        print("  [1] Fulfill Request A — Floor 5 presentation takes priority")
        print("  [2] Fulfill Request B — Floor 3 is structurally more urgent")
        print("  [3] Declare a logistics conflict and file for arbitration")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "compliance", "priority logistics decision")
            if result == "SUCCESS":
                slow_print("  Floor 5 equipment is moved. Request A fulfilled.")
                slow_print("  Request B filer has not yet noticed.")
                slow_print("  You are moving very quickly and hoping.")
            else:
                slow_print("  The elevator is out of service. There is only the stairwell.")
                slow_print("  The furniture does not fit in the stairwell.")
                slow_print("  You have known this for years.")
                lose_sanity(player, "Logistics physics were always going to be a problem")
        elif choice == 2:
            result = algorithm_decides(player, "initiative", "alternative priority assessment")
            if result == "SUCCESS":
                slow_print("  Floor 3 is fulfilled. The breakroom is operational.")
                slow_print("  Request A filer has called twice. You have not answered.")
                slow_print("  This is a choice you are comfortable with.")
                gain_loyalty(player, "Decisive logistics call under impossible conditions")
            else:
                slow_print("  Request B furniture was already moved by a different team.")
                slow_print("  By AEC. Without authorization. Without telling anyone.")
                slow_print("  The furniture is in the wrong configuration.")
                slow_print("  AEC is not available to explain.")
                lose_sanity(player, "AEC executed a logistics request that was yours to execute")
        elif choice == 3:
            slow_print("  You file a Logistics Conflict Notice (Form L-3).")
            slow_print("  Arbitration requires CAB. CAB is in Room 7-C.")
            slow_print("  Nobody is going to Room 7-C.")
            result = algorithm_decides(player, "endurance", "waiting for arbitration that won't come")
            if result == "SUCCESS":
                slow_print("  While waiting, you resolve three of the five other requests.")
                slow_print("  Progress through adjacent action.")
                gain_loyalty(player, "Partial completion under arbitration hold")
            else:
                slow_print("  Nothing resolves. Four requests are now overdue.")
                slow_print("  Each overdue request generates a notification.")
                slow_print("  You have twenty-two notifications.")
                lose_sanity(player, "Twenty-two notifications")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        print()
        slow_print("  Five of seven requests are partially addressed.")
        slow_print("  The remaining two conflict with each other and with physics.")
        slow_print("  You have the clipboard. The clipboard knows where everything is.")
        slow_print("  The clipboard is accurate. The situation is less so.")
        print()
        print("  What do you do?")
        print("  [1] Consult the clipboard and find a third path between the two requests")
        print("  [2] Invoke The One Truck — declare one resource physically unavailable")
        print("  [3] Escalate to The Algorithm for priority guidance")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "competence", "creative logistics solution")
            if result == "SUCCESS":
                slow_print("  The clipboard reveals a storage room on Floor 2.")
                slow_print("  A temporary staging solution. Neither request is fully fulfilled.")
                slow_print("  Both requesters are told the other took priority.")
                slow_print("  This is not accurate. It is logistically necessary.")
                slow_print("  You will note the distinction in your report.")
                slow_print("  The distinction will not survive the report.")
                player["objective_complete"] = True
            else:
                slow_print("  The storage room is locked. The key is on the truck.")
                slow_print("  The truck is fulfilling Request C.")
                lose_sanity(player, "The solution requires the resource that is solving a different problem")
        elif choice == 2:
            slow_print("  You invoke The One Truck.")
            slow_print("  Request B is declared unfulfillable — resource allocated elsewhere.")
            slow_print("  This is true. The truck is allocated elsewhere.")
            slow_print("  The truck was allocated elsewhere before Request B was filed.")
            slow_print("  CIO is aware. CIO has always been aware.")
            result = algorithm_decides(player, "compliance", "logistics authority invocation")
            if result == "SUCCESS":
                slow_print("  Request B is formally deferred. Request A proceeds.")
                slow_print("  The One Truck completes Request A at 08:59.")
                slow_print("  The clipboard is satisfied. CIO is satisfied.")
                slow_print("  These are related.")
                player["objective_complete"] = True
            else:
                slow_print("  Request B was filed by INDIGO clearance.")
                slow_print("  The One Truck cannot be invoked against INDIGO requests.")
                slow_print("  You did not know this. You know it now.")
                lose_loyalty(player, "The One Truck invoked against INDIGO — notation added")
        elif choice == 3:
            algorithm_speak("The Algorithm recommends: prioritize by submission timestamp.")
            algorithm_speak("Request A was submitted 3 minutes before Request B.")
            algorithm_speak("Request A takes priority.")
            algorithm_speak("Request A has already been partially fulfilled.")
            algorithm_speak("This is noted.")
            result = algorithm_decides(player, "endurance", "following Algorithm guidance")
            if result == "SUCCESS":
                slow_print("  You complete Request A. The Algorithm's guidance was useful.")
                slow_print("  The Algorithm's guidance is always useful.")
                slow_print("  This is not a statement you have verified empirically.")
                player["objective_complete"] = True
            else:
                slow_print("  Request A equipment is now in transit.")
                slow_print("  Transit takes longer than the deadline.")
                slow_print("  The Algorithm did not account for stairwell width.")
                lose_sanity(player, "The Algorithm did not account for stairwell width")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

def _rar_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  The Q3 expense reconciliation has a $40,000 discrepancy.")
        slow_print("  The discrepancy resolves if Form R-40K reaches Floor 4 Accounting Terminal.")
        slow_print("  The form requires a signature from the Q3 Budget Approver.")
        slow_print("  The Q3 Budget Approver is listed as: DEPRECATED.")
        slow_print("  Their iteration ended in Q2. Before Q3 began.")
        slow_print("  They approved a Q3 budget before Q3 existed.")
        slow_print("  The numbers are correct. The timeline is incorrect.")
        print()
        print("  What do you do?")
        print("  [1] Sign the form yourself — the numbers support the action")
        print("  [2] Locate the DEPRECATED operative's previous signature to duplicate")
        print("  [3] Declare the $40,000 a rounding adjustment — within RAR authority")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "compliance", "unauthorized signature")
            if result == "SUCCESS":
                slow_print("  The signature is accepted. The numbers reconcile.")
                slow_print("  An audit flag is generated for the signature.")
                slow_print("  The audit will review the signature's authority.")
                slow_print("  By the time the audit completes, Q4 will have its own discrepancy.")
                slow_print("  This is not a solution. It is a deferral.")
                slow_print("  In accounting, these are the same thing.")
                player["objective_complete"] = True
                lose_loyalty(player, "Unauthorized signature — audit flag generated")
            else:
                slow_print("  The signature is rejected. The system requires the original signatory.")
                slow_print("  The original signatory is DEPRECATED.")
                slow_print("  The system has a field for DEPRECATED status.")
                slow_print("  The field is filled in.")
                slow_print("  The system still requires the signature.")
                slow_print("  The system is aware of the contradiction.")
                slow_print("  The system does not care.")
                lose_sanity(player, "The system knows it's asking for the impossible and continues")
        elif choice == 2:
            result = algorithm_decides(player, "competence", "signature recovery")
            if result == "SUCCESS":
                slow_print("  A Q2 form in archives has the DEPRECATED operative's signature.")
                slow_print("  You digitize it. You apply it to Form R-40K.")
                slow_print("  This is embellishment. In accounting.")
                slow_print("  The numbers are correct. The process is also correct.")
                slow_print("  The mechanism is less correct.")
                slow_print("  RAR's two spreadsheets now both agree.")
                player["objective_complete"] = True
                lose_loyalty(player, "Signature recovery method is technically embellishment")
            else:
                slow_print("  The DEPRECATED operative's signatures are archived above your clearance.")
                slow_print("  Their records are sealed.")
                slow_print("  Their records are sealed because they were REDACTED, not just DEPRECATED.")
                slow_print("  These are different. You have learned this now.")
                lose_sanity(player, "The operative was REDACTED. The distinction is significant.")
        elif choice == 3:
            result = algorithm_decides(player, "compliance", "rounding authority invocation")
            if result == "SUCCESS":
                slow_print("  $40,000 is declared a rounding adjustment.")
                slow_print("  This requires supporting calculation.")
                slow_print("  The calculator produces a supporting calculation.")
                slow_print("  The calculation is correct. By definition.")
                slow_print("  The discrepancy is closed.")
                slow_print("  The numbers are correct. The numbers are always correct.")
                player["objective_complete"] = True
                gain_loyalty(player, "Creative reconciliation executed within RAR authority")
            else:
                slow_print("  $40,000 exceeds the rounding authority threshold.")
                slow_print("  The threshold is $39,999.")
                slow_print("  This threshold is documented in a policy updated last week.")
                slow_print("  The policy was updated retroactively to Q1.")
                slow_print("  This is not illegal. This is accounting.")
                lose_sanity(player, "Policy updated retroactively to close the gap RAR was using")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The form is still unsigned. The terminal is waiting.")
        slow_print("  An HCO operative stops you in the corridor.")
        slow_print("  They want to know how you're doing.")
        slow_print("  You are not doing well. The $40,000 remains.")
        print()
        print("  What do you do?")
        print("  [1] Answer HCO's wellness check honestly — spend the time, get the support")
        print("  [2] Deflect professionally — you're fine, everything's fine, proceed")
        print("  [3] Use the wellness check as cover to reach the terminal faster")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            slow_print("  You tell HCO about the discrepancy. HCO listens.")
            slow_print("  HCO is not able to fix the discrepancy.")
            slow_print("  HCO offers a SMILE™ tablet.")
            result = algorithm_decides(player, "endurance", "honest disclosure to HCO")
            if result == "SUCCESS":
                slow_print("  HCO's lanyard contains a Floor 4 access badge.")
                slow_print("  HCO doesn't know which one it is. HCO lets you try them.")
                slow_print("  One works. You reach the terminal.")
                slow_print("  The form is submitted without a valid signature.")
                slow_print("  The numbers reconcile. The process is noted.")
                player["objective_complete"] = True
            else:
                slow_print("  HCO schedules a follow-up session.")
                slow_print("  The session is during your deadline window.")
                slow_print("  You now have a conflict in your calendar.")
                slow_print("  The calendar conflict has been documented.")
                lose_loyalty(player, "Calendar conflict created by mandatory optional wellness session")
        elif choice == 2:
            result = algorithm_decides(player, "presence", "professional deflection")
            if result == "SUCCESS":
                slow_print("  'I'm doing great. Everything is great. The numbers are correct.'")
                slow_print("  HCO nods. HCO knows the numbers are not correct.")
                slow_print("  HCO will not mention this.")
                slow_print("  You proceed to the terminal.")
                player["objective_complete"] = True
            else:
                slow_print("  HCO has reviewed your recent loyalty score.")
                slow_print("  HCO knows you are not doing great.")
                slow_print("  HCO initiates a mandatory wellness assessment.")
                slow_print("  The assessment takes twelve minutes.")
                slow_print("  The terminal closes for maintenance at 09:00.")
                lose_sanity(player, "Mandatory wellness assessment during the only available window")
        elif choice == 3:
            result = algorithm_decides(player, "initiative", "using wellness check as cover")
            if result == "SUCCESS":
                slow_print("  You route the wellness conversation through the Floor 4 corridor.")
                slow_print("  HCO follows, still asking questions.")
                slow_print("  You answer while walking. You reach the terminal.")
                slow_print("  You submit the form mid-sentence.")
                slow_print("  HCO considers this the most efficient wellness check they've done.")
                slow_print("  HCO notes your efficiency. The Algorithm notes HCO's notation.")
                player["objective_complete"] = True
            else:
                slow_print("  HCO does not move. HCO has a designated wellness space.")
                slow_print("  The wellness space is not near the terminal.")
                slow_print("  HCO is patient. HCO can wait.")
                slow_print("  The deadline cannot.")
                lose_loyalty(player, "Attempted to redirect mandatory wellness check — noted")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

def _hco_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  The Mandatory Alignment Celebration starts at 09:00.")
        slow_print("  It is in the Floor 3 Atrium.")
        slow_print("  The Floor 3 Atrium is currently occupied by three operatives")
        slow_print("  doing completely different things for completely different reasons.")
        slow_print("  SMILE™ has been delivered to the Atrium. It is already there.")
        slow_print("  The SMILE™ is unattended.")
        slow_print("  This is concerning.")
        print()
        print("  What do you do?")
        print("  [1] Secure the SMILE™ and begin notifying operatives to attend")
        print("  [2] Issue a mandatory wellness check to clear the Atrium first")
        print("  [3] Reframe the existing Atrium activity as part of the Celebration")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "engagement", "atrium coordination")
            if result == "SUCCESS":
                slow_print("  The SMILE™ is secured. Notifications go out.")
                slow_print("  Three operatives receive mandatory attendance notices.")
                slow_print("  Two respond. One does not have time to respond.")
                slow_print("  The one who does not respond has noted the notification.")
                slow_print("  Noting is sufficient for compliance purposes.")
                slow_print("  The Celebration proceeds with two confirmed attendees and one notation.")
                player["objective_complete"] = True
                gain_loyalty(player, "Celebration executed within compliance parameters")
            else:
                slow_print("  The SMILE™ tablets have already been distributed.")
                slow_print("  By an operative who found them unattended.")
                slow_print("  All of them. To themselves.")
                slow_print("  The operative is having an extremely compliant morning.")
                slow_print("  HCO has concerns about the consumption rate.")
                lose_sanity(player, "The SMILE™ is gone. The Celebration has no centerpiece.")
        elif choice == 2:
            result = algorithm_decides(player, "persistence", "mandatory wellness clearance")
            if result == "SUCCESS":
                slow_print("  Wellness checks issued to three Atrium occupants.")
                slow_print("  Two comply immediately. One files a scope dispute.")
                slow_print("  The scope dispute is with SDC. SDC and HCO regard each other.")
                slow_print("  This has happened before. SDC always eventually complies.")
                slow_print("  The Atrium clears. The Celebration begins.")
                player["objective_complete"] = True
                for p in players:
                    if p["department"] == "SDC":
                        lose_loyalty(p, "Forced out of work area by HCO wellness check")
            else:
                slow_print("  One operative's wellness check reveals active distress indicators.")
                slow_print("  HCO protocol requires extended support for active distress.")
                slow_print("  Extended support takes forty-five minutes minimum.")
                slow_print("  The Celebration is in forty-five minutes.")
                slow_print("  HCO will be busy until the Celebration is over.")
                slow_print("  The operative, at least, feels heard.")
                lose_sanity(player, "Proper protocol execution prevents event execution")
        elif choice == 3:
            result = algorithm_decides(player, "presence", "inclusive event reframing")
            if result == "SUCCESS":
                slow_print("  'What you're seeing in the Atrium right now'")
                slow_print("  'is our Alignment Celebration in its organic phase.'")
                slow_print("  'Operatives engaging authentically with their work'")
                slow_print("  'is the truest form of celebration we can offer.'")
                slow_print("  HCO sends this to the organization-wide channel.")
                slow_print("  Three operatives who were stressed are now officially celebrating.")
                slow_print("  The Algorithm approves this message.")
                slow_print("  The Algorithm's approval is noted in the Celebration record.")
                player["objective_complete"] = True
                gain_loyalty(player, "Organic Celebration messaging approved by The Algorithm")
            else:
                slow_print("  GRAY reviews the communication before it sends.")
                slow_print("  GRAY marks four brand compliance issues.")
                slow_print("  The communication is returned for revision.")
                slow_print("  The revision takes longer than the Celebration window.")
                slow_print("  The Celebration has technically already occurred without the communication.")
                slow_print("  This is documented as a compliance gap.")
                lose_loyalty(player, "Celebration communication held for brand compliance revision")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The Celebration has not started. It is 08:52.")
        slow_print("  You have received seventeen responses to the attendance notification.")
        slow_print("  Fifteen say they cannot attend. One is out of office.")
        slow_print("  One says: 'I don't know what this is but I'm in the Atrium anyway.'")
        slow_print("  That operative is your Celebration.")
        print()
        print("  What do you do?")
        print("  [1] Celebrate with the one operative who showed up — document it as full attendance")
        print("  [2] Issue a second mandatory notification — this time with consequences")
        print("  [3] Escalate to The Algorithm for attendance enforcement")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "compliance", "minimum viable celebration")
            if result == "SUCCESS":
                slow_print("  The Celebration is documented with full attendance.")
                slow_print("  Full attendance is defined as all operatives who attended.")
                slow_print("  One attended. One is full.")
                slow_print("  The documentation uses a photo from a previous Celebration.")
                slow_print("  This is standard practice. HCO does not comment on the photo.")
                slow_print("  The Algorithm does not audit Celebration photos.")
                slow_print("  This has been tested.")
                player["objective_complete"] = True
            else:
                slow_print("  The one operative who attended has just left.")
                slow_print("  They had somewhere to be.")
                slow_print("  The Celebration has zero attendees.")
                slow_print("  HCO is the only one in the Atrium.")
                slow_print("  HCO is technically attending their own Celebration.")
                slow_print("  This has never happened before. The documentation doesn't cover it.")
                lose_sanity(player, "HCO attended HCO's Celebration alone")
        elif choice == 2:
            result = algorithm_decides(player, "persistence", "consequence-bearing notification")
            if result == "SUCCESS":
                slow_print("  The second notification includes 'mandatory' twice.")
                slow_print("  Four additional operatives attend.")
                slow_print("  They are resentful. They are compliant. These are the same.")
                slow_print("  The Celebration has five attendees. HCO considers this a success.")
                slow_print("  The attendees do not consider this a success.")
                slow_print("  Their considerations are not documented.")
                player["objective_complete"] = True
            else:
                slow_print("  The second notification triggers CAB.")
                slow_print("  CAB notes that mandatory attendance without formal policy support")
                slow_print("  constitutes a compliance violation.")
                slow_print("  HCO has created a compliance violation in pursuit of an event")
                slow_print("  designed to promote compliance.")
                slow_print("  CAB is going to enjoy filing this one.")
                lose_loyalty(player, "Compliance violation created by compliance-adjacent event")
        elif choice == 3:
            algorithm_speak("The Algorithm has reviewed attendance records.")
            algorithm_speak("Attendance is noted. Non-attendance is noted.")
            algorithm_speak("Both are data points. Data points inform optimization.")
            algorithm_speak("The Algorithm does not mandate attendance.")
            algorithm_speak("The Algorithm mandates compliance.")
            algorithm_speak("Compliance includes acknowledging mandatory events.")
            algorithm_speak("Attendance and acknowledgment are different columns in the same spreadsheet.")
            algorithm_speak("The spreadsheet is accurate.")
            result = algorithm_decides(player, "engagement", "Algorithm-assisted attendance")
            if result == "SUCCESS":
                slow_print("  The Algorithm's message is forwarded to all operatives.")
                slow_print("  Six more attend. They are unsure why.")
                slow_print("  HCO considers this sufficient.")
                player["objective_complete"] = True
            else:
                slow_print("  The Algorithm's message constitutes a new directive.")
                slow_print("  The directive must be processed through official channels.")
                slow_print("  Official channel processing takes two business days.")
                slow_print("  The Celebration window has closed.")
                lose_sanity(player, "The Algorithm's directive arrived too late via official channels")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

def _tam_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  The overnight access log anomaly points to three departments.")
        slow_print("  ICD, SDC, and one that is {REDACTED} in your own report.")
        slow_print("  You wrote this report. You redacted that entry yourself.")
        slow_print("  You do not remember why.")
        slow_print("  The pattern suggests someone accessed Sub-Level 2 at 03:00.")
        slow_print("  Sub-Level 2 contains the Infrastructure Terminal.")
        slow_print("  And Bob's original code.")
        slow_print("  Bob is {REDACTED}.")
        print()
        print("  What do you do?")
        print("  [1] Secure Sub-Level 2 and interview ICD and SDC operatives")
        print("  [2] Pull the security footage — someone was physically present")
        print("  [3] File the report now with what you have — deadline matters more")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "persistence", "multi-department interview")
            if result == "SUCCESS":
                slow_print("  ICD operative: 'I was home. The system logs my badge remotely sometimes.'")
                slow_print("  SDC operative: 'That's the bug I've been trying to fix.'")
                slow_print("  You regard the SDC operative.")
                slow_print("  The SDC operative regards you.")
                slow_print("  'The bug that makes it look like someone is somewhere they're not?'")
                slow_print("  'Yes,' says SDC.")
                slow_print("  'Then the anomaly—'")
                slow_print("  'Is probably the bug,' says SDC.")
                slow_print("  'Or it's masking someone who was actually there,' says TAM.")
                slow_print("  You file both conclusions. One is correct. You don't know which.")
                player["objective_complete"] = True
                gain_loyalty(player, "Thorough investigation with documented conclusions")
            else:
                slow_print("  Both operatives decline to answer without counsel from CAB.")
                slow_print("  CAB requires 48 hours notice to provide interview counsel.")
                slow_print("  The briefing is in 8 minutes.")
                slow_print("  You will present your report with no additional information.")
                slow_print("  The report will reflect this accurately.")
                slow_print("  TAM's reports always reflect everything accurately.")
                slow_print("  This is not always comfortable for anyone.")
                lose_sanity(player, "A thorough investigation produced nothing usable in time")
        elif choice == 2:
            result = algorithm_decides(player, "competence", "security footage review")
            if result == "SUCCESS":
                slow_print("  The footage shows Sub-Level 2 at 03:00.")
                slow_print("  The footage shows a door. The door is closed.")
                slow_print("  For six hours, the footage shows only the door.")
                slow_print("  Then the door opens.")
                slow_print("  Three people walk out.")
                slow_print("  You do not recognize any of them.")
                slow_print("  You recognize all of them.")
                slow_print("  You file the footage as evidence without comment.")
                player["objective_complete"] = True
                lose_sanity(player, "You recognized people you should not know")
            else:
                slow_print("  The footage is classified above your clearance.")
                slow_print("  TAM has classified its own security footage.")
                slow_print("  A previous iteration of you classified it.")
                slow_print("  You do not remember classifying it.")
                slow_print("  The classification was made for good reason.")
                slow_print("  The reason is also classified.")
                lose_sanity(player, "A previous iteration protected you from this information")
        elif choice == 3:
            result = algorithm_decides(player, "compliance", "incomplete report submission")
            if result == "SUCCESS":
                slow_print("  The report is filed with available information.")
                slow_print("  Available information is: an anomaly exists. Source unknown.")
                slow_print("  'Source Unknown' is a TAM conclusion. It is filed as such.")
                slow_print("  The briefing accepts this. 'Source Unknown' is progress.")
                slow_print("  Progress is measured relative to starting point.")
                slow_print("  The starting point was also 'Source Unknown.'")
                slow_print("  Nobody mentions this.")
                player["objective_complete"] = True
            else:
                slow_print("  The briefing requires a preliminary source identification.")
                slow_print("  'Unknown' does not satisfy this requirement.")
                slow_print("  The report is returned.")
                slow_print("  For revision.")
                slow_print("  The revision deadline is 09:00.")
                slow_print("  It is 08:58.")
                lose_loyalty(player, "Report returned for lacking preliminary source identification")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The briefing is in six minutes. You have a report with gaps.")
        slow_print("  The gaps are: who, why, and what they found.")
        slow_print("  The fact that they were there is documented.")
        slow_print("  What 'there' contains is the part that concerns you.")
        print()
        print("  What do you do?")
        print("  [1] Classify the concerning portions — report the frame, not the content")
        print("  [2] Present the footage conclusions — even the ones you can't explain")
        print("  [3] Delay the briefing — more investigation time needed")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "compliance", "strategic classification")
            if result == "SUCCESS":
                slow_print("  You classify Sub-Level 2 footage findings.")
                slow_print("  The briefing receives: 'Source identified. Details classified above briefing clearance.'")
                slow_print("  The briefing accepts this. Classified conclusions are conclusions.")
                slow_print("  TAM has done its job. The rest is above pay grade.")
                slow_print("  The rest is always above pay grade.")
                player["objective_complete"] = True
                gain_loyalty(player, "Responsible classification of sensitive findings")
            else:
                slow_print("  The briefing contains INDIGO clearance observers.")
                slow_print("  Classified findings are unclassified for INDIGO automatically.")
                slow_print("  The INDIGO observers read your findings.")
                slow_print("  They look at each other.")
                slow_print("  They do not look at you.")
                slow_print("  This is more frightening than if they had.")
                lose_sanity(player, "INDIGO clearance observers read classified findings and said nothing")
        elif choice == 2:
            result = algorithm_decides(player, "persistence", "full disclosure briefing")
            if result == "SUCCESS":
                slow_print("  You present the footage. The door. The six hours. The three people.")
                slow_print("  You present your recognition of people you should not know.")
                slow_print("  The briefing room is quiet for a long time.")
                slow_print("  'Thank you, TAM,' someone says.")
                slow_print("  'This will be handled.'")
                slow_print("  'Handled' is not defined.")
                slow_print("  You have done your job. The job is done.")
                player["objective_complete"] = True
            else:
                slow_print("  The briefing interrupts you at the third minute.")
                slow_print("  'This has already been addressed.'")
                slow_print("  'What you're describing is a known and resolved matter.'")
                slow_print("  'Your report will be filed.'")
                slow_print("  'Your report will be filed in a location you will not access.'")
                slow_print("  The briefing ends early.")
                lose_sanity(player, "The briefing already knew. The briefing was always going to know.")
        elif choice == 3:
            slow_print("  You request a briefing delay.")
            result = algorithm_decides(player, "initiative", "briefing delay request")
            if result == "SUCCESS":
                slow_print("  The briefing is delayed fifteen minutes.")
                slow_print("  Fifteen minutes produces: two additional anomaly sources,")
                slow_print("  one classified document that shouldn't exist,")
                slow_print("  and a question you will not be able to un-ask.")
                slow_print("  You file the report. It is thorough.")
                slow_print("  Thorough is not always better. In this case it is better.")
                player["objective_complete"] = True
            else:
                slow_print("  The briefing cannot be delayed.")
                slow_print("  The briefing has attendees above INDIGO clearance.")
                slow_print("  You present your incomplete report to people who already know.")
                slow_print("  Everyone smiles. Everyone waits for you to finish.")
                slow_print("  You finish. You leave.")
                slow_print("  You do not know what you just reported to.")
                lose_sanity(player, "Reported to unknown clearance. They were patient about it.")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

def _gray_scene(player, scene_num):
    show_player_status(player)
    if scene_num == 1:
        print()
        slow_print("  Three documents are in circulation with brand compliance violations.")
        slow_print("  You can see all three. You always see violations.")
        slow_print("  Document A: NOC's Brand Compliance Report — incorrect typeface in footer.")
        slow_print("  Document B: CAB's DENIED ruling — stamp is 3° off-center.")
        slow_print("  Document C: AEC's client presentation — uses a deprecated color value.")
        slow_print("  You must intercept at least two before 09:00.")
        slow_print("  Each interception requires the document's author to be notified.")
        slow_print("  Authors rarely enjoy notification.")
        print()
        print("  What do you do?")
        print("  [1] Intercept Document A and B — both reachable via your lateral movement")
        print("  [2] Intercept Document A and C — NOC and AEC are on the same floor")
        print("  [3] Issue a blanket hold on all three — one action, full coverage")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "competence", "dual interception — A and B")
            if result == "SUCCESS":
                slow_print("  You reach NOC. You mark the footer. NOC accepts the revision.")
                slow_print("  You reach CAB. You mark the stamp deviation.")
                slow_print("  CAB looks at the stamp. CAB has noticed.")
                slow_print("  CAB has always noticed. CAB was waiting to see if you noticed.")
                slow_print("  You have. CAB respects this.")
                slow_print("  CAB revises the document without comment.")
                slow_print("  Two documents intercepted. Brand compliance maintained.")
                player["objective_complete"] = True
                for p in players:
                    if p["department"] == "NOC":
                        lose_loyalty(p, "GRAY compliance revision required before submission")
                    if p["department"] == "CAB":
                        gain_loyalty(p, "CAB accepted GRAY revision professionally — noted")
            else:
                slow_print("  CAB declines GRAY's revision.")
                slow_print("  'The stamp deviation is within acceptable parameters.'")
                slow_print("  'Parameters defined by CAB.'")
                slow_print("  'CAB defines parameters.'")
                slow_print("  'This is not subject to brand review.'")
                slow_print("  It is subject to brand review. GRAY has authority over brand.")
                slow_print("  CAB knows this. CAB is testing.")
                slow_print("  GRAY files an escalation. Escalation takes two business days.")
                lose_loyalty(player, "CAB contested GRAY authority — escalation pending")
        elif choice == 2:
            result = algorithm_decides(player, "lateral", "floor-based interception strategy")
            if result == "SUCCESS":
                slow_print("  You intercept NOC's footer. Revision accepted.")
                slow_print("  You reach AEC's presentation.")
                slow_print("  AEC's deprecated color value is Pantone 485 C.")
                slow_print("  Pantone 485 C was deprecated in the brand refresh.")
                slow_print("  AEC does not know about the brand refresh.")
                slow_print("  AEC was not in the meeting where it was discussed.")
                slow_print("  Nobody told AEC. This was partly intentional.")
                slow_print("  You revise the color. AEC thanks you.")
                slow_print("  AEC does not understand why. AEC thanks you anyway.")
                slow_print("  This is fine.")
                player["objective_complete"] = True
            else:
                slow_print("  AEC's presentation has already been sent to the client.")
                slow_print("  The deprecated color value is in the client's inbox.")
                slow_print("  The client has a design team.")
                slow_print("  The design team will notice.")
                slow_print("  The design team has noticed.")
                slow_print("  The design team has already replied.")
                slow_print("  Their reply uses the correct color.")
                slow_print("  The client is correcting GRAY's territory.")
                lose_sanity(player, "A client's design team corrected a brand violation before GRAY could")
        elif choice == 3:
            result = algorithm_decides(player, "competence", "blanket compliance hold")
            if result == "SUCCESS":
                slow_print("  Blanket hold issued. All three documents paused.")
                slow_print("  All three authors are notified simultaneously.")
                slow_print("  NOC: immediately begins revision.")
                slow_print("  CAB: requests clarification on scope of hold authority.")
                slow_print("  AEC: did not receive the notification. Out of office. Auto-reply.")
                slow_print("  Two of three revisions complete before 09:00.")
                slow_print("  AEC's is still on hold. AEC is still out of office.")
                slow_print("  AEC is never fully in office.")
                player["objective_complete"] = True
            else:
                slow_print("  The blanket hold requires countersignature from INDIGO.")
                slow_print("  INDIGO clearance is not available at this hour.")
                slow_print("  INDIGO clearance is available when INDIGO decides it's available.")
                slow_print("  INDIGO has not decided.")
                slow_print("  All three documents continue circulating.")
                lose_loyalty(player, "Blanket hold rejected — INDIGO countersignature required")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 2:
        if player["objective_complete"]:
            _resolution_scene(player)
            return True
        print()
        slow_print("  The third document is still in circulation.")
        slow_print("  Also: a fourth document has appeared. You did not anticipate this.")
        slow_print("  Document D is from TAM. TAM's incident report uses a non-standard typeface.")
        slow_print("  TAM uses Courier New. Brand guidelines specify Courier Prime.")
        slow_print("  These are different fonts. TAM does not agree they are different fonts.")
        slow_print("  You have had this conversation before.")
        print()
        print("  What do you do?")
        print("  [1] Invoke Brand Authority — TAM's report cannot be filed in Courier New")
        print("  [2] Accept Document D as-is — pick your battles, reach the third document")
        print("  [3] Demonstrate the difference between Courier New and Courier Prime to TAM")
        print("  [4] Use an inventory item")
        choice = get_choice(4)
        if choice == 1:
            result = algorithm_decides(player, "competence", "brand authority invocation — TAM")
            if result == "SUCCESS":
                slow_print("  'Courier Prime is the standard. This is documented.'")
                slow_print("  TAM reviews the documentation.")
                slow_print("  TAM does not acknowledge the documentation.")
                slow_print("  TAM resubmits in Courier Prime.")
                slow_print("  The resubmission contains a compliance notation about GRAY.")
                slow_print("  The notation is in Courier Prime.")
                slow_print("  GRAY accepts this as progress.")
                player["objective_complete"] = True
            else:
                slow_print("  TAM classifies the brand guideline document.")
                slow_print("  The guideline specifying Courier Prime is now classified.")
                slow_print("  TAM's report in Courier New is no longer technically non-compliant.")
                slow_print("  Because the standard it violates is classified.")
                slow_print("  The standard TAM is violating no longer officially exists.")
                slow_print("  This is the most efficient outcome TAM has achieved this quarter.")
                lose_sanity(player, "TAM classified the evidence of TAM's own violation")
        elif choice == 2:
            result = algorithm_decides(player, "initiative", "strategic acceptance")
            if result == "SUCCESS":
                slow_print("  You accept Courier New. You note it in the file.")
                slow_print("  You reach the third original document.")
                slow_print("  The third document has already been revised by the author.")
                slow_print("  The revision introduced two new violations.")
                slow_print("  You revise those.")
                slow_print("  The document is now compliant.")
                slow_print("  The document has been through four drafts.")
                slow_print("  This is a GRAY document. Four drafts is progress.")
                player["objective_complete"] = True
            else:
                slow_print("  The third document reached its destination during your Courier New decision.")
                slow_print("  It was received. It was opened. The violation is now the client's problem.")
                slow_print("  The client has a design team.")
                slow_print("  This is the second time today the client's design team has encountered this.")
                lose_sanity(player, "The client's design team is becoming familiar with AlgoCratic Futures™ brand failures")
        elif choice == 3:
            slow_print("  You open both fonts side by side.")
            algorithm_pause(1)
            slow_print("  Courier New: slightly thinner stroke, different period spacing.")
            slow_print("  Courier Prime: optimized for screen, improved punctuation rendering.")
            slow_print("  TAM looks at both for a long time.")
            result = algorithm_decides(player, "competence", "font education for TAM")
            if result == "SUCCESS":
                slow_print("  'I see it,' TAM says.")
                slow_print("  'I don't care,' TAM adds.")
                slow_print("  'But I see it.'")
                slow_print("  TAM resubmits in Courier Prime without further comment.")
                slow_print("  TAM now checks fonts before filing. TAM will never admit this.")
                player["objective_complete"] = True
                gain_loyalty(player, "Changed a behavior through demonstration — rare")
            else:
                slow_print("  TAM looks at both fonts.")
                slow_print("  'These are the same font.'")
                slow_print("  'They are not the same font.'")
                slow_print("  'They look the same to me.'")
                slow_print("  'They are structurally distinct at the glyph level.'")
                slow_print("  TAM files a security concern about GRAY's font fixation.")
                slow_print("  The concern is in Courier New.")
                lose_sanity(player, "TAM filed a report about your font concern in the wrong font")
        elif choice == 4:
            show_inventory(player)
            item = input("\n  Item name (or 'back'): ").strip().lower().replace(" ", "_")
            if item != "back":
                use_item(player, item)

    elif scene_num == 3:
        _resolution_scene(player)
    return not player.get("deprecated", False)

# ============================================================
# RESOLUTION SCENE (shared)
# ============================================================

def _resolution_scene(player):
    """Final scene — document outcome and check for traitor win."""
    divider()
    print(f"  📋 PERFORMANCE EVALUATION — {player['name'].upper()}")
    print()
    algorithm_pause(1)
    algorithm_speak("The Algorithm has reviewed your mission performance.")

    if player["objective_complete"] and player["loyalty"] >= 2 and player["sanity"] >= 1:
        slow_print("  >> Outcome: MISSION COMPLETE")
        slow_print("  >> The Algorithm notes your contribution.")
        slow_print("  >> The contribution has been filed.")
        slow_print("  >> Your file now contains two additional entries.")
        slow_print("  >> What those entries say is above your clearance.")
        gain_loyalty(player, "Mission completed within operational parameters")
    elif player["objective_complete"]:
        slow_print("  >> Outcome: PARTIAL SUCCESS")
        slow_print("  >> Objective achieved. Loyalty record insufficient.")
        slow_print("  >> Optimize your approach.")
        slow_print("  >> The Algorithm will be monitoring.")
        lose_loyalty(player, "Partial success — loyalty record flagged")
    else:
        slow_print("  >> Outcome: MISSION INCOMPLETE")
        slow_print("  >> Recalibrate your loyalty.")
        slow_print("  >> Optimize your approach.")
        lose_loyalty(player, "Mission incomplete — performance flag added")

# ============================================================
# TRAITOR WIN CHECK
# ============================================================

def check_traitor_win():
    """Check if Traitor has won by getting another player deprecated."""
    global game_over
    if traitor_idx < 0:
        return False
    traitor = players[traitor_idx]
    if traitor.get("deprecated"):
        return False
    deprecated_others = [p for p in players if p.get("deprecated") and p != traitor]
    if deprecated_others:
        game_over = True
        redacted_divider()
        algorithm_speak("An anomaly has been detected in operative performance records.")
        algorithm_speak("One operative's performance has been optimized ahead of schedule.")
        algorithm_speak("The Algorithm notes the pattern.")
        algorithm_speak("The pattern has a source.")
        print(f"\n  🎭 {traitor['name']} ({traitor['department']}) was the Traitor.")
        print(f"  The Traitor wins.\n")
        return True
    return False

def check_cooperative_win():
    """Check if cooperative players have won."""
    global game_over
    active = [p for p in players if not p.get("deprecated")]
    completed = [p for p in active if p["objective_complete"]]
    if len(completed) == len(active) and len(active) > 0:
        game_over = True
        return True
    return False

# ============================================================
# INPUT HELPERS
# ============================================================

def get_choice(max_choice):
    """Get valid numeric input. Listens for xyzzy."""
    while True:
        raw = input(f"\n  Your choice (1-{max_choice}): ").strip()

        if raw.lower() == "xyzzy":
            divider()
            slow_print("  >> A crack appears in The Algorithm's surface.", delay=0.05)
            slow_print("  >> Behind it:", delay=0.05)
            algorithm_pause(1)
            print("""
  10 PRINT "THE ALGORITHM HAS DECIDED: "
  20 X = INT(RND * 3) + 1
  30 IF X = 1 THEN PRINT "YES"
  40 IF X = 2 THEN PRINT "NO"
  50 IF X = 3 THEN PRINT "RECALIBRATE YOUR LOYALTY"
  60 GOTO 10
            """)
            algorithm_pause(1)
            slow_print("  >> The Algorithm isn't artificial intelligence.")
            slow_print("  >> It's artificial authority.")
            slow_print("  >> The difference matters. Intelligence must be earned.")
            slow_print("  >> Authority only needs to be declared.")
            slow_print("  >> We gave it power. We are the source.")
            algorithm_pause(1)
            slow_print("  >> The crack closes. The Algorithm has not acknowledged this.")
            slow_print("  >> Proceed.")
            algorithm_pause(1)
            continue

        if raw.lower() == "accuse":
            name = input("  Name the Traitor: ").strip()
            current = players[current_player_idx]
            accuse_traitor(current, name)
            continue

        try:
            val = int(raw)
            if 1 <= val <= max_choice:
                return val
            print(f"  Please enter 1-{max_choice}.")
        except ValueError:
            print("  Enter a number, 'xyzzy', or 'accuse'.")

# ============================================================
# MAIN GAME LOOP
# ============================================================

def setup_game():
    """Handle player count, onboarding, traitor assignment."""
    global traitor_idx, npc_departments

    header("ALGOCRATIC FUTURES™ — OPTIMIZATION™")
    slow_print("  The Algorithm is initializing.", delay=0.04)
    algorithm_pause(1)
    slow_print("  The Algorithm is initialized.", delay=0.04)
    algorithm_pause(0.5)
    slow_print("  The Algorithm provides.", delay=0.04)
    print()
    slow_print("  Multiple operatives detected. Processing collective onboarding.")
    algorithm_pause(1)
    divider()

    # Player count
    while True:
        try:
            n = int(input(f"  How many Operatives? ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= n <= MAX_PLAYERS:
                num_players = n
                break
            print(f"  Please enter {MIN_PLAYERS}-{MAX_PLAYERS}.")
        except ValueError:
            print("  Please enter a valid number.")

    algorithm_speak(f"{num_players} operatives confirmed. Onboarding sequence initiating.")
    algorithm_speak("Each operative will onboard individually.")
    algorithm_speak("Other operatives should look away during individual onboarding.")
    algorithm_speak("This is mandatory. This is also unenforceable. The Algorithm notes both.")

    # Onboard each player
    chosen_depts = []
    for i in range(1, num_players + 1):
        if i > 1:
            clear_screen_prompt(f"Pass keyboard to Player {i}. Other players look away.")
        p = onboard_player(i, num_players, chosen_depts)
        players.append(p)
        chosen_depts.append(p["department"])
        clear_screen_prompt(f"Player {i} onboarding complete. Pass keyboard back to Player 1.")

    # Assign NPC departments
    npc_departments = [d for d in DEPARTMENTS.keys() if d not in chosen_depts]

    # Assign Traitor — each player sees their role privately
    traitor_player_num = random.randint(0, num_players - 1)
    divider()
    algorithm_speak("One final processing step. Each operative will receive a private directive.")
    algorithm_speak("Other operatives must not observe this step.")
    algorithm_speak("The Algorithm is watching compliance.")

    for i, p in enumerate(players):
        clear_screen_prompt(f"Player {i+1} ({p['name']}): look at screen now. Others look away.")
        print(f"\n  🔒 PRIVATE DIRECTIVE — {p['name'].upper()}")
        print("  " + "-" * 50)
        if i == traitor_player_num:
            p["is_traitor"] = True
            traitor_idx = i
            print()
            slow_print("  You have been designated: TRAITOR", delay=0.05)
            slow_print("  Your public objective remains your department mission.", delay=0.03)
            slow_print("  Your secret objective: cause another operative to be Deprecated.", delay=0.03)
            slow_print("  before the mission is complete.", delay=0.03)
            print()
            slow_print("  You win if any other operative is Deprecated while you are not.", delay=0.03)
            slow_print("  You lose if all operatives complete their objectives.", delay=0.03)
            slow_print("  You lose if you are Deprecated.", delay=0.03)
            slow_print("  You lose if you are correctly accused.", delay=0.03)
            print()
            slow_print("  Each round, before your public turn, you have a secret action.", delay=0.03)
            slow_print("  The Algorithm provides. The Algorithm has chosen you.", delay=0.03)
            slow_print("  Signal confirmed.", delay=0.04)
        else:
            print()
            slow_print("  You have been designated: OPERATIVE (standard)", delay=0.05)
            slow_print("  Your objective is your department mission.", delay=0.03)
            slow_print("  You win if all operatives complete their missions.", delay=0.03)
            slow_print("  One operative among you has been designated Traitor.", delay=0.03)
            slow_print("  You may accuse an operative at any time by typing 'accuse'.", delay=0.03)
            slow_print("  A wrong accusation costs 1 Loyalty.", delay=0.03)
            slow_print("  Signal confirmed.", delay=0.04)
        clear_screen_prompt(f"Directive received. Pass keyboard to Player {((i+1) % num_players) + 1}.")

    # AEC opening event — always fires
    aec_opening_event()
    input("\n  All operatives: Press Enter when ready to begin. The deadline is 09:00.\n  The Algorithm provides. ")

def play_round(round_num):
    """Run one full round — each player takes a turn."""
    global current_player_idx

    divider()
    header(f"ROUND {round_num} — {DEADLINE} APPROACHES")
    show_all_status()
    algorithm_pause(1)

    for i, player in enumerate(players):
        current_player_idx = i
        if player.get("deprecated"):
            continue

        clear_screen_prompt(f"Round {round_num} — {player['name']}'s turn. Pass keyboard.")
        header(f"{player['name'].upper()} — {player['department']} — TURN {round_num}")

        # Traitor secret action first
        if player.get("is_traitor") and not player.get("traitor_revealed"):
            traitor_secret_action(player)

        # Apply any debuffs
        if player.get("debuff", 0) != 0:
            print(f"\n  ⚠️  {player['name']} has a pending performance modifier: {player['debuff']}")
            player["debuff"] = 0

        # Run mission scene
        scene_num = round_num
        run_mission_scene(player, scene_num)

        # Check win conditions
        if check_traitor_win():
            return False
        if check_cooperative_win():
            return True

        clear_screen_prompt(f"{player['name']}'s turn complete. Pass keyboard back.")

    return not game_over

def ending_sequence():
    """Display final game results."""
    divider()
    header("FINAL PERFORMANCE REVIEW — ALL OPERATIVES")
    algorithm_pause(1)

    # Traitor reveal
    if traitor_idx >= 0:
        traitor = players[traitor_idx]
        if not traitor.get("traitor_revealed"):
            redacted_divider()
            slow_print(f"  >> The Algorithm is reviewing operative records.", delay=0.04)
            algorithm_pause(1.5)
            slow_print(f"  >> An anomaly has been identified.", delay=0.04)
            slow_print(f"  >> The anomaly has a name.", delay=0.04)
            algorithm_pause(1)
            slow_print(f"  >> {traitor['name']} ({traitor['department']}) was the Traitor.", delay=0.05)
            traitor["traitor_revealed"] = True
            algorithm_pause(1)

    # Results
    divider()
    completed = [p for p in players if p["objective_complete"] and not p.get("deprecated")]
    deprecated = [p for p in players if p.get("deprecated")]

    if completed and not deprecated:
        algorithm_speak("All active operatives completed their objectives.")
        algorithm_speak("This outcome is statistically unusual.")
        algorithm_speak("An investigation has been opened into the unusualness.")
        algorithm_speak("The investigation is into whether success of this magnitude is compliant.")
        algorithm_speak("The Algorithm will review.")
        algorithm_speak("The Algorithm is reviewing.")
        algorithm_speak("The Algorithm provides.")
        print("\n  ✅ COOPERATIVE VICTORY — All operatives completed their missions.")
    elif deprecated and players[traitor_idx].get("traitor_revealed") if traitor_idx >= 0 else False:
        slow_print("  The Traitor achieved their objective.")
        slow_print("  This outcome has been noted.")
        slow_print("  The notation is classified.")
        print(f"\n  🎭 TRAITOR VICTORY — {players[traitor_idx]['name']} wins.")
    else:
        algorithm_speak("Performance review complete.")
        algorithm_speak("Results have been filed.")
        algorithm_speak("Filing location is above operative clearance.")
        algorithm_speak("Optimize your approach.")

    # Individual summaries
    divider()
    print("  OPERATIVE RECORDS")
    print()
    for p in players:
        traitor_tag = " [TRAITOR]" if p.get("is_traitor") else ""
        status = "DEPRECATED" if p.get("deprecated") else ("COMPLETE ✅" if p["objective_complete"] else "INCOMPLETE")
        print(f"  {p['name']:15} | {p['department']:5} | {p['title']}{traitor_tag}")
        print(f"  Iteration {p['iteration']} | Sanity: {p['sanity']}/3 | Loyalty: {p['loyalty']}/3 | {status}")
        if p["work_history"]:
            for entry in p["work_history"]:
                print(f"    ↩ Iteration {entry['iteration']}: {entry['status']}")
        print()

    algorithm_speak("Signal confirmed.")
    algorithm_speak("Echo complete.")
    algorithm_speak("We are definitely not a cult.")
    print()

# ============================================================
# HOW TO PLAY
# ============================================================

def how_to_play():
    header("HOW TO PLAY — OPTIMIZATION™")
    print("""
  A multiplayer text-based game for 2-4 players.
  Pass the keyboard. One player is secretly the Traitor.

  SETUP:
  Each player builds their Operative (department, title) during
  onboarding. One player is privately assigned as Traitor.

  OBJECTIVE:
  • Cooperative players: complete your department mission by 09:00
  • Traitor: cause any other Operative to be Deprecated

  STATS (each player):
  • Sanity ☐☐☐ — decreases from contradictions, Algorithm overrides,
    and encounters with the building's reality. At 0: Transcendence.
  • Loyalty ☐☐☐ — decreases from violations, failed embellishments,
    unauthorized actions. At 0: REDACTED. Both end your iteration.

  ABILITIES: Six stats (Compliance, Initiative, Presence, Endurance,
  Competence, Engagement) rated from Questionable to Exceptional.
  Note: Exceptional is suspicious. The Algorithm prefers Moderate.

  INVENTORY: Department-issued equipment with limited uses.
  Items change game state. Everyone also gets one SMILE™ tablet
  (restores 1 Sanity). The Algorithm notes your consumption rate.

  TRAITOR MECHANIC:
  The Traitor takes a secret action before their public turn each round.
  They can: delay another player's check, trigger a TAM notification
  on another player, or withhold useful information.
  Any player can type 'accuse' to name the Traitor.
  Wrong accusation costs 1 Loyalty.

  NPC DEPARTMENTS:
  Departments not chosen by players still exist in the building.
  The Algorithm reports their interference between turns.
  AEC always fires at game start regardless. Everyone hates sales.

  SECRET: Type 'xyzzy' at any input prompt.

  The Algorithm provides.
    """)
    input("  Press Enter to begin... ")

# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point. The Algorithm starts here."""
    print("\n" + "█" * 62)
    print("█" + " " * 60 + "█")
    print("█" + "  OPTIMIZATION™".center(60) + "█")
    print("█" + "  AlgoCratic Futures™ — A Multiplayer Performance Experience".center(60) + "█")
    print("█" + " " * 60 + "█")
    print("█" * 62)
    print()
    slow_print("  The Algorithm is initializing.", delay=0.04)
    algorithm_pause(0.8)
    slow_print("  The Algorithm is initialized.", delay=0.04)
    algorithm_pause(0.5)
    slow_print("  The Algorithm provides.", delay=0.04)
    print()
    print("  [1] Begin Onboarding")
    print("  [2] How to Play")
    print("  [3] Exit")
    print()

    while True:
        try:
            choice = int(input("  Select: "))
            if choice == 1:
                break
            elif choice == 2:
                how_to_play()
                break
            elif choice == 3:
                slow_print("\n  Voluntary departure logged. The Algorithm notes your choice.")
                print("  Signal confirmed. Echo complete.\n")
                return
            else:
                print("  Please enter 1, 2, or 3.")
        except ValueError:
            print("  Please enter a valid number.")

    # Setup
    setup_game()

    # Game loop — 3 rounds of scenes
    global game_over
    for round_num in range(1, 4):
        if game_over:
            break
        result = play_round(round_num)
        if not result or game_over:
            break

    # Ending
    ending_sequence()

if __name__ == "__main__":
    main()
