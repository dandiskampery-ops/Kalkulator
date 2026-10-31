# Kalkulator cen samochodów kempingowych Carthago

Jednoplikowy kalkulator ceny pojazdu Carthago i Malibu (`kalkulator.html`) — rabaty
modelowe, rabaty na pakiety i opcje, koszty dodatkowe oraz skonto za płatność w
terminie 14 dni. Ten sam układ obsługuje telefon (jedna kolumna, kwota „Do
zapłaty netto” przyklejona do dolnej krawędzi ekranu) i komputer (formularz plus
kalkulacja przyklejona z prawej strony), w jasnym i ciemnym motywie.

Zasady liczenia odtworzone są z faktur Carthago **200/57964** (chic c-line I 4.9
LE L, Sales Type DI4, rok modelowy 2027) oraz starszych **200/56721** (e-line I 64
XL QB, DI2) i **200/56533** (C2-Tourer I 147 RB-LE, DI0), a dla Malibu z faktury
**200/31139** (Malibu I 470 RB-LE „K”, Sales Type VW3) — wraz z towarzyszącymi im
potwierdzeniami zamówień.

## Uruchomienie

Kalkulator działa na telefonie i na komputerze, bez instalacji — jako strona
pod adresem GitHub Pages (instrukcja niżej) albo jako opublikowany Artifact.
Wprowadzone dane zapisują się lokalnie w przeglądarce (`localStorage`), osobno
na każdym urządzeniu.

## Pliki projektu

| Plik | Rola |
|---|---|
| `kalkulator.html` | **źródło** — cała logika i wygląd kalkulatora; publikowane jako Artifact, dlatego celowo bez znaczników `<!doctype>`, `<html>`, `<head>` i `<body>` |
| `build.py` | opakowuje źródło w pełną stronę `index.html` (nagłówek, manifest, ikony, service worker) i stempluje wersję w `sw.js` |
| `index.html` | wersja PWA — plik generowany, nie edytować ręcznie |
| `manifest.webmanifest` | nazwa, ikony i kolory aplikacji |
| `sw.js` | service worker: praca offline i wykrywanie nowej wersji |
| `icon-*.png`, `apple-touch-icon.png` | ikony aplikacji |

Po każdej zmianie w `kalkulator.html`:

```bash
python3 build.py      # przebudowuje index.html i stempluje sw.js
git add -A && git commit -m "opis zmiany" && git push
```

Wdrożenie na Cloudflare Pages rusza samo po `push`. Wersję opublikowaną jako
Artifact trzeba dodatkowo opublikować ponownie pod tym samym adresem.

## Aplikacja (PWA) na GitHub Pages

Kalkulator działa jako aplikacja instalowana na telefonie i komputerze: własna
ikona, pełny ekran, **działanie offline** (po pierwszym otwarciu wszystko siedzi
w pamięci przeglądarki) i pasek „Jest nowsza wersja” po wdrożeniu zmian.

Docelowy adres: **https://dandiskampery-ops.github.io/Kalkulator/**

### 1. Włączenie GitHub Pages

1. GitHub → repozytorium `Kalkulator` → **Settings** → **General** → sekcja
   *Danger Zone* → **Change visibility** → **Public**. GitHub Pages na koncie
   darmowym publikuje tylko z repozytoriów publicznych.
2. **Settings** → **Pages** → *Build and deployment*:
   * **Source**: `Deploy from a branch`,
   * **Branch**: `claude/carthago-price-calculator-hp0h04`, katalog `/ (root)`,
   * **Save**.
3. Po kilku minutach strona żyje pod adresem powyżej. Każdy kolejny `push`
   publikuje się automatycznie.

Strona jest publiczna — kto zna adres, zobaczy też stawki rabatowe wpisane jako
domyślne. Jeśli kiedyś ma to być zamknięte, ten sam zestaw plików działa na
Cloudflare Pages z Cloudflare Access (logowanie kodem z maila, darmowe do 50
osób).

### 2. Instalacja na urządzeniu

* **Android / Chrome**: otwórz adres → menu → *Zainstaluj aplikację*.
* **iPhone / Safari**: otwórz adres → ikona udostępniania → *Do ekranu
  początkowego*.
* **Windows / macOS**: w Chrome lub Edge ikona instalacji w pasku adresu.

Po instalacji kalkulator działa bez internetu, a dane każdej kalkulacji zapisują
się lokalnie na urządzeniu.

## Ceny z cennika: netto czy brutto

W konfiguracji Carthago ceny podane są **brutto z polskim VAT 23%**, a podstawą
faktury jest cena netto **każdej pozycji z osobna** (brutto ÷ 1,23, zaokrąglone
do groszy). Przełącznik „Ceny z cennika” decyduje, jak traktowane są wpisywane
kwoty:

* **netto** — kwoty brane wprost (domyślnie),
* **brutto z VAT 23%** — każda pozycja dzielona przez 1,23 przed rabatem.

Suma pozycji przeliczonych osobno różni się o grosze od przeliczenia sumy
zbiorczej — faktura liczy właśnie po pozycjach, dlatego pakiety i opcje warto
wpisywać pojedynczo.

## Zasady rabatowania

### Pojazd bazowy

Wszystkie rabaty procentowe liczone są **od ceny katalogowej netto** i
**sumują się** (nie kaskadowo). Kwota każdego rabatu zaokrąglana jest osobno do
pełnych groszy — tak jak na fakturze.

| Rabat | Nazwa na fakturze | Stawka |
|---|---|---|
| Rabat modelowy | *Model range discount* / *Basic discount* | wg modelu (tabela niżej) |
| Rabat DI | *Order type discount* (*Dispo-* / *Demo Discount*) | wg Sales Type: DI0 = 0%, DI2 = 2%, DI4 (dispo) = 4%, VW3 (demo) = 3% |
| Rabat CI | *CI discount* | 3% — tylko na starszych fakturach Carthago, domyślnie wyłączony |
| Quality Bonus | *Quality Bonus* | Carthago 3%, Malibu 2% |
| Rabat specjalny | *Special discount* | wpisywany ręcznie — kwotowo albo procentowo |

| Model | Rabat modelowy | Quality Bonus | Rabat DI | Razem |
|---|---:|---:|---:|---:|
| C1-Tourer | 10% | 3% | 4% (dispo) | 17% |
| C2-Tourer | 11% | 3% | 4% (dispo) | 18% |
| Chic C-Line (T / I Integra) | 11% | 3% | 4% (dispo) | 18% |
| Chic E-Line | 12% | 3% | 4% (dispo) | 19% |
| Chic S-Plus | 12% | 3% | 4% (dispo) | 19% |
| Malibu I | 10% | 2% | 3% (demo) | 15% |
| Malibu T | 10% | 2% | 3% (demo) | 15% |
| Inny model | ręcznie | — | — | — |

Wybór modelu ustawia od razu pełny zestaw rabatów z faktur tej marki — Carthago
jak na 200/57964, Malibu jak na 200/31139 — i wyłącza rabat CI, którego na tych
fakturach nie ma. „Inny model” niczego nie zmienia: rabaty wpisuje się ręcznie.

Stawki DI, CI i Quality Bonus są edytowalne przy przełącznikach — rabat DI
zależy od typu sprzedaży (Sales Type), więc dla innego typu zamówienia wystarczy
zmienić stawkę albo wyłączyć przełącznik. Rabat specjalny ma obok pola
wybór jednostki: **kwota** albo **%** (procent liczony od ceny katalogowej
netto).

### Pakiety i opcje

* **Pakiety — 15%** rabatu, liczone osobno dla każdego pakietu.
* **Opcje — 18%** rabatu, liczone osobno dla każdej opcji.

### Koszty z faktury (bez rabatu, w skoncie)

Pozycje doliczane do faktury Carthago i Malibu w pełnej wysokości, bez rabatu,
ale **wchodzące do podstawy skonta**:

| Pozycja | Nazwa na fakturze | Kwota domyślna |
|---|---|---:|
| Prior carriage charges | *Subtotal transport* (poz. 100002) | 603,57 € |
| Delivery costs | *Subtotal transport cost* (poz. 100005) | 729,30 € |
| Insurance allowance | *Insurance allowance* (poz. 100007) | 25,00 € |

Kwoty są takie same na fakturach Carthago 200/57964 i Malibu 200/31139 i są
wpisane domyślnie; można je zmienić albo usunąć (np. przy odbiorze w fabryce).
W kalkulacjach zapisanych w starszej wersji kalkulatora puste pola i dawne
18,50 € zostają raz uzupełnione tymi kwotami — kwoty wpisane ręcznie zostają.

### Podatek akcyzowy

Naliczany **od ceny końcowej faktury** — po wszystkich rabatach i po skoncie.
Stawka zależy od podwozia i jest edytowalna:

| Podwozie | Stawka akcyzy |
|---|---|
| Mercedes-Benz | 3,1% |
| Fiat | 18,6% |
| Iveco | 18,6% |
| Bez akcyzy | 0% |

### Transport do Polski (na końcu)

Koszt własny **1200 € netto**, włączany przełącznikiem. Nie jest rabatowany,
**nie wchodzi do podstawy skonta** i dochodzi **po akcyzie** — jako ostatnia
pozycja kalkulacji.

Kwota transportu jest zawsze **w euro**. Przy cenniku w EUR doliczana jest wprost
(a w sekcji „W złotych” przeliczona po kursie); przy cenniku w PLN kalkulator
przelicza ją po kursie EUR/PLN, np. „Transport do Polski · 1200,00 € × 4,2635 =
5116,20 zł”. Bez kursu transport nie wchodzi do kwoty, a kalkulacja pokazuje
ostrzeżenie „wpisz kurs EUR/PLN”. W kalkulacjach zapisanych przy dawnej stawce
1100 € kwota zmienia się raz na 1200 € (inna kwota wpisana ręcznie zostaje).

### Skonto za płatność w terminie 14 dni

**2% od sumy faktury Carthago** — razem z jej kosztami bez rabatu (*Payment
within 14 days 2% discount, term of payment 30 days*), bez transportu do
Polski.

## Kolejność wyliczeń

```
1. Pojazd netto   = cena katalogowa − rabat modelowy − DI − CI − Quality Bonus − rabat specjalny
2. Pakiety netto  = suma pozycji pomniejszonych o 15% (każda osobno)
3. Opcje netto    = suma pozycji pomniejszonych o 18% (każda osobno)
4. Po rabatach    = 1 + 2 + 3
5. Suma faktury   = Po rabatach + koszty z faktury (carriage, delivery, insurance)
6. Skonto         = Suma faktury × 2%
7. Faktura po skoncie = Suma faktury − skonto
8. Akcyza         = Faktura po skoncie × stawka podwozia (3,1% / 18,6%)
9. Cena po akcyzie = Faktura po skoncie + akcyza
10. Koszt auta    = Cena po akcyzie + transport do Polski (jeśli włączony)
11. VAT (domyślnie 0% — dostawa wewnątrzwspólnotowa) i brutto od kwoty końcowej
12. W złotych (gdy wpisany kurs) = faktura po skoncie, akcyza i transport
    przeliczone po kursie EUR/PLN, każda pozycja osobno

Kwoty rabatów, skonta, akcyzy i VAT zaokrąglane są handlowo do groszy przed
dodaniem (4,145 → 4,15), tak jak na fakturze.
```

## Sprawdzenie na fakturach

Faktura **200/57964** (chic c-line I 4.9 LE L, DI4), model „Chic C-Line”, pozycje
wpisane cenami brutto z potwierdzenia zamówienia, tryb „brutto z VAT 23%”:

| Pozycja | Kalkulator | Faktura |
|---|---:|---:|
| Pojazd po rabatach (11% + Quality Bonus 3% + dispo 4%) | 102 493,33 | 102 493,33 |
| Pakiety po rabacie 15% | 15 763,00 | 15 763,00 |
| Opcje po rabacie 18% | 5 020,01 | 5 020,01 |
| Wartość katalogowa netto | 149 658,53 | 149 658,53 |
| Rabaty razem | 26 382,19 | 26 382,19 |
| Koszty z faktury (603,57 + 729,30 + 25,00) | 1 357,87 | 1 357,87 |
| Suma faktury netto | 124 634,21 | 124 634,21 |
| Skonto 2% | 2 492,68 | 2 492,68 |
| **Do zapłaty netto** | **122 141,53** | **122 141,53** |

Starsze faktury Carthago miały rabat CI 3% zamiast Quality Bonus i insurance
18,50 € — żeby je odtworzyć, trzeba wyłączyć Quality Bonus, ustawić DI według
Sales Type, włączyć CI i wpisać koszty z faktury:

Faktura **200/56533** (C2-Tourer I 147 RB-LE), pozycje wpisane cenami brutto z
konfiguracji, tryb cennika „brutto z VAT 23%”:

| Pozycja | Kalkulator | Faktura |
|---|---:|---:|
| Pojazd po rabatach (11% + CI 3%) | 91 334,79 | 91 334,79 |
| Pakiety po rabacie 15% | 15 832,12 | 15 832,12 |
| Opcje po rabacie 18% | 4 009,99 | 4 009,99 |
| Wartość katalogowa netto | 129 719,52 | 129 719,52 |
| Rabaty razem | 18 542,62 | 18 542,62 |
| Koszty z faktury (603,57 + 729,30 + 18,50) | 1 351,37 | 1 351,37 |
| Suma faktury netto | 112 528,27 | 112 528,27 |
| Skonto 2% | 2 250,57 | 2 250,57 |
| **Do zapłaty netto** | **110 277,70** | **110 277,70** |

Faktura **200/56721** (e-line I 64 XL QB, DI2): rabaty na pojeździe 12% + DI 2% +
CI 3% + rabat specjalny 3 353,66 € dają 135 067,40 € — zgodnie z fakturą.

Faktura **200/31139** (Malibu I 470 RB-LE „K”, VW3), model „Malibu I”, pozycje
wpisane cenami brutto z potwierdzenia zamówienia, tryb „brutto z VAT 23%”:

| Pozycja | Kalkulator | Faktura |
|---|---:|---:|
| Pojazd po rabatach (10% + Quality Bonus 2% + demo 3%) | 87 439,43 | 87 439,43 |
| Pakiety po rabacie 15% | 16 008,34 | 16 008,34 |
| Opcje po rabacie 18% | 3 319,99 | 3 319,99 |
| Wartość katalogowa netto | 125 752,03 | 125 752,03 |
| Rabaty razem | 18 984,27 | 18 984,27 |
| Koszty z faktury (603,57 + 729,30 + 25,00) | 1 357,87 | 1 357,87 |
| Suma faktury netto | 108 125,63 | 108 125,63 |
| Skonto 2% | 2 162,51 | 2 162,51 |
| **Do zapłaty netto** | **105 963,12** | **105 963,12** |

Dalszy ciąg kalkulacji dla faktury 200/56533 (Mercedes-Benz, transport
włączony): 110 277,70 + akcyza 3,1% (3 418,61) = 113 696,31, plus transport
1 200,00 → **114 896,31 €**. Dla podwozia Fiat lub Iveco (18,6%): akcyza
20 511,65 → **131 989,35 €**.

## Pozostałe funkcje

* Waluta cennika **EUR / PLN** oraz edytowalna stawka VAT (0% = dostawa
  wewnątrzwspólnotowa; wiersze VAT i brutto pojawiają się dopiero przy stawce
  większej od zera).
* **Kurs EUR/PLN** — przy cenniku w EUR kalkulacja pokazuje dodatkowo sekcję
  „W złotych” (faktura po skoncie, akcyza, transport i koszt auta), a pasek na
  telefonie kwotę w złotych; przy cenniku w PLN kurs przelicza transport do
  Polski. Kurs średni EUR z tabeli A NBP pobiera się sam przy otwarciu
  kalkulatora (gdy pole jest puste albo kurs pochodzi z NBP) i na przycisk
  **NBP**; numer tabeli i data są widoczne też na wydruku. Kurs wpisany ręcznie
  zostaje, dopóki się go nie zmieni, a „Wyczyść” kursu nie kasuje.
* Kwoty można wpisywać po polsku, po niemiecku jak na fakturach i po angielsku —
  `130 630`, `130.630,00`, `130,630.00` i `18 626,03` działają poprawnie;
  wklejone „€” czy „EUR” są pomijane.
* Pole ceny pojazdu nazywa się po prostu „Cena katalogowa” — o tym, czy kwota
  jest netto czy brutto, decyduje przełącznik „Ceny z cennika”.
* Przycisk **Drukuj / PDF** — wydruk zawiera samo podsumowanie oferty z datą,
  bez pól formularza.
* Przycisk **Wyczyść** — reset do wartości domyślnych.
