import sys
import pprint

from flask import Blueprint, request, jsonify, session
from app.main import import_character, run_simulation, initialise_simulation
from app.socketio_setup import socketio
from flask_socketio import emit

main = Blueprint("main", __name__)
pp = pprint.PrettyPrinter(width=200)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', {'data': 'got it!'})

def log_session_size():
    session_keys_count = len(session.keys())
    print(f"Session contains {session_keys_count} keys")
    
    # not compatible with pypy
    # session_size = sys.getsizeof(str(session))
    # print(f"Session size: {session_size} bytes")

@main.route("/import_character", methods=["GET"])
def import_character_route():
    session.clear()
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")

    paladin, healing_targets = import_character(character_name, realm)
    
    paladin.reset_state()
    # print("Talents")
    # pp.pprint(paladin.class_talents)
    
    session["character_name"] = character_name
    session["realm"] = realm
    
    session["modifiable_data"] = {"class_talents": {}, "spec_talents": {}, "race": "", "consumables": {}}

    return jsonify({
        "message": f"Character imported successfully, {character_name}, {realm}",
        "class_talents": paladin.class_talents,
        "spec_talents": paladin.spec_talents,
        "race": paladin.race,
        "consumable": paladin.consumables
    })

@main.route("/update_character", methods=["POST"])
def update_character_route():
    user_input = request.json
    print("User Input:", user_input)
    modifiable_data = session.get("modifiable_data", {})
    
    if "class_talents" in user_input:
        for talent, value in user_input["class_talents"].items():
            modifiable_data["class_talents"][talent] = value

    if "spec_talents" in user_input:
        for talent, value in user_input["spec_talents"].items():
            modifiable_data["spec_talents"][talent] = value
            
    for item in user_input:
        if item not in ["class_talents", "spec_talents"]:
            modifiable_data[item] = user_input[item]
            
    print(modifiable_data)
    session["modifiable_data"] = modifiable_data
    log_session_size()

    return jsonify({"message": "Character updated successfully"})

@main.route("/run_simulation", methods=["GET"])
def run_simulation_route():
    character_name = session.get("character_name")
    realm = session.get("realm")

    if not character_name or not realm:
        return jsonify({"error": "Character name or realm not found in session"}), 400

    encounter_length = request.args.get("encounter_length", default=60, type=int)
    iterations = request.args.get("iterations", default=1, type=int)
    time_warp_time = request.args.get("time_warp_time", default=0, type=int)

    paladin, healing_targets = import_character(character_name, realm)
    
    print(session["modifiable_data"])
    
    modifiable_data = session.get("modifiable_data", {})
    paladin.update_character(
        race=modifiable_data.get("race"),
        class_talents=modifiable_data.get("class_talents"),
        spec_talents=modifiable_data.get("spec_talents"),
        consumables=modifiable_data.get("consumables")
    )
        
    simulation = initialise_simulation(paladin, healing_targets, encounter_length, iterations, time_warp_time)

    # pp.pprint(paladin.class_talents)
    results = run_simulation(simulation)

    return jsonify(results)