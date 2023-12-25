from flask import Blueprint, request, jsonify
from backend.app.simulation.main import run_simulation

main = Blueprint('main', __name__)

@main.route('/simulate', methods=["GET"])
def simulate():
    character_name = request.args.get("character_name")
    realm = request.args.get("realm")
    
    if not character_name or not realm:
        return jsonify({"error": "Missing character name or realm"}), 400
    
    results = run_simulation(character_name, realm)
    return jsonify(results)