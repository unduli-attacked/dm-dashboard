from flask import Flask, render_template, request, g
from util import Ais, Combat
import json
import time

app = Flask(__name__)

debug = True
combatStart = False
startTime=str(time.time())

combat = None
ais = None

def log(logStr):
    fl = open('log_'+startTime+'.txt', 'a')
    fl.write(str(time.time())+" | "+logStr+'\n')
    fl.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/initiative')
def initiative():
    global combatStart
    global combat

    init = {'ais': 0, 'eli': 0, 'houdini': 0, 'kevin': 0, 'fake-kevin': 0, 'tarhun': 0, 'tobbler': 0, 'other': 0}
    if combatStart:
        init=combat.init_dict
    return render_template('initiative.html', d=init)

@app.route('/data', methods=['POST'])
def getData():
    global combat
    global ais
    retData = {}
    retData["reactions"] = combat.get_reactions()
    retData["currentPlayer"] = combat.get_current_player()
    retData["aisHP"] = ais.get_HP()
    retData["aisLegResist"] = ais.get_leg_resist()
    retData["aisForm"] = ais.get_form()
    log("TRANSMITTING DATA: "+json.dumps(retData))
    return retData
        

@app.route('/next_turn', methods=['POST'])
def nextTurn():
    global combat
    global ais
    # next turn has been clicked
    reqData = request.get_json()
    if 'data' in reqData:
        reqData = reqData['data']
    print("NEXT TURN INITIATED")
    retData = reqData

    #incrament turn
    combat.next_turn(reqData['reactions'])

    # update ais stats for longevity
    ais.set_HP(reqData['aisHP'])
    ais.set_leg_resist(reqData['aisLegResist'])
    ais.set_form(reqData['aisForm'])

    # pass new turn data to angular
    retData['currentPlayer'] = combat.get_current_player()
    retData['reactions'] = combat.get_reactions()
    if retData['currentPlayer'] == 'ais':
        ais.reset_leg()
        retData['aisForm'] = ais.get_form()

    log("TRANSMITTING DATA: "+json.dumps(retData))
    return retData

@app.route('/change_form', methods=['POST'])
def changeForm():
    global combat
    global ais

    reqData = request.get_json()
    if 'data' in reqData:
        reqData = reqData['data']
    retData = reqData

    ais.set_HP(reqData['aisHP'])
    ais.set_leg_resist(reqData['aisLegResist'])
    ais.set_form(reqData['aisForm'])
    combat.set_reactions(reqData['reactions'])

    retData['aisForm'] = ais.change_form()

    log("TRANSMITTING DATA: "+json.dumps(retData))
    return retData


@app.route('/play')
def play():
    global combatStart
    global combat
    global ais

    init = {}
    for key, value in request.args.items():
        init[key] = value

    if not combatStart:
        # initial initiative
        combatStart = True
        ais = Ais()
        combat = Combat(init, ais)
    else:
        combat.reset_initiative(init)

    print("INITIATING COMBAT\nInitiative:", combat.get_initiative())

    return render_template('play.html', reactions=combat.get_initiative())

if __name__ == "__main__":
    app.run(debug=debug)