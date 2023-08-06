from typing import List


class Person(dict):
    name: str

    def __init__(self, name: str):
        super().__init__()
        self.name = self['name'] = name


class Recommendations(dict):
    person: Person
    suggested_friends: List[Person]

    def __init__(self, person_name: str, suggested_friends: List[str]):
        super().__init__()
        self['person'] = Person(person_name)
        self['suggested_friends'] = [Person(sf) for sf in suggested_friends]
