from ThingsManager.LocationModel import LocationModel
from DatabaseManager.Connection import Connection


class Locations(LocationModel):
    def __init__(self, loca_id=None, loca_room=None):
        super(Locations, self).__init__(loca_id, loca_room)

    def insert_location(self, loca_room):
        conn = Connection()
        try:
            sql = "INSERT INTO localizacao (loca_sala) VALUES('" + str(loca_room) + "')"
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

    def search_all_locations(self):
        try:
            sql = "SELECT * FROM localizacao WHERE loca_excluido = 0 ORDER BY loca_sala ASC"
            conn = Connection()
            cursor = conn.execute_sql(sql)

            if (cursor.rowcount == 0):
                return False

            listLocations = []
            for data in cursor.fetchall():
                locationModel = LocationModel(loca_id=data[0], loca_room=data[1])
                listLocations.append(locationModel)
            return listLocations
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_location_by_id(self, loca_id):
        try:
            sql = "SELECT * FROM localizacao WHERE loca_excluido = 0 AND loca_id = " + str(loca_id)
            conn = Connection()
            cursor = conn.execute_sql(sql)
            data = cursor.fetchone()

            if data != None:
                return LocationModel(loca_id=data[0], loca_room=data[1])
            return False
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def edit_location(self, loca_id, loca_room):
        try:
            sql = "UPDATE localizacao set loca_sala = '" + str(loca_room) + "' WHERE loca_id =  " + str(loca_id) + ""
            print(sql);
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



    def generate_sql_insert_locations(self):
        try:
            conn = Connection()

            data = ""

            cursor = conn.execute_sql("SELECT * FROM `localizacao`;")
            for row in cursor.fetchall():
                data += "INSERT INTO `localizacao` VALUES("
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
