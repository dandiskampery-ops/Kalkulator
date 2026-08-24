# Kalkulator cen samochodów kempingowych Carthago

Jednoplikowy kalkulator ceny pojazdu Carthago (`kalkulator.html`) — rabaty
modelowe, rabaty na pakiety i opcje, koszty dodatkowe oraz skonto za płatność w
terminie 14 dni. Ten sam układ obsługuje telefon (jedna kolumna, kwota „Do
zapłaty netto” przyklejona do dolnej krawędzi ekranu) i komputer (formularz plus
kalkulacja przyklejona z prawej strony), w jasnym i ciemnym motywie.

Zasady liczenia odtworzone są z faktur Carthago **200/56721** (e-line I 64 XL QB,
Sales Type DI2) i **200/56533** (C2-Tourer I 147 RB-LE, Sales Type DI0) wraz z
towarzyszącymi im potwierdzeniami zamówień.

## Uruchomienie

Kalkulator jest opublikowany jako strona pod linkiem — działa na telefonie i na
komputerze, bez instalacji. Wprowadzone dane zapisują się lokalnie w
przeglądarce (`localStorage`), osobno na każdym urządzeniu.

## Plik źródłowy

`kalkulator.html` celowo nie zawiera znaczników `<!doctype>`, `<html>`,
`<head>` i `<body>` — są dodawane automatycznie przy publikacji. Po każdej
zmianie w tym pliku trzeba go opublikować ponownie pod tym samym adresem, żeby
link pokazywał aktualną wersję.

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
| Rabat DI | *Order type discount* | wg Sales Type: DI0 = 0%, DI2 = 2% |
| Rabat CI | *CI discount* | 3% |
| Rabat specjalny | *Special discount* | wpisywany ręcznie — kwotowo albo procentowo |

| Model | Rabat modelowy |
|---|---|
| C1-Tourer | 10% |
| C2-Tourer | 11% |
| Chic C-Line (T / I Integra) | 11% |
| Chic E-Line | 12% |
| Chic S-Plus | 12% |
| Inny model | wpisywany ręcznie |

Stawki DI i CI są edytowalne przy przełącznikach — na fakturach rabat DI zależy
od typu sprzedaży (Sales Type), a CI wynosi 3%. Rabat specjalny ma obok pola
wybór jednostki: **kwota** albo **%** (procent liczony od ceny katalogowej
netto).

### Pakiety i opcje

* **Pakiety — 15%** rabatu, liczone osobno dla każdego pakietu.
* **Opcje — 18%** rabatu, liczone osobno dla każdej opcji.

### Koszty z faktury (bez rabatu, w skoncie)

Pozycje doliczane do faktury Carthago w pełnej wysokości, bez rabatu, ale
**wchodzące do podstawy skonta**:

| Pozycja | Nazwa na fakturze | Uwagi |
|---|---|---|
| Prior carriage charges | *Subtotal transport* (poz. 100002) | np. 407,29 lub 603,57 € |
| Delivery costs | *Subtotal transport cost* (poz. 100005) | np. 0,00 lub 729,30 € |
| Insurance allowance | *Insurance allowance* (poz. 100007) | 18,50 € na obu fakturach |

Trzy pozycje są wpisane domyślnie — wystarczy uzupełnić kwoty z faktury.

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

Koszt własny **1100 € netto**, włączany przełącznikiem. Nie jest rabatowany,
**nie wchodzi do podstawy skonta** i dochodzi **po akcyzie** — jako ostatnia
pozycja kalkulacji.

### Skonto za płatność w terminie 14 dni

**2% od sumy faktury Carthago** — razem z jej kosztami bez rabatu (*Payment
within 14 days 2% discount, term of payment 30 days*), bez transportu do
Polski.

## Kolejność wyliczeń

```
1. Pojazd netto   = cena katalogowa − rabat modelowy − DI − CI − rabat specjalny
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

Kwoty skonta, akcyzy i VAT zaokrąglane są do groszy przed dodaniem, tak jak na
fakturze.
```

## Sprawdzenie na fakturach

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

Dalszy ciąg kalkulacji dla pierwszego przykładu (Mercedes-Benz, transport
włączony): 110 277,70 + akcyza 3,1% (3 418,61) = 113 696,31, plus transport
1 100,00 → **114 796,31 €**. Dla podwozia Fiat lub Iveco (18,6%): akcyza
20 511,65 → **131 889,35 €**.

## Pozostałe funkcje

* Waluta **EUR / PLN** oraz edytowalna stawka VAT (0% = dostawa
  wewnątrzwspólnotowa; wiersze VAT i brutto pojawiają się dopiero przy stawce
  większej od zera).
* Kwoty można wpisywać po polsku — `130 630` i `18 626,03` działają tak samo.
* Pole ceny pojazdu nazywa się po prostu „Cena katalogowa” — o tym, czy kwota
  jest netto czy brutto, decyduje przełącznik „Ceny z cennika”.
* Przycisk **Drukuj / PDF** — wydruk zawiera samo podsumowanie oferty z datą,
  bez pól formularza.
* Przycisk **Wyczyść** — reset do wartości domyślnych.
