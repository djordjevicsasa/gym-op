import podaci
import validacija
import pregled
import main
import datetime
import fajlovi

#1. tacka --> prijava na sistem

def prijava():
    print(f"\n{"=" *4} {" Prijava "} {"=" *4}")

    korisnicko_ime = validacija.validacija_in("\n1. Korisnicko ime: ", podaci.registrovani)

    validacija.validacija_lozinke("\n2. Lozinka (minimum 7 karaktera i barem 1 cifru): ", "prijava", korisnicko_ime)

    main.uloga(korisnicko_ime)

#4. tacka --> pretraga programa treninga

def pretraga_programa():
    print(f"\n{"=" * 4} {" Pretraga programa "} {"=" * 4}\n")
    print("1. Naziv programa")
    print("2. Vrsta programa")
    print("3. Vreme trajanja")
    print("4. Uplaceni paket")
    print("5. Visekriterijumska")
    print("0. Izlazak")

    podaci.pretrazeni_programi.clear()

    pom = validacija.validacija_radnje(5)

    if pom == 1:
        pregled.pregled_programa(podaci.programi)

        pom = validacija.validacija_stringa("\nNaziv programa: ")

        pretraga_programa_pomoc("naziv_programa", pom)

    elif pom == 2:
        pregled.pregled_programa(podaci.programi)

        pom = validacija.validacija_stringa("\nVrsta: ")

        pretraga_programa_pomoc("vrsta", pom)

    elif pom == 3:
        pretraga_programa_po_trajanju()

    elif pom == 4:
        pregled.pregled_programa(podaci.programi)

        pom = validacija.validacija_paketa("\nPaket (standardni/premium): ")

        pretraga_programa_pomoc("paket", pom)

    elif pom == 5:
        visekriterijumska_pretraga_programa()

    if pom != 0:
        if podaci.pretrazeni_programi != {}:
            pregled.pregled_programa(podaci.pretrazeni_programi)
        else:
            print("\nNe postoji")

def pretraga_programa_pomoc(kriterijum, pom):
    for kljuc, vrednost in podaci.programi.items():
        if pom == vrednost[kriterijum]:
            podaci.pretrazeni_programi[kljuc] = vrednost

def pretraga_programa_po_trajanju():
    print(f"\n{"=" * 4} {" Pretraga programa po vremenu "} {"=" * 4}\n")

    print("1. Minimalno vreme")
    print("2. Maksimalno vreme")
    print("3. Navodjenje granica")

    pom = validacija.validacija_radnje(3)

    if pom == 1:
        pregled.pregled_programa(podaci.programi)
        mini = validacija.validacija_broja("\nDonja granica: ")

        for kljuc, rec in podaci.programi.items():
            if int(rec["trajanje"]) >= mini:
                podaci.pretrazeni_programi[kljuc] = rec

    elif pom == 2:
        pregled.pregled_programa(podaci.programi)
        maxi = validacija.validacija_broja("\nGornja granica: ")

        for kljuc, rec in podaci.programi.items():
            if int(rec["trajanje"]) <= maxi:
                podaci.pretrazeni_programi[kljuc] = rec

    elif pom == 3:
        pregled.pregled_programa(podaci.programi)
        mini = validacija.validacija_broja("\nDonja granica: ")
        maxi = validacija.validacija_broja("\nGornja granica: ")

        maxi = validacija.validacija_granice(mini,maxi,"\nGornja granica: ")

        for kljuc, rec in podaci.programi.items():
            if mini <= int(rec["trajanje"]) <= maxi:
                podaci.pretrazeni_programi[kljuc] = rec

#5. tacka --> visekriterijumska pretraga programa treninga

def visekriterijumska_pretraga_programa():
    pom = podaci.programi.copy()

    print("\nDa li zelite da pretrazite po tom kriterijumu")

    kriterijum_naziv = validacija.validacija_da_li("\nNaziv (da/ne): ")
    kriterijum_vrsta = validacija.validacija_da_li("\nVrsta (da/ne): ")
    kriterijum_trajanje = validacija.validacija_da_li("\nTrajanje (da/ne): ")
    kriterijum_paket = validacija.validacija_da_li("\nPaket (da/ne): ")

    if kriterijum_naziv == "da" and podaci.programi != {}:
        pregled.pregled_programa(podaci.programi)

        naziv = validacija.validacija_stringa("\nNaziv programa: ")
        pretraga_programa_pomoc("naziv_programa", naziv)

        podaci.programi = podaci.pretrazeni_programi.copy()
        podaci.pretrazeni_programi.clear()

    if kriterijum_vrsta == "da" and podaci.programi!={}:
        pregled.pregled_programa(podaci.programi)

        vrsta = validacija.validacija_stringa("\nVrsta programa: ")
        pretraga_programa_pomoc("vrsta", vrsta)

        podaci.programi = podaci.pretrazeni_programi.copy()
        podaci.pretrazeni_programi.clear()

    if kriterijum_trajanje == "da" and podaci.programi != {}:
        pretraga_programa_po_trajanju()

        podaci.programi = podaci.pretrazeni_programi.copy()
        podaci.pretrazeni_programi.clear()

    if kriterijum_paket == "da" and podaci.programi != {}:
        pregled.pregled_programa(podaci.programi)

        paket = validacija.validacija_paketa("\nPaket (standradni/premium): ")
        pretraga_programa_pomoc("paket", paket)

        podaci.programi = podaci.pretrazeni_programi.copy()
        podaci.pretrazeni_programi.clear()

    podaci.pretrazeni_programi = podaci.programi.copy()
    podaci.programi = pom.copy()

#6. tacka --> pretraga termina treninga

def pretraga_termina(recnik):
    print(f"\n{"=" * 4} {" Pretraga termina "} {"=" * 4}\n")

    print("1. Program treninga")
    print("2. Sala")
    print("3. Uplaceni paket")
    print("4. Datum odrzavanja")
    print("5. Vreme odrzavanja")
    print("0. Izlazak")

    podaci.pretrazeni_treninzi.clear()

    pom = validacija.validacija_radnje(5)

    if pom == 1:
        pregled.pregled_programa(podaci.programi)

        pretraga_termina_naziv_programa(recnik)

    elif pom == 2:
        pregled.pregled_sala(podaci.sale)

        pretraga_termina_sifra_sale(recnik)

    elif pom == 3:
        pregled.pregled_programa(podaci.programi)

        pretraga_termina_paket_programa(recnik)

    elif pom == 4:
        pregled.pregled_termina(podaci.termini)

        pretraga_termina_datum_odrzavanja(recnik)

    elif pom == 5:
        pretraga_termina_po_vremenu(recnik)

    if pom != 0:
        if podaci.pretrazeni_treninzi != {}:
            pregled_treninga_pomoc(podaci.pretrazeni_treninzi)
            return True
        else:
            print("\nNe postoji")
            return False

def pretraga_termina_naziv_programa(recnik):
    naziv_programa = validacija.validacija_in("\nNaziv programa: ", podaci.programi)

    for kljuc, vrednost in recnik.items():

        if naziv_programa == vrednost["naziv_programa"]:
            pretrazeni_treninzi_set(kljuc, vrednost)

def pretraga_termina_sifra_sale(recnik):
    sifra_sale = validacija.validacija_in("\nSifra sale: ", podaci.sale)

    for kljuc, vrednost in recnik.items():

        if sifra_sale == vrednost["sifra_sale"]:
            pretrazeni_treninzi_set(kljuc, vrednost)

def pretraga_termina_paket_programa(recnik):
    paket = validacija.validacija_paketa("\nPaket (standardni/premium): ")

    for kljuc, vrednost in recnik.items():

        naziv_programa = vrednost["naziv_programa"]

        if paket == podaci.programi[naziv_programa]["paket"]:
            pretrazeni_treninzi_set(kljuc, vrednost)

def pretraga_termina_datum_odrzavanja(recnik):
    datum_odrzavanja = validacija.validacija_vremena("\nDatum (YYYY-MM-DD): ", "%Y-%m-%d")

    for kljuc, vrednost in recnik.items():

        if datum_odrzavanja.date() == vrednost["datum_odrzavanja"]:
            pretrazeni_treninzi_set(kljuc, vrednost)

def pretraga_termina_po_vremenu(recnik):
    print(f"\n{"=" * 4} {" Pretraga termina po vremenu "} {"=" * 4}")
    print("\n1. Pocetak termina")
    print("2. Kraj termina")
    print("3. Navodjenje granica")

    pom = validacija.validacija_radnje(3)

    if pom == 1:
        pregled.pregled_treninga(podaci.treninzi)

        mini = validacija.validacija_vremena("\nPocetak termina (HH:MM): ", "%H:%M").time()

        for kljuc, vrednost in recnik.items():

            if mini <= vrednost["pocetak"]:
                pretrazeni_treninzi_set(kljuc, vrednost)

    elif pom == 2:
        pregled.pregled_treninga(podaci.treninzi)

        maxi = validacija.validacija_vremena("\nKraj termina (HH:MM): ", "%H:%M").time()

        for kljuc, vrednost in recnik.items():

            if maxi >= vrednost["kraj"]:
                pretrazeni_treninzi_set(kljuc, vrednost)

    elif pom == 3:
        pregled.pregled_treninga(podaci.treninzi)

        mini = validacija.validacija_vremena("\nPocetak termina (HH:MM): ", "%H:%M")
        maxi = validacija.validacija_vremena("\nKraj termina (HH:MM): ", "%H:%M")

        maxi = validacija.validacija_granice(mini, maxi, "\nKraj termina: ")

        for kljuc, vrednost in recnik.items():

            if mini.time() <= vrednost["pocetak"] and maxi.time() >= vrednost["kraj"]:
                pretrazeni_treninzi_set(kljuc, vrednost)

def pretrazeni_treninzi_set(kljuc, vrednost):
    naziv_programa = vrednost["naziv_programa"]

    pom2 = {"naziv_programa": naziv_programa, "vrsta": podaci.programi[naziv_programa]["vrsta"],
            "sifra_sale": vrednost["sifra_sale"], "datum_odrzavanja": vrednost["datum_odrzavanja"],
            "pocetak": vrednost["pocetak"], "kraj": vrednost["kraj"],
            "paket": podaci.programi[naziv_programa]["paket"]}

    podaci.pretrazeni_treninzi[kljuc] = pom2

def pregled_treninga_pomoc(recnik):
    pom = False

    for sifra_termina, pom in recnik.items():
        datum_odrzavanja = pom["datum_odrzavanja"]

        if pregled.buduci_termin(datum_odrzavanja):
            pom = True
            break

    if pom:
        print(f"\n| {"sifra termina":<20} | {"naziv programa":<20} | {"vrsta programa":<20} | {"sala":<20} | {"datum odrzavanja":<20} | {"pocetak":<20} | {"kraj":<20} | {"uplaceni paket":<20}")
        print("-" * 180)

        for sifra_termina, pom in recnik.items():
            datum_odrzavanja = pom["datum_odrzavanja"]

            if pregled.buduci_termin(datum_odrzavanja):
                print(f"| {sifra_termina:<20} | {pom["naziv_programa"]:<20} | {pom["vrsta"]:<20} "
                      f"| {pom["sifra_sale"]:<20} | {pom["datum_odrzavanja"].strftime("%Y-%m-%d"):<20} "
                      f"| {pom["pocetak"].strftime("%H:%M"):<20} | {pom["kraj"].strftime("%H:%M"):<20} "
                      f"| {pom["paket"]:<20}")
    else:
        print("Ne postoji\n")

#7. tacka --> registracija

def registracija():
    print(f"\n{"=" * 4}{" Registracija "}{"=" * 4}")

    korisnicko_ime = validacija.validacija_not_in("\n1. Korisnicko ime: ", podaci.registrovani)

    lozinka = validacija.validacija_lozinke("\n2. Lozinka (minimum 7 karaktera i barem 1 cifru): ","","")

    ime = validacija.validacija_stringa("\n3. Ime: ")

    prezime = validacija.validacija_stringa("\n4. Prezime: ")

    datum_registracije = datetime.date.today()
    kraj_aktivnosti = datetime.datetime.today() + datetime.timedelta(days=30)
    kraj_aktivnosti = kraj_aktivnosti.date()

    pom = {"korisnicko_ime": korisnicko_ime, "lozinka": lozinka, "ime": ime, "prezime": prezime,
           "uloga": "clan", "status": "aktivan", "paket": "standardni",
           "datum_registracije": datum_registracije, "pocetak_aktivnosti":datum_registracije, "kraj_aktivnosti":kraj_aktivnosti}

    podaci.registrovani[korisnicko_ime] = pom

    fajlovi.sacuvaj_registrovane_u_fajl()
    main.meni_clana(korisnicko_ime)