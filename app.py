from flask import Flask, render_template, request, g
from util import Combat
import json
import time

app = Flask(__name__)

debug = True
combatStart = False
startTime=str(time.time())

combat = None
goddesses = None
goddess_names = ['tymora', 'llira', 'loviatar', 'mielikki', 'tiamat']

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

    init = {'Tymora': 0, 'Llira': 0, 'Loviatar': 0, 'Mielikki': 0, 'Tiamat': 0, 'eli': 0, 'houdini': 0, 'kevin': 0, 'fakeKevin': 0, 'tarhun': 0, 'tobbler': 0, 'other': 0}
    if combatStart:
        init=combat.init_dict
    return render_template('initiative.html', d=init)

@app.route('/data', methods=['POST'])
def getData():
    global combat
    global goddesses
    retData = {}
    retData["reactions"] = combat.get_reactions()
    retData["currentPlayer"] = combat.get_current_player()
    retData["goddesses"] = goddesses
    log("TRANSMITTING DATA: "+json.dumps(retData))
    return retData
        

@app.route('/next_turn', methods=['POST'])
def nextTurn():
    global combat
    global goddesses
    # next turn has been clicked
    reqData = request.get_json()
    if 'data' in reqData:
        reqData = reqData['data']
    print("NEXT TURN INITIATED")
    retData = reqData

    #incrament turn
    combat.next_turn(reqData['reactions'])

    # update goddess stats for longevity
    goddesses = reqData['goddesses']

    # pass new turn data to angular
    retData['currentPlayer'] = combat.get_current_player()
    retData['reactions'] = combat.get_reactions()
    if retData['currentPlayer'].lower() in goddess_names:
        for i in range(len(goddesses)):
            print(retData['currentPlayer'].lower(), goddesses[i]['name'].lower())
            if (goddesses[i]['name'].lower() == retData['currentPlayer'].lower()):
                goddesses[i]['leg_action_rem'] = goddesses[i]['leg_action_num']
                goddesses[i]['hp'] = min(615, goddesses[i]['hp']+30)
                
        retData['aisForm'] = goddesses

    log("TRANSMITTING DATA: "+json.dumps(retData))
    return retData


@app.route('/play')
def play():
    global combatStart
    global combat
    global goddesses

    init = {}
    for key, value in request.args.items():
        init[key] = value

    if not combatStart:
        # initial initiative
        combatStart = True
        goddesses = json.load(open('./static/goddesses.json', 'r'))['goddesses']
        combat = Combat(init)
    else:
        combat.reset_initiative(init)

    print("INITIATING COMBAT\nInitiative:", combat.get_initiative())

    return render_template('play.html', reactions=combat.get_initiative())

if __name__ == "__main__":
    app.run(debug=debug)