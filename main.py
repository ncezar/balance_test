from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

account_balances = [
    {'id': "100", 'amount': 20},
    {'id':"200", 'amount' :50},
    {'id':"300", 'amount': 0}
]

def find_account(account_id, balances):
    for acc in balances:
        if acc['id'] == account_id:
            return acc
    #se a conta nao existir        
    return None

def increase_amount(account_id, value, balances):
    value = int(value)
    if value > 0:
        account_id['amount'] += value
        # print(account_id['amount'])
        response = {
            "destination": {
                "id": account_id['id'],
                "balance": account_id['amount']
            }
        }

        return jsonify(response), 201
    # se amount menor       
    return "Insufficient amount", 404


def withdraw_amount(account_id, value, balances):
    value = int(value)
    if value < account_id['amount']:
            # print(account_id['amount'])
            account_id['amount'] -= value
            # print(account_id['amount'] )
            response = {
                "origin": {
                    "id": account_id['id'],
                    "balance": account_id['amount']
                }
            }

            return jsonify(response), 201
    else:
        return "Missing amount", 400
    #se a conta nao existir        
    return '0', 404

def transfer_amount(origin, destination, value):
    value = int(value)
    if value < origin['amount']:
        origin['amount'] -= value
        destination['amount'] +=value


        response = {
            "origin": {
                "id": origin['id'],
                "balance": origin['amount']
            },
            "destination": {
                "id": destination['id'],
                "balance": destination['amount']
            },
        }

        return jsonify(response), 201
    else:
        return "Missing amount", 400


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/balance', methods=['GET'])
def balance():
    account_id = request.args.get('account_id')
    # id_conta, saldo = get_data()

    if not account_id:
        return "Missing account_id", 400
    found_account = find_account(account_id, account_balances)

    if found_account:
        return str(found_account['amount']), 200
    else:
        return str(0), 404  # Not found
    


@app.route('/event', methods=['POST'])
def event():
    type_event = request.args.get('type')
    destination_id = request.args.get('destination')
    origin_id = request.args.get('origin')
    value = request.args.get('amount')
    
    
    if type_event is None:
        return "Missing type", 400

    # # Se a conta não existir, cria com saldo zero
    # if destination not in accounts:
    #     accounts[destination] = 0
    if type_event== "deposit":
        if destination_id:
            destination = find_account(destination_id, account_balances)
            if destination:
                result = increase_amount(destination, value, account_balances)
                return result   
                
            else:            
                #nao existe entao cria uma nova
                new_account = {'id': destination_id, 'amount': value}
                account_balances.append(new_account)
                response = {
                            "destination": {
                                "id": new_account['id'],
                                "balance": new_account['amount']
                            }
                        }

                return jsonify(response), 201
        return 'Missing destination', 404

    if type_event == "withdraw":
        if origin_id:
            origin = find_account(origin_id, account_balances)
            if origin:            
                result = withdraw_amount(origin, value, account_balances)
                return result
        else:
            return "Missing origin", 404

    if type_event == "transfer":
        if destination_id and origin_id:
            destination = find_account(destination_id, account_balances)
            origin = find_account(origin_id, account_balances)
            if destination and origin:
                result = transfer_amount(origin, destination, value)
                return result          
        else:
            return "Missing destination or origin", 400
        
    # return render_template('index.html', type_event=type_event, destination=destination, amount=amount) 

@app.route('/reset', methods=['POST'])
def reset():
    global account_balances
    account_balances = []
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)