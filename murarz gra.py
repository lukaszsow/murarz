import pygame
import random
import sys
import time

pygame.init()

SZEROKOSC, WYSOKOSC = 800, 600
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Symulator Murarza')

BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
NIEBIESKI = (0, 0, 255)
SZARY = (200, 200, 200)
BRAZOWY = (139, 69, 19)

czcionka_mala = pygame.font.SysFont('Verdana', 20)
czcionka_srednia = pygame.font.SysFont('Verdana', 30)
czcionka_duza = pygame.font.SysFont('Verdana', 50)

class StanGry:
    def __init__(self):
        self.pieniadze = 0
        self.exp = 0
        self.aktualna_zaprawa = "Podstawowa"
        self.bonus_zaprawa = 1
        self.poziom = 1
        self.czas_akcji = 0.0

stan = StanGry()

def rysuj_tekst(tekst, czcionka, kolor, x, y, srodek=False):
    obraz = czcionka.render(tekst, True, kolor)
    prostokat = obraz.get_rect()
    if srodek:
        prostokat.center = (x, y)
    else:
        prostokat.topleft = (x, y)
    ekran.blit(obraz, prostokat)
    return prostokat

def rysuj_przycisk(tekst, x, y, szerokosc, wysokosc, kolor_nieaktywny, kolor_aktywny):
    pozycja_myszy = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    prostokat = pygame.Rect(x, y, szerokosc, wysokosc)
    if prostokat.collidepoint(pozycja_myszy):
        pygame.draw.rect(ekran, kolor_aktywny, prostokat)
        if klikniecie:
            return True
    else:
        pygame.draw.rect(ekran, kolor_nieaktywny, prostokat)
    pygame.draw.rect(ekran, CZARNY, prostokat, 2)
    rysuj_tekst(tekst, czcionka_srednia, CZARNY, prostokat.centerx, prostokat.centery, True)
    return False

def cutscenka():
    tekst_cutscenki = [
        "Masz 18 lat.",
        "Ojciec właśnie wyrzucił Cię z domu.",
        "\"Idź pracować, darmozjadzie!\" - krzyczał.",
        "Nie masz wykształcenia ani perspektyw.",
        "Ale masz dwie ręce do pracy.",
        "Postanawiasz zostać...",
        "Murarzem.",
        "To początek Twojej murarskiej przygody...",
        "Naciśnij SPACJĘ, aby rozpocząć grę."
    ]
    linia = 0
    czas = 0
    predkosc_tekstu = 1.5
    while linia < len(tekst_cutscenki):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        czas_teraz = time.time()
        if czas_teraz - czas > predkosc_tekstu:
            czas = czas_teraz
            linia += 1
        ekran.fill(CZARNY)
        for i in range(min(linia, len(tekst_cutscenki))):
            rysuj_tekst(tekst_cutscenki[i], czcionka_srednia, BIALY, SZEROKOSC // 2, 150 + i * 50, True)
        pygame.display.flip()

def minigra_stawianie_cegiel(poziom_trudnosci=None, specjalne=False):
    plansza = []
    szerokosc_cegly = 60
    wysokosc_cegly = 30
    
    if specjalne:
        ilosc_kolumn = 10
        ilosc_wierszy = 10
    else:
        ilosc_kolumn = 7
        ilosc_wierszy = 5
    
    odstep = 2
    
    czas_trwania = 20
    if poziom_trudnosci:
        if poziom_trudnosci == "Łatwe":
            czas_trwania = 30
        elif poziom_trudnosci == "Średnie":
            czas_trwania = 20
        elif poziom_trudnosci == "Trudne":
            czas_trwania = 10
        elif poziom_trudnosci == "Ultra":
            czas_trwania = 40
    
    for wiersz in range(ilosc_wierszy):
        nowy_wiersz = []
        for kolumna in range(ilosc_kolumn):
            if random.random() < 0.7:
                nowy_wiersz.append(1)
            else:
                nowy_wiersz.append(0)
        plansza.append(nowy_wiersz)
    
    puste_miejsca = sum(row.count(0) for row in plansza)
    postawione_cegly = 0
    
    czas_start = time.time()
    minigra_aktywna = True
    bonus_czasowy = 0
    czas_pozostaly = czas_trwania
    
    while minigra_aktywna:
        czas_teraz = time.time()
        czas_pozostaly = max(0, czas_start + czas_trwania - czas_teraz)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                for wiersz in range(ilosc_wierszy):
                    for kolumna in range(ilosc_kolumn):
                        lewy = (SZEROKOSC - (szerokosc_cegly + odstep) * ilosc_kolumn) // 2 + kolumna * (szerokosc_cegly + odstep)
                        gorny = 100 + wiersz * (wysokosc_cegly + odstep)
                        
                        if (lewy <= x <= lewy + szerokosc_cegly and 
                            gorny <= y <= gorny + wysokosc_cegly and 
                            plansza[wiersz][kolumna] == 0):
                            plansza[wiersz][kolumna] = 1
                            postawione_cegly += 1
                            
                            if postawione_cegly >= puste_miejsca:
                                minigra_aktywna = False
        
        if czas_pozostaly <= 0:
            minigra_aktywna = False
            
        ekran.fill(SZARY)
        
        for wiersz in range(ilosc_wierszy):
            for kolumna in range(ilosc_kolumn):
                lewy = (SZEROKOSC - (szerokosc_cegly + odstep) * ilosc_kolumn) // 2 + kolumna * (szerokosc_cegly + odstep)
                gorny = 100 + wiersz * (wysokosc_cegly + odstep)
                
                kolor = BRAZOWY if plansza[wiersz][kolumna] == 1 else BIALY
                pygame.draw.rect(ekran, kolor, (lewy, gorny, szerokosc_cegly, wysokosc_cegly))
                pygame.draw.rect(ekran, CZARNY, (lewy, gorny, szerokosc_cegly, wysokosc_cegly), 1)
        
        rysuj_tekst(f"Czas: {int(czas_pozostaly)} s", czcionka_srednia, CZARNY, 10, 10)
        rysuj_tekst(f"Postawione cegły: {postawione_cegly}/{puste_miejsca}", czcionka_srednia, CZARNY, 10, 50)
        
        pygame.display.flip()
    
    zlecenie_ukonczone = postawione_cegly >= puste_miejsca
    procent_ukonczenia = postawione_cegly / puste_miejsca if puste_miejsca > 0 else 0
    podstawowa_nagroda_pieniadze = int(50 * procent_ukonczenia * stan.bonus_zaprawa)
    podstawowa_nagroda_exp = int(15 * procent_ukonczenia)
    
    if zlecenie_ukonczone and czas_pozostaly > 0:
        bonus_czasowy = int(czas_pozostaly * 2)
        podstawowa_nagroda_pieniadze += bonus_czasowy
        podstawowa_nagroda_exp += bonus_czasowy // 3
    
    ekran.fill(SZARY)
    
    if zlecenie_ukonczone:
        rysuj_tekst("Minigra zakończona!", czcionka_duza, CZARNY, SZEROKOSC // 2, 150, True)
        rysuj_tekst(f"Postawiłeś {postawione_cegly} z {puste_miejsca} cegieł ({int(procent_ukonczenia * 100)}%)", 
                  czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst(f"Zarabiasz: {podstawowa_nagroda_pieniadze} zł", czcionka_srednia, CZARNY, SZEROKOSC // 2, 270, True)
        rysuj_tekst(f"Zdobywasz: {podstawowa_nagroda_exp} exp", czcionka_srednia, CZARNY, SZEROKOSC // 2, 320, True)
        
        if czas_pozostaly > 0:
            rysuj_tekst(f"Bonus za szybkość: {bonus_czasowy} zł", czcionka_srednia, ZIELONY, SZEROKOSC // 2, 370, True)
    else:
        rysuj_tekst("Czas minął! Zlecenie niezakończone.", czcionka_duza, CZERWONY, SZEROKOSC // 2, 150, True)
        rysuj_tekst(f"Postawiłeś tylko {postawione_cegly} z {puste_miejsca} cegieł ({int(procent_ukonczenia * 100)}%)", 
                  czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst("Brak nagrody!", czcionka_srednia, CZERWONY, SZEROKOSC // 2, 270, True)
    
    rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 450, True)
    
    pygame.display.flip()
    
    czekaj_na_klikniecie = True
    while czekaj_na_klikniecie:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                czekaj_na_klikniecie = False
                
    if not poziom_trudnosci:
        stan.pieniadze += podstawowa_nagroda_pieniadze
        stan.exp += podstawowa_nagroda_exp
        
        stary_poziom = stan.poziom
        stan.poziom = 1 + stan.exp // 80
        
        if stan.poziom > stary_poziom:
            ekran.fill(SZARY)
            rysuj_tekst(f"Awans na poziom {stan.poziom}!", czcionka_duza, ZIELONY, SZEROKOSC // 2, 250, True)
            rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 350, True)
            pygame.display.flip()
            
            czekaj_na_klikniecie = True
            while czekaj_na_klikniecie:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        czekaj_na_klikniecie = False
    
    return zlecenie_ukonczone, podstawowa_nagroda_pieniadze, podstawowa_nagroda_exp

def kup_skrzynke():
    wybrano_skrzynke = False
    
    while not wybrano_skrzynke:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        ekran.fill(SZARY)
        rysuj_tekst("Wybierz skrzynkę", czcionka_duza, CZARNY, SZEROKOSC // 2, 100, True)
        rysuj_tekst(f"Masz: {stan.pieniadze} zł", czcionka_srednia, CZARNY, SZEROKOSC // 2, 150, True)
        
        przycisk_skrzynka1 = rysuj_przycisk("Skrzynka 50 zł", SZEROKOSC // 2 - 130, 200, 260, 50, (200, 150, 100), (230, 180, 130))
        przycisk_skrzynka2 = rysuj_przycisk("Skrzynka 100 zł", SZEROKOSC // 2 - 130, 300, 260, 50, (150, 150, 200), (180, 180, 230))
        przycisk_skrzynka3 = rysuj_przycisk("Skrzynka 150 zł", SZEROKOSC // 2 - 130, 400, 260, 50, (150, 200, 150), (180, 230, 180))
        przycisk_powrot = rysuj_przycisk("Powrót", SZEROKOSC // 2 - 100, 460, 200, 40, CZERWONY, (255, 100, 100))
        
        if przycisk_skrzynka1 and stan.pieniadze >= 50:
            wybrano_skrzynke = True
            stan.pieniadze -= 50
            otworz_skrzynke(1)
        elif przycisk_skrzynka2 and stan.pieniadze >= 100:
            wybrano_skrzynke = True
            stan.pieniadze -= 100
            otworz_skrzynke(2)
        elif przycisk_skrzynka3 and stan.pieniadze >= 150:
            wybrano_skrzynke = True
            stan.pieniadze -= 150
            otworz_skrzynke(3)
        elif przycisk_powrot:
            return
            
        pygame.display.flip()

def otworz_skrzynke(poziom_skrzynki):
    zaprawy = {
        1: [
            {"nazwa": "Podstawowa", "bonus": 1, "szansa": 60},
            {"nazwa": "Wzmocniona", "bonus": 1.2, "szansa": 30},
            {"nazwa": "Premium", "bonus": 1.5, "szansa": 10}
        ],
        2: [
            {"nazwa": "Podstawowa", "bonus": 1, "szansa": 40},
            {"nazwa": "Wzmocniona", "bonus": 1.2, "szansa": 40},
            {"nazwa": "Premium", "bonus": 1.5, "szansa": 15},
            {"nazwa": "Super Premium", "bonus": 2, "szansa": 5}
        ],
        3: [
            {"nazwa": "Wzmocniona", "bonus": 1.2, "szansa": 45},
            {"nazwa": "Premium", "bonus": 1.5, "szansa": 30},
            {"nazwa": "Super Premium", "bonus": 2, "szansa": 20},
            {"nazwa": "Ultra Premium", "bonus": 3, "szansa": 5}
        ]
    }
    
    lista_zapraw = zaprawy[poziom_skrzynki]
    losowa_liczba = random.randint(1, 100)
    suma_szans = 0
    wylosowana_zaprawa = {"nazwa": "Podstawowa", "bonus": 1, "szansa": 100}
    
    for zaprawa in lista_zapraw:
        suma_szans += zaprawa["szansa"]
        if losowa_liczba <= suma_szans:
            wylosowana_zaprawa = zaprawa
            break
    
    for i in range(10):
        ekran.fill(SZARY)
        rysuj_tekst("Otwieranie skrzynki...", czcionka_duza, CZARNY, SZEROKOSC // 2, 200, True)
        szerokosc_skrzynki = 200
        wysokosc_skrzynki = 150
        lewy = SZEROKOSC // 2 - szerokosc_skrzynki // 2
        gorny = 250
        kolor_skrzynki = (200 + random.randint(-20, 20), 150 + random.randint(-20, 20), 100 + random.randint(-20, 20))
        pygame.draw.rect(ekran, kolor_skrzynki, (lewy, gorny, szerokosc_skrzynki, wysokosc_skrzynki))
        pygame.draw.rect(ekran, CZARNY, (lewy, gorny, szerokosc_skrzynki, wysokosc_skrzynki), 3)
        pygame.display.flip()
        pygame.time.delay(200)
    
    ekran.fill(SZARY)
    rysuj_tekst("Wylosowałeś zaprawę:", czcionka_duza, CZARNY, SZEROKOSC // 2, 150, True)
    rysuj_tekst(f"{wylosowana_zaprawa['nazwa']}", czcionka_duza, ZIELONY, SZEROKOSC // 2, 220, True)
    rysuj_tekst(f"Bonus: x{wylosowana_zaprawa['bonus']}", czcionka_srednia, CZARNY, SZEROKOSC // 2, 280, True)
    
    if wylosowana_zaprawa['bonus'] > stan.bonus_zaprawa:
        stan.aktualna_zaprawa = wylosowana_zaprawa['nazwa']
        stan.bonus_zaprawa = wylosowana_zaprawa['bonus']
        rysuj_tekst("To lepsza zaprawa niż miałeś!", czcionka_srednia, ZIELONY, SZEROKOSC // 2, 330, True)
    else:
        rysuj_tekst("Masz już lepszą zaprawę", czcionka_srednia, CZERWONY, SZEROKOSC // 2, 330, True)
    
    rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 400, True)
    pygame.display.flip()
    
    czekaj_na_klikniecie = True
    while czekaj_na_klikniecie:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                czekaj_na_klikniecie = False

def generuj_zlecenia():
    poziomy_trudnosci = [
        {"nazwa": "Łatwe", "mnoznik": 0.5},
        {"nazwa": "Średnie", "mnoznik": 1.0},
        {"nazwa": "Trudne", "mnoznik": 2.0}
    ]
    
    rodzaje_zlecen = [
        "Naprawa muru",
        "Budowa ogrodzenia",
        "Budowa garażu",
        "Remont łazienki",
        "Budowa komina",
        "Wyburzanie ściany",
        "Układanie posadzki",
        "Budowa altanki",
        "Renowacja bruku"
    ]
    
    zlecenia = []
    
    for _ in range(3):
        poziom = random.choice(poziomy_trudnosci)
        rodzaj = random.choice(rodzaje_zlecen)
        
        base_pieniadze = 100 * stan.poziom
        base_exp = 20 * stan.poziom
        
        pieniadze = int(base_pieniadze * poziom["mnoznik"] * (0.9 + random.random() * 0.2))
        exp = int(base_exp * poziom["mnoznik"] * (0.9 + random.random() * 0.2))
        
        zlecenia.append({
            "nazwa": f"{poziom['nazwa']} zlecenie: {rodzaj}",
            "pieniadze": pieniadze,
            "exp": exp,
            "poziom_trudnosci": poziom["nazwa"]
        })
    
    if stan.poziom >= 5:
        zlecenia.append({
            "nazwa": "SPECJALNE: Ultra Mur",
            "pieniadze": 500 * stan.poziom,
            "exp": 100 * stan.poziom,
            "specjalne": True,
            "poziom_trudnosci": "Ultra"
        })
    
    return zlecenia

def idz_na_zlecenie():
    zlecenia = generuj_zlecenia()
    wybrano_zlecenie = False
    
    while not wybrano_zlecenie:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        ekran.fill(SZARY)
        rysuj_tekst("Wybierz zlecenie", czcionka_duza, CZARNY, SZEROKOSC // 2, 80, True)
        
        y_start = 150
        przyciski = []
        
        for i, zlecenie in enumerate(zlecenia):
            przycisk = rysuj_przycisk(
                f"{zlecenie['nazwa']}", 
                SZEROKOSC // 2 - 300, y_start + i * 80, 600, 60, 
                (100, 150, 200), (130, 180, 230)
            )
            przyciski.append(przycisk)
            
            rysuj_tekst(f"Zapłata: {zlecenie['pieniadze']} zł    EXP: {zlecenie['exp']}", 
                      czcionka_mala, CZARNY, SZEROKOSC // 2, y_start + i * 80 + 70, True)
        
        przycisk_powrot = rysuj_przycisk("Powrót", 15, 15, 165, 40, CZERWONY, (255, 100, 100))
        
        for i, klikniety in enumerate(przyciski):
            if klikniety:
                wybrano_zlecenie = True
                zlecenie = zlecenia[i]
                
                if "specjalne" in zlecenie and zlecenie["specjalne"]:
                    minigra_ultra_mur(zlecenie)
                else:
                    wykonaj_zlecenie(zlecenie)
        
        if przycisk_powrot:
            return
            
        pygame.display.flip()

def wykonaj_zlecenie(zlecenie):
    zlecenie_ukonczone, nagroda_pieniadze, nagroda_exp = minigra_stawianie_cegiel(
        poziom_trudnosci=zlecenie.get("poziom_trudnosci"))
    
    if zlecenie_ukonczone:
        ekran.fill(SZARY)
        rysuj_tekst("Zlecenie wykonane!", czcionka_duza, ZIELONY, SZEROKOSC // 2, 150, True)
        rysuj_tekst(f"Zarobiłeś: {nagroda_pieniadze} zł", czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst(f"Zdobywasz: {nagroda_exp} exp", czcionka_srednia, CZARNY, SZEROKOSC // 2, 270, True)
        
        stan.pieniadze += nagroda_pieniadze
        stan.exp += nagroda_exp
    else:
        ekran.fill(SZARY)
        rysuj_tekst("Zlecenie niewykonane!", czcionka_duza, CZERWONY, SZEROKOSC // 2, 150, True)
        rysuj_tekst("Nie zdążyłeś postawić wszystkich cegieł w terminie!", czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst("Nie otrzymujesz zapłaty.", czcionka_srednia, CZERWONY, SZEROKOSC // 2, 270, True)
    
    rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 350, True)
    
    pygame.display.flip()
    
    czekaj_na_klikniecie = True
    while czekaj_na_klikniecie:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                czekaj_na_klikniecie = False
    
    if zlecenie_ukonczone:
        stary_poziom = stan.poziom
        ile_poziomow = stan.exp // 80
        stan.poziom = 1 + ile_poziomow
        
        if stan.poziom > stary_poziom:
            ekran.fill(SZARY)
            rysuj_tekst(f"Awans na poziom {stan.poziom}!", czcionka_duza, ZIELONY, SZEROKOSC // 2, 250, True)
            rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 350, True)
            pygame.display.flip()
            
            czekaj_na_klikniecie = True
            while czekaj_na_klikniecie:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        czekaj_na_klikniecie = False

def minigra_ultra_mur(zlecenie):
    zlecenie_ukonczone, nagroda_pieniadze, nagroda_exp = minigra_stawianie_cegiel(
        poziom_trudnosci="Ultra", specjalne=True)
    
    if zlecenie_ukonczone:
        ekran.fill(SZARY)
        rysuj_tekst("GRATULACJE!", czcionka_duza, ZIELONY, SZEROKOSC // 2, 150, True)
        rysuj_tekst("Ukończyłeś Ultra Mur!", czcionka_duza, ZIELONY, SZEROKOSC // 2, 200, True)
        rysuj_tekst(f"Zarobiłeś: {nagroda_pieniadze} zł", czcionka_srednia, CZARNY, SZEROKOSC // 2, 270, True)
        rysuj_tekst(f"Zdobywasz: {nagroda_exp} exp", czcionka_srednia, CZARNY, SZEROKOSC // 2, 320, True)
        
        pygame.display.flip()
        pygame.time.delay(2000)
        
        ekran.fill(CZARNY)
        rysuj_tekst("KONIEC GRY!", czcionka_duza, BIALY, SZEROKOSC // 2, 180, True)
        rysuj_tekst("Przeszedłeś symulator murarza", czcionka_srednia, BIALY, SZEROKOSC // 2, 250, True)
        rysuj_tekst("Dziękujemy za grę", czcionka_srednia, BIALY, SZEROKOSC // 2, 300, True)
        rysuj_tekst(f"Twój końcowy poziom: {stan.poziom}", czcionka_srednia, BIALY, SZEROKOSC // 2, 350, True)
        rysuj_tekst(f"Twoje końcowe pieniądze: {stan.pieniadze} zł", czcionka_srednia, BIALY, SZEROKOSC // 2, 390, True)
        rysuj_tekst("Kliknij, aby zakończyć", czcionka_srednia, BIALY, SZEROKOSC // 2, 450, True)
        
        pygame.display.flip()
        
        czekaj_na_klikniecie = True
        while czekaj_na_klikniecie:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pygame.quit()
                    sys.exit()
    else:
        ekran.fill(SZARY)
        rysuj_tekst("Ultra Mur - NIEPOWODZENIE", czcionka_duza, CZERWONY, SZEROKOSC // 2, 150, True)
        rysuj_tekst("Nie zdążyłeś ukończyć zadania w wyznaczonym czasie!", czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst("Spróbuj ponownie, gdy będziesz gotowy.", czcionka_srednia, CZARNY, SZEROKOSC // 2, 270, True)
        rysuj_tekst("Kliknij, aby kontynuować", czcionka_srednia, CZARNY, SZEROKOSC // 2, 350, True)
        
        pygame.display.flip()
        
        czekaj_na_klikniecie = True
        while czekaj_na_klikniecie:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    czekaj_na_klikniecie = False

def cheat():
    stan.poziom = 10
    stan.pieniadze = 10000
    stan.exp = 800
    stan.bonus_zaprawa = 3
    stan.aktualna_zaprawa = "Ultra Premium"

muzyka = pygame.mixer.Sound("piosenka z bajki sąsiedzi.wav")
muzyka.set_volume(0.05)

def glowna_petla():
    cutscenka()
    muzyka.play(loops = -1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    cheat()
                
        czas_teraz = time.time()
        if czas_teraz - stan.czas_akcji < 0.1:
            continue
            
        ekran.fill(SZARY)
        
        poziom_exp = stan.exp % 80
        maks_exp = 80
        
        rysuj_tekst(f"Poziom: {stan.poziom}", czcionka_srednia, CZARNY, 10, 10)
        rysuj_tekst(f"Doświadczenie: {poziom_exp}/{maks_exp}", czcionka_srednia, CZARNY, 10, 50)
        rysuj_tekst(f"Pieniądze: {stan.pieniadze} zł", czcionka_srednia, CZARNY, 10, 90)
        rysuj_tekst(f"Aktualna zaprawa: {stan.aktualna_zaprawa} (x{stan.bonus_zaprawa})", czcionka_srednia, CZARNY, 10, 130)
        
        szerokosc_przycisku = 240
        wysokosc_przycisku = 60
        odstep = 20
        y_przycisku = WYSOKOSC - wysokosc_przycisku - 30
        
        przycisk_cegla = rysuj_przycisk("Postaw cegłę", 
            odstep, 
            y_przycisku, 
            szerokosc_przycisku, 
            wysokosc_przycisku, 
            (100, 150, 100), 
            (130, 180, 130))
        
        przycisk_skrzynka = rysuj_przycisk("Kup skrzynkę", 
             SZEROKOSC // 2 - szerokosc_przycisku // 2, 
            y_przycisku, 
            szerokosc_przycisku, 
            wysokosc_przycisku, 
            (150, 100, 100), 
            (180, 130, 130))
        
        if stan.poziom >= 5:
            nazwa_przycisku = "Ultra Zlecenie"
        else:
            nazwa_przycisku = "Idź na zlecenie"
            
        przycisk_zlecenie = rysuj_przycisk(nazwa_przycisku, 
            SZEROKOSC - szerokosc_przycisku - odstep, 
            y_przycisku, 
            szerokosc_przycisku, 
            wysokosc_przycisku, 
            (100, 100, 150), 
            (130, 130, 180))
        
        przycisk_cheat = rysuj_przycisk("CHEAT", 650, 20, 115, 35, (80, 80, 80), (120, 120, 120))
        
        if przycisk_cegla:
            stan.czas_akcji = time.time()
            minigra_stawianie_cegiel()
        elif przycisk_skrzynka:
            stan.czas_akcji = time.time()
            kup_skrzynke()
        elif przycisk_zlecenie:
            stan.czas_akcji = time.time()
            idz_na_zlecenie()
        elif przycisk_cheat:
            stan.czas_akcji = time.time()
            cheat()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    glowna_petla()