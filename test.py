class Voter(object):
    def __init__(self, position, agenda_setter, veto_player):
        self.position = position
        self.agenda_setter = agenda_setter
        self.veto_player = veto_player

voterA = Voter((1.0, 2.0), True, False)
voterB = Voter((3.2, 4.1), False, True)

voters = [voterA, voterB]
vetos = []
for i in range(0,2):
    voters[i].position = 13
    if voters[i].veto_player == True:
        pasta = voters[i]


print voterA.position
print voterB.position

pasta.position = 1000

print voterA.position
print voterB.position
