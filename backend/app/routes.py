import sys
from flask import Blueprint, request, jsonify, session
from app.main import import_character, run_simulation, initialise_simulation

main = Blueprint("main", __name__)

def log_session_size():
    session_size = sys.getsizeof(str(session))
    print(f"Session size: {session_size} bytes")

@main.route("/import_character", methods=["GET"])
def import_character_route():
    session.clear()
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")

    paladin, healing_targets = import_character(character_name, realm)
    
    session["character_name"] = character_name
    session["realm"] = realm
    
    session["modifiable_data"] = {"spec_talents": {}, "race": ""}

    return jsonify({
        "message": f"Character imported successfully, {character_name}, {realm}",
        "spec_talents": paladin.spec_talents,
        "race": paladin.race,
    })

@main.route("/update_character", methods=["POST"])
def update_character_route():
    user_input = request.json
    # print("User Input:", user_input)
    modifiable_data = session.get("modifiable_data", {})
    # print(modifiable_data)
    
    if "spec_talents" in user_input:
        for talent, value in user_input["spec_talents"].items():
            modifiable_data["spec_talents"][talent] = value
    else:
        modifiable_data.update(user_input)
    # print(modifiable_data)
    session["modifiable_data"] = modifiable_data
    # print(session["modifiable_data"]["talents"])
    log_session_size()

    return jsonify({"message": "Character updated successfully"})

@main.route("/run_simulation", methods=["GET"])
def run_simulation_route():
    character_name = session.get("character_name")
    realm = session.get("realm")

    if not character_name or not realm:
        return jsonify({"error": "Character name or realm not found in session"}), 400

    encounter_length = request.args.get("encounter_length", default=30, type=int)
    iterations = request.args.get("iterations", default=1, type=int)

    paladin, healing_targets = import_character(character_name, realm)
    
    if "race" in session["modifiable_data"]:
        paladin.update_race(session["modifiable_data"]["race"])
    if "spec_talents" in session["modifiable_data"]:
        paladin.update_talents(session["modifiable_data"]["spec_talents"])
        
    simulation = initialise_simulation(paladin, healing_targets, encounter_length, iterations)

    results = run_simulation(simulation)

    return jsonify(results)