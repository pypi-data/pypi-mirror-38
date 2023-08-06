class Person(dict):

    def __init__(self, name):
        super().__init__()
        self.name = self['name'] = name


class Recommendations(dict):

    def __init__(self, person_name, suggested_friends):
        super().__init__()
        self.person = self['person'] = Person(person_name)
        self.suggested_friends = self['suggested_friends'] = suggested_friends
