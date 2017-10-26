import os
from flask import jsonify, request, Flask, render_template, url_for, session
import json
from SynchronizationManager.ThingsSynchronization import ThingsSynchronization
from ThingsManager.Locations import Locations
from ThingsManager.Things import Things
from ThingsManager.ThingsXLocation import ThingsXLocation
from UserManager.User import User
from werkzeug.utils import redirect
import string
import random


def cria_sessao(id, nome, email, permission, token):
    session['id'] = id
    session['nome'] = nome
    session['email'] = email
    session['permission'] = permission
    session['token'] = token


# def get_sessao():


def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, lê chaves e valores; converte valores
    if isinstance(obj, dict):
        return {k: para_dict(v) for k, v in obj.items()}
    # Se for uma lista ou tupla, lê elementos; também converte
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    # Se for qualquer outra coisa, usa sem conversão
    else:
        return obj


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    if session.get('token') is None:
        return render_template('/login.html')
    return render_template('/inicial.html')


@app.route('/post_login', methods=['POST'])
def post_login():
    email = request.form['email']
    password = request.form['password']

    user = User()
    try:
        response = user.autenticate(email, password)
        if response == False:
            return render_template('/login.html', message="You have entered an invalid username or password",
                                   alertlevel="danger")
        else:
            cria_sessao(response.id, response.name, response.email, response.permission, response.token)
            return render_template('/inicial.html', message="Welcome", alertlevel="success", user=response)
    except Exception as e:
        print(e)
        return render_template('/login.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/inicial')
def inicial():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    return render_template('/inicial.html')


@app.route('/about')
def about():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    return render_template('/about.html')


@app.route('/locations')
def locations():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    location = Locations()
    locations = location.search_all_locations()

    return render_template('/locations.html', locations=locations)


@app.route('/findlocation', methods=['POST'])
def findlocation():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    id = request.form['id']
    location = Locations()
    locations = location.search_all_locations()
    try:
        response = location.search_location_by_id(id)
        if response == False:
            return render_template('/locations.html', message="Error finding locations", alertlevel="danger")
        else:
            return render_template('/locations.html', locations=locations, location=response)

    except Exception as e:
        return render_template('/locations.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/editlocation', methods=['POST'])
def editlocation():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    location = Locations()
    locations = location.search_all_locations()
    nome = request.form['name']
    id = request.form['id']
    try:
        response = location.edit_location(id, nome)
        if response == False:
            return render_template('/locations.html', message="Error updating location", alertlevel="danger",
                                   locations=locations)
        else:
            return render_template('/locations.html', message="Location updated", alertlevel="success",
                                   locations=locations)

    except Exception as e:
        return render_template('/locations.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/users')
def users():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    user = User()
    users = user.search_all_users()

    return render_template('/users.html', users=users)


@app.route('/adduser', methods=['POST'])
def adduser():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    user = User()
    users = user.search_all_users()
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))

    try:
        response = user.insert_new_user(nome, email, senha, token, permissao)
        if response == True:
            return render_template('/users.html', message="User added successfully", alertlevel="success", users=users)
        else:
            return render_template('/users.html', message="Error adding user", alertlevel="danger", users=users)

    except Exception as e:
        return render_template('/users.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger", users=users)


@app.route('/findUser', methods=['POST'])
def findUser():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    id = request.form['id']
    user = User()
    users = user.search_all_users()
    try:
        response = user.search_user_by_id(id)
        if response == False:
            return render_template('/users.html', message="Error finding user", alertlevel="danger")
        else:
            return render_template('/users.html', users=users, user1=response)

    except Exception as e:
        return render_template('/users.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/findThing', methods=['POST'])
def findThing():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    numThing = request.form['numeroPat']

    things = Things()
    try:
        response = things.search_things_by_num1(numThing)

        if response == False:
            return render_template('/things.html', message="No thing found with given number", alertlevel="warning")
        else:
            return render_template('/things.html', thing=response)
    except Exception as e:
        return render_template('/things.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/editUser', methods=['POST'])
def editUser():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    user = User()

    id = request.form['id1']
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']

    users = user.search_all_users()

    try:
        response = user.edit_user(id, nome, email, senha, permissao)
        if response == False:
            return render_template('/users.html', message="Error while editing user", alertlevel="danger", users=users)
        else:
            return render_template('/users.html', message="User successfully edited", alertlevel="success", users=users)

    except Exception as e:
        return render_template('/users.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/editThing', methods=['POST'])
def editThing():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    id = request.form['id']
    descricao = request.form['descricao']
    num1 = request.form['num1']
    num2 = request.form['num2']
    preco = request.form['preco']
    situacao = request.form['situacao']
    estado = request.form['estado']
    observacao = request.form['observacao']

    thing = Things()

    try:
        response = thing.update_thing2(id, descricao, num1, num2, preco, situacao, estado, observacao)
        if response == True:
            return render_template('/things.html', message="Thing successfully edited", alertlevel="success")
        else:
            return render_template('/things.html', message="Error while editing thing", alertlevel="warning")
    except Exception as e:
        return render_template('/things.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/voltar', methods=['POST'])
def voltar():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    return render_template('/inicial.html')


@app.route('/things')
def things():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    return render_template('/things.html')


@app.route('/addthing', methods=['POST'])
def addthing():
    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    descricao = request.form['descricao']
    num1 = request.form['num1']
    num2 = request.form['num2']
    preco = request.form['preco']
    situacao = request.form['situacao']
    estado = request.form['estado']
    observacao = request.form['observacao']

    thing = Things()
    try:
        response = thing.insert_new_thing(num1, num2, descricao, preco, situacao, estado, observacao)
        if response == True:
            return render_template('/things.html',
                                   message="Thing successfully added",
                                   alertlevel="success")
        else:
            return render_template('/things.html',
                                   message="Error adding thing",
                                   alertlevel="danger")

    except Exception as e:
        return render_template('/things.html',
                               message="A database error has occurred. Contact your system administrator",
                               alertlevel="danger")


@app.route('/quit')
def quit():
    session.clear()
    return render_template('/login.html')


@app.route('/thingsgrid', methods=['get'])
def thingsgrid():

    if session.get('token') is None:
        return render_template('/login.html', message="You have to login to access this module", alertlevel="warning")
    acao = request.args.get("acao")
    message = ''
    things = Things()
    thingsXLocation = ThingsXLocation()
    response = things.search_all_things()
    if acao == "search":
        tipo_busca = request.args.get("tipo_busca")
        dado = request.args.get("dado_busca")
        print(tipo_busca)
        if tipo_busca != '-1':
            if tipo_busca == '4':
                response = []
                dado2 = request.args.get("dado_busca2")
                resp = things.search_things_by_num1(dado2)
                if resp == False:
                    message = "No thing found!"
                elif resp == 'ERRO':
                    message = 'Ocorreu um erro no servidor'
                else:
                    response.append(resp)
            elif dado != '-1':
                if tipo_busca == '1':
                    response = things.search_things_by_location(dado)

                elif tipo_busca == '2':
                    response = thingsXLocation.search_things_over_by_location(dado)
                elif tipo_busca == '3':
                    response = thingsXLocation.search_things_missing_by_location(dado)
    if response == False:
        response = []
        message = "No thing found!"
    if response == 'ERRO':
        response = []
        message = "Error while searching"
    location = Locations()
    locations = location.search_all_locations()

    if message != '':
        return render_template('/thingsgrid.html', things=response, locations=locations, message=message,
                               alertlevel="warning")
    else:
        return render_template('/thingsgrid.html', things=response, locations=locations)


# END VIEWS

@app.route('/user_autenticate/email=<string:email>&password=<string:password>', methods=['GET'])
def logar(email, password):
    user = User()
    response = user.autenticate(email, password)
    if response == False:
        return jsonify({'response': 'Nenhum usuario encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_by_num/token=<string:token>&num=<string:num>', methods=['GET'])
def search_things_by_num(token, num):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_by_num1(num)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_actived_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_act_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_actives_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_inactived_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_inact_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_inactives_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_all_things_inactived/token=<string:token>', methods=['GET'])
def search_all_things_inactives(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_all_things_inactives()
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/active_thing_by_num/token=<string:token>&num=<string:num>', methods=['GET'])
def active_thing_by_num(token, num):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    exits = things.search_things_by_num1(num)
    if exits:
        response = things.active_things_by_num1(num)
        if response == False:
            return jsonify({'response': 'Ocorreu um erro ao ativar a etiqueta'})
        else:
            return jsonify({'response': 'true'})
    else:
        return jsonify({'response': 'Objeto não encontrado'})


@app.route('/search_locations/token=<string:token>', methods=['GET'])
def search_locations(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    location = Locations()
    response = location.search_all_locations()
    if response == False:
        return jsonify({'response': 'Nenhuma localizacao encontrada'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_missing_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_missing_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    thingsXLocation = ThingsXLocation()
    response = thingsXLocation.search_things_missing_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_over_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_over_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    thingsXLocation = ThingsXLocation()
    response = thingsXLocation.search_things_over_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/synchronize_location/token=<string:token>&locaid=<string:location>&num=<string:num_patr>', methods=['GET'])
def synchronize_location(token, location, num_patr):
    # verifica validade do token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})
    else:
        user_id = resp.id

    thingsSynchronization = ThingsSynchronization()
    response = thingsSynchronization.synchronize_location(num_patr, location, user_id)
    if response == True:
        return jsonify({'response': 'true'})
    else:
        return jsonify({'response': response})


@app.route(
    '/edit_thing/token=<string:token>&num=<string:num_patr>&locaid=<string:location>&situation=<string:situation>&state=<string:state>&note=<string:note>',
    methods=['GET'])
def edit_things(token, num_patr, location, situation, state, note):
    # verifica validade do token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})
    else:
        user_id = resp.id

    thingsSynchronization = ThingsSynchronization()
    response = thingsSynchronization.synchronize_things(num_patr, situation, state, note, user_id, location)
    if response == True:
        return jsonify({"response": "OK"})
    else:
        return jsonify({"response": response})


@app.route('/search_all_things_actived/token=<string:token>', methods=['GET'])
def search_all_things_actives(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_all_things_actives()
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


# Busca dados do banco
token_padrao_get_db = "123"


@app.route('/get_locations_db/token=<string:token>', methods=['GET'])
def get_locations_db(token):
    if token != token_padrao_get_db:
        return jsonify({'response': 'Token Invalido'})

    location = Locations()
    return json.dumps(para_dict(location.get_all_locations_db()))


@app.route('/get_things_db/token=<string:token>', methods=['GET'])
def get_things_db(token):
    if token != token_padrao_get_db:
        return jsonify({'response': 'Token Invalido'})

    things = Things()

    return json.dumps(para_dict(things.get_all_things_db()))


@app.route('/get_things_location_db/token=<string:token>', methods=['GET'])
def get_things_location_db(token):
    if token != token_padrao_get_db:
        return jsonify({'response': 'Token Invalido'})

    things_location = ThingsXLocation()

    return json.dumps(para_dict(things_location.get_things_x_location_db()))


@app.route('/get_users_db/token=<string:token>', methods=['GET'])
def get_users_db(token):
    if token != token_padrao_get_db:
        return jsonify({'response': 'Token Invalido'})

    user = User()

    return json.dumps(para_dict(user.get_users_db()))


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    app.run(debug=True, port=8080)
