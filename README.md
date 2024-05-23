<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]

<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="frontend/public/readme-images/paladin-pink-favicon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Holy Paladin Sim</h3>

  <p align="center">
    An app that simulates healing for Holy Paladins in World of Warcraft: Dragonflight
    <br />
    <a href="https://seacelery.github.io/holy-paladin-sim/">Live website</a>

  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ul>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#license">License</a></li>
  </ul>
</details>

## About

This project started out as a tool I made for a friend who plays professionally, but the scope really grew as it became clearer just how much is left to how something feels rather than the actual numbers behind it and so I figured it was time we got some real answers. I really tried to put all of the control in the user's hands here to make it as simple or as complicated as desired, for example it can be used to quickly work out if one piece of equipment is better than another, or you can delve into the super fine details of the priority list that would otherwise be complete guesswork. 

For the technologies, I kept it simple with a Python backend and plain Javascript & CSS frontend because I really wanted to get the fundamentals down before properly learning React. I deployed it with the help of Docker, Celery workers for the simulation itself, and Redis.

Importantly, I will be keeping this maintained for the next expansion, The World Within, with many of the changes already implemented!

<img src="frontend/public/readme-images/simulation_page.png" alt="Image 5" style="width: 100%; height: auto; margin-bottom: 10px; border: 1px solid #3c3241">

<p align="right"><a href="#readme-top">back to top</a></p>

## Features

* Simulate a range of conditions to tailor your gameplay towards the encounter you're facing
* Change your character's loadout - including talents, equipment, group and external buffs
* Use a preset priority list or create your own to discover the optimal way to play in various situations
* Detailed graphs, tables, and a timeline overview of the encounter that lets you see the precise details of the simulation
* Preview many of the new changes from future patches in action to be prepared ahead of time
* Includes a standard dark mode theme & a more paladin-inspired dark mode theme

<p align="right"><a href="#readme-top">back to top</a></p>

## Usage

### Import your character
<img src="frontend/public/readme-images/import_page.png" alt="Import image">

### Options
<div>
    <img src="frontend/public/readme-images/options_page.png" alt="Options image">
</div>
<div style="margin-bottom: 5px;">
    For accuracy, always simulate with at least 100 iterations. Single iteration sims can be helpful if you just want to confirm the simulation is doing what you expect it to based on the priority list via the timeline tab.
</div>

### Talents
<div>
    <img src="frontend/public/readme-images/talents_page.png" alt="Talents image">
</div>
<div style="margin-bottom: 5px;">
    Left click an icon to add a talent point, right click to remove them.
</div>

### Equipment
<div>
    <img src="frontend/public/readme-images/equipment_page.png" alt="Equipment image">
</div>
<div style="margin-bottom: 5px;">
    Clicking on the item level in either the currently equipped or replace item boxes will allow you to change it, updating the stats to the proper values. You can add leech by clicking on an empty stat field and typing any amount you want.
</div>

### Buffs & Consumables
<div>
    <img src="frontend/public/readme-images/buffs_page.png" alt="Buffs and Consumables image">
</div>
<div style="margin-bottom: 5px;">
    Some buffs like Innervate and Power Infusion have timer options where you can set each specific timer or press the repeat button to use it on cooldown after the first specified time.
</div>

### Priority List
<div>
    <img src="frontend/public/readme-images/priolist_page.png" alt="Priority List image">
</div>
<div style="margin-bottom: 5px;">
    There are some helpful buttons in the top right to aid you in creating priority lists:
    <br>
    <br>
    Presets: 
    it's recommended to stick with a preset priority list at first as it can get very complicated. 
    <br>
    Copy: this allows you to copy your current priority list in text form.
    <br>
    Paste: here you can paste a priority list or write it from scratch, which will be displayed in the UI when it's saved.
    <br>
    Help: for when you want to create your own priority list - it contains all of the conditions and operations that can be used in the priority list, with some examples.
</div>
  
### Optionally give your simulation a name, then press Simulate and take a look at the results!

<p align="right"><a href="#readme-top">back to top</a></p>

## Installation

If you have PyPy3 installed, you can use "pypy3" in place of "python" in the following commands for a performance increase, but it's not required.

#### 1. Clone the local repository found here: https://github.com/seacelery/holy-paladin-sim-local
```bash
  git clone https://github.com/seacelery/holy-paladin-sim-local.git
  cd holy-paladin-sim-local
```
#### 2. Create & activate a virtual environment:
```bash
    python -m venv .venv
    .venv\Scripts\activate
```
#### 3. Install dependencies:
```bash
    cd backend
    pip install -r requirements.txt
```
#### 4. Obtain a free Battle.net API key from https://develop.battle.net/access/clients & create a .env file in the root directory with your client ID and client secret included:
```bash
    CLIENT_ID="your id here"
    CLIENT_SECRET="your secret here"
```
#### 5. Run the flask server:
```bash
    python run.py
```
#### 6. In a new terminal, navigate back to holy-paladin-sim-local and run an HTTP server:
```bash
    python -m http.server 5500
```
#### 7. Access the application:

Finally, go to http://127.0.0.1:5500/frontend/public/ to use the app.

<p align="right"><a href="#readme-top">back to top</a></p>

## Features to come

* Changing stats on crafted equipment
* Overhealing for each spell based on a log or user input
* Import characters from CN/KR/TW servers

<p align="right"><a href="#readme-top">back to top</a></p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

[license-shield]: https://img.shields.io/github/license/seacelery/holy-paladin-sim-local.svg?style=for-the-badge
[license-url]: https://github.com/seacelery/holy-paladin-sim-local/blob/master/LICENSE.txt