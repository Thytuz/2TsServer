from UserManager import UserModel
from UserManager.UserModel import UserModel
from DatabaseManager.Connection import Connection


class User(UserModel):
    def __init__(self, id=None, name=None, email=None, password=None, permission=None, token=None):
        super(User, self).__init__(id, name, email, password, permission, token)

    def autenticate(self, email, password):
        conn = Connection()
        try:
            cursor = conn.execute_sql(
                "SELECT * FROM usuarios WHERE usua_excluido = 0 AND usua_email ='" + email + "' AND usua_senha = '" + password + "'")
            if cursor.rowcount == 0:
                return False
            else:
                data = cursor.fetchone();
                return UserModel(id=str(data[0]), name=str(data[1]), email=str(data[2]), permission=str(data[4]),
                                 token=str(data[5]))
                # return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def verify_token(self, token):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT * FROM usuarios WHERE usua_excluido = 0 AND usua_token = '" + token + "'")
            if cursor.rowcount == 0:
                return False
            else:
                data = cursor.fetchone()
                return UserModel(id=str(data[0]), name=str(data[1]), email=str(data[2]), permission=str(data[4]),
                                 token=str(data[5]))
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def insert_new_user(self, name, email, password, token, permission='3'):
        try:
            sql = "INSERT INTO usuarios (usua_nome, usua_email, usua_senha, usua_permissao, usua_token) VALUES('" + str(
                name) + "','" + str(email) + "','" + str(password) + "', '" + str(permission) + "','" + str(
                token) + "')"
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            conn.close_connection()

    def edit_user(self, id, name, email, password, permission):
        try:
            sql = "UPDATE usuarios set usua_nome = '" + str(name) + "', usua_email = '" + str(
                email) + "', usua_senha='" + str(password) + "', usua_permissao = '" + str(
                permission) + "' WHERE usua_id =  " + str(id) + ""
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        finally:
            conn.close_connection()

    def search_user_by_id(self, id):
        try:
            sql = "SELECT * FROM usuarios WHERE usua_excluido = 0 AND usua_id = " + str(id)
            conn = Connection()
            cursor = conn.execute_sql(sql)
            data = cursor.fetchone()

            if data != None:
                return UserModel(id=data[0], name=data[1], email=data[2], permission=data[4])
            return False
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_all_users(self):
        try:
            sql = "SELECT * FROM usuarios WHERE usua_excluido = 0 ORDER BY usua_nome"
            conn = Connection()
            cursor = conn.execute_sql(sql)

            if (cursor.rowcount == 0):
                return False

            listUsers = []
            for data in cursor.fetchall():
                userModel = UserModel(id=data[0], name=data[1], email=data[2], permission=data[4])
                listUsers.append(userModel)
            return listUsers
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()


    def generate_sql_insert_users(self):
        try:
            conn = Connection()

            data = ""

            cursor = conn.execute_sql("SELECT * FROM `usuarios`;")
            for row in cursor.fetchall():
                data += "INSERT INTO `usuarios` VALUES("
                first = True
                for field in row:
                    if not first:
                        data += ', '
                    if field == None:
                        data += 'null'
                    else:
                        data += '"' + str("" if field == None else field) + '"'

                    first = False

                data += ");\n"
            data += "\n\n"
            return data
        except Exception as e:
            return False
        finally:
            conn.close_connection()
