from DatabaseManager.Connection import Connection
from ThingsManager.LocationModel import LocationModel
from ThingsManager.ThingsModel import ThingsModel
from ThingsManager.ThingsXLocationModel import ThingsXLocationModel


class ThingsXLocation(object):

    """
    busca coisas que pertencem a uma localização
    mas não foi encontrado
    """
    def search_things_missing_by_location(self, loca_id):
        try:
            sql = "SELECT pabe_id, pabe_num_patr1, pabe_num_patr2," \
                  " pabe_descricao, pabe_situacao, pabe_valor, pabe_dt_cadastro," \
                  " pabe_estado,loca_1.loca_sala as pabe_loca_sala, pabe_observacao," \
                  " pabe_etiqueta_ativa, pblo_id, loca_2.loca_sala as pblo_loca_sala," \
                  " pblo_usua_id, pblo_dt_primeira_leitura, pblo_dt_ultima_leitura," \
                  " loca_1.loca_id as pabe_location_id, loca_2.loca_id as pblo_location_id " \
                  " FROM patr_bens_x_localizacao INNER JOIN patr_bens ON pabe_id = pblo_pabe_id" \
                  " INNER JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id" \
                  " INNER JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id" \
                  " WHERE pblo_loca_id <> '"+str(loca_id)+"' AND pabe_loca_id ='"+str(loca_id)+"'"
            print(sql)
            conn = Connection()
            cursor = conn.execute_sql(sql)
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[16] == None else data[16]),
                                         loca_room=str("" if data[8] == None else data[8]))
                location_current = LocationModel(loca_id=str("0" if data[17] == None else data[17]),
                                                 loca_room=str("" if data[12] == None else data[12]))

                thingsModel = ThingsXLocationModel(code_things=str(data[0]),
                                                   nr_things1=str("0" if data[1] == None else data[1]),
                                                   nr_things2=str("0" if data[2] == None else data[2]),
                                                   description=str(data[3]),
                                                   situation=str("" if data[4] == None else data[4]),
                                                   value=str("0" if data[5] == None else data[5]),
                                                   date_registre=str("" if data[6] == None else data[6]),
                                                   state=str("" if data[7] == None else data[7]), location=location,
                                                   note=str("" if data[9] == None else data[9]),
                                                   tag_activated=str("0" if data[10] == None else data[10]),
                                                   location_current=location_current,
                                                   pblo_id=str("0" if data[11] == None else data[11]),
                                                   pblo_loca_id=str("0" if data[17] == None else data[17]),
                                                   pblo_usua_id=str("0" if data[13] == None else data[13]),
                                                   pblo_dt_first_read=str("" if data[14] == None else data[14]),
                                                   pblo_dt_last_read=str("" if data[15] == None else data[15]))
                listThings.append(thingsModel)
                print(thingsModel.nr_things2)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    """
    busca coisas que não pertencem a determinada localização, mas estão la
    """
    def search_things_over_by_location(self, loca_id):
        try:
            conn = Connection()
            cursor = conn.execute_sql("SELECT pabe_id, pabe_num_patr1, pabe_num_patr2,"
                                      " pabe_descricao, pabe_situacao, pabe_valor,"
                                      " pabe_dt_cadastro, pabe_estado,"
                                      " loca_1.loca_sala as pabe_loca_sala, pabe_observacao,"
                                      " pabe_etiqueta_ativa, pblo_id, loca_2.loca_sala as pblo_loca_sala,"
                                      " pblo_usua_id, pblo_dt_primeira_leitura, pblo_dt_ultima_leitura,"
                                      " loca_1.loca_id as pabe_location_id, loca_2.loca_id as pblo_location_id " \
                                      " FROM patr_bens_x_localizacao INNER JOIN patr_bens ON pabe_id = pblo_pabe_id"
                                      " INNER JOIN localizacao AS loca_1 ON loca_1.loca_id = pabe_loca_id"
                                      " INNER JOIN localizacao AS loca_2 ON loca_2.loca_id = pblo_loca_id"
                                      " WHERE pblo_loca_id ='"+str(loca_id)+"' AND pabe_loca_id <>'"+str(loca_id)+"'")
            if cursor.rowcount == 0:
                return False
            listThings = []
            for data in cursor.fetchall():
                location = LocationModel(loca_id=str("0" if data[16] == None else data[16]),
                                         loca_room=str("" if data[8] == None else data[8]))
                location_current = LocationModel(loca_id=str("0" if data[17] == None else data[17]),
                                                 loca_room=str("" if data[12] == None else data[12]))

                thingsModel = ThingsXLocationModel(code_things=str(data[0]),
                                                   nr_things1=str("0" if data[1] == None else data[1]),
                                                   nr_things2=str("0" if data[2] == None else data[2]),
                                                   description=str(data[3]),
                                                   situation=str("" if data[4] == None else data[4]),
                                                   value=str("0" if data[5] == None else data[5]),
                                                   date_registre=str("" if data[6] == None else data[6]),
                                                   state=str("" if data[7] == None else data[7]), location=location,
                                                   note=str("" if data[9] == None else data[9]),
                                                   tag_activated=str("0" if data[10] == None else data[10]),
                                                   location_current=location_current,
                                                   pblo_id=str("0" if data[11] == None else data[11]),
                                                   pblo_loca_id=str("0" if data[17] == None else data[17]),
                                                   pblo_usua_id=str("0" if data[13] == None else data[13]),
                                                   pblo_dt_first_read=str("" if data[14] == None else data[14]),
                                                   pblo_dt_last_read=str("" if data[15] == None else data[15]))
                listThings.append(thingsModel)
                print(thingsModel.nr_things2)
            return listThings
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()


    def check_thing_location_exists(self, nr_things1):
        try:
            sql = "SELECT * FROM patr_bens_x_localizacao INNER JOIN patr_bens ON pblo_pabe_id = pabe_id WHERE pabe_num_patr1 =  "+ str(nr_things1)
            conn = Connection()
            cursor = conn.execute_sql(sql)
            if(cursor.rowcount == 0):
                return False
            return True
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()

    def insert_patr_bens_x_localizacao(self, pabe_id, loca_id, user):
        try:
            sql = "INSERT INTO patr_bens_x_localizacao (pblo_pabe_id, pblo_loca_id, pblo_usua_id) VALUES('"+str(pabe_id)+"', '"+str(loca_id)+"', '"+str(user)+"')"
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


    def update_thing_location(self, pabe_id, loca_id, user):
        try:
            sql = "UPDATE patr_bens_x_localizacao SET pblo_loca_id = '"+str(loca_id)+"', pblo_usua_id = '"+str(user)+"' WHERE pblo_pabe_id = "+pabe_id
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

    def get_location_current(self, pabe_id):
        try:
            sql = "SELECT pblo_loca_id FROM patr_bens_x_localizacao WHERE pblo_pabe_id =  "+ str(pabe_id)
            conn = Connection()
            cursor = conn.execute_sql(sql)
            if(cursor.rowcount == 0):
                return False
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return 'ERRO'
        finally:
            conn.close_connection()