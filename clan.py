import validacija
import pregled
import neregistrovani
import administrator
import podaci
import datetime
import fajlovi

#9. tacka --> rezervacija mesta clana

def rezervacija_mesta_clana(korisnicko_ime):
    print(f"\n{"=" * 4}{" Rezervacija mesta clana "}{"=" * 4}")

    if podaci.registrovani[korisnicko_ime]["status"] == "neaktivan":
        print("\nNeaktivni ste")
        return False

    print("\n1. Direktni unos sifre termina")
    print("2. Pretraga termina")

    radnja = validacija.validacija_radnje(2)

    podaci.pretrazeni_termini = podaci.termini.copy()
    pretrazeni_termini_set(korisnicko_ime)

    if datetime.date.today().weekday()!=4:
        set_termina_clana_pom(korisnicko_ime)

    if radnja == 1:
        pregled.pregled_termina(podaci.pretrazeni_termini)
    else:
        if not neregistrovani.pretraga_termina(podaci.pretrazeni_termini):
            return False

    sifra_termina = validacija.validacija_sifre_termina("\nSifra_termina: ")

    id_rezervacije = len(podaci.rezervacije)

    administrator.prikaz_mesta_u_obliku_matrice(sifra_termina, podaci.rezervacije)

    if validacija.validacija_popunjen_termin():
        return False

    rezervacija_mesta_clana_pom(id_rezervacije, korisnicko_ime, sifra_termina)

    pom = validacija.validacija_da_li("\nDa li zelite da dodate rezervaciju za neki drugi termin (da/ne): ")

    if pom == "da":
        rezervacija_mesta_clana(korisnicko_ime)

def pretrazeni_termini_set(korisnicko_ime):
    for id_rezervacije, vrednost in podaci.rezervacije.items():
        sifra_termina = vrednost["sifra_termina"]

        if vrednost["korisnicko_ime"] == korisnicko_ime:
            del podaci.pretrazeni_termini[sifra_termina]

def set_termina_clana_pom(korisnicko_ime):
    podaci.pretrazeni_pomoc.clear()

    for sifra_termina, vrednost in podaci.pretrazeni_termini.items():
        naziv_programa = vrednost["naziv_programa"]
        datum_odrzavanja = vrednost["datum_odrzavanja"]

        if pregled.buduci_termin(datum_odrzavanja) == False or (podaci.programi[naziv_programa]["paket"] == "premium" and podaci.registrovani[korisnicko_ime]["paket"] == "standardni"):
            continue

        podaci.pretrazeni_pomoc[sifra_termina] = vrednost

    podaci.pretrazeni_termini = podaci.pretrazeni_pomoc.copy()
    podaci.pretrazeni_pomoc.clear()

def rezervacija_mesta_clana_pom(id_rezervacije, korisnicko_ime, sifra_termina):
    rezervisano_mesto = validacija.validacija_nerezervisano_mesto("\nRezervisi mesto (x-rezervisana, ostala slobodna): ")

    datum_rezervacije = datetime.date.today()

    pomrez = {"korisnicko_ime": korisnicko_ime, "sifra_termina": sifra_termina,
              "oznaka_mesta": rezervisano_mesto, "datum_rezervacije": datum_rezervacije, "instruktor":""}

    podaci.rezervacije[id_rezervacije] = pomrez
    fajlovi.sacuvaj_rezervacije_u_fajl()

#10. tacka --> Pregled rezervacija

def pregled_rezervacije_clana(korisnicko_ime, recnik):
    print(f"\n{"=" * 4} Pregled rezervacije clana {"=" * 4}")

    if not is_found_clan(korisnicko_ime,recnik):
        return False

    print(f"\n| {"id rezervacije": <20} | {"korisnicko ime": <20} | {"sifra termina": <20} "
          f"| {"oznaka mesta": <20} | {"naziv programa": <20} | {"datum rezervacije": <20}"
          f" | {"pocetak": <20}  | {"kraj": <20}")

    print("-" * 160)

    for kljuc, pom in recnik.items():
        if pom["korisnicko_ime"] == korisnicko_ime:
            sifra_termina = pom["sifra_termina"]

            print(f"| {kljuc:<20} | {korisnicko_ime: <20} | {sifra_termina:<20} | {pom["oznaka_mesta"]:<20} "
                  f"| {podaci.termini[sifra_termina]["naziv_programa"]:<20} | {pom["datum_rezervacije"].strftime("%Y-%m-%d"):<20} "
                  f"| {podaci.termini[sifra_termina]["pocetak"].strftime("%H:%M"):<20} | {podaci.termini[sifra_termina]["kraj"].strftime("%H:%M"):<20}")

def is_found_clan(korisnicko_ime, recnik):
    found = False

    for id_rez, vrednost in recnik.items():
        if vrednost["korisnicko_ime"] == korisnicko_ime:
            found = True
            break

    if not found:
        print("\nNemate rezervisan termin")
        return False
    else:
        return True

#11. tacka --> Ponistavanje rezervacije mesta

def ponistavanje_rezervacije_mesta(korisnicko_ime):
    print(f"\n{"=" * 4} Ponistavanje rezervacije clana {"=" * 4}")

    if not is_found_clan(korisnicko_ime, podaci.rezervacije):
        return False

    print("\n1. Direktni unos id rezervacije")
    print("2. Pretraga rezervacije")

    radnja = validacija.validacija_radnje(2)

    if radnja == 1:
        if not is_found_clan(korisnicko_ime,podaci.rezervacije):
            return False

        pregled_rezervacije_clana(korisnicko_ime, podaci.rezervacije)
    else:
        pretrazivanje_rezervacija(korisnicko_ime)

        if not is_found_clan(korisnicko_ime,podaci.pretrazeni_rezervacije):
            return False

        pregled_rezervacije_clana(korisnicko_ime, podaci.pretrazeni_rezervacije)
        podaci.pretrazeni_rezervacije.clear()

    id_rezervacije = validacija.validacija_istekle_rezervacije()

    if id_rezervacije != "istekla":
        print("\nUspesno ste obrisali")
        del podaci.rezervacije[id_rezervacije]
        fajlovi.sacuvaj_rezervacije_u_fajl()

    pom = validacija.validacija_da_li("\nDa li zelite da obrisete jos neku rezervaciju: ")

    if pom == "da":
        ponistavanje_rezervacije_mesta(korisnicko_ime)

def pretrazivanje_rezervacija(korisnicko_ime):
    podaci.pretrazeni_termini.clear()
    podaci.pretrazeni_pomoc.clear()
    podaci.pretrazeni_rezervacije.clear()

    for id_rez, vrednost in podaci.rezervacije.items():
        if vrednost["korisnicko_ime"]==korisnicko_ime:
            sifra_termina = vrednost["sifra_termina"]
            podaci.pretrazeni_termini[sifra_termina]=podaci.termini[sifra_termina]
            podaci.pretrazeni_pomoc[id_rez]=vrednost

    pregled.pregled_termina(podaci.pretrazeni_termini)
    sifra_termina = validacija.validacija_sifre_termina("\n1. Sifra termina: ")

    administrator.prikaz_mesta_u_obliku_matrice(sifra_termina, podaci.pretrazeni_pomoc)

    if validacija.validacija_popunjen_termin():
        return False

    rezervisano_mesto = validacija.validacija_rezervisano_mesto("\n2. Rezervisano mesto (x-rezervisana): ")

    for id_rez, vrednost in podaci.pretrazeni_pomoc.items():
        if vrednost["oznaka_mesta"]==rezervisano_mesto and vrednost["sifra_termina"] == sifra_termina:
            podaci.pretrazeni_rezervacije[id_rez]=vrednost

    podaci.pretrazeni_termini.clear()
    podaci.pretrazeni_pomoc.clear()