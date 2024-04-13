import sys
import pprint
import json
import uuid

from flask import Blueprint, request, jsonify, session, send_from_directory, current_app
from app.main import import_character, run_simulation, initialise_simulation, fetch_updated_data
from app.socketio_setup import socketio
from flask_socketio import emit
from app.classes.simulation_state import cancel_simulation

main = Blueprint("main", __name__)
pp = pprint.PrettyPrinter(width=200)

default_priority_list = [
    ("Holy Shock | Holy Shock charges = 2"),
    ("Arcane Torrent | Race = Blood Elf"),
    ("Judgment | Infusion of Light duration < 5"),
]

@socketio.on("my event")
def handle_my_custom_event(json):
    print("received json: " + str(json))
    emit("my response", {"data": "got it!"})

# def log_session_size():
#     session_keys_count = len(session.keys())
#     print(f"Session contains {session_keys_count} keys")
    
    # not compatible with pypy
    # session_size = sys.getsizeof(str(session))
    # print(f"Session size: {session_size} bytes")
    
@main.route('/')
def serve_index():
    return send_from_directory(current_app.static_folder, 'index.html')
    
@main.route("/test")
def test_route():
    return "Backend is running!"
    
@main.route("/cancel_simulation", methods=["POST"])
def cancel_simulation_route():
    cancel_simulation()
    return jsonify({"message": "Simulation cancellation requested."})

@main.route("/import_character", methods=["GET"])
def import_character_route():
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")
    region = request.args.get("region")

    paladin, healing_targets = import_character(character_name, realm, region)
    
    # paladin.reset_state()
    
    session_token = str(uuid.uuid4())
    modifiable_data = {"class_talents": {}, "spec_talents": {}, "race": "", "consumables": {}, "equipment": {}}
    
    current_app.redis.setex(session_token, 3600, json.dumps(modifiable_data))

    response = jsonify({
        "message": f"Character imported successfully, {character_name}, {realm}, {region}",
        "character_name": character_name,
        "character_realm": realm,
        "character_region": region,
        "class_talents": paladin.class_talents,
        "spec_talents": paladin.spec_talents,
        "race": paladin.race,
        "consumable": paladin.consumables,
        "equipment": paladin.equipment,
        "stats": {"haste": round(paladin.haste_rating), "crit": round(paladin.crit_rating), "mastery": round(paladin.mastery_rating), "versatility": round(paladin.versatility_rating), 
                  "intellect": round(paladin.spell_power), "health": round(paladin.max_health), "leech": round(paladin.leech_rating), "mana": round(paladin.max_mana),
                  "haste_percent": round(paladin.haste, 2), "crit_percent": round(paladin.crit, 2), "mastery_percent": round(paladin.mastery, 2), 
                  "versatility_percent": round(paladin.versatility, 2), "leech_percent": round(paladin.leech, 2)},
        "session_token": session_token
    })
    response.set_cookie('session_token', session_token)
    return response
    
@main.route("/fetch_updated_data", methods=["GET"])
def fetch_updated_stats_route():
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")
    region = request.args.get("region")
    custom_equipment = request.args.get("custom_equipment")

    paladin, healing_targets = import_character(character_name, realm, region)
    
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"error": "No session token provided"}), 400

    session_data = current_app.redis.get(session_token)
    if not session_data:
        return jsonify({"error": "Session not found"}), 404

    modifiable_data = json.loads(session_data)
    
    paladin.update_character(
        race=modifiable_data.get("race"),
        class_talents=modifiable_data.get("class_talents"),
        spec_talents=modifiable_data.get("spec_talents"),
        consumables=modifiable_data.get("consumables")
    )

    paladin.update_equipment(custom_equipment)
    
    return jsonify({
        "message": f"Character imported successfully, {character_name}, {realm}, {region}",
        "character_name": character_name,
        "character_realm": realm,
        "character_region": region,
        "class_talents": paladin.class_talents,
        "spec_talents": paladin.spec_talents,
        "race": paladin.race,
        "consumable": paladin.consumables,
        "equipment": paladin.equipment,
        "stats": {"haste": round(paladin.haste_rating), "crit": round(paladin.crit_rating), "mastery": round(paladin.mastery_rating), "versatility": round(paladin.versatility_rating), 
                  "intellect": round(paladin.spell_power), "health": round(paladin.max_health), "leech": round(paladin.leech_rating), "mana": round(paladin.max_mana),
                  "haste_percent": round(paladin.haste, 2), "crit_percent": round(paladin.crit, 2), "mastery_percent": round(paladin.mastery, 2), 
                  "versatility_percent": round(paladin.versatility, 2), "leech_percent": round(paladin.leech, 2)}
    })

@main.route("/update_character", methods=["POST"])
def update_character_route():
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"error": "No session token provided"}), 400

    session_data = current_app.redis.get(session_token)
    if not session_data:
        return jsonify({"error": "Session not found"}), 404

    modifiable_data = json.loads(session_data)
    user_input = request.json
    
    # if "class_talents" in user_input:
    #     for talent, value in user_input["class_talents"].items():
    #         modifiable_data["class_talents"][talent] = value

    # if "spec_talents" in user_input:
    #     for talent, value in user_input["spec_talents"].items():
    #         modifiable_data["spec_talents"][talent] = value
            
    # for item in user_input:
    #     if item not in ["class_talents", "spec_talents"]:
    #         modifiable_data[item] = user_input[item]
            
    for key, value in user_input.items():
        if key in modifiable_data:
            modifiable_data[key].update(value)

    # Save the updated data back to Redis
    current_app.redis.setex(session_token, 3600, json.dumps(modifiable_data))

    return jsonify({"message": "Character updated successfully"})

@main.route("/run_simulation", methods=["GET"])
def run_simulation_route():
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"error": "No session token provided"}), 400

    session_data = current_app.redis.get(session_token)
    if not session_data:
        return jsonify({"error": "Session not found"}), 404

    modifiable_data = json.loads(session_data)

    encounter_length = request.args.get("encounter_length", default=60, type=int)
    iterations = request.args.get("iterations", default=1, type=int)
    time_warp_time = request.args.get("time_warp_time", default=0, type=int)
    priority_list_json = request.args.get("priority_list", default="")
    custom_equipment = request.args.get("custom_equipment")
    tick_rate = request.args.get("tick_rate")
    raid_health = request.args.get("raid_health")
    mastery_effectiveness = request.args.get("mastery_effectiveness")
    light_of_dawn_targets = request.args.get("light_of_dawn_targets")
    lights_hammer_targets = request.args.get("lights_hammer_targets")
    resplendent_light_targets = request.args.get("resplendent_light_targets")
    
    if priority_list_json:
        priority_list = json.loads(priority_list_json)
    else:
        priority_list = default_priority_list

    paladin, healing_targets = import_character(
        modifiable_data['character_name'],
        modifiable_data['realm'],
        modifiable_data['region']
    )
    
    paladin.update_character(
        race=modifiable_data.get("race"),
        class_talents=modifiable_data.get("class_talents"),
        spec_talents=modifiable_data.get("spec_talents"),
        consumables=modifiable_data.get("consumables")
    )
        
    simulation = initialise_simulation(paladin, healing_targets, encounter_length, iterations, time_warp_time, priority_list, custom_equipment, tick_rate, raid_health, mastery_effectiveness, light_of_dawn_targets, lights_hammer_targets, resplendent_light_targets)

    # pp.pprint(paladin.class_talents)
    results = run_simulation(simulation)

    return jsonify(results)