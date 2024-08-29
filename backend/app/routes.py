import pprint
import json
import uuid
import logging

from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_cors import cross_origin
from app.main import import_character

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)
pp = pprint.PrettyPrinter(width=200)
    
@main.route('/')
def serve_index():
    return send_from_directory(current_app.static_folder, "index.html")
    
@main.route("/test")
def test_route():
    return "Backend is running!"

@main.route("/import_character", methods=["GET"])
def import_character_route():
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")
    region = request.args.get("region")
    version = request.args.get("version")

    paladin, healing_targets = import_character(character_name, realm, region, version)
    
    session_token = str(uuid.uuid4())
    modifiable_data = {"class_talents": {}, "spec_talents": {}, "lightsmith_talents": {}, "herald_of_the_sun_talents": {}, "race": "", "consumables": {}, "equipment": {}, "character_name": character_name, "realm": realm, "region": region, "ptr": paladin.ptr, "version": version}
    
    current_app.redis.setex(session_token, 3600, json.dumps(modifiable_data))

    response = jsonify({
        "message": f"Character imported successfully, {character_name}, {realm}, {region}",
        "character_name": character_name,
        "character_realm": realm,
        "character_region": region,
        "class_talents": paladin.class_talents,
        "spec_talents": paladin.spec_talents,
        "lightsmith_talents": paladin.lightsmith_talents,
        "herald_of_the_sun_talents": paladin.herald_of_the_sun_talents,
        "race": paladin.race,
        "consumable": paladin.consumables,
        "equipment": paladin.equipment,
        "stats": {"haste": round(paladin.haste_rating), "crit": round(paladin.crit_rating), "mastery": round(paladin.mastery_rating), "versatility": round(paladin.versatility_rating), 
                  "intellect": round(paladin.spell_power), "health": round(paladin.max_health), "leech": round(paladin.leech_rating), "mana": round(paladin.max_mana),
                  "haste_percent": round(paladin.haste, 2), "crit_percent": round(paladin.crit, 2), "mastery_percent": round(paladin.mastery, 2), 
                  "versatility_percent": round(paladin.versatility, 2), "leech_percent": round(paladin.leech, 2)},
        "ptr": paladin.ptr,
        "session_token": session_token
    })
    response.set_cookie("session_token", session_token, samesite="None", secure=True, httponly=True)
    return response
    
@main.route("/fetch_updated_data", methods=["POST"])
@cross_origin(origins=["https://seacelery.github.io", "http://localhost:5000"], supports_credentials=True)
def fetch_updated_stats_route():
    data = request.json
    character_name = data["character_name"]
    realm = data["realm"]
    region = data["region"]
    custom_equipment = data["custom_equipment"]
    version = data["version"]

    paladin, healing_targets = import_character(character_name, realm, region, version)

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
        lightsmith_talents=modifiable_data.get("lightsmith_talents"),
        herald_of_the_sun_talents=modifiable_data.get("herald_of_the_sun_talents"),
        consumables=modifiable_data.get("consumables")
    )
    paladin.update_equipment(custom_equipment)
    
    return jsonify({
        "message": "Character updated successfully",
        "character_name": character_name,
        "character_realm": realm,
        "character_region": region,
        "class_talents": paladin.class_talents,
        "spec_talents": paladin.spec_talents,
        "race": paladin.race,
        "consumable": paladin.consumables,
        "equipment": paladin.equipment,
        "stats": {
            "haste": round(paladin.haste_rating), "crit": round(paladin.crit_rating), "mastery": round(paladin.mastery_rating), "versatility": round(paladin.versatility_rating), 
            "intellect": round(paladin.spell_power), "health": round(paladin.max_health), "leech": round(paladin.leech_rating), "mana": round(paladin.max_mana),
            "haste_percent": round(paladin.haste, 2), "crit_percent": round(paladin.crit, 2), "mastery_percent": round(paladin.mastery, 2), 
            "versatility_percent": round(paladin.versatility, 2), "leech_percent": round(paladin.leech, 2)
        },
        "ptr": paladin.ptr
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
    
    current_app.logger.debug(f"Modifiable data before update: {modifiable_data}")
    current_app.logger.debug(f"User input {user_input}")
            
    for key, value in user_input.items():
        if key in modifiable_data:
            if isinstance(modifiable_data[key], dict):
                modifiable_data[key].update(value)
            else:
                modifiable_data[key] = value

    current_app.redis.setex(session_token, 1200, json.dumps(modifiable_data))
    current_app.logger.debug(f"Modifiable data after update: {modifiable_data}")

    return jsonify({"message": "Character updated successfully"})