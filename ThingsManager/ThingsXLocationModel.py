from ThingsManager.ThingsModel import ThingsModel


class ThingsXLocationModel(ThingsModel):

    def __init__(self,code_things = None, nr_things1 = None, nr_things2 = None, description = None, situation = None, value = None, date_registre = None, state = None, location = None, note = None, tag_activated = None, location_current = None, pblo_id = None, pblo_loca_id = None, pblo_usua_id = None, pblo_dt_first_read = None, pblo_dt_last_read = None):
        super(ThingsXLocationModel, self).__init__(code_things, nr_things1, nr_things2, description, situation, value, date_registre, state , location , note, tag_activated, location_current)
        self.pblo_id = pblo_id
        self.pblo_loca_id = pblo_loca_id
        self.pblo_usua_id = pblo_usua_id
        self.pblo_dt_first_read = pblo_dt_first_read
        self.pblo_dt_last_read = pblo_dt_last_read