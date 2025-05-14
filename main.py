from flask import Flask, render_template, request


app = Flask(__name__)

account_balances = [
    {'id': "100", 'amount': 20},
    {'id':"200", 'amount' :50},
    {'id':"300", 'amount': 0}
]

def find_amount(account_id, balances):
    for acc in balances:
        if acc['id'] == account_id:
            return acc['amount']
    return None  # Not found

def increase_amount(account_id, value, balances):
    for acc in balances:
        if acc['id'] == account_id:
            acc['amount'] += value
            response = {
                "destination": {
                    "id": account_id,
                    "balance": acc['amount']
                }
            }

            return jsonify(response), 201
    #se a conta nao existir        
    new_account = {'id': account_id, 'amount': value}
    balances.append(new_account)
    response = {
                "destination": {
                    "id": new_account['id'],
                    "balance": new_account['amount']
                }
            }

    return jsonify(response), 201

def withdraw_amount(account_id, value, balances):
    for acc in balances:
        if acc['id'] == account_id:
            if value < acc['amount']:
                acc['amount'] -= value
                response = {
                    "origin": {
                        "id": account_id,
                        "balance": acc['amount']
                    }
                }

                return jsonify(response), 201
            else:
                return "Missing amount", 400
    #se a conta nao existir        
    return '0', 404

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/balance', methods=['GET'])
def balance():
    account_id = request.args.get('account_id')
    # id_conta, saldo = get_data()
    if not account_id:
        return "Missing account_id", 400
    
    balance = find_amount(account_id, account_balances)
    
    if balance is None:
        return str(0), 404

    # Retorna apenas o número como resposta, com status 200
    return str(balance), 200
    #return render_template('balance.html', account_id=account_id, balance='1000') 


@app.route('/event', methods=['POST'])
def event():
    type_event = request.args.get('type')
    destination = request.args.get('destination')
    origin = request.args.get('origin')
    amount = request.args.get('amount')
    

    if type_event is None or destination is None:
        return "Missing destination or type", 400

    # # Se a conta não existir, cria com saldo zero
    # if destination not in accounts:
    #     accounts[destination] = 0
    if type_event is 'deposit':
        increase_amount(destination, amount, account_balances)

    if type_event is 'withdraw':
        withdraw_amount(origin, amount, account_balances)
    


    return render_template('index.html', type_event=type_event, destination=destination, amount=amount) 