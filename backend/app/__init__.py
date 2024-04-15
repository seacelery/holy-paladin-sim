import os
import sys
import json
from flask import Flask, current_app
import redis
import certifi
import pickle
from app.routes import main as main_blueprint
from app.main import import_character
import logging
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from celery_config import make_celery
import eventlet

# from app.classes.run_simulation_task import run_simulation_task
from app.classes.simulation import Simulation, check_cancellation, reset_simulation

app = Flask(__name__, static_url_path="", static_folder="../../docs")

os.environ['REDIS_TLS_URL'] = 'rediss://:p07047fba795b7692e9c289c32b9129f04db91f5a51dadc7949bc932ea6d05bc0@ec2-34-250-232-88.eu-west-1.compute.amazonaws.com:10760'

app.config["REDIS_TLS_URL"] = os.getenv("REDIS_TLS_URL")
app.redis = redis.Redis.from_url(
    app.config["REDIS_TLS_URL"],
    ssl_cert_reqs='none'
)

app.config.update(
    CELERY_BROKER_URL=app.config["REDIS_TLS_URL"] + '?ssl_cert_reqs=none',
    CELERY_RESULT_BACKEND=app.config["REDIS_TLS_URL"] + '?ssl_cert_reqs=none',
)

print(app.config["CELERY_BROKER_URL"])
sys.stdout.flush()
print(app.config["CELERY_RESULT_BACKEND"])
sys.stdout.flush()

app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_key")

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

CORS(app, supports_credentials=True, origins=["https://seacelery.github.io"], allow_headers=[
    "Content-Type", "Authorization", "X-Requested-With"], allow_methods=["GET", "POST", "OPTIONS"])

app.register_blueprint(main_blueprint)

# Initialize Celery
celery = make_celery(app)
print("Initializing Celery in app:", celery)
sys.stdout.flush()

def create_app():
    return app

def create_socketio(app):
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", logger=True, engineio_logger=True)
    register_socketio_events(socketio)
    return socketio

def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('start_simulation')
    def handle_start_simulation(data):
        # session_token = data.get('session_token')
        # print(f"data received {session_token}")
        # sys.stdout.flush()
        # run_simulation_task.delay()
        session_token = data.get('session_token')
        print(f"data received {session_token}")
        sys.stdout.flush()
        if not session_token:
            emit('error', {"error": "No session token provided"})
            return

        session_data = current_app.redis.get(session_token)
        if not session_data:
            emit('error', {"error": "Session not found"})
            return

        modifiable_data = json.loads(session_data)

        # Assuming import_character and other functions are accessible here
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

        paladin_pickled = pickle.dumps(paladin)
        healing_targets_pickled = pickle.dumps(healing_targets)

        simulation_params = {
            "paladin": paladin_pickled,
            "healing_targets_list": healing_targets_pickled,
            "encounter_length": int(data['encounter_length']),
            "iterations": int(data['iterations']),
            "time_warp_time": int(data['time_warp_time']),
            "priority_list": data["priority_list"],
            "custom_equipment": data["custom_equipment"],
            "tick_rate": float(data['tick_rate']),
            "raid_health": int(data['raid_health']),
            "mastery_effectiveness": int(data['mastery_effectiveness']),
            "light_of_dawn_targets": int(data['light_of_dawn_targets']),
            "lights_hammer_targets": int(data['lights_hammer_targets']),
            "resplendent_light_targets": int(data['resplendent_light_targets']),
        }

        print("Emitting simulation complete event.")
        sys.stdout.flush()
        result = run_simulation_task.delay(simulation_parameters=simulation_params)
        emit('simulation_started', {'message': "Simulation started successfully, monitor progress via WebSocket.", 'task_id': str(result.id)})

@celery.task
def process_paladin(paladin_data):
    # Deserialize the Paladin object
    paladin = pickle.loads(paladin_data)
    # Here you can add the code to process the Paladin object
    # For example, simulate or calculate results
    return paladin

@celery.task(bind=True)
def run_simulation_task(self, simulation_parameters):
    print("Simulation task RUNNING")
    sys.stdout.flush()
    app = current_app._get_current_object()
    socketio = SocketIO(app, async_mode='eventlet')
    
    simulation = Simulation(**simulation_parameters)
    
    paladin_pickled = simulation_parameters.pop('paladin_pickled')
    paladin = pickle.loads(paladin_pickled)
    simulation_parameters['paladin'] = paladin
    
    healing_targets_pickled = simulation_parameters.pop('healing_targets_pickled')
    healing_targets = pickle.loads(healing_targets_pickled)
    simulation_parameters['healing_targets_list'] = healing_targets
        
    full_ability_breakdown_results = {}
    full_self_buff_breakdown_results = {}
    full_target_buff_breakdown_results= {}
    full_aggregated_target_buff_breakdown_results = {}
    full_glimmer_count_results = {}
    full_tyrs_count_results = {}
    full_awakening_count_results = {}
    full_healing_timeline_results = {}
    full_mana_timeline_results = {}
    full_holy_power_timeline_results = {}
    full_cooldowns_breakdown_results = {}
    
    full_awakening_trigger_times_results = {}

    # first spell belongs to the second
    sub_spell_map = {
            "Reclamation (Holy Shock)": "Holy Shock",
            "Reclamation (Crusader Strike)": "Crusader Strike",
            "Divine Revelations (Holy Light)": "Holy Light",
            "Divine Revelations (Judgment)": "Judgment",
            "Holy Shock (Divine Toll)": "Divine Toll",
            "Holy Shock (Divine Resonance)": "Divine Toll",
            "Holy Shock (Rising Sunlight)": "Daybreak",
            "Glimmer of Light": "Holy Shock",
            "Glimmer of Light (Daybreak)": "Daybreak",
            "Glimmer of Light (Rising Sunlight)": "Holy Shock (Rising Sunlight)",
            "Glimmer of Light (Glistening Radiance (Light of Dawn))": "Light of Dawn",
            "Glimmer of Light (Glistening Radiance (Word of Glory))": "Word of Glory",
            "Glimmer of Light (Divine Toll)": "Holy Shock (Divine Toll)",
            "Resplendent Light": "Holy Light",
            "Crusader's Reprieve": "Crusader Strike",
            "Greater Judgment": "Judgment",
            "Judgment of Light": "Judgment",
            "Afterimage": "Word of Glory",
            "Barrier of Faith (Holy Shock)": "Barrier of Faith",
            "Barrier of Faith (Flash of Light)": "Barrier of Faith",
            "Barrier of Faith (Holy Light)": "Barrier of Faith",
            "Blessing of Summer": "Blessing of the Seasons",
            "Blessing of Autumn": "Blessing of the Seasons",
            "Blessing of Winter": "Blessing of the Seasons",
            "Blessing of Spring": "Blessing of the Seasons",
            "Blossom of Amirdrassil Large HoT": "Blossom of Amirdrassil",
            "Blossom of Amirdrassil Small HoT": "Blossom of Amirdrassil",
            "Blossom of Amirdrassil Absorb": "Blossom of Amirdrassil",
            "Veneration": "Hammer of Wrath",
            "Golden Path": "Consecration",
            "Seal of Mercy": "Consecration",
            "Avenging Crusader (Judgment)": "Avenging Crusader",
            "Avenging Crusader (Crusader Strike)": "Avenging Crusader",
        }
    
    # complete all simulation iterations and process the data of each
    for i in range(simulation.iterations):
        if check_cancellation():
            reset_simulation()
            return
        
        # reset simulation states
        print(i)
        if not simulation.test:
            socketio.emit("iteration_update", {"iteration": i + 1}, broadcast=True, namespace="/")
            simulation.paladin.reset_state()
            simulation.reset_simulation()
            simulation.paladin.apply_consumables()
            simulation.paladin.apply_item_effects()
            simulation.paladin.apply_buffs_on_encounter_start()
            
        eventlet.sleep(0)
        
        # only record some data on the last iteration
        if i == simulation.iterations - 1:
            simulation.paladin.last_iteration = True
            
        simulation.simulate()
        
        simulation.update_final_cooldowns_breakdown_times()
        
        ability_breakdown = simulation.paladin.ability_breakdown
        self_buff_breakdown = simulation.paladin.self_buff_breakdown
        target_buff_breakdown = simulation.paladin.target_buff_breakdown
        glimmer_counts = simulation.paladin.glimmer_counts
        tyrs_counts = simulation.paladin.tyrs_counts
        awakening_counts = simulation.paladin.awakening_counts
        healing_timeline = simulation.paladin.healing_timeline
        mana_timeline = simulation.paladin.mana_timeline
        holy_power_timeline = simulation.paladin.holy_power_timeline
        cooldowns_breakdown = simulation.aura_healing
        
        # accumulate cooldown breakdown results
        for aura, instances in cooldowns_breakdown.items():
            for instance_number, data in instances.items():
                if aura not in full_cooldowns_breakdown_results:
                    full_cooldowns_breakdown_results[aura] = {}
                if instance_number not in full_cooldowns_breakdown_results[aura]:
                    full_cooldowns_breakdown_results[aura][instance_number] = {"total_healing": 0, "total_duration": 0, "start_time": 0, "end_time": 0, "count": 0}

                full_cooldowns_breakdown_results[aura][instance_number]["total_healing"] += data["total_healing"]
                full_cooldowns_breakdown_results[aura][instance_number]["count"] += 1

                if data["end_time"] is not None and data["start_time"] is not None:
                    duration = data["end_time"] - data["start_time"]
                    full_cooldowns_breakdown_results[aura][instance_number]["total_duration"] += duration
                    full_cooldowns_breakdown_results[aura][instance_number]["start_time"] += data["start_time"]
                    full_cooldowns_breakdown_results[aura][instance_number]["end_time"] += data["end_time"]
        
        # accumulate awakening trigger results
        for key, value in simulation.paladin.awakening_trigger_times.items():
            full_awakening_trigger_times_results[key] = full_awakening_trigger_times_results.get(key, 0) + value
        
        # PROCESS ABILITY HEALING
        def add_sub_spell_healing(primary_spell_data):
            total_healing = primary_spell_data.get("total_healing", 0)

            for sub_spell_name, sub_spell_data in primary_spell_data.get('sub_spells', {}).items():
                total_healing += sub_spell_data.get("total_healing", 0)
                
                # add healing and hits from nested sub-spells
                for nested_sub_spell_data in sub_spell_data.get("sub_spells", {}).values():
                    total_healing += nested_sub_spell_data.get("total_healing", 0)

            return total_healing
        
        def combine_beacon_sources_by_prefix(prefix, beacon_sources):
            combined_source = {
                "healing": 0,
                "hits": 0
            }
            keys_to_delete = []

            for spell, data in beacon_sources.items():
                if spell.startswith(prefix):
                    combined_source["healing"] += data["healing"]
                    combined_source["hits"] += data["hits"]
                    keys_to_delete.append(spell)

            for key in keys_to_delete:
                del beacon_sources[key]

            beacon_sources[prefix] = combined_source
        
        def add_spell_if_sub_spell_but_no_casts(main_spell, sub_spell):
            if sub_spell in ability_breakdown and main_spell not in ability_breakdown:
                ability_breakdown[main_spell] = {
                    "total_healing": 0,
                    "casts": 0,
                    "hits": 0,
                    "targets": {},
                    "crits": 0,
                    "mana_spent": 0,
                    "mana_gained": 0,
                    "holy_power_gained": 0,
                    "holy_power_spent": 0,
                    "holy_power_wasted": 0,
                    "sub_spells": {},
                    "source_spells": {}
                } 
            
        add_spell_if_sub_spell_but_no_casts("Consecration", "Golden Path")
        add_spell_if_sub_spell_but_no_casts("Avenging Crusader", "Avenging Crusader (Judgment)")
        add_spell_if_sub_spell_but_no_casts("Avenging Crusader", "Avenging Crusader (Crusader Strike)")
        
        # process data to include crit percent
        for spell, data in ability_breakdown.items():
            if data["hits"] > data["casts"]:
                data["crit_percent"] = round((data["crits"] / data["hits"]) * 100, 1)
            else:
                data["crit_percent"] = round((data["crits"] / data["casts"]) * 100, 1) if data["casts"] > 0 else 0
                    
            for target, target_data in data["targets"].items():
                target_data["crit_percent"] = round((target_data["crits"] / target_data["casts"]) * 100, 1) if target_data["casts"] > 0 else 0
        
        # assign sub-spell data to primary spell
        for spell, data in ability_breakdown.items():
            if spell in sub_spell_map:
                primary_spell = sub_spell_map[spell]
                ability_breakdown[primary_spell]["sub_spells"][spell] = data
        
        for primary_spell, primary_data in ability_breakdown.items():
            if primary_spell in sub_spell_map.values():
                # add sub-spell healing to the primary spell's healing
                primary_data["total_healing"] = add_sub_spell_healing(primary_data)
                
                # total crits and hits required for crit percent calculation  
                total_crits = primary_data.get("crits", 0)
                total_hits = primary_data.get("hits", 0)
                total_mana_gained = primary_data.get("mana_gained", 0)
                total_holy_power_gained = primary_data.get("holy_power_gained", 0)
                total_holy_power_wasted = primary_data.get("holy_power_wasted", 0)
                if primary_spell == "Blessing of the Seasons":
                    total_mana_spent = primary_data.get("mana_spent", 0)
                    total_casts = primary_data.get("casts", 0)

                for sub_spell_data in primary_data.get("sub_spells", {}).values():
                    total_crits += sub_spell_data.get("crits", 0)
                    total_hits += sub_spell_data.get("hits", 0)
                    total_mana_gained += sub_spell_data.get("mana_gained", 0)
                    total_holy_power_gained += sub_spell_data.get("holy_power_gained", 0)
                    total_holy_power_wasted += sub_spell_data.get("holy_power_wasted", 0)
                    if primary_spell == "Blessing of the Seasons":
                        total_mana_spent += sub_spell_data.get("mana_spent", 0)
                        total_casts += sub_spell_data.get("casts", 0)

                    for nested_sub_spell_data in sub_spell_data.get("sub_spells", {}).values():
                        total_crits += nested_sub_spell_data.get("crits", 0)
                        total_hits += nested_sub_spell_data.get("hits", 0)
                        total_mana_gained += nested_sub_spell_data.get("mana_gained", 0)
                        total_holy_power_gained += nested_sub_spell_data.get("holy_power_gained", 0)
                        total_holy_power_wasted += nested_sub_spell_data.get("holy_power_wasted", 0)
                    
                # display holy power for a spell as the sum of its sub-spells
                primary_data["mana_gained"] = total_mana_gained
                primary_data["holy_power_gained"] = total_holy_power_gained
                primary_data["holy_power_wasted"] = total_holy_power_wasted
                if primary_spell == "Blessing of the Seasons":
                    primary_data["mana_spent"] = total_mana_spent
                    primary_data["casts"] = total_casts
                
                # this line is responsible for whether the crit percent propagates back up the table
                # primary_data["crit_percent"] = round((total_crits / total_hits) * 100, 1) if total_hits > 0 else 0
        
        # remove the primary spell data for sub-spells        
        for spell in [
            "Holy Shock (Divine Toll)", "Holy Shock (Divine Resonance)", "Holy Shock (Rising Sunlight)" , "Glimmer of Light", 
            "Glimmer of Light (Daybreak)", "Glimmer of Light (Rising Sunlight)", "Glimmer of Light (Divine Toll)", 
            "Glimmer of Light (Glistening Radiance (Light of Dawn))", "Glimmer of Light (Glistening Radiance (Word of Glory))", 
            "Resplendent Light", "Greater Judgment", "Judgment of Light", "Crusader's Reprieve", "Afterimage", "Reclamation (Holy Shock)", 
            "Reclamation (Crusader Strike)", "Divine Revelations (Holy Light)", "Divine Revelations (Judgment)", "Blessing of Summer", 
            "Blessing of Autumn", "Blessing of Winter", "Blessing of Spring", "Blossom of Amirdrassil Absorb", "Blossom of Amirdrassil Large HoT", 
            "Blossom of Amirdrassil Small HoT", "Barrier of Faith (Holy Shock)", "Barrier of Faith (Flash of Light)", "Barrier of Faith (Holy Light)", 
            "Veneration", "Golden Path", "Seal of Mercy", "Avenging Crusader (Judgment)", "Avenging Crusader (Crusader Strike)"
            ]:
            if spell in ability_breakdown:
                del ability_breakdown[spell]
                        
        # combine beacon glimmer sources into one spell
        if "Beacon of Light" in ability_breakdown:
            beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]   
            combine_beacon_sources_by_prefix("Glimmer of Light", beacon_source_spells)
            combine_beacon_sources_by_prefix("Holy Shock", beacon_source_spells)
        
        excluded_spells = ["Divine Toll", "Daybreak", "Judgment", "Crusader Strike"]
        
        for spell in ability_breakdown:
            if spell not in excluded_spells:
                total_sub_spell_healing = 0
                sub_spells = ability_breakdown[spell]["sub_spells"]
                
                for sub_spell in sub_spells:
                    total_sub_spell_healing += sub_spells[sub_spell]["total_healing"]
                
                if total_sub_spell_healing > 0:   
                    sub_spells[spell] = {
                        "total_healing": 0,
                        "casts": 0,
                        "hits": 0,
                        "targets": {},
                        "crits": 0,
                        "mana_spent": 0,
                        "mana_gained": 0,
                        "holy_power_gained": 0,
                        "holy_power_spent": 0,
                        "holy_power_wasted": 0,
                        "sub_spells": {}
                    }
                    
                    sub_spells[spell]["total_healing"] = ability_breakdown[spell]["total_healing"] - total_sub_spell_healing
                    sub_spells[spell]["casts"] = ability_breakdown[spell]["casts"]
                    sub_spells[spell]["hits"] = ability_breakdown[spell]["hits"]
                    sub_spells[spell]["targets"] = ability_breakdown[spell]["targets"]
                    sub_spells[spell]["crits"] = ability_breakdown[spell]["crits"]
                    sub_spells[spell]["crit_percent"] = ability_breakdown[spell]["crit_percent"]
                    sub_spells[spell]["mana_spent"] = ability_breakdown[spell]["mana_spent"]
                    sub_spells[spell]["mana_gained"] = ability_breakdown[spell]["mana_gained"]
                    sub_spells[spell]["holy_power_gained"] = ability_breakdown[spell]["holy_power_gained"]
                    sub_spells[spell]["holy_power_spent"] = ability_breakdown[spell]["holy_power_spent"]
                    sub_spells[spell]["holy_power_wasted"] = ability_breakdown[spell]["holy_power_wasted"]
        
        for spell in ability_breakdown:
            total_sub_sub_spell_healing = 0
            sub_spells = ability_breakdown[spell]["sub_spells"]
            
            for sub_spell in sub_spells:
                sub_sub_spells = sub_spells[sub_spell]["sub_spells"]
                if len(sub_sub_spells) > 0:
                    for sub_sub_spell in sub_sub_spells:
                        total_sub_sub_spell_healing += sub_sub_spells[sub_sub_spell]["total_healing"]      
                        
                    if total_sub_spell_healing > 0:   
                        sub_sub_spells[sub_spell] = {
                            "total_healing": 0,
                            "casts": 0,
                            "hits": 0,
                            "targets": {},
                            "crits": 0,
                            "mana_spent": 0,
                            "mana_gained": 0,
                            "holy_power_gained": 0,
                            "holy_power_spent": 0,
                            "holy_power_wasted": 0,
                            "sub_spells": {}
                        }
                        
                        sub_sub_spells[sub_spell]["total_healing"] = sub_spells[sub_spell]["total_healing"] - total_sub_sub_spell_healing
                        sub_sub_spells[sub_spell]["casts"] = sub_spells[sub_spell]["casts"]
                        sub_sub_spells[sub_spell]["hits"] = sub_spells[sub_spell]["hits"]
                        sub_sub_spells[sub_spell]["targets"] = sub_spells[sub_spell]["targets"]
                        sub_sub_spells[sub_spell]["crits"] = sub_spells[sub_spell]["crits"]
                        sub_sub_spells[sub_spell]["crit_percent"] = sub_spells[sub_spell]["crit_percent"]
                        sub_sub_spells[sub_spell]["mana_spent"] = sub_spells[sub_spell]["mana_spent"]
                        sub_sub_spells[sub_spell]["mana_gained"] = sub_spells[sub_spell]["mana_gained"]
                        sub_sub_spells[sub_spell]["holy_power_gained"] = sub_spells[sub_spell]["holy_power_gained"]
                        sub_sub_spells[sub_spell]["holy_power_spent"] = sub_spells[sub_spell]["holy_power_spent"]
                        sub_sub_spells[sub_spell]["holy_power_wasted"] = sub_spells[sub_spell]["holy_power_wasted"]
        
        # remove spells that aren't actually spells but have subspells               
        for spell in ["Blossom of Amirdrassil", "Hammer of Wrath", "Consecration", "Avenging Crusader"]:
            if spell in ability_breakdown:
                if spell in ability_breakdown[spell]["sub_spells"]:
                    del ability_breakdown[spell]["sub_spells"][spell]
        
        # PROCESS BUFFS                
        def process_buff_data(events):
            def add_time(buff_name, time):
                if buff_name in buff_summary:
                    buff_summary[buff_name]["total_duration"] += time
                    buff_summary[buff_name]["uptime"] += time / simulation.encounter_length
                    buff_summary[buff_name]["count"] += 1
                else:
                    buff_summary[buff_name] = {"total_duration": time, "uptime": time / simulation.encounter_length, "count": 1, "average_duration": 0}
            
            buff_summary = {}
            active_buffs = {}
            
            for event in events:
                buff_name = event["buff_name"]
                event_time = event["time"]
                event_type = event["type"]
                
                if event_type == "applied":
                    if buff_name in active_buffs:
                        active_duration = event_time - active_buffs.pop(buff_name)
                        add_time(buff_name, active_duration)
                        active_buffs[buff_name] = event_time
                    else:
                        active_buffs[buff_name] = event_time
                elif event_type == "expired":
                    if buff_name in active_buffs:
                        active_duration = event_time - active_buffs.pop(buff_name)
                        add_time(buff_name, active_duration)
                    
            for buff_name, start_time in active_buffs.items():
                active_duration = simulation.encounter_length - start_time
                add_time(buff_name, active_duration)

            for buff in buff_summary:
                buff_summary[buff]["average_duration"] = buff_summary[buff]["total_duration"] / buff_summary[buff]["count"]
            
            return buff_summary
        
        # include targets separately
        def process_target_buff_data(events):
            def add_time(buff_name, target, time):
                if buff_name not in buff_summary:
                    buff_summary[buff_name] = {}
                if target not in buff_summary[buff_name]:
                    buff_summary[buff_name][target] = {
                        "total_duration": 0, 
                        "uptime": 0, 
                        "count": 0, 
                        "average_duration": 0
                    }
                buff_summary[buff_name][target]["total_duration"] += time
                buff_summary[buff_name][target]["uptime"] += time / simulation.encounter_length
                buff_summary[buff_name][target]["count"] += 1

            buff_summary = {}
            active_buffs = {}

            for event in events:
                buff_name = event["buff_name"]
                target = event["target"]
                event_time = event["time"]
                event_type = event["type"]
                key = (buff_name, target)

                if event_type == "applied":
                    if key in active_buffs:
                        active_duration = event_time - active_buffs.pop(key)
                        add_time(buff_name, target, active_duration)
                    active_buffs[key] = event_time
                elif event_type == "expired":
                    if key in active_buffs:
                        active_duration = event_time - active_buffs.pop(key)
                        add_time(buff_name, target, active_duration)

            for key, start_time in active_buffs.items():
                buff_name, target = key
                active_duration = simulation.encounter_length - start_time
                add_time(buff_name, target, active_duration)

            for buff_name in buff_summary:
                for target in buff_summary[buff_name]:
                    buff_data = buff_summary[buff_name][target]
                    buff_data["average_duration"] = buff_data["total_duration"] / buff_data["count"]

            return buff_summary
        
        # include all targets combined
        def process_aggregated_target_buff_data(events):
            def add_time(buff_name, time):
                if buff_name in buff_summary:
                    buff_summary[buff_name]["total_duration"] += time
                    buff_summary[buff_name]["uptime"] += time / simulation.encounter_length
                    buff_summary[buff_name]["count"] += 1
                else:
                    buff_summary[buff_name] = {"total_duration": time, "uptime": time / simulation.encounter_length, "count": 1, "average_duration": 0}
            
            buff_summary = {}
            active_buffs = {}
            
            for event in events:
                buff_name = event["buff_name"]
                event_time = event["time"]
                event_type = event["type"]
                target = event["target"]
                
                if event_type == "applied":
                    if buff_name in active_buffs:
                        active_duration = event_time - active_buffs.pop(buff_name)[0]
                        add_time(buff_name, active_duration)
                        active_buffs[buff_name] = [event_time, target]
                    else:
                        active_buffs[buff_name] = [event_time, target]
                elif event_type == "expired":
                    if buff_name in active_buffs:
                        if target in active_buffs[buff_name]:
                            active_duration = event_time - active_buffs.pop(buff_name)[0]
                            add_time(buff_name, active_duration)
                        
            for buff_name, start_time in active_buffs.items():
                active_duration = simulation.encounter_length - start_time[0]
                add_time(buff_name, active_duration)

            for buff in buff_summary:
                buff_summary[buff]["average_duration"] = buff_summary[buff]["total_duration"] / buff_summary[buff]["count"]
            
            return buff_summary
        
        # COLLECT RESULTS FOR ALL ITERATIONS
        full_ability_breakdown_results.update({f"iteration {i}": ability_breakdown})
        
        self_buff_summary = process_buff_data(self_buff_breakdown)
        full_self_buff_breakdown_results.update({f"iteration {i}": self_buff_summary})
        
        target_buff_summary = process_target_buff_data(target_buff_breakdown)
        full_target_buff_breakdown_results.update({f"iteration {i}": target_buff_summary})
        
        aggregated_target_buff_summary = process_aggregated_target_buff_data(target_buff_breakdown)
        full_aggregated_target_buff_breakdown_results.update({f"iteration {i}": aggregated_target_buff_summary})
        
        full_glimmer_count_results.update({f"iteration {i}": glimmer_counts})
        full_tyrs_count_results.update({f"iteration {i}": tyrs_counts})
        full_awakening_count_results.update({f"iteration {i}": awakening_counts})
        
        full_healing_timeline_results.update({f"iteration {i}": healing_timeline})
        full_mana_timeline_results.update({f"iteration {i}": mana_timeline})
        full_holy_power_timeline_results.update({f"iteration {i}": holy_power_timeline})
    
    # COMBINE AND AVERAGE ALL KEYS OVER ITERATIONS       
    def combine_results(*dicts):
        def add_dicts(d1, d2):
            for key in d2:
                if key in d1:
                    if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                        add_dicts(d1[key], d2[key])
                    elif isinstance(d1[key], (int, float)) and isinstance(d2[key], (int, float)):
                        d1[key] += d2[key]
                else:
                    d1[key] = d2[key]

        combined_results = {}
        for d in dicts:
            add_dicts(combined_results, d)
        return combined_results
    
    def get_all_iterations_results(full_ability_breakdown_results):
        iteration_results = [value for key, value in full_ability_breakdown_results.items() if key.startswith("iteration")]
        return iteration_results

    def average_out_simulation_results(simulation_results, iterations):
        for key in simulation_results:
            if isinstance(simulation_results[key], dict):
                average_out_simulation_results(simulation_results[key], iterations)
            elif isinstance(simulation_results[key], (int, float)):
                simulation_results[key] /= iterations
                
        return simulation_results
    
    def return_complete_combined_results(full_results):
        all_iteration_results = get_all_iterations_results(full_results)
        combined_results = combine_results(*all_iteration_results)
        return average_out_simulation_results(combined_results, simulation.iterations)
        
    average_ability_breakdown = return_complete_combined_results(full_ability_breakdown_results)
    average_self_buff_breakdown = return_complete_combined_results(full_self_buff_breakdown_results)
    average_target_buff_breakdown = return_complete_combined_results(full_target_buff_breakdown_results)
    average_aggregated_target_buff_breakdown = return_complete_combined_results(full_aggregated_target_buff_breakdown_results)
    average_glimmer_counts = return_complete_combined_results(full_glimmer_count_results)
    average_tyrs_counts = return_complete_combined_results(full_tyrs_count_results)
    average_awakening_counts = return_complete_combined_results(full_awakening_count_results)
    average_healing_timeline = return_complete_combined_results(full_healing_timeline_results)
    average_mana_timeline = return_complete_combined_results(full_mana_timeline_results)
    average_holy_power_timeline = return_complete_combined_results(full_holy_power_timeline_results)
    
    # calculate average hps
    total_healing = 0
    for ability in average_ability_breakdown:
        total_healing += average_ability_breakdown[ability]["total_healing"]
    average_hps = total_healing / simulation.encounter_length
    
    # adjust cooldowns breakdown for number of iterations
    for aura, instances in full_cooldowns_breakdown_results.items():
        for instance, details in instances.items():
            details["total_duration"] /= details["count"]
            details["total_healing"] /= details["count"]
            details["hps"] = details["total_healing"] / details["total_duration"]
            details["start_time"] /= details["count"]
            details["end_time"] /= details["count"]
    
    # adjust healing timeline from tick rate increments to integers
    adjusted_average_healing_timeline = {}        
    for timestamp, healing in average_healing_timeline.items():
        rounded_time = int(timestamp)
        adjusted_average_healing_timeline[rounded_time] = adjusted_average_healing_timeline.get(rounded_time, 0) + healing
    
    full_results = {
        "healing_timeline": adjusted_average_healing_timeline,
        "mana_timeline": average_mana_timeline,
        "holy_power_timeline": average_holy_power_timeline,
        "ability_breakdown": average_ability_breakdown,
        "self_buff_breakdown": average_self_buff_breakdown,
        "target_buff_breakdown": average_target_buff_breakdown,
        "aggregated_target_buff_breakdown": average_aggregated_target_buff_breakdown,
        "glimmer_counts": average_glimmer_counts,
        "tyrs_counts": average_tyrs_counts,
        "awakening_counts": average_awakening_counts,
        "awakening_triggers": full_awakening_trigger_times_results,
        "priority_breakdown": simulation.paladin.priority_breakdown,
        "cooldowns_breakdown": full_cooldowns_breakdown_results
    }
    
    simulation_details = {
        "encounter_length": simulation.encounter_length,
        "paladin_name": simulation.paladin.name,
        "iterations": simulation.iterations,
        "max_mana": simulation.paladin.max_mana,
        "average_hps": average_hps,
        "equipment": simulation.paladin.equipment,
        # "stats": simulation.paladin.stats_after_buffs
        "stats": {"haste": round(simulation.paladin.haste_rating), "crit": round(simulation.paladin.crit_rating), "mastery": round(simulation.paladin.mastery_rating), "versatility": round(simulation.paladin.versatility_rating), 
                "intellect": round(simulation.paladin.spell_power), "health": round(simulation.paladin.max_health), "leech": round(simulation.paladin.leech_rating), "mana": round(simulation.paladin.max_mana),
                "haste_percent": round(simulation.paladin.haste, 2), "crit_percent": round(simulation.paladin.crit, 2), "mastery_percent": round(simulation.paladin.mastery, 2), 
                "versatility_percent": round(simulation.paladin.versatility, 2), "leech_percent": round(simulation.paladin.leech, 2)},
        "talents": {"class_talents": simulation.paladin.class_talents, "spec_talents": simulation.paladin.spec_talents},
        "priority_list": simulation.priority_list_text
    }

    print("Emitting simulation complete event.")
    sys.stdout.flush()
    socketio.emit("simulation_complete", full_results, namespace="/")
    return {"results": full_results, "simulation_details": simulation_details}

# import os

# from flask import Flask
# from flask_cors import CORS
# from .socketio_setup import socketio
# from app.routes import main as main_blueprint

# flask_secret_key = os.getenv("FLASK_SECRET_KEY")

# import logging

# logging.basicConfig(level=logging.DEBUG)

# def create_app():
#     app = Flask(__name__, static_url_path='', static_folder='../../docs')
#     app.logger.setLevel(logging.DEBUG)
#     app.secret_key = flask_secret_key
#     CORS(app, supports_credentials=True)
#     app.register_blueprint(main_blueprint)
    
#     socketio.init_app(app)
#     return app