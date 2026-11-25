import validacija
import datetime
import podaci
import pregled
import fajlovi
import izvestavanja

#19. Registracija novih instruktora/administratora

def registracija_novih_instruktora_administratora():
    print(f"\n{"=" * 4} {" Registracija novih instuktora/administratora "} {"=" * 4}")

    print("\n1. Instruktor")
    print("2. Administrator")

    pom = validacija.validacija_radnje(2)

    korisnicko_ime = validacija.validacija_not_in("\n1. Korisnicko ime: ", podaci.registrovani)
    lozinka = validacija.validacija_lozinke("\n2. Lozinka (minimum 7 karaktera i barem 1 cifru): ", "", "")
    ime = validacija.validacija_stringa("\n3. Ime: ")
    prezime = validacija.validacija_stringa("\n4. Prezime: ")

    if pom == 1:
        uloga = "instruktor"
    else:
        uloga = "administrator"

    datum_registracije = datetime.date.today()

    pom = {"korisnicko_ime": korisnicko_ime, "lozinka": lozinka, "ime": ime, "prezime": prezime,
           "uloga": uloga, "status": "aktivan", "paket": "",
           "datum_registracije": datum_registracije, "pocetak_aktivnosti": datum_registracije, "kraj_aktivnosti": ""}

    podaci.registrovani[korisnicko_ime] = pom
    fajlovi.sacuvaj_registrovane_u_fajl()

#20. izvestavanje

def izvestavanje():
    print(f"\n{"=" * 4} {" Izvestavanje "} {"=" * 4}")

    print("\n1. Datum rezervacije")
    print("2. Datum termina treninga")
    print("3. Datum rezervacije i odabranog instruktora")
    print("4. Dan odrzavanja termina")
    print("5. Broj rezervacija po instruktorima")
    print("6. Broj rezervacija po paketu clanstva")
    print("7. Najpopularniji programi treninga")
    print("8. Najpopularniji dan u nedelji")
    print("0. Izlaz")

    pom = validacija.validacija_radnje(8)

    podaci.pretrazeni_rezervacije.clear()

    if pom == 1:
        pregled.pregled_rezervacija(podaci.rezervacije)

        datum_rezervacije = validacija.validacija_vremena("\nDatum rezervacije: ","%Y-%m-%d").date()

        izvestavanje_datum_rezervacije(datum_rezervacije)
    elif pom == 2:
        pregled.pregled_termina(podaci.termini)

        datum_odrzvanja = validacija.validacija_vremena("\nDatum termina treninga: ","%Y-%m-%d").date()

        izvestavanje_datum_termina(datum_odrzvanja)
    elif pom == 3:
        izvestavanje_datum_rezervacije_instruktor()
    elif pom == 4:
        izvestavanje_dan_u_nedelji()
    elif pom == 5:
        izvestavanje_broj_rezervacija_instruktora()
    elif pom == 6:
        izvestavanje_broj_rezervacija_po_paketu_clanstva()
    elif pom == 7:
        izvestavanje_najpopularniji_programi()
    elif pom == 8:
        izvestavanje_najpopularniji_dan_u_nedelji()

    podaci.pretrazeni_rezervacije.clear()

def izvestavanje_datum_rezervacije(datum_rezervacije):
    for kljuc, vrednost in podaci.rezervacije.items():
        if vrednost["datum_rezervacije"] == datum_rezervacije:
            podaci.pretrazeni_rezervacije[kljuc] = vrednost

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_rezervacija(podaci.pretrazeni_rezervacije)
        izvestavanja.sacuvaj_izvestaje_rezervacija_u_fajl()
    else:
        print("\nNe postoji")

def izvestavanje_datum_termina(datum_odrzavanja):
    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]

        if podaci.termini[sifra_termina]["datum_odrzavanja"] == datum_odrzavanja:
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_rezervacija(podaci.pretrazeni_rezervacije)
        izvestavanja.sacuvaj_izvestaje_rezervacija_u_fajl()
    else:
        print("\nNe postoji")

def izvestavanje_datum_rezervacije_instruktor():
    podaci.pretrazeni_registrovani.clear()

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        if vrednost["instruktor"]!="":
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

    pregled.pregled_rezervacija(podaci.pretrazeni_rezervacije)

    datum_rezervacije = validacija.validacija_vremena("\n1. Datum rezervacije: ","%Y-%m-%d").date()

    for id_rezervacije, vrednost in podaci.pretrazeni_rezervacije.items():
        instruktor = vrednost["instruktor"]

        if vrednost["datum_rezervacije"] == datum_rezervacije:
            podaci.pretrazeni_registrovani[instruktor] = podaci.registrovani[instruktor]

    pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

    korisnicko_ime = validacija.validacija_in("\n2. Korisnicko ime instruktora: ", podaci.pretrazeni_registrovani)

    podaci.pretrazeni_rezervacije.clear()

    for kljuc, vrednost in podaci.rezervacije.items():
        if vrednost["datum_rezervacije"] == datum_rezervacije and vrednost["instruktor"] == korisnicko_ime:
            podaci.pretrazeni_rezervacije[kljuc] = vrednost

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_rezervacija(podaci.pretrazeni_rezervacije)
        izvestavanja.sacuvaj_izvestaje_rezervacija_u_fajl()
    else:
        print("\nNe postoji")

def izvestavanje_dan_u_nedelji():
    pregled.pregled_termina(podaci.termini)

    dan = validacija.validacija_stringa("\nDan u nedelji: ")

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]
        dani = podaci.termini[sifra_termina]["dani"]

        if dan == dani:
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_rezervacija(podaci.pretrazeni_rezervacije)
        izvestavanja.sacuvaj_izvestaje_rezervacija_u_fajl()
    else:
        print("\nNe postoji")

def izvestavanje_broj_rezervacija_instruktora():
    for kljuc, vrednost in podaci.registrovani.items():
        broj = 0
        if vrednost["uloga"] == "instruktor":
            for kljuc2, vrednost2 in podaci.rezervacije.items():
                datum_rezervacije = vrednost2["datum_rezervacije"]

                if (vrednost2["instruktor"] == kljuc and
                        (datetime.datetime.today() - datetime.timedelta(days=30)).date()
                <= datum_rezervacije <= datetime.date.today()):
                    broj+=1

            podaci.pretrazeni_rezervacije[kljuc] = broj

    podaci.sortiran = dict(sorted(podaci.pretrazeni_rezervacije.items(), key=lambda x:x[1], reverse = True))

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_broja(podaci.sortiran, "instruktor")
        izvestavanja.sacuvaj_izvestaje_broja_u_fajl(podaci.sortiran)
    else:
        print("\nNe postoji")

def izvestavanje_broj_rezervacija_po_paketu_clanstva():
    brp = 0
    brs = 0

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]
        naziv_programa = podaci.termini[sifra_termina]["naziv_programa"]

        datum_rezervacije = vrednost["datum_rezervacije"]

        if ((datetime.datetime.today() - datetime.timedelta(days=30)).date()
                <= datum_rezervacije <= datetime.date.today()):
            if podaci.programi[naziv_programa]["paket"] == "standardni":
                brs += 1
            if podaci.programi[naziv_programa]["paket"] == "premium":
                brp += 1

    podaci.pretrazeni_rezervacije["standarni"] = brs
    podaci.pretrazeni_rezervacije["premium"] = brp

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_broja(podaci.pretrazeni_rezervacije, "paket")
        izvestavanja.sacuvaj_izvestaje_broja_u_fajl(podaci.pretrazeni_rezervacije)
    else:
        print("\nNe postoji")

def izvestavanje_najpopularniji_programi():
    for kljuc, vrednost in podaci.programi.items():
        br = 0
        for id_rezervacije, vrednost2 in podaci.rezervacije.items():
            sifra_termina = vrednost2["sifra_termina"]
            naziv_programa = podaci.termini[sifra_termina]["naziv_programa"]

            datum_rezervacije = vrednost2["datum_rezervacije"]

            if ((datetime.datetime.today() - datetime.timedelta(days=365)).date()
                    <= datum_rezervacije <= datetime.date.today() and naziv_programa == kljuc):
                br += 1

        podaci.pretrazeni_rezervacije[kljuc] = br

    podaci.sortiran = dict(sorted(podaci.pretrazeni_rezervacije.items(), key = lambda x:x[1], reverse=True))

    br = 0

    podaci.najpopularniji.clear()

    for kljuc, vrednost in podaci.sortiran.items():
        if br == 3:
            break

        podaci.najpopularniji[kljuc] = vrednost
        br+=1

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_broja(podaci.najpopularniji, "program")
        izvestavanja.sacuvaj_izvestaje_broja_u_fajl(podaci.najpopularniji)
    else:
        print("\nNe postoji")

def izvestavanje_najpopularniji_dan_u_nedelji():
    podaci.pretrazeni_rezervacije = {"ponedeljak":0, "utorak":0, "sreda":0, "cetvrtak":0, "petak":0, "subota":0, "nedelja":0}

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]
        dani = podaci.termini[sifra_termina]["dani"]

        if dani == "ponedeljak":
            podaci.pretrazeni_rezervacije["ponedeljak"] += 1
        elif dani == "utorak":
            podaci.pretrazeni_rezervacije["utorak"] += 1
        elif dani == "sreda":
            podaci.pretrazeni_rezervacije["sreda"] += 1
        elif dani == "cetvrtak":
            podaci.pretrazeni_rezervacije["cetvrtak"] += 1
        elif dani == "petak":
            podaci.pretrazeni_rezervacije["petak"] += 1
        elif dani == "subota":
            podaci.pretrazeni_rezervacije["subota"] += 1
        else:
            podaci.pretrazeni_rezervacije["nedelja"] += 1

    maks = max(podaci.pretrazeni_rezervacije.values())

    podaci.najpopularniji.clear()

    for kljuc, vrednost in podaci.pretrazeni_rezervacije.items():
        if vrednost == maks:
            podaci.najpopularniji[kljuc] = vrednost

    if podaci.pretrazeni_rezervacije != {}:
        izvestavanja.pregled_broja(podaci.najpopularniji, "dan")
        izvestavanja.sacuvaj_izvestaje_broja_u_fajl(podaci.najpopularniji)
    else:
        print("\nNe postoji")

#21. tacka --> Mesecna nagrada lojalnosti

def mesecna_nagrada_lojalnosti():
    print(f"\n{"=" * 4} {" Mesecna nagrada lojalnosti "} {"=" * 4}")

    if datetime.date.strftime(datetime.date.today(),"%Y-%m-%d") != "%Y-%m-01":
        print("\nNije prvi u mesecu")
        return False

    pom = 0

    for kljuc1, vrednost1 in podaci.registrovani.items():
        br = 0

        if vrednost1["uloga"] != "clan":
            continue

        for kljuc2, vrednost2 in podaci.rezervacije.items():

            datum_rezervacija = vrednost2["datum_rezervacije"]
            if (vrednost2["korisnicko_ime"] == kljuc1
                    and (datetime.datetime.today()-datetime.timedelta(days=30)).date() <= datum_rezervacija <= datetime.date.today()):
                br+=1

        if br>27:
            podaci.registrovani[kljuc1]["paket"] = "premium"
            podaci.registrovani[kljuc1]["status"] = "aktivan"

            kraj_aktivnosti = datetime.datetime.today() + datetime.timedelta(days=30)
            kraj_aktivnosti = kraj_aktivnosti.date()

            podaci.registrovani[kljuc1]["pocetak_aktivnosti"] = datetime.date.today()
            podaci.registrovani[kljuc1]["kraj_aktivnosti"] = kraj_aktivnosti

            print(f"\n{kljuc1} je ostvario mesecnu nagradu lojalnosti")
            pom = 1

    if pom == 0:
        print("\nNiko nije ostvario mesecnu nagradu lojalnosti")

    fajlovi.sacuvaj_registrovane_u_fajl()

#22. tacka --> prikaz mesta u obliku matrice

def prikaz_mesta_u_obliku_matrice(sifra_termina, recnik):
    podaci.tabela.clear()
    podaci.red_vrsta.clear()
    sifra_treninga = sifra_termina[:4]
    sifra_sale = podaci.treninzi[sifra_treninga]["sifra_sale"]

    for pom_red in range(int(podaci.sale[sifra_sale]["broj_redova"])):
        red = pom_red+1
        print(f"\n{"red " + str(red) + " |":<10} ", end="")
        for pom_vrsta in range(int(podaci.sale[sifra_sale]["oznaka_mesta_u_svakom_redu"])):
            vrsta = pom_vrsta+1
            mesto = chr(96+vrsta)
            oznaka_mesta = str(red)+str(mesto)

            slobodno = True

            for kljuc, vrednost in recnik.items():
                if sifra_termina == vrednost["sifra_termina"] and oznaka_mesta in vrednost["oznaka_mesta"]:
                    slobodno = False

            if slobodno:
                pom = {oznaka_mesta: mesto}
                print(f"{mesto:<5}", end="")
            else:
                pom = {oznaka_mesta: "x"}
                print(f"{"x":<5}", end="")

            podaci.red_vrsta.update(pom)

        podaci.tabela[red] = podaci.red_vrsta.copy()
        print()

#24. tacka --> Unos, izmena i brisanje programa treninga

def upravljenje_programima():
    print(f"\n{"=" * 4} {" Upravljanje programima "} {"=" * 4}")

    print("\n1. Unos programa")
    print("2. Izmena programa")
    print("3. Brisanje programa")
    print("0. Izlazak")

    pom = validacija.validacija_radnje(3)

    if pom == 1 or pom == 2:
        naziv_programa = None

        pregled.pregled_programa(podaci.programi)

        if pom == 1:
            naziv_programa = validacija.validacija_not_in("\n1. Naziv programa: ", podaci.programi)

        if pom == 2:
            naziv_programa = validacija.validacija_in("\n1. Naziv programa: ", podaci.programi)

        vrsta = validacija.validacija_stringa("\n2. Vrsta programa: ")

        trajanje = validacija.validacija_broja("\n3. Trajanje: ")

        podaci.pretrazeni_registrovani.clear()

        for kljuc, vrednost in podaci.registrovani.items():
            if vrednost["uloga"] == "instruktor":
                podaci.pretrazeni_registrovani[kljuc] = vrednost

        pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

        instruktori = validacija.validacija_instruktora_i_dana("\n4. Instruktori u formatu (instuktor1 instruktor2): ", podaci.pretrazeni_registrovani)

        opis = validacija.validacija_stringa("\n5. Opis: ")

        if pom == 1:
            paket = validacija.validacija_paketa("\n6. Paket (standardni/premium): ")
        else:
            paket = podaci.programi[naziv_programa]["paket"]

        pom2 = {"naziv_programa": naziv_programa, "vrsta": vrsta, "trajanje": trajanje,
               "instruktori": instruktori, "opis": opis, "paket": paket}

        podaci.programi[naziv_programa] = pom2
        fajlovi.sacuvaj_programe_u_fajl()

    elif pom == 3:
        pregled.pregled_programa(podaci.programi)

        naziv_programa = validacija.validacija_in("\nNaziv programa: ", podaci.programi)

        del podaci.programi[naziv_programa]
        fajlovi.sacuvaj_programe_u_fajl()

        for kljuc, vrednost in podaci.termini.items():
            sifra_treninga = kljuc[:4]

            if vrednost["naziv_programa"] == naziv_programa:
                vrednost["naziv_programa"] = ""
                podaci.treninzi[sifra_treninga]["naziv_programa"] = ""

                fajlovi.sacuvaj_treninge_u_fajl()

#25. tacka --> Unos, izmena i brisanje treninga

def upravljenje_treninzima():
    print(f"\n{"=" * 4} {" Upravljanje treninzima "} {"=" * 4}")

    print("\n1. Unos treninga")
    print("2. Izmena treninga")
    print("3. Brisanje treninga")
    print("0. Izlazak")

    pom = validacija.validacija_radnje(3)

    if pom == 1 or pom == 2:
        sifra_treninga = None

        pregled.pregled_treninga(podaci.treninzi)

        if pom == 1:
            sifra_treninga = validacija.validacija_not_in("\n1. Sifra treninga: ", podaci.treninzi)

        if pom == 2:
            sifra_treninga = validacija.validacija_in("\n1. Sifra treninga: ", podaci.treninzi)

        pregled.pregled_sala(podaci.sale)

        sifra_sale = validacija.validacija_in("\n2. Sifra sale: ", podaci.sale)

        pocetak = validacija.validacija_vremena("\n3. Pocetak: ", "%H:%M")

        kraj = validacija.validacija_vremena("\n4. Kraj: ", "%H:%M")

        validacija.validacija_granice(pocetak,kraj, "\n4. Kraj: ")

        dani = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]

        dani = validacija.validacija_instruktora_i_dana("\n5. Dani u formatu (ponedeljak sreda): ", dani)
        #dani = validacija.validacija_instruktora_i_dana("\n5. Dani: ")

        pregled.pregled_programa(podaci.programi)

        naziv_programa = validacija.validacija_in("\n6. Naziv programa: ", podaci.programi)

        pom2 = {"sifra_treninga": sifra_treninga, "sifra_sale": sifra_sale, "pocetak": pocetak,
                "kraj": kraj, "dani": dani, "naziv_programa": naziv_programa}

        podaci.treninzi[sifra_treninga] = pom2
        fajlovi.sacuvaj_treninge_u_fajl()

        if pom == 1:
            dodavanje_termina(sifra_treninga, pom2)

    elif pom == 3:
        pregled.pregled_treninga(podaci.treninzi)

        sifra_treninga = validacija.validacija_sifre_treninga("\nSifra treninga: ")

        del podaci.treninzi[sifra_treninga]
        fajlovi.sacuvaj_treninge_u_fajl()

        for kljuc in list(podaci.termini.keys()):
            if kljuc[:4] == sifra_treninga:
                del podaci.termini[kljuc]

        fajlovi.sacuvaj_termine_u_fajl()

#unos i brisanje termina

def dodavanje_termina(sifra_treninga, vrednost):
    dani = vrednost["dani"].split(",")

    for i in range(0, len(dani)):
        for j in range(0,2):
            dani[i] = dani[i].strip()
            sifra_termina = str(sifra_treninga) + str(i+1) + str(j+1)

            broj = dani_u_nedelji(dani[i], j)

            datum_odrzavanja = datetime.datetime.today()+datetime.timedelta(days=broj)

            pom = {"sifra_termina":sifra_termina, "datum_odrzavanja":datum_odrzavanja.date(), "sifra_sale":vrednost["sifra_sale"],
                   "pocetak":vrednost["pocetak"], "kraj":vrednost["kraj"], "dani":dani[i], "naziv_programa":vrednost["naziv_programa"]}

            podaci.termini[sifra_termina] = pom

    fajlovi.sacuvaj_termine_u_fajl()

#dani u nedelji

def dani_u_nedelji(dan, nedelja):
    if dan == "ponedeljak":
        br = 0
    elif dan == "utorak":
        br = 1
    elif dan == "sreda":
        br = 2
    elif dan == "cetvrtak":
        br = 3
    elif dan == "petak":
        br = 4
    elif dan == "subota":
        br = 5
    else:
        br = 6

    pom = br - datetime.date.today().weekday()

    if pom<=0:
        if nedelja == 0:
            return pom+7
        else:
            return pom+14
    else:
        if nedelja == 0:
            return pom
        else:
            return pom+7