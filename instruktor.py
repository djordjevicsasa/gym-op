import pregled
import podaci
import validacija
import administrator
import datetime
import fajlovi
import neregistrovani

# 12. tacka --> rezervacija mesta instruktora

def rezervacija_mesta_instruktora(korisnicko_ime):
    print(f"\n{"=" * 4}{" Rezervacija mesta instruktora "}{"=" * 4}")

    print("\n1. Direktni unos sifre termina")
    print("2. Pretraga termina")

    radnja = validacija.validacija_radnje(2)

    set_termini_pom_instruktora(korisnicko_ime)

    if radnja == 1:
        pregled.pregled_termina(podaci.pretrazeni_termini)
    else:
        if not neregistrovani.pretraga_termina(podaci.pretrazeni_termini):
            return False

    sifra_termina = validacija.validacija_sifre_termina("\nSifra_termina: ")

    set_registrovani_korisnici(sifra_termina)

    if not podaci.pretrazeni_registrovani:
        print("\nSvi korisnici su vec rezervisali taj termin")
        return False

    pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

    korisnicko_ime_clana = validacija.validacija_in("\nKorisnicko ime clana: ", podaci.pretrazeni_registrovani)

    administrator.prikaz_mesta_u_obliku_matrice(sifra_termina,podaci.rezervacije)

    if validacija.validacija_popunjen_termin():
        return False

    id_rezervacije = len(podaci.rezervacije)

    rezervacija_mesta_instruktora_pom(id_rezervacije, korisnicko_ime, korisnicko_ime_clana, sifra_termina)

    pom = validacija.validacija_da_li("\nDa li zelite da rezervisete mesta za neki drugi termin (da/ne): ")

    if pom == "da":
        rezervacija_mesta_instruktora(korisnicko_ime)

def set_termini_pom_instruktora(korisnicko_ime):
    for sifra_termina, vrednost in podaci.termini.items():
        naziv_programa = vrednost["naziv_programa"]
        datum_odrzavanja = vrednost["datum_odrzavanja"]

        if validacija.validacija_instruktor_program(naziv_programa, korisnicko_ime) and pregled.buduci_termin(datum_odrzavanja) == True:
            podaci.pretrazeni_termini[sifra_termina]=vrednost

def set_registrovani_korisnici(sifra_termina):
    podaci.pretrazeni_registrovani.clear()

    naziv_programa = podaci.termini[sifra_termina]["naziv_programa"]
    paket_programa = podaci.programi[naziv_programa]["paket"]

    for korisnicko_ime, vrednost in podaci.registrovani.items():
        found = False

        for id_rez, vrednost2 in podaci.rezervacije.items():
            if vrednost2["korisnicko_ime"] == korisnicko_ime and vrednost2["sifra_termina"] == sifra_termina:
                found = True

        if vrednost["uloga"] == "clan" and vrednost["status"] == "aktivan" and found==False:
            if datetime.date.today().weekday() != 4:
                if vrednost["paket"] == "premium":
                    podaci.pretrazeni_registrovani[korisnicko_ime] = vrednost
                elif paket_programa!="premium":
                    podaci.pretrazeni_registrovani[korisnicko_ime] = vrednost
            else:
                podaci.pretrazeni_registrovani[korisnicko_ime] = vrednost

def rezervacija_mesta_instruktora_pom(id_rezervacije, korisnicko_ime, korisnicko_ime_clana, sifra_termina):
    rezervisano_mesto = validacija.validacija_nerezervisano_mesto("\nRezervisi mesto (x-rezervisana, ostala slobodna): ")

    datum_rezervacije = datetime.date.today()

    pomrez = {"korisnicko_ime": korisnicko_ime_clana, "sifra_termina": sifra_termina,
              "oznaka_mesta": rezervisano_mesto, "datum_rezervacije": datum_rezervacije, "instruktor":korisnicko_ime}

    podaci.rezervacije[id_rezervacije] = pomrez
    fajlovi.sacuvaj_rezervacije_u_fajl()

# 13. tacka --> Pregled rezervacija instruktora

def pregled_rezervacije_instruktora(korisnicko_ime, recnik):
    print(f"\n{"=" * 4} Pregled rezervacije instuktora {"=" * 4}")

    if not is_found_instruktor(korisnicko_ime,recnik):
        return False

    print(
        f"\n| {"id rezervacije": <20} | {"korisnicko ime": <20} | {"sifra termina": <20} | {"ime clana": <20} | {"prezime clana": <20} | {"korisnicko ime clana": <20} "
        f"| {"naziv programa": <20} | {"datum rezervacije": <20} | {"pocetak": <20} | {"kraj": <20} | {"oznaka mesta": <20}")

    print("-" * 220)

    for kljuc, clanovi in recnik.items():
        sifra_termina = clanovi["sifra_termina"]
        korisnicko_ime_clana = clanovi["korisnicko_ime"]

        if clanovi["instruktor"] == korisnicko_ime:
            print(f"| {kljuc: <20} | {korisnicko_ime:<20} | {sifra_termina:<20} | {podaci.registrovani[korisnicko_ime_clana]["ime"]:<20} "
                  f"| {podaci.registrovani[korisnicko_ime_clana]["prezime"]:<20} | {korisnicko_ime_clana:<20}"
                  f"| {podaci.termini[sifra_termina]["naziv_programa"]:<20} | {clanovi["datum_rezervacije"].strftime("%Y-%m-%d"):<20} "
                  f"| {podaci.termini[sifra_termina]["pocetak"].strftime("%H:%M"):<20} | {podaci.termini[sifra_termina]["kraj"].strftime("%H:%M"):<20} | {clanovi["oznaka_mesta"]:<20}")

# 14. tacka --> Ponistavanje rezervacije mesta instuktora

def ponistavanje_rezervacije_mesta_instuktora(korisnicko_ime):
    print(f"\n{"=" * 4} Ponistavanje rezervacije instuktora {"=" * 4}")

    if not is_found_instruktor(korisnicko_ime, podaci.rezervacije):
        return False

    print("\n1. Direktni unos id rezervacije")
    print("2. Pretraga rezervacije")

    radnja = validacija.validacija_radnje(2)

    if radnja == 1:
        if not is_found_instruktor(korisnicko_ime, podaci.rezervacije):
            return False

        pregled_rezervacije_instruktora(korisnicko_ime, podaci.rezervacije)
    else:
        instruktor_pretrazivanje_rezervacija(korisnicko_ime)

        if not is_found_instruktor(korisnicko_ime, podaci.pretrazeni_rezervacije):
            return False

        pregled_rezervacije_instruktora(korisnicko_ime, podaci.pretrazeni_rezervacije)
        podaci.pretrazeni_rezervacije.clear()

    id_rezervacije = validacija.validacija_istekle_rezervacije()

    if id_rezervacije != "istekla":
        del podaci.rezervacije[id_rezervacije]
        fajlovi.sacuvaj_rezervacije_u_fajl()

    pom = validacija.validacija_da_li("\nDa li zelite da obrsite jos neku rezervaciju: ")

    if pom == "da":
        ponistavanje_rezervacije_mesta_instuktora(korisnicko_ime)

def is_found_instruktor(korisnicko_ime, recnik):
    found = False

    for id_rez, vrednost in recnik.items():
        if vrednost["instruktor"] == korisnicko_ime:
            found = True
            break

    if not found:
        print("\nNemate rezervisan termin")
        return False
    else:
        return True

def instruktor_pretrazivanje_rezervacija(korisnicko_ime):
    podaci.pretrazeni_termini.clear()
    podaci.pretrazeni_pomoc.clear()
    podaci.pretrazeni_rezervacije.clear()

    for id_rez, vrednost in podaci.rezervacije.items():
        if vrednost["instruktor"] == korisnicko_ime:
            sifra_termina = vrednost["sifra_termina"]
            podaci.pretrazeni_termini[sifra_termina] = podaci.termini[sifra_termina]
            podaci.pretrazeni_pomoc[id_rez] = vrednost

    pregled.pregled_termina(podaci.pretrazeni_termini)
    sifra_termina = validacija.validacija_sifre_termina("\n1. Sifra termina: ")

    administrator.prikaz_mesta_u_obliku_matrice(sifra_termina, podaci.pretrazeni_pomoc)

    if validacija.validacija_popunjen_termin():
        return False

    rezervisano_mesto = validacija.validacija_rezervisano_mesto("\n2. Rezervisano mesto (x-rezervisana): ")

    for id_rez, vrednost in podaci.pretrazeni_pomoc.items():
        if vrednost["oznaka_mesta"] == rezervisano_mesto and vrednost["sifra_termina"] == sifra_termina:
            podaci.pretrazeni_rezervacije[id_rez] = vrednost

    podaci.pretrazeni_termini.clear()
    podaci.pretrazeni_pomoc.clear()

# 15. Pretraga rezervisanih mesta

def pretraga_rezervacija(korisnicko_ime):
    print(f"\n{"=" * 4}{" Pretraga rezervacija "}{"=" * 4}\n")
    print("1. Sifra treninga")
    print("2. Ime clana")
    print("3. Prezime clana")
    print("4. Datum odrzavanja")
    print("5. Vreme pocetka/kraja")
    print("0. Izlazak")

    pom = validacija.validacija_radnje(5)

    podaci.pretrazeni_rezervacije.clear()

    if pom == 1:
        pregled.pregled_treninga(podaci.treninzi)

        sifra_treninga = validacija.validacija_sifre_treninga("\nSifra treninga: ")

        pretraga_rezervacije_po_treningu(sifra_treninga, korisnicko_ime)
    elif pom == 2:
        pretraga_clanova()

        pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

        ime_clana = validacija.validacija_stringa("\nIme clana: ")

        pretraga_rezervacije_po_clanu("ime", ime_clana, korisnicko_ime)
    elif pom == 3:
        pretraga_clanova()

        pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

        prezime_clana = validacija.validacija_stringa("\nPrezime clana: ")

        pretraga_rezervacije_po_clanu("prezime", prezime_clana, korisnicko_ime)
    elif pom == 4:
        pregled.pregled_termina(podaci.termini)

        pretraga_rezervacije_po_terminu(korisnicko_ime)
    elif pom == 5:
        pregled.pregled_treninga(podaci.treninzi)

        pretraga_rezervacije_po_vremenu(korisnicko_ime)

    if pom != 0:
        if podaci.pretrazeni_rezervacije != {}:
            pregled_rezervacije_instruktora(korisnicko_ime, podaci.pretrazeni_rezervacije)
        else:
            print("\nNe postoji")

def pretraga_clanova():
    podaci.pretrazeni_registrovani.clear()

    for korisnicko_ime, vrednost in podaci.registrovani.items():
        if vrednost["uloga"] == "clan" and vrednost["status"] == "aktivan":
            podaci.pretrazeni_registrovani[korisnicko_ime] = vrednost

def pretraga_rezervacije_po_treningu(sifra_treninga, korisnicko_ime):
    for kljuc, vrednost in podaci.rezervacije.items():
        if vrednost["sifra_termina"][:4] == sifra_treninga and vrednost["instruktor"] == korisnicko_ime:
            podaci.pretrazeni_rezervacije[kljuc] = vrednost

def pretraga_rezervacije_po_clanu(parametar, pom, korisnicko_ime):
    for id_rezervacije, vrednost in podaci.rezervacije.items():
        korime = vrednost["korisnicko_ime"]

        if vrednost["instruktor"] == korisnicko_ime and podaci.registrovani[korime][parametar] == pom:
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

def pretraga_rezervacije_po_terminu(korisnicko_ime):
    datum_odrzavanja = validacija.validacija_vremena("\nDatum odrzavanja termina: ", "%Y-%m-%d").date()

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]

        if podaci.termini[sifra_termina]["datum_odrzavanja"] == datum_odrzavanja and vrednost["instruktor"] == korisnicko_ime:
            print("da")
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

def pretraga_rezervacije_po_vremenu(korisnicko_ime):
    mini = validacija.validacija_vremena("\nPocetak: ", "%H:%M")
    maxi = validacija.validacija_vremena("\nKraj: ", "%H:%M")
    maxi = validacija.validacija_granice(mini, maxi, "\nKraj: ")

    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]

        if (vrednost["instruktor"] == korisnicko_ime
                and mini.time() <= podaci.termini[sifra_termina]["pocetak"] and maxi.time() >= podaci.termini[sifra_termina]["kraj"]):
            podaci.pretrazeni_rezervacije[id_rezervacije] = vrednost

# 16. Aktivacija statusa clana

def aktivacija_statusa_clana():
    print(f"\n{"=" * 4}{" Aktivacija statusa clana "}{"=" * 4}")

    podaci.pretrazeni_registrovani.clear()

    for kljuc, vrednost in podaci.registrovani.items():
        if vrednost["uloga"] == "clan" and vrednost["status"] == "neaktivan":
            podaci.pretrazeni_registrovani[kljuc] = vrednost

    if podaci.pretrazeni_registrovani == {}:
        print("\nNe postoji")
        return False

    pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

    korisnicko_ime_clana = validacija.validacija_in("\nKorisnicko ime clana: ", podaci.pretrazeni_registrovani)

    podaci.registrovani[korisnicko_ime_clana]["status"] = "aktivan"
    podaci.registrovani[korisnicko_ime_clana]["paket"] = "standardni"

    kraj_aktivnosti = datetime.datetime.today() + datetime.timedelta(days=30)
    kraj_aktivnosti = kraj_aktivnosti.date()

    podaci.registrovani[korisnicko_ime_clana]["pocetak_aktivnosti"] = datetime.date.today()
    podaci.registrovani[korisnicko_ime_clana]["kraj_aktivnosti"] = kraj_aktivnosti

    print(f"\n{korisnicko_ime_clana} je aktivan do {podaci.registrovani[korisnicko_ime_clana]["kraj_aktivnosti"]}")
    fajlovi.sacuvaj_registrovane_u_fajl()

# datum isteka aktivnosti

def datum_isteka_aktivnosti():
    for korisnicko_ime, vrednost in podaci.registrovani.items():
        if vrednost["status"] == "aktivan" and vrednost["uloga"] == "clan":
            kraj_aktivnosti = datetime.datetime.strptime(vrednost["kraj_aktivnosti"],"%Y-%m-%d")

            if datetime.datetime.today() >= kraj_aktivnosti:
                vrednost["status"] = "neaktivan"
                vrednost["paket"] = ""

    fajlovi.sacuvaj_registrovane_u_fajl()

# 17. Aktivacija premium paketa clanstva

def aktivacija_premium_paketa_clana():
    print(f"\n{"=" * 4}{" Aktivacija premium paketa "}{"=" * 4}")

    podaci.pretrazeni_registrovani.clear()

    for kljuc, vrednost in podaci.registrovani.items():
        if vrednost["uloga"] == "clan" and vrednost["paket"] == "standardni":
            podaci.pretrazeni_registrovani[kljuc] = vrednost

    if podaci.pretrazeni_registrovani == {}:
        print("\nNe postoji")
        return False

    pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

    korisnicko_ime_clana = validacija.validacija_in("\nKorisnicko ime clana: ", podaci.pretrazeni_registrovani)

    podaci.registrovani[korisnicko_ime_clana]["paket"] = "premium"
    print(f"\n{korisnicko_ime_clana} ima premium paket do {podaci.registrovani[korisnicko_ime_clana]["kraj_aktivnosti"]}")
    fajlovi.sacuvaj_registrovane_u_fajl()

# 18. Izmena rezervacije mesta

def izmena_rezervacije(korisnicko_ime):
    print(f"\n{"=" * 4}{" Izmena rezervacije "}{"=" * 4}")

    if not is_found_instruktor(korisnicko_ime,podaci.rezervacije):
        return False

    instruktor_pretrazivanje_rezervacija(korisnicko_ime)

    pregled_rezervacije_instruktora(korisnicko_ime, podaci.pretrazeni_rezervacije)

    id_clana = validacija.validacija_istekle_rezervacije()

    if id_clana == "istekla":
        return False

    # izmena rezervacije

    set_termini_pom_instruktora(korisnicko_ime)

    pregled.pregled_termina(podaci.pretrazeni_termini)

    sifra_termina = validacija.validacija_sifre_termina("\n1. Sifra termina: ")

    set_registrovani_korisnici(sifra_termina)

    pregled.pregled_registrovanih(podaci.pretrazeni_registrovani)

    korisnicko_ime_clana = validacija.validacija_in("\n2. Korisnicko ime clana: ", podaci.pretrazeni_registrovani)

    administrator.prikaz_mesta_u_obliku_matrice(sifra_termina, podaci.rezervacije)

    if validacija.validacija_popunjen_termin():
        return False

    rezervisano_mesto = validacija.validacija_nerezervisano_mesto("\n3. Rezervisano mesto (x-rezervisana): ")

    podaci.rezervacije[id_clana]["sifra_termina"] = sifra_termina
    podaci.rezervacije[id_clana]["korisnicko_ime"] = korisnicko_ime_clana
    podaci.rezervacije[id_clana]["oznaka_mesta"] = rezervisano_mesto

    fajlovi.sacuvaj_rezervacije_u_fajl()

    print("\nizmena je uspesno izvrsena")