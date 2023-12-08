from session import Session

#TestDaten

Spieler = ["A","B","C","D","E"]

test_session = Session("Test")

test_session.new_session(Spieler, force = True)

for i in range(5):
    print(i)
    test_session.log_game(Spieler[0:4], test_session.NORMALSPIEL, Spieler[1:3], 4, 1)
    print(test_session.Bockrunden)
for i in range(2):
    print(i)
    test_session.log_game(Spieler[0:4], test_session.NORMALSPIEL, Spieler[1:3], 4, 0)
    print(test_session.Bockrunden)

test_session2 = Session("Test")
test_session2.load_session()

print(test_session.Bockrunden)
print(test_session2.Bockrunden)

print(test_session.Punkte.df)
print(test_session2.Punkte.df)