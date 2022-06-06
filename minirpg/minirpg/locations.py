class Location:

    type_oasis = 'Oasis'
    type_desert = 'Desert'
    type_forest = 'Forest'
    type_mountain = 'Mountain'

    def __init__(self, name, type_of):
        self.name = name
        self.type_of = type_of

    @property
    def name(self):
        return self.name

    @property
    def type_of(self):
        return self.type_of

    def desert(self, name):
        self.name = name
        self.type_of = self.type_desert

    def oasis(self, name):
        self.name = name
        self.type_of = self.type_oasis

    def forest(self, name):
        self.name = name
        self.type_of = self.type_forest

    def mountain(self, name):
        self.name = name
        self.type_of = self.type_mountain

    def start_location(self):
        self.oasis('Start location')

    def sahara_desert(self):
        self.desert('Sahara Desert')

    def sahara_desert(self):
        self.desert('Sahara Desert')

    def maple_forest(self):
        self.forest('Maple forest')

    def mountain_forest(self):
        self.mountain('Mountain forest')

    def winter_forest(self):
        self.mountain('Winter forest')

    def oasis(self):
        self.oasis('Oasis')
