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

def minigra_stawianie_cegiel():
    plansza = []
    szerokosc_cegly = 60
    wysokosc_cegly = 30
    ilosc_kolumn = 7
    ilosc_wierszy = 5
    odstep = 2
    
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
    czas_trwania = 20
    minigra_aktywna = True
    
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
    nagroda_pieniadze = int(50 * procent_ukonczenia * stan.bonus_zaprawa)
    nagroda_exp = int(15 * procent_ukonczenia)
    
    ekran.fill(SZARY)
    
    if zlecenie_ukonczone:
        rysuj_tekst("Minigra zakończona!", czcionka_duza, CZARNY, SZEROKOSC // 2, 150, True)
        rysuj_tekst(f"Postawiłeś {postawione_cegly} z {puste_miejsca} cegieł ({int(procent_ukonczenia * 100)}%)", 
                  czcionka_srednia, CZARNY, SZEROKOSC // 2, 220, True)
        rysuj_tekst(f"Zarabiasz: {nagroda_pieniadze} zł", czcionka_srednia, CZARNY, SZEROKOSC // 2, 270, True)
        rysuj_tekst(f"Zdobywasz: {nagroda_exp} exp", czcionka_srednia, CZARNY, SZEROKOSC // 2, 320, True)
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
                
    stan.pieniadze += nagroda_pieniadze
    stan.exp += nagroda_exp
    
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

def glowna_petla():
    cutscenka()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
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
        
        if przycisk_cegla:
            stan.czas_akcji = time.time()
            minigra_stawianie_cegiel()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    glowna_petla()