# import os
from flask import jsonify, request, Flask, render_template, url_for
import json
from SynchronizationManager.ThingsSynchronization import ThingsSynchronization
from ThingsManager.Locations import Locations
from ThingsManager.Things import Things
from ThingsManager.ThingsXLocation import ThingsXLocation
from UserManager.User import User
from werkzeug.utils import redirect
import string
import random


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


@app.route('/')
def index():
    return render_template('/login.html')


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
            return render_template('/inicial.html', message="Welcome", alertlevel="success", user=response)
    except Exception as e:
        print(e)
        return "Erro no servidor. Contate o Analista"


@app.route('/inicial')
def inicial():
    return render_template('/inicial.html')


@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/locations')
def locations():
    location = Locations()
    locations = location.search_all_locations()

    return render_template('/locations.html', locations=locations)


@app.route('/findlocation', methods=['POST'])
def findlocation():
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
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/editlocation', methods=['POST'])
def editlocation():
    location = Locations()
    nome = request.form['name']
    id = request.form['id']
    try:
        response = location.edit_location(id, nome)
        if response == False:
            return render_template('/locations.html', message="Error updating location", alertlevel="danger")
        else:
            return render_template('/locations.html', message="Location updated", alertlevel="success")

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/users')
def users():
    user = User()
    users = user.search_all_users()

    return render_template('/users.html', users=users)


@app.route('/adduser', methods=['POST'])
def adduser():
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))

    user = User()

    try:
        response = user.insert_new_user(nome, email, senha, token, permissao)
        if response == True:
            return "sucesso"
        else:
            return "Erro ao cadastrar usuário."

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/findUser', methods=['POST'])
def findUser():
    id = request.form['id']
    user = User()
    users = user.search_all_users()
    try:
        response = user.search_user_by_id(id)
        if response == False:
            return "Erro ao buscar usuário"
        else:
            return render_template('/users.html', users=users, user1=response)

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/findThing', methods=['POST'])
def findThing():
    numThing = request.form['numeroPat']

    things = Things()
    try:
        response = things.search_things_by_num1(numThing)

        if response == False:
            return "Nenhuma coisa encontrada com o número informado"
        else:
            return render_template('/things.html', thing=response)
    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/editUser', methods=['POST'])
def editUser():
    id = request.form['id1']
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']

    user = User()
    try:
        response = user.edit_user(id, nome, email, senha, permissao)
        if response == False:
            return "Erro ao atualizar usuário"
        else:
            return "Usuario atualizado com sucesso"

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/editThing', methods=['POST'])
def editThing():
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
            return "Coisa atualizada com sucesso"
        else:
            return "Erro ao atualizar coisa"
    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável!'


@app.route('/voltar', methods=['POST'])
def voltar():
    return render_template('/inicial.html')


@app.route('/things')
def things():
    return render_template('/things.html')


@app.route('/addthing', methods=['POST'])
def addthing():
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
            return "Coisa cadastrada com sucesso."
        else:
            return "Erro ao cadastrar coisa."

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsável !!'


@app.route('/quit')
def quit():
    return render_template('/login.html')


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

    things = Things()
    response = things.search_locations()
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


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    app.run(debug=True, port=8080)
