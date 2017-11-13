from DatabaseManager.Connection import Connection
from ThingsManager.LocationModel import LocationModel
from ThingsManager.ThingsModel import ThingsModel


class Things(ThingsModel):
    def __init__(self, code_things=None, nr_things1=None, nr_things2=None, description=None, situation=None, value=None,
                 date_registre=None, state=None, location=None, note=None, tag_activated=None):
        super(Things, self).__init__(code_things, nr_things1, nr_things2, description, situation, value, date_registre,
                                     state, location, note, tag_activated)

    def search_things_by_num1(self, nr_things1):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2,"
                                      " pabe_descricao, pabe_situacao, pabe_valor, pabe_dt_cadastro,"
                                      " pabe_estado, loca_1.loca_id AS pabe_location_id,"
                                      " loca_1.loca_sala AS pabe_location_sala, pabe_observacao,"
                                      " pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id,"
                                      " loca_2.loca_sala AS pblo_location_sala"
                                      " FROM patr_bens LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id"
                                      " LEFT JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pabe_excluido = 0 AND pabe_num_patr1 = '" + str(nr_things1) + "'")
            if cursor.rowcount == 0:
                return False
            data = cursor.fetchone()
            location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                     loca_room=str("" if data[9] == None else data[9]))
            location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                             loca_room=str("" if data[13] == None else data[13]))
            thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                      nr_things2=str("0" if data[2] == None else data[2]),
                                      description=str("" if data[3] == None else data[3]),
                                      situation=str("" if data[4] == None else data[4]),
                                      value=str("0" if data[5] == None else data[5]),
                                      date_registre=str("" if data[6] == None else data[6]),
                                      state=str("" if data[7] == None else data[7]), location=location,
                                      note=str("" if data[10] == None else data[10]),
                                      tag_activated=str("0" if data[11] == None else data[11]),
                                      location_current=location_current)
            return thingsModel
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_things_actives_by_location(self, loca_id):
        try:
            sql = "SELECT pabe_id, pabe_num_patr1, pabe_num_patr2," \
                  " pabe_descricao, pabe_situacao, pabe_valor, pabe_dt_cadastro," \
                  " pabe_estado, loca_1.loca_id AS pabe_location_id, loca_1.loca_sala AS pabe_location_sala," \
                  " pabe_observacao, pabe_etiqueta_ativa," \
                  " loca_2.loca_id AS pblo_location_id, loca_2.loca_sala AS pblo_location_sala" \
                  " FROM patr_bens LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id" \
                  " INNER JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id" \
                  " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id" \
                  " WHERE pabe_excluido = 0 AND pabe_etiqueta_ativa = 1 AND loca_1.loca_id ='" + str(loca_id) + "'"
            conn = Connection()
            cursor = conn.execute_sql(sql)
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_things_inactives_by_location(self, loca_id):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2, pabe_descricao,"
                                      " pabe_situacao, pabe_valor, pabe_dt_cadastro, pabe_estado,"
                                      " loca_1.loca_id AS pabe_location_id, loca_1.loca_sala AS pabe_location_sala,"
                                      " pabe_observacao, pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id,"
                                      " loca_2.loca_sala AS pblo_location_sala FROM patr_bens "
                                      " LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id"
                                      " INNER JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pabe_excluido = 0 AND pabe_etiqueta_ativa = 0 AND pabe_loca_id ='" + str(
                loca_id) + "'")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_all_things_inactives(self):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2, pabe_descricao,"
                                      " pabe_situacao, pabe_valor, pabe_dt_cadastro, pabe_estado,"
                                      " loca_1.loca_id AS pabe_location_id, loca_1.loca_sala AS pabe_location_sala,"
                                      " pabe_observacao, pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id,"
                                      " loca_2.loca_sala AS pblo_location_sala FROM patr_bens"
                                      " LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id"
                                      " LEFT JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pabe_excluido = 0 AND pabe_etiqueta_ativa = 0 ")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_things_by_location(self, loca_id):
        try:
            sql = "SELECT pabe_id, pabe_num_patr1, pabe_num_patr2, pabe_descricao," \
                  " pabe_situacao, pabe_valor, pabe_dt_cadastro, pabe_estado," \
                  " loca_1.loca_id AS pabe_location_id, loca_1.loca_sala AS pabe_location_sala," \
                  " pabe_observacao, pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id," \
                  " loca_2.loca_sala AS pblo_location_sala FROM patr_bens" \
                  " LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id" \
                  " INNER JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id" \
                  " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id" \
                  " WHERE pabe_excluido = 0 AND pabe_loca_id = '" + str(loca_id) + "'"
            conn = Connection()
            cursor = conn.execute_sql(sql)
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def active_things_by_num1(self, nr_things1):
        try:
            sql = "UPDATE patr_bens set pabe_etiqueta_ativa = 1 WHERE pabe_num_patr1 = " + str(nr_things1)
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        finally:
            conn.close_connection()

    def update_thing(self, code_things, situation, state, note):
        try:
            sql = "UPDATE patr_bens SET pabe_situacao = '" + str(situation) + "', pabe_estado = '" + str(
                state) + "', pabe_observacao = '" + str(note) + "' WHERE pabe_id = " + code_things
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        finally:
            conn.close_connection()

    def update_thing2(self, code_things, description, num1, num2, localizacao, price, situation, state, note):
        try:
            sql = "UPDATE patr_bens SET pabe_num_patr1 = '" + str(
                num1) + "', pabe_num_patr2 = '" + str(num2) + "', pabe_descricao = '" + str(
                description) + "', pabe_loca_id = '" + str(localizacao) + "', pabe_valor = '" + str(
                price) + "', pabe_dt_cadastro = CURRENT_TIMESTAMP(), pabe_situacao = '" + str(
                situation) + "', pabe_estado = '" + str(state) + "', pabe_observacao = '" + str(
                note) + "' WHERE pabe_id = '" + str(code_things) + "'"
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

    def insert_new_thing(self, thingNum1, thingNum2, thingName, thingLocation, thingPrice, thingSituation,
                         thingCondition,
                         thingObservation):
        try:
            sql = "INSERT INTO patr_bens (pabe_num_patr1, pabe_num_patr2, pabe_descricao, pabe_loca_id, pabe_valor, pabe_dt_cadastro, pabe_situacao, pabe_estado, pabe_observacao, pabe_etiqueta_ativa) VALUES('" + str(
                thingNum1) + "','" + str(thingNum2) + "','" + str(thingName) + "','" + str(thingLocation) + "','" + str(
                thingPrice) + "', CURRENT_TIMESTAMP() ,'" + str(thingSituation) + "','" + str(
                thingCondition) + "','" + str(thingObservation) + "', '0')"
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

    def search_all_things_actives(self):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2, pabe_descricao,"
                                      " pabe_situacao, pabe_valor, pabe_dt_cadastro, pabe_estado,"
                                      " loca_1.loca_id AS pabe_location_id, loca_1.loca_sala AS pabe_location_sala,"
                                      " pabe_observacao, pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id,"
                                      " loca_2.loca_sala AS pblo_location_sala FROM patr_bens"
                                      " LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id"
                                      " LEFT JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pabe_excluido = 0 AND pabe_etiqueta_ativa = 1 ")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def get_all_things_db(self):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2, pabe_descricao,"
                                      " pabe_situacao, pabe_valor, pabe_dt_cadastro, pabe_estado,"
                                      " pabe_observacao, pabe_etiqueta_ativa, pabe_loca_id"
                                      " FROM patr_bens")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]),
                                          note=str("" if data[8] == None else data[8]),
                                          tag_activated=str("0" if data[9] == None else data[9]),
                                          location=str("0" if data[10] == None else data[10]))
                listThings.append(thingsModel)

            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def search_all_things(self):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2,"
                                      " pabe_descricao, pabe_situacao, pabe_valor, pabe_dt_cadastro,"
                                      " pabe_estado, loca_1.loca_id AS pabe_location_id,"
                                      " loca_1.loca_sala AS pabe_location_sala, pabe_observacao,"
                                      " pabe_etiqueta_ativa, loca_2.loca_id AS pblo_location_id,"
                                      " loca_2.loca_sala AS pblo_location_sala"
                                      " FROM patr_bens LEFT JOIN patr_bens_x_localizacao ON pabe_id = pblo_pabe_id"
                                      " LEFT JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " LEFT JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pabe_excluido = 0 ")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[8] == None else data[8]),
                                         loca_room=str("" if data[9] == None else data[9]))
                location_current = LocationModel(loca_id=str("0" if data[12] == None else data[12]),
                                                 loca_room=str("" if data[13] == None else data[13]))
                thingsModel = ThingsModel(code_things=str(data[0]), nr_things1=str("0" if data[1] == None else data[1]),
                                          nr_things2=str("0" if data[2] == None else data[2]),
                                          description=str("" if data[3] == None else data[3]),
                                          situation=str("" if data[4] == None else data[4]),
                                          value=str("0" if data[5] == None else data[5]),
                                          date_registre=str("" if data[6] == None else data[6]),
                                          state=str("" if data[7] == None else data[7]), location=location,
                                          note=str("" if data[10] == None else data[10]),
                                          tag_activated=str("0" if data[11] == None else data[11]),
                                          location_current=location_current)
                listThings.append(thingsModel)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()
