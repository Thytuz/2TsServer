from DatabaseManager.Connection import Connection
from ThingsManager.Things import Things
from ThingsManager.ThingsXLocation import ThingsXLocation


class ThingsSynchronization(object):

    def synchronize_location(self, nr_things1, location, user):
        thingsXLocation = ThingsXLocation()
        things = Things()

        thingsExists = things.search_things_by_num1(nr_things1)
        if thingsExists != False:
            pabe_id = thingsExists.code_things
            exists = thingsXLocation.check_thing_location_exists(nr_things1)

            if exists == True:
                update = thingsXLocation.update_thing_location(pabe_id, location, user)
                if update:
                    return True
                else:
                    return 'Ocorreu um erro ao atualizar a localização da coisa'
            elif exists == False:
                insert = thingsXLocation.insert_patr_bens_x_localizacao(pabe_id, location, user)
                if insert:
                    return True
                else:
                    return 'Ocorreu um erro ao inserir a localização da coisa'
            else:
                return 'Ocorreu um erro ao verificar a localização atual da coisa'
        elif thingsExists == False:
            return 'Codigo da coisa inexistente'
        else:
            return 'Ocorreu um erro ao verificar se a coisa existe'

    def synchronize_things(self, nr_things1, situation, state, note, user,current_location):
        things = Things()
        thingsXLocation = ThingsXLocation()


        thingsExists = things.search_things_by_num1(nr_things1)
        if thingsExists != False:
            pabe_id = thingsExists.code_things
            update = things.update_thing( pabe_id, situation, state, note)
            if update == False:
                return 'Ocorreu um erro ao atualizar o objeto'

            if current_location != None and current_location != "0":
                exists = thingsXLocation.check_thing_location_exists(nr_things1)
                if exists == True:
                    current_location_db = thingsXLocation.get_location_current(pabe_id)
                    if current_location != False and current_location != 'ERRO':
                        if current_location_db != current_location:
                            update = thingsXLocation.update_thing_location(pabe_id, current_location, user)
                            if update:
                                return True
                            else:
                                return 'Ocorreu um erro ao atualizar a localização da coisa'

                elif exists == False:
                    insert = thingsXLocation.insert_patr_bens_x_localizacao(pabe_id, current_location, user)
                    if insert:
                        return True
                    else:
                        return 'Ocorreu um erro ao inserir a localização da coisa'
                else:
                    return 'Ocorreu um erro ao verificar a localização atual da coisa'
            return True
        elif thingsExists == False:
            return 'Codigo da coisa inexistente'
        else:
            return 'Ocorreu um erro ao verificar se a coisa existe'
