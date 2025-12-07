import random # Ezzel választjuk ki véletlenszerűen a szót.
import PySimpleGUI as sg # Ez a könyvtár felelős a grafikus ablakunkért (a GUI-ért).

# -----------------------------------------------
# 1. Játék Állapota és Beállítások
# -----------------------------------------------

# A szavak, amikből a gép választani fog. Mind nagybetűs, hogy könnyebb legyen a kezelés.
SZAVAK = ["PROGRAMOZAS", "AKASZTOFA", "PYTHON", "BEADANDO", "NEMBIROMMAR", "NEBUKTASSONMEG"]
max_hibak = 6 # Fixen 6 hibás tipp után vége a játéknak (ennyi képünk van).

# Játék inicializálása (Új játék indításakor ezt a függvényt hívjuk)
def jatek_inditasa():
    """Új játék kezdetekor beállítja az állapotot."""
    # Véletlenszerűen kiválasztunk egy szót a listából és nagybetűssé tesszük.
    titkos_szo = random.choice(SZAVAK).upper()
    # Ebben a halmazban tároljuk, hogy mely betűket találta már el a játékos.
    kitalalt_betuk = set()
    # A hibás tippek száma, kezdetben nulla.
    hibas_tippek = 0
    # Visszaadjuk a játék alapállapotát.
    return titkos_szo, kitalalt_betuk, hibas_tippek

# Először is beállítjuk a játék kezdeti állapotát.
titkos_szo, kitalalt_betuk, hibas_tippek = jatek_inditasa()
hasznalt_betuk = set() # Ez tárolja az összes már tippelt betűt (rosszat és jót is).

# -----------------------------------------------
# 2. Logikai Függvények (A játék agya)
# -----------------------------------------------

def szot_megjelenit(titkos_szo, kitalalt_betuk):
    """
    Ez a rész felelős azért, hogy a kitalálatlan betűk helyett aláhúzást ('_') mutassunk.
    Pl. ha a szó 'PYTHON', és kitaláltuk a 'P'-t, akkor 'P _ _ _ _ _' lesz.
    """
    megjelenitett_szo = ""
    for betu in titkos_szo:
        if betu in kitalalt_betuk:
            # Ha a betű benne van a kitaláltak között, kiírjuk.
            megjelenitett_szo += betu + " "
        else:
            # Ha nincs benne, aláhúzást teszünk a helyére.
            megjelenitett_szo += "_ "
    return megjelenitett_szo.strip()

def nyertel_ellenorzes(titkos_szo, kitalalt_betuk):
    """
    Ez egy egyszerű ellenőrzés: megnézzük, hogy a titkos szó minden betűje
    benne van-e már a 'kitalalt_betuk' halmazban.
    """
    return all(betu in kitalalt_betuk for betu in titkos_szo)

# -----------------------------------------------
# 3. PYSIMPLEGUI ELRENDEZÉS (LAYOUT)
# -----------------------------------------------

# Létrehozzuk az első maszkolt szót, ami megjelenik a játék indításakor.
kezdeti_megjelenites = szot_megjelenit(titkos_szo, kitalalt_betuk)

# Itt definiáljuk az ablakunk kinézetét (ez egy lista, ami sorokat tartalmaz):
layout = [
    # 1. sor: Itt jelenik meg az akasztófa képe.
    # sg.Push() fixálja a képet középen, hogy ne ugorjon el!
    [sg.Push(), sg.Image(filename='0.png', size=(200, 400), key='-IMAGE-', subsample=4), sg.Push()],
    
    # 2. sor: Itt a maszkolt szó nagy betűkkel, középre igazítva.
    [sg.Text(kezdeti_megjelenites, size=(20, 1), justification='center', 
             font=('Helvetica', 30), key='-WORD-')],
    
    # 3. sor: A beviteli mező és a két gomb (Tipp és Új Játék).
    [sg.Text('Tippelj betűt:'), sg.Input(key='-INPUT-', size=(3, 1), enable_events=True, focus=True), 
     sg.Button('Tipp', key='-GUESS_BUTTON-'), sg.Button('Új Játék', key='-NEW_GAME-')],
    
    # 4. sor: Itt láthatja a felhasználó, hogy mely betűket használta már.
    [sg.Text('Már használt betűk: ', key='-USED_LETTERS-')],
    
    # 5. sor: Itt adjuk a visszajelzéseket (Helyes/Rossz tipp, Nyertél/Vesztettél).
    [sg.Text('Kezdődhet a játék!', key='-MESSAGE-')]
]

# -----------------------------------------------
# 4. ABLAK ÉS ESEMÉNYCIKLUS (FŐ CIKLUS)
# -----------------------------------------------

# Létrehozzuk az ablakot, fix méretet adunk neki, hogy ne változzon (ez volt az ugrálás ellenszere).
ablak = sg.Window('Akasztófa Játék', layout, finalize=True, size=(500, 700))

jatek_fut = True # Logikai változó, ami igaz, amíg a játék tart.

while True:
    # Ez a sor vár egy eseményre (pl. gombnyomásra vagy ablak bezárására).
    event, values = ablak.read()
    
    # Ha bezárják az ablakot, kilépünk a ciklusból.
    if event == sg.WIN_CLOSED:
        break

    # Új játék indítása
    if event == '-NEW_GAME-':
        # Visszaállítjuk az összes változót a 'jatek_inditasa' függvénnyel.
        titkos_szo, kitalalt_betuk, hibas_tippek = jatek_inditasa()
        hasznalt_betuk = set()
        jatek_fut = True
        
        # Frissítjük a GUI elemeket az alapállapothoz.
        ablak['-WORD-'].update(szot_megjelenit(titkos_szo, kitalalt_betuk))
        ablak['-IMAGE-'].update(filename='0.png', subsample=4) # Vissza a 0. képhez.
        ablak['-USED_LETTERS-'].update('Már használt betűk: ')
        ablak['-MESSAGE-'].update('Kezdődhet a játék!')

    # Tipp gomb eseménye (ez a legfontosabb logika)
    if jatek_fut and event == '-GUESS_BUTTON-':
        
        tipp = values['-INPUT-'].upper().strip() # Kinyerjük a tippet, nagybetűsítjük, szóközöket levágjuk.
        ablak['-INPUT-'].update('') # Kiürítjük a beviteli mezőt.

        # Ellenőrizzük, hogy csak egy betűt adott-e meg a felhasználó.
        if not tipp or len(tipp) != 1 or not tipp.isalpha():
            ablak['-MESSAGE-'].update('Kérlek, egyetlen betűt adj meg!', text_color='red')
            continue # Tovább lépünk, nem számoljuk hibának.
        
        # Ellenőrizzük, hogy már tippelte-e ezt a betűt.
        if tipp in hasznalt_betuk:
            ablak['-MESSAGE-'].update(f"A(z) {tipp} betűt már tippelted!", text_color='orange')
            continue
            
        hasznalt_betuk.add(tipp) # Hozzáadjuk a tippelt betűk halmazához.
        # Frissítjük a használt betűk listáját.
        ablak['-USED_LETTERS-'].update(f'Már használt betűk: {", ".join(sorted(hasznalt_betuk))}')

        if tipp in titkos_szo:
            # Találat!
            kitalalt_betuk.add(tipp)
            ablak['-WORD-'].update(szot_megjelenit(titkos_szo, kitalalt_betuk)) # Frissítjük a maszkolt szót.
            ablak['-MESSAGE-'].update('Helyes találat!', text_color='green')

            # Ellenőrizzük, hogy ezzel nyert-e.
            if nyertel_ellenorzes(titkos_szo, kitalalt_betuk):
                ablak['-MESSAGE-'].update(f'GRATULÁLOK! Kitaláltad a szót: {titkos_szo}', text_color='blue')
                jatek_fut = False # Lezárjuk a játékot.
                
        else:
            # Rossz találat!
            hibas_tippek += 1
            # Frissítjük a képet a hibás tippek száma alapján (1.png, 2.png, stb.).
            ablak['-IMAGE-'].update(filename=f'{hibas_tippek}.png', subsample=4) 
            ablak['-MESSAGE-'].update(f'Rossz találat! Még {max_hibak - hibas_tippek} próbálkozás van.', text_color='red')

            # Ellenőrizzük, hogy ezzel vesztett-e.
            if hibas_tippek >= max_hibak:
                ablak['-MESSAGE-'].update(f'VÉGE A JÁTÉKNAK! A szó: {titkos_szo}', text_color='red')
                jatek_fut = False # Lezárjuk a játékot.

ablak.close() # Ha kilépünk a ciklusból, bezárjuk az ablakot.