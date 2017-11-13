class ThingsModel(object):
    def __init__(self, code_things=None, nr_things1=None, nr_things2=None, description=None, situation=None, value=None,
                 date_registre=None, state=None, location=None, note=None, tag_activated=None, location_current=None):
        self.code_things = code_things
        self.nr_things1 = nr_things1
        self.nr_things2 = nr_things2
        self.description = description
        self.situation = situation
        self.value = value
        self.date_registre = date_registre
        self.state = state
        self.location = location
        self.note = note
        self.tag_activated = tag_activated
        self.location_current = location_current
