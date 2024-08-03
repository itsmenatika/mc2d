## [◀️](/docs/index.md) [📑](/docs/index.md) /[docs](/docs/index.md)/[pl](/docs/pl/index.md)/[resourceManager](/docs/pl/resourceManager.md) [🇵🇱](/docs/pl/resourceManager.md) 󠁧[🇺🇸](/docs/en/resourceManager.md)
<br><br><br><br>

# Podstawy

## Czym jest resource Manager?

Resource Manager jest narzędziem które ma za cel cachowanie wszelkich danych które muszą być ładowane z pliku lub przerabiane. Wszystkie twoje grafiki, dane gui, dane o blokach oraz entity powinny być ładowane własnie poprzez jego, zwłaszcza jeśli dana rzecz jest używana dość często. Cachowanie w ten sposób pozwala uniknąć niepotrzebnego ładowania dysku lub ponownego jego odrabiania oraz tworzenia kopii tych samych rzeczy (resource Manager zwróci referencję tego samego obiektu jeśli się poprosi o ten sam (jeśli chcesz kopię, należy to powiedzieć jasno resource Managerowi). 

## Gdzie jest zlokalizowany?

Całość resource Managera jest zlokalizowana w **bin/namespace.py**, głównie w klasie **resourceManager**



# Metody

## metody ładowania/cachowania

### loadTextureFromFile()

**wymaga instancji:** tak
**argumenty (1):**
      * name: str -> ścieżka do pliku
**zwraca:** 
      * result: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> wynik
      * result: None -> gdy wystąpi jakikolwiek błąd

Cachuje daną teksturę oraz zwraca ją.



## metody zapisu

**MOŻE KIEDYŚ, AKTUALNIE BRAK**

## metody obróbki źródeł

### applyDarkToTexture()

**wymaga instancji:** nie
**argumenty (2):**
    * image: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> pierwotny obraz
    * lightValue: int -> wartość (zakres 16>i>=0)    
**zwraca:** 
  * result: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> wynik

Tworzy kopię przesłanego obrazu i nakłada na ten obraz ciemność z zakresu (0-15). Zwraca ten obraz. Zalecane jest korzystanie z innych metod takich jak [getTexture()](docs/pl/resourceManager.md#getTexture())

> [!IMPORTANT]  
> Zwracana rzecz nie jest tutaj cachowana!

## metody pozyskiwania źródeł oraz scachowanych informacji

### getTexture() **ZALECANE**

**wymaga instancji:** tak
**argumenty: (2+)**
     * name: str -> nazwa zawartości, zwykle ścieżka do pliku
     * disableTryingToGet: bool = False -> czy wyłączyć próbę pozyskiwania zawartości gdy tekstura nie zostanie znaleziona w cachu 
     * other: kwargs -> dodatkowe opcje
          - lightValue: int -> czy pozyskiwać teksturę z nałożoną paletą ciemności (zakres 0-15)
**zwraca:**
     * result: pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> gdy tekstura została scachowana wcześniej/udało się ją pozyskać
     * result: None -> gdy nie udało się z jakiekolwiek powodu uzyskać grafiki


### getBlockInformation()
**wymaga instancji:** tak
**argumenty:** name: str -> id bloku
**zwraca:** dict lub None

pozyskuje informacje o danym bloku





## metody dostępu oraz uzyskiwania informacji

### getAmountOfResources()

**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** int (zakres >=0)

Zwraca liczbe scachowanych źródeł (czyli pomijając scachowane dane bloków, entity i gui)

### getAmountOfCached()

**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** int (zakres >=0)

Zwraca liczbe scachowanych rzeczy.

### getGame()

**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** Game

Jest to metoda która pozwala na uzyskanie referencji do klas.
