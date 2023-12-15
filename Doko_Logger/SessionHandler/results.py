from dateutil.parser import parse

def Results(session):
    # Load Session Module for Session Points
    #session = Session(filename, add_json=False)
    #session.load_session()

    # Letzte Runde lesen
    endrunde = session.Punkte.df.loc[len(session.Punkte.df)-1]

    # Get Session Info
    Datum = session.data["Session_Info"]["Datum"]
    Session_Spieler = session.Spieler
    
    #Position berechnen
    Positionen = __session_position(endrunde[Session_Spieler])

    # Stats erstellen
    stats = {}
    for Spieler in Session_Spieler:
        session_Spielerstats = {}

        #Session_Info
        session_Spielerstats["Datum"] = parse(Datum)
        session_Spielerstats["Runden"] = endrunde["Runde"]
        session_Spielerstats["Spieler"]= Session_Spieler

        #Endstand
        session_Spielerstats["Punkte"] = endrunde[Spieler]
        session_Spielerstats["Position"] = Positionen[Spieler]
        
        #Persönliche Stats
        session_Spielerstats.update(__session_performance(Spieler, session))
        
        #Statistik anhängen
        stats[Spieler] = session_Spielerstats

    return stats



def __session_performance(Spieler, session):
    # Performance für alles Spiele der Session für angegebenen Spieler erstellen
    performance = { "Siege":0, 
                    "Soli":0, 
                    "Soli_gewonnen":0, 
                    "bestes_Spiel": -10000, 
                    "schlechtestes_Spiel": 10000}

    # Spiele durchgehen
    for Spiel in session.data["Spiele"]:

        # Nur wenn aktiver Spieler:
        if Spieler in Spiel["Spieler"]:

            #Punkte für Spieler im Spiel berechnen (Punkte, Soli, Bockrunden)
            Punkte = session.Punkte.calc_points(Spiel)[Spieler]

            # Siege
            if Spieler in Spiel["Gewinner"]:
                performance["Siege"] += 1

            # Soli / Soli_gewonnen
            if Spiel["Spieltyp"] == session.SOLO:
                if len(Spiel["Gewinner"])==1 and (Spieler in Spiel["Gewinner"]):
                    performance["Soli"] += 1
                    performance["Soli_gewonnen"] += 1
                elif len(Spiel["Gewinner"])==3 and not (Spieler in Spiel["Gewinner"]):
                    performance["Soli"] += 1
            
            # bestes_Spiel / schlechtestes_Spiel
            if Punkte > performance["bestes_Spiel"]:
                performance["bestes_Spiel"] = Punkte
            if Punkte < performance["schlechtestes_Spiel"]:
                performance["schlechtestes_Spiel"] = Punkte

    return performance



def __session_position(endstand):
    
    # Spieler nach Punkten aufsteigen sortieren 
    Namen_sortiert = endstand.sort_values(ascending=False).index
    
    #In Dict umrechnen und Gleichstand herausrechnen
    Positionen={Namen_sortiert[0]:1}
    for i in range(1,len(Namen_sortiert),1):
        if endstand[Namen_sortiert[i]]==endstand[Namen_sortiert[i-1]]:
            Positionen[Namen_sortiert[i]]=Positionen[Namen_sortiert[i-1]]
        else:
            Positionen[Namen_sortiert[i]]=i+1
    
    return Positionen
