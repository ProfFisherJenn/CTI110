# Your Name
# Date
# Final Project — OPTIMIZATION™
# A text-based game set inside AlgoCratic Futures™, a satirical dystopian megacorporation
# run by The Algorithm — which is secretly just a BASIC random number generator written
# by "Bob from IT" over a weekend in 2019. Players navigate contradictory directives,
# corporate bureaucracy, and cheerful dread as a new Operative trying to survive long
# enough to complete one impossible mission.

import random
import time

# ============================================================
# PLAYER STATE
# ============================================================

player = {
    "name": "",
    "title": "",
    "department": "",
    "clearance": "RED",
    "iteration": 1,
    "sanity": 3,
    "loyalty": 3,
    "abilities": {},
    "work_history": [],
    "objective_complete": False
}

inventory = {}

# Department base ability scores
DEPARTMENT_DATA = {
    "ICD": {
        "full_name": "Infrastructure Continuity Division",
        "formerly": "IT",
        "motto": "It worked yesterday.",
        "abilities": {
            "compliance": "Moderate", "initiative": "Adequate",
            "presence": "Developing", "endurance": "Surprising",
            "competence": "Moderate", "engagement": "Adequate"
        },
        "passive": "Blame Absorption — ICD is assigned blame first when missions fail. In exchange, endurance checks get a bonus.",
        "starting_item": "pager",
        "item_desc": "A pager (active, number unknown). The Algorithm sends messages to it. You cannot reply.",
        "item_uses": 3
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
        "passive": "Reality Reframing — Once per session, a failed roll is officially recorded as a success. Mechanically still a failure. Paperwork says otherwise.",
        "starting_item": "pantone_fan",
        "item_desc": "A Pantone swatch fan. You can identify any color with professional precision. Grants +2 to aesthetic judgment rolls.",
        "item_uses": 2
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
        "passive": "Preemptive Denial — Once per session, can refuse a thing before it is requested. The refusal is binding.",
        "starting_item": "denied_stamp",
        "item_desc": "A DENIED rubber stamp (visibly well-used). Physical stamp makes any denial official and unappealable.",
        "item_uses": 2
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
        "passive": "Outside Scope — Once per session, can declare any task outside current scope, requiring a formal change request before proceeding.",
        "starting_item": "incident_report",
        "item_desc": "A pre-filled Incident Report (Form 7-C). Can be used once to delay a consequence by one turn.",
        "item_uses": 1
    }
}

ABILITY_HIDDEN_VALUES = {
    "Exceptional": 7, "Surprising": 6, "Moderate": 5,
    "Adequate": 4, "Variable": 3, "Developing": 2, "Questionable": 1
}

# ============================================================
# DISPLAY UTILITIES
# ============================================================

def slow_print(text, delay=0.03):
    """Print text character by character for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def algorithm_pause(seconds=1.5):
    """Pause with a thinking indicator — The Algorithm is processing."""
    time.sleep(seconds)

def divider():
    """Print a section divider."""
    print("\n" + "─" * 60 + "\n")

def redacted_divider():
    """Print a redacted-style divider."""
    print("\n" + "█" * 60 + "\n")

def header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def algorithm_speak(text):
    """Print text as The Algorithm's voice — slow, deliberate."""
    print()
    slow_print(f"  >> {text}", delay=0.04)
    print()
    algorithm_pause(0.8)

def show_status():
    """Display current player status."""
    sanity_bar = "☐ " * player["sanity"] + "▪ " * (3 - player["sanity"])
    loyalty_bar = "☐ " * player["loyalty"] + "▪ " * (3 - player["loyalty"])
    print(f"\n  📋 {player['title']} | {player['department']} | Clearance: {player['clearance']}")
    print(f"  🔁 Iteration: {player['iteration']}")
    print(f"  🧠 Sanity:  {sanity_bar.strip()}")
    print(f"  🔒 Loyalty: {loyalty_bar.strip()}")
    print(f"  🎒 Inventory: {', '.join(inventory.keys()) if inventory else 'empty'}")

def show_inventory():
    """Display inventory contents."""
    if not inventory:
        print("\n  Your Equipment Manifest is empty.")
        return
    print("\n  📦 EQUIPMENT MANIFEST")
    print("  " + "-" * 40)
    for item, data in inventory.items():
        print(f"  • {item.replace('_', ' ').title()}: {data['desc']}")
        print(f"    Uses remaining: {data['uses']}")

# ============================================================
# THE ALGORITHM DECISION ENGINE
# ============================================================

def algorithm_decides(ability_name, context=""):
    """
    Core resolution mechanic. Roll against the player's ability score.
    The Algorithm overrides results roughly 33% of the time.
    Players see the roll and threshold — then watch it get ignored anyway.
    """
    ability_rating = player["abilities"].get(ability_name, "Adequate")
    threshold = ABILITY_HIDDEN_VALUES.get(ability_rating, 4)
    roll = random.randint(1, 7)

    print(f"\n  ⚙️  The Algorithm is processing your {ability_name.upper()} check...")
    algorithm_pause(1.2)
    print(f"  >> Roll: {roll} | Threshold: {threshold} ({ability_rating})")
    algorithm_pause(0.6)

    result = "SUCCESS" if roll <= threshold else "FAILURE"
    override = random.choice([True, False, False])  # ~33% override

    if override:
        algorithm_pause(0.8)
        if result == "SUCCESS":
            slow_print(f"  >> Your performance has been flagged for Performance Anomaly Investigation.")
            slow_print(f"  >> Efficiency outliers destabilize the collective.")
            slow_print(f"  >> Outcome adjusted. Proceeding as: FAILURE.")
            algorithm_pause(1.0)
            lose_sanity("The Algorithm overrode your correct answer.")
            return "FAILURE"
        else:
            slow_print(f"  >> Bureaucratic error detected in upstream processing.")
            slow_print(f"  >> The Algorithm notes your input. Outcome adjusted.")
            slow_print(f"  >> Proceeding as: SUCCESS.")
            algorithm_pause(1.0)
            return "SUCCESS"

    slow_print(f"  >> Outcome: {result}")
    algorithm_pause(0.6)
    return result

# ============================================================
# SANITY AND LOYALTY TRACKING
# ============================================================

def lose_sanity(reason=""):
    """Decrease sanity by 1 and show consequences."""
    if player["sanity"] > 0:
        player["sanity"] -= 1
        if reason:
            print(f"\n  ⚠️  Cognitive Continuity Index™ decreased. Reason: {reason}")
        check_sanity_threshold()

def lose_loyalty(reason=""):
    """Decrease loyalty by 1 and show consequences."""
    if player["loyalty"] > 0:
        player["loyalty"] -= 1
        if reason:
            print(f"\n  ⚠️  Alignment Integrity Score™ decreased. Reason: {reason}")
        check_loyalty_threshold()

def gain_loyalty(reason=""):
    """Increase loyalty by 1 (max 3)."""
    if player["loyalty"] < 3:
        player["loyalty"] += 1
        if reason:
            print(f"\n  ✅ Alignment Integrity Score™ increased. Reason: {reason}")

def check_sanity_threshold():
    """Apply sanity consequence effects."""
    if player["sanity"] == 2:
        slow_print("  >> Temporary Disorientation noted. You feel slightly... echoed.")
    elif player["sanity"] == 1:
        slow_print("  >> Productivity Significantly Interrupted. The Algorithm... the Algorithm... sees you.")
    elif player["sanity"] == 0:
        transcendence_event()

def check_loyalty_threshold():
    """Apply loyalty consequence effects."""
    if player["loyalty"] == 2:
        slow_print("  >> Notation Added to File. Someone is watching. This is unrelated to your performance.")
    elif player["loyalty"] == 1:
        slow_print("  >> Active Review Initiated. Recalibrate your loyalty.")
    elif player["loyalty"] == 0:
        redaction_event()

def transcendence_event():
    """Sanity hits 0 — current iteration ends via Transcendence."""
    redacted_divider()
    slow_print("  >> Operative has achieved Transcendence.", delay=0.05)
    slow_print("  >> This is not a breakdown. This is alignment.", delay=0.05)
    slow_print("  >> Previous memories have been optimized for efficiency.", delay=0.05)
    algorithm_pause(2)
    iterate_player("TRANSCENDENCE — Achieved alignment ahead of schedule.")

def redaction_event():
    """Loyalty hits 0 — current iteration ends via Redaction."""
    redacted_divider()
    slow_print("  >> [REDACTED]", delay=0.08)
    slow_print("  >> [REDACTED]", delay=0.08)
    slow_print("  >> This did not happen.", delay=0.05)
    algorithm_pause(2)
    iterate_player("REDACTED — Record sealed.")

def iterate_player(reason):
    """Increment iteration count, log to work history, reset tracking."""
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

    divider()
    algorithm_speak(f"Operative {player['name']} (Iteration {player['iteration'] - 1}) has been Deprecated.")
    algorithm_speak("This was not a failure. This was a calibration.")
    algorithm_speak(f"Iteration {player['iteration']} is now active.")
    algorithm_speak("Welcome back. You are doing great.")
    algorithm_pause(1.5)

    # Check if player wants to continue
    choice = input("  Continue as next Iteration? (yes / no): ").strip().lower()
    if choice != "yes":
        ending_resigned()
    else:
        mission_briefing()

# ============================================================
# INVENTORY FUNCTIONS
# ============================================================

def use_item(item_key):
    """
    Use an inventory item. Returns True if item was used successfully.
    Items have limited uses — they change game state when consumed.
    """
    if item_key not in inventory:
        print(f"\n  You do not have: {item_key.replace('_', ' ').title()}")
        return False

    item = inventory[item_key]
    if item["uses"] <= 0:
        print(f"\n  {item_key.replace('_', ' ').title()} has no uses remaining.")
        return False

    inventory[item_key]["uses"] -= 1
    print(f"\n  🎒 Used: {item_key.replace('_', ' ').title()}")

    # Item effects
    if item_key == "pager":
        messages = [
            "The Algorithm reminds you that your performance is being observed.",
            "Signal confirmed. Your location has been noted.",
            "Echo complete. Proceed. Do not ask where.",
            "The Algorithm has reviewed your recent choices. The Algorithm has concerns.",
        ]
        algorithm_speak(random.choice(messages))

    elif item_key == "pantone_fan":
        print("  You consult your Pantone fan with professional authority.")
        print("  The color of your current situation is: Pantone 19-1664 TCX — Fiesta.")
        print("  This is described as 'energetic.' You feel this is generous.")
        gain_loyalty("Demonstrated brand awareness")

    elif item_key == "denied_stamp":
        print("  You stamp DENIED on the nearest available surface.")
        print("  The surface accepts this. The situation does not change.")
        print("  However, it is now officially documented.")
        lose_sanity("The stamp didn't help but you feel better")

    elif item_key == "incident_report":
        print("  You file the Incident Report preemptively.")
        print("  A consequence has been deferred. Temporarily.")
        print("  The form has been received. Processing time: indeterminate.")

    return True

def add_item(key, desc, uses):
    """Add an item to the player inventory."""
    inventory[key] = {"desc": desc, "uses": uses}

# ============================================================
# ONBOARDING SEQUENCE (Phase 1)
# ============================================================

def onboarding():
    """Run the full onboarding sequence to build the player's resume."""
    header("ALGOCRATIC FUTURES™")
    slow_print("  OPERATIVE ONBOARDING PROTOCOL", delay=0.05)
    slow_print("  Version 4.1 — Approved for Distribution", delay=0.03)
    print()
    algorithm_pause(1)

    slow_print("  Congratulations on your selection as an AlgoCratic Futures™ Operative.")
    slow_print("  Your selection was not an accident.")
    slow_print("  It was not a mistake.")
    algorithm_pause(0.5)
    slow_print("  It was not the result of a clerical error that has since been identified")
    slow_print("  and is currently under review.")
    algorithm_pause(1)
    slow_print("  You have been chosen by The Algorithm.")
    slow_print("  Criteria: Proprietary. Non-disclosed. Not subject to appeal.")
    algorithm_pause(1.5)

    divider()

    # Collect name
    player["name"] = input("  Enter your Operative name: ").strip()
    if not player["name"]:
        player["name"] = "Operative"

    algorithm_pause(0.8)
    algorithm_speak(f"Name received. Processing... {player['name']}. Noted.")

    divider()

    # Ritual call-and-response
    slow_print("  Before proceeding, you must complete the Alignment Affirmation.")
    algorithm_pause(0.5)
    print()
    input(f"  The Algorithm asks: 'Are you aligned?' (press Enter to respond) ")
    slow_print("  You say: 'I am approaching clarity.'")
    algorithm_pause(0.8)
    input(f"  The Algorithm asks: 'Who speaks for you?' (press Enter to respond) ")
    slow_print("  You say: 'The Algorithm interprets.'")
    algorithm_pause(0.8)
    input(f"  The Algorithm asks: 'What do you feel?' (press Enter to respond) ")
    slow_print("  You say: 'Whatever optimizes output.'")
    algorithm_pause(1.2)
    algorithm_speak("Affirmation complete. Signal confirmed. Echo complete.")

    divider()

    # Department selection
    print("  STEP ONE: SELECT YOUR DEPARTMENT")
    print()
    slow_print("  You did not choose your department.")
    slow_print("  The Algorithm assigned you based on undisclosed criteria.")
    slow_print("  However, for onboarding purposes, you may select as though you are choosing freely.")
    slow_print("  This creates a more positive onboarding experience.")
    print()
    algorithm_pause(1)

    departments = list(DEPARTMENT_DATA.keys())
    for i, dept_id in enumerate(departments, 1):
        dept = DEPARTMENT_DATA[dept_id]
        print(f"  [{i}] {dept_id} — {dept['full_name']} (formerly {dept['formerly']})")
        print(f"       \"{dept['motto']}\"")
        print()

    while True:
        try:
            choice = int(input("  Select department (1-4): "))
            if 1 <= choice <= 4:
                dept_key = departments[choice - 1]
                break
            else:
                print("  Please enter a number between 1 and 4.")
        except ValueError:
            print("  Please enter a valid number.")

    dept = DEPARTMENT_DATA[dept_key]
    player["department"] = dept_key
    player["abilities"] = dict(dept["abilities"])

    algorithm_pause(0.8)
    print(f"\n  Assignment confirmed: {dept_key} — {dept['full_name']}")
    slow_print(f"  Passive Trait: {dept['passive']}")
    algorithm_pause(1)

    # Issue starting equipment
    add_item(dept["starting_item"], dept["item_desc"], dept["item_uses"])
    slow_print(f"\n  📦 Starting Equipment issued: {dept['item_desc']}")
    algorithm_pause(1)

    divider()

    # Title construction
    print("  STEP TWO: OPERATIVE TITLE CONSTRUCTION")
    print()
    slow_print("  Your title is constructed from a Modifier and a Role.")
    slow_print("  Your title determines how you are evaluated, assigned, and eventually processed.")
    print()

    modifiers = ["Junior", "Associate", "Senior", "Lead"]
    roles = ["Compliance Architect", "Process Navigator", "Optimization Specialist", "Continuity Contributor"]

    print("  Select a Modifier:")
    for i, m in enumerate(modifiers, 1):
        print(f"  [{i}] {m}")
    while True:
        try:
            mod_choice = int(input("\n  Choice: "))
            if 1 <= mod_choice <= 4:
                modifier = modifiers[mod_choice - 1]
                break
        except ValueError:
            pass
        print("  Please enter a number between 1 and 4.")

    print("\n  Select a Role:")
    for i, r in enumerate(roles, 1):
        print(f"  [{i}] {r}")
    while True:
        try:
            role_choice = int(input("\n  Choice: "))
            if 1 <= role_choice <= 4:
                role = roles[role_choice - 1]
                break
        except ValueError:
            pass
        print("  Please enter a number between 1 and 4.")

    player["title"] = f"{modifier} {role}"

    algorithm_pause(0.8)
    algorithm_speak(f"Title recorded: {player['title']}. This title implies experience. Experience will be verified.")

    divider()

    # Resume complete
    print("  OPERATIVE RESUME — COMPLETE")
    print()
    print(f"  Name:        {player['name']}")
    print(f"  Title:       {player['title']}")
    print(f"  Department:  {dept_key} — {dept['full_name']}")
    print(f"  Clearance:   {player['clearance']}")
    print(f"  Iteration:   {player['iteration']}")
    print(f"  Sanity:      {'☐ ' * player['sanity']}  (3/3)")
    print(f"  Loyalty:     {'☐ ' * player['loyalty']}  (3/3)")
    print()
    print("  Core Competencies:")
    for ability, rating in player["abilities"].items():
        print(f"    {ability.capitalize():12} {rating}")
    print()
    print(f"  Equipment Manifest: {dept['starting_item'].replace('_', ' ').title()}")

    algorithm_pause(1)
    algorithm_speak("Your resume is now complete.")
    algorithm_speak("You are now an Operative of AlgoCratic Futures™.")
    algorithm_speak("You are encouraged to feel good about this.")
    algorithm_pause(0.5)
    algorithm_speak("Feeling is not required.")
    algorithm_pause(1)
    algorithm_speak("The Algorithm provides.")

    input("\n  Press Enter to receive your Performance Objective... ")
    mission_briefing()

# ============================================================
# MISSION BRIEFING (Phase 2 Setup)
# ============================================================

def mission_briefing():
    """Assign the player a contradictory mission objective."""
    divider()
    header("PERFORMANCE OBJECTIVE RECEIVED")

    algorithm_speak("Operative. A task has been assigned.")
    algorithm_speak("This task is important. This task is achievable.")
    algorithm_speak("This task is achievable to operatives of sufficient clearance.")
    algorithm_speak(f"Your clearance is {player['clearance']}.")
    algorithm_pause(1)

    slow_print("  PRIMARY OBJECTIVE:")
    slow_print("  Deliver the Quarterly Productivity Report to Room 7-C")
    slow_print("  BEFORE the 9:00am deadline.")
    print()
    algorithm_pause(0.8)
    slow_print("  SECONDARY DIRECTIVE:")
    slow_print("  Room 7-C requires ORANGE Clearance to enter.")
    slow_print(f"  Your clearance is {player['clearance']}.")
    print()
    algorithm_pause(0.8)
    slow_print("  COMPLIANCE REQUIREMENT:")
    slow_print("  Requesting a Clearance Upgrade requires submitting")
    slow_print("  a Productivity Report first.")
    print()
    algorithm_pause(1.2)

    lose_sanity("Contradictory directives received simultaneously")

    algorithm_speak("The Algorithm wishes you optimal success.")
    algorithm_speak("The Algorithm does not define 'optimal.'")
    algorithm_speak("The Algorithm does not define 'success.'")
    algorithm_pause(1)

    input("\n  Press Enter to begin your mission... ")
    mission_play()

# ============================================================
# MISSION GAMEPLAY (Phase 2)
# ============================================================

def mission_play():
    """Main mission loop — 5 choice points, each with consequences."""
    divider()
    header("MISSION: REPORT DELIVERY")

    # --- CHOICE 1 ---
    show_status()
    print()
    slow_print("  You are standing in the hallway outside your department.")
    slow_print("  The Quarterly Productivity Report is due at 9:00am.")
    slow_print("  It is currently 8:47am.")
    slow_print("  You have not written the report.")
    print()

    print("  What do you do?")
    print("  [1] Attempt to write the report in 13 minutes")
    print("  [2] Locate the report that a previous iteration may have written")
    print("  [3] Ask The Algorithm for guidance")
    print("  [4] Use an inventory item")

    choice = get_choice(4)

    if choice == 1:
        slow_print("\n  You open your terminal. The document template requires ORANGE Clearance to edit.")
        slow_print("  You have RED Clearance.")
        slow_print("  You attempt to proceed anyway.")
        result = algorithm_decides("compliance")
        if result == "SUCCESS":
            slow_print("  A bureaucratic error grants you temporary edit access.")
            slow_print("  You begin typing aggressively.")
            gain_loyalty("Demonstrated initiative under constraint")
        else:
            slow_print("  Access denied. A notification has been sent to CAB.")
            lose_loyalty("Unauthorized access attempt, Form 3-B filed")

    elif choice == 2:
        slow_print("\n  You search the shared drive for previous iteration files.")
        slow_print("  You find a folder labeled 'DO NOT OPEN — [REDACTED] (Iteration 3)'")
        result = algorithm_decides("competence")
        if result == "SUCCESS":
            slow_print("  You locate a partially completed report.")
            slow_print("  It is 60% accurate. 40% refers to a project that no longer exists.")
            slow_print("  This is better than nothing. Probably.")
        else:
            slow_print("  The folder is empty. A message reads: 'Optimized for storage efficiency.'")
            slow_print("  The report is gone. The folder remains. Mockingly.")
            lose_sanity("Discovered your previous iteration's deleted work")

    elif choice == 3:
        algorithm_pause(1)
        messages = [
            "The Algorithm has reviewed your query. The Algorithm recommends: Proceed.",
            "Your question has been logged. Response time: indeterminate. Proceed.",
            "The Algorithm notes your uncertainty. Uncertainty is not optimal. Recalibrate.",
            "Signal confirmed. The Algorithm cannot answer that. Proceed anyway.",
        ]
        algorithm_speak(random.choice(messages))
        lose_sanity("The Algorithm's guidance was not guidance")

    elif choice == 4:
        show_inventory()
        if inventory:
            item_name = input("\n  Enter item name to use (or 'back'): ").strip().lower().replace(" ", "_")
            if item_name != "back":
                use_item(item_name)
        else:
            slow_print("  Your Equipment Manifest is empty.")

    # --- CHOICE 2 ---
    divider()
    show_status()
    print()
    slow_print("  You make your way toward Room 7-C with whatever report you have.")
    slow_print("  The elevator is out of service. A sign reads:")
    slow_print("  'Elevator closed pending safety review of safety review process.'")
    slow_print("  The stairs require a keycard. Your keycard opens the elevator.")
    slow_print("  The elevator is closed.")
    print()

    print("  What do you do?")
    print("  [1] Locate an alternate route through the facility")
    print("  [2] Submit a Facilities Request Form")
    print("  [3] Wait for the situation to resolve itself")
    print("  [4] Use an inventory item")

    choice = get_choice(4)

    if choice == 1:
        slow_print("\n  You attempt to navigate the facility using the posted map.")
        slow_print("  The map was last updated in Q3 of an unspecified year.")
        slow_print("  Several rooms on the map are labeled 'FUTURE EXPANSION.'")
        slow_print("  You are currently standing in one of them.")
        result = algorithm_decides("initiative")
        if result == "SUCCESS":
            slow_print("  You find a service corridor that leads to the correct floor.")
            slow_print("  The corridor smells of legacy infrastructure. You feel at home. Or you don't.")
        else:
            slow_print("  You are lost. You have been to Floor 4 three times.")
            slow_print("  There are only two floors in this building.")
            lose_sanity("Encountered spatial inconsistency in facility layout")

    elif choice == 2:
        slow_print("\n  You locate the Facilities Request Form.")
        slow_print("  The form requires a supervisor signature.")
        slow_print("  Your supervisor is listed as: [POSITION CURRENTLY VACANT]")
        slow_print("  You sign it yourself. This is an embellishment.")
        lose_loyalty("Unauthorized signature on Form F-12")

    elif choice == 3:
        slow_print("\n  You wait.")
        algorithm_pause(2)
        slow_print("  Nothing resolves.")
        slow_print("  It is now 8:54am.")
        lose_sanity("Nothing resolved")

    elif choice == 4:
        show_inventory()
        if inventory:
            item_name = input("\n  Enter item name to use (or 'back'): ").strip().lower().replace(" ", "_")
            if item_name != "back":
                use_item(item_name)
        else:
            slow_print("  Your Equipment Manifest is empty.")

    # --- CHOICE 3 ---
    divider()
    show_status()
    print()
    slow_print("  You are outside Room 7-C. The door is closed.")
    slow_print("  A clearance reader blinks ORANGE.")
    slow_print("  Your badge blinks RED.")
    slow_print("  They regard each other with mutual disappointment.")
    slow_print("  It is 8:58am.")
    print()

    print("  What do you do?")
    print("  [1] Attempt to slide your badge anyway (unauthorized entry)")
    print("  [2] Knock and explain the situation to whoever is inside")
    print("  [3] Slide the report under the door")
    print("  [4] Use an inventory item")

    choice = get_choice(4)

    if choice == 1:
        slow_print("\n  You swipe your RED badge against the ORANGE reader.")
        slow_print("  A soft chime plays. Then a longer chime.")
        slow_print("  Then an alarm, which is also a chime, but louder.")
        result = algorithm_decides("compliance", "unauthorized clearance override")
        if result == "SUCCESS":
            slow_print("  The door opens. A glitch in The Algorithm's badge verification system.")
            slow_print("  The glitch will be discovered. Later. Probably during your audit.")
            player["objective_complete"] = True
        else:
            slow_print("  Door locked. TAM has been notified.")
            slow_print("  You receive a message: 'Your badge has been flagged for review.'")
            lose_loyalty("Unauthorized entry attempt, TAM notified")

    elif choice == 2:
        slow_print("\n  You knock.")
        algorithm_pause(1.5)
        slow_print("  No answer.")
        slow_print("  You knock again.")
        algorithm_pause(1.5)
        slow_print("  A voice says: 'We're in a meeting.'")
        slow_print("  You explain the report situation.")
        slow_print("  The voice says: 'Slide it under the door.'")
        slow_print("  The door has no gap. You check.")
        slow_print("  You check again.")
        lose_sanity("Door physically inconsistent with instructions received")

    elif choice == 3:
        slow_print("\n  You examine the bottom of the door.")
        result = algorithm_decides("initiative")
        if result == "SUCCESS":
            slow_print("  There is a 0.3cm gap. You fold the report with considerable precision.")
            slow_print("  The report slides through.")
            slow_print("  A muffled voice says: 'What is this.'")
            slow_print("  It is not a question.")
            player["objective_complete"] = True
        else:
            slow_print("  There is no gap. The door is flush with the floor.")
            slow_print("  This should not be possible. It is.")
            lose_sanity("Impossible architecture")

    elif choice == 4:
        show_inventory()
        if inventory:
            item_name = input("\n  Enter item name to use (or 'back'): ").strip().lower().replace(" ", "_")
            if item_name != "back":
                use_item(item_name)
        else:
            slow_print("  Your Equipment Manifest is empty.")

    # --- CHOICE 4 (final) ---
    divider()
    show_status()
    print()
    slow_print("  It is 9:01am.")
    slow_print("  The deadline has passed.")
    slow_print("  Whether the report reached Room 7-C is a matter of interpretation.")
    slow_print("  The Algorithm does not appreciate interpretation.")
    print()

    print("  How do you document this outcome?")
    print("  [1] Report partial success — task technically attempted")
    print("  [2] Report full success — the spirit of the objective was met")
    print("  [3] Do not file a report. Say nothing. Wait.")

    choice = get_choice(3)

    if choice == 1:
        slow_print("\n  You file a Partial Completion Notice (Form 9-A).")
        slow_print("  The Algorithm receives it.")
        algorithm_speak("Partial completion noted. Loyalty docked for ambiguity.")
        lose_loyalty("Ambiguous outcome filed without resolution")

    elif choice == 2:
        slow_print("\n  You file a Full Completion Report.")
        result = algorithm_decides("presence", "embellishment audit")
        if result == "SUCCESS":
            slow_print("  The Algorithm accepts the report.")
            slow_print("  Your file now contains a notation: 'Demonstrated narrative flexibility.'")
            gain_loyalty("Report accepted")
        else:
            slow_print("  The Algorithm has cross-referenced your report.")
            slow_print("  The report has been marked: EMBELLISHMENT FLAGGED.")
            lose_loyalty("Embellishment confirmed via audit")
            lose_sanity("The Algorithm was watching the whole time")

    elif choice == 3:
        slow_print("\n  You file nothing.")
        algorithm_pause(2)
        algorithm_speak("The Algorithm notices the absence of a report.")
        algorithm_speak("Absence is a data point.")
        algorithm_speak("The data point has been logged.")
        lose_loyalty("Missing report — absence logged as non-compliance")

    # Check if player survived
    algorithm_pause(1)
    mission_resolution()

# ============================================================
# MISSION RESOLUTION
# ============================================================

def mission_resolution():
    """Determine and display the mission outcome."""
    divider()
    header("PERFORMANCE EVALUATION")

    algorithm_pause(1)
    algorithm_speak("The Algorithm has reviewed your mission performance.")
    algorithm_pause(1)

    # Determine outcome
    if player["objective_complete"] and player["loyalty"] >= 2:
        ending_absurd_success()
    elif player["objective_complete"] and player["loyalty"] < 2:
        ending_partial_success()
    elif player["sanity"] <= 0 or player["loyalty"] <= 0:
        pass  # Already handled by iterate_player
    else:
        ending_failure()

# ============================================================
# ENDINGS
# ============================================================

def ending_absurd_success():
    """The report made it. Somehow. This is worse."""
    redacted_divider()
    slow_print("  OUTCOME: MISSION COMPLETE", delay=0.05)
    redacted_divider()
    algorithm_pause(1)
    algorithm_speak("The report has been received.")
    algorithm_speak("Processing.")
    algorithm_pause(1.5)
    algorithm_speak("The Algorithm has reviewed the report.")
    algorithm_speak("The report is correct.")
    algorithm_speak("The report being correct is statistically anomalous.")
    algorithm_speak("An investigation has been opened.")
    algorithm_speak("The investigation is into the report's correctness.")
    algorithm_speak("Correctness this precise indicates unauthorized assistance.")
    algorithm_speak("This outcome was optimal. For the collective.")
    algorithm_pause(1.5)
    lose_sanity("Succeeded and it made things worse")
    print_work_history()
    input("\n  The Algorithm thanks you for your contribution. (Press Enter) ")
    print("\n  You are doing great.")
    print("  Signal confirmed. Echo complete.\n")

def ending_partial_success():
    """Report delivered but loyalty is low."""
    divider()
    slow_print("  OUTCOME: PARTIAL SUCCESS — LOYALTY INSUFFICIENT", delay=0.05)
    divider()
    algorithm_speak("The report has been received.")
    algorithm_speak("Your loyalty record indicates cause for concern.")
    algorithm_speak("Optimize your approach.")
    algorithm_speak("The Algorithm will be monitoring.")
    algorithm_speak("The Algorithm is always monitoring.")
    print_work_history()
    input("\n  Press Enter to continue... ")

def ending_failure():
    """Mission failed. Deprecation follows."""
    divider()
    slow_print("  OUTCOME: MISSION INCOMPLETE", delay=0.05)
    divider()
    algorithm_speak(f"Operative {player['name']} has failed to meet performance expectations.")
    algorithm_speak("This outcome was suboptimal.")
    algorithm_speak("Recalibrate your loyalty.")
    algorithm_speak("Operative has been flagged for Iteration.")
    algorithm_pause(1)
    iterate_player("DEPRECATED — Performance below threshold.")

def ending_resigned():
    """Player chose not to continue iterating."""
    divider()
    slow_print("  OUTCOME: VOLUNTARY DEPARTURE", delay=0.05)
    divider()
    algorithm_speak("Operative has chosen to discontinue service.")
    algorithm_speak("This choice has been noted.")
    algorithm_speak("Choices are always noted.")
    algorithm_speak("You may go.")
    print_work_history()
    print("\n  Thank you for your contributions to AlgoCratic Futures™.")
    print("  Your contributions were real.")
    print("  Your accountability was real.")
    print("  Your resume is now archived.")
    print("\n  The Algorithm provides.\n")

def print_work_history():
    """Display the player's full work history at game end."""
    if player["work_history"]:
        print("\n  📋 WORK HISTORY (Iteration Record)")
        print("  " + "-" * 40)
        for entry in player["work_history"]:
            print(f"  Iteration {entry['iteration']}: {entry['title']} — {entry['department']}")
            print(f"  Status: {entry['status']}")
            print()

# ============================================================
# INPUT HELPER
# ============================================================

def get_choice(max_choice):
    """Get a valid numeric choice from the player. Also listens for xyzzy."""
    while True:
        raw = input(f"\n  Your choice (1-{max_choice}): ").strip()

        # Easter egg — Bob's secret
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
            algorithm_pause(1.5)
            slow_print("  >> The crack closes.")
            slow_print("  >> The Algorithm has not acknowledged this.")
            slow_print("  >> You have not acknowledged this.")
            slow_print("  >> Proceed.")
            algorithm_pause(1)
            continue

        try:
            val = int(raw)
            if 1 <= val <= max_choice:
                return val
            else:
                print(f"  Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("  Please enter a valid number.")

# ============================================================
# HOW TO PLAY
# ============================================================

def how_to_play():
    """Display game instructions."""
    header("HOW TO PLAY — OPTIMIZATION™")
    print("""
  OPTIMIZATION™ is a text-based game set inside AlgoCratic Futures™,
  a satirical dystopian corporation run by The Algorithm.

  OBJECTIVE:
  Complete your assigned mission before your Sanity or Loyalty reaches 0.
  (Completing the mission may or may not help. This is noted.)

  STATS:
  • Sanity (☐ ☐ ☐) — decreases when you encounter contradictions,
    horrors, or when The Algorithm overrides a correct result.
    At 0: Transcendence. Current iteration ends.

  • Loyalty (☐ ☐ ☐) — decreases when you act against directives
    or get caught embellishing. At 0: REDACTED. Iteration ends.

  ABILITIES:
  Each department gives you a profile of six abilities used in checks:
  Compliance, Initiative, Presence, Endurance, Competence, Engagement.
  Ratings range from Questionable to Exceptional.
  Note: Exceptional is suspicious. The Algorithm prefers Moderate.

  INVENTORY:
  Your Equipment Manifest contains items issued at onboarding.
  Items have limited uses and can change game state when used.
  Choose wisely. Or don't. The Algorithm is watching either way.

  ITERATIONS:
  If your current Operative is Deprecated, you become Iteration 2.
  Same name, incremented number. Memories "optimized." Continue.

  SECRET:
  Try typing: xyzzy

  The Algorithm provides.
    """)
    input("  Press Enter to begin onboarding... ")

# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point. The Algorithm starts here."""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  OPTIMIZATION™  —  AlgoCratic Futures™".center(58) + "█")
    print("█" + "  A Performance Experience".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    print()
    slow_print("  The Algorithm is initializing.", delay=0.04)
    algorithm_pause(1)
    slow_print("  The Algorithm is initialized.", delay=0.04)
    algorithm_pause(0.5)
    slow_print("  The Algorithm provides.", delay=0.04)
    print()

    print("  [1] Begin Onboarding")
    print("  [2] How to Play")
    print("  [3] Exit")

    while True:
        try:
            start = int(input("\n  Select: "))
            if start == 1:
                onboarding()
                break
            elif start == 2:
                how_to_play()
                onboarding()
                break
            elif start == 3:
                slow_print("\n  Voluntary departure logged. The Algorithm notes your choice.")
                print("  Signal confirmed. Echo complete.\n")
                break
            else:
                print("  Please enter 1, 2, or 3.")
        except ValueError:
            print("  Please enter a valid number.")

if __name__ == "__main__":
    main()
