## [◀️](/docs/pl/index.md) [📑](/docs/pl/index.md) /[docs](/docs/index.md)/[pl](/docs/pl/index.md)/[resourceManager](/docs/pl/resourceManager.md) [🇵🇱](/docs/pl/resourceManager.md) 󠁧[🇺🇸](/docs/en/resourceManager.md)
<br><br><br><br>

# Podstawy

## Czym jest resource Manager?

Resource Manager jest narzędziem które ma za cel cachowanie wszelkich danych które muszą być ładowane z pliku lub przerabiane. Wszystkie twoje grafiki, dane gui, dane o blokach oraz entity powinny być ładowane własnie poprzez jego, zwłaszcza jeśli dana rzecz jest używana dość często. Cachowanie w ten sposób pozwala uniknąć niepotrzebnego ładowania dysku lub ponownego jego odrabiania oraz tworzenia kopii tych samych rzeczy (resource Manager zwróci referencję tego samego obiektu jeśli się poprosi o ten sam (jeśli chcesz kopię, należy to powiedzieć jasno resource Managerowi). 

## Gdzie jest zlokalizowany?

Całość resource Managera jest zlokalizowana w **bin/namespace.py**, głównie w klasie **resourceManager**


# Namespace

## Czym jest?

jest to przestrzeń nazw zawierająca dane o wszystkich istniejących id, entitach (rodzaje) oraz blokach (rodzaje). Jest ładowania za pomocą  [self.namespaceReload()](docs/pl/resourceManager.md#loadfromNameSpace())

## struktura

TODO: przetłumaczenie struktury na polski

```json
 "environment": {
        "bin_loc": ABSOLUTE_LOCALIZATION_OF_GAME_BIN (str),
        "version": VERSION_OF_THE_GAME (int),
        "versionInt": INTVERSION_OFTHEGAME (int),
    }, # basic environment information
    "IDInts": {
      intID: stringID
     }, # a dictionary of int ids
    "IDIntsList": [], # a list of id ints
    "blocksFastLighting": {
        "blockStringName": {
            1: pygame.surface.Surface
        }
    }, # NOT USED ANYMORE
    "id_type": {
        stringID: block, gui, unknown,  or entity
    }, # types of id with corresponding type for them
    "blocks": {
        stringID: {
            "module": module (module), # module of the game
            "id": name (str), # string id
            "intID": idINT (int), # int id
            "type": "block", 
            "class": the main class of this block (class inherting from Block),
            "MAINTEXTURE_loc": localization to a raw main Texture that was written in class (str),
            "MAINTEXTURE_loc_with": localization to a raw main Texture that was written in class, but compiled (str),
            "ISMAINTEXTURETRANSPARENT": flag if main texture is transparent (bool),
            "MAINTEXTURE_RENDER": render of a main texture,
            "MAINTEXTURE_object": the same as MAINTEXTURE_RENDER (THATS THE SAME REFERENCE),
            "MAINTEXTURE_get": lambda: self.getTexture(mainClassData.MAINTEXTURE) # DONT USE IT
        }
    }, # list of blocks
    "entities": {
        stringID: {
            "module": module (module), # module of the game
            "id": name (str), # string id
            "type": "entity", 
            "class": the main class of this entity (class inherting from Block),
            "MAINTEXTURE_loc": localization to a raw main Texture that was written in class (str),
            "MAINTEXTURE_loc_with": localization to a raw main Texture that was written in class, but compiled (str),
            "ISMAINTEXTURETRANSPARENT": flag if main texture is transparent (bool),
            "MAINTEXTURE_RENDER": render of a main texture,
            "MAINTEXTURE_object": the same as MAINTEXTURE_RENDER (THATS THE SAME REFERENCE),
            "MAINTEXTURE_get": lambda: self.getTexture(mainClassData.MAINTEXTURE) # DONT USE IT
        }
    } # list of entities


```



# Metody

<br><br><br><br>
## metody ładowania/cachowania

<br><br>
### loadFromNameSpace()
**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** None

Jest to metoda która jest wywoływana automatycznie przy inicjalizacji obiektu oraz przez [self.namespaceReload()](docs/pl/resourceManager.md#namespaceReload()), powoduje ona załadowanie przestrzenii nazw oraz scachowanie automatycznie wielu rzeczy (takie jak tekstury entity, bloków itd). 


<br><br>
### loadTextureFromFile()

**wymaga instancji:** tak

**argumenty (1):**
* name: str -> ścieżka do pliku
  
**zwraca:** 
* result: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> wynik
* result: None -> gdy wystąpi jakikolwiek błąd

Cachuje daną teksturę oraz zwraca ją.

przykład użycia:
```python
x: pygame.surface.Surface | None = resourceManager.loadTextureFromFile("resource/gui/x.png")

if x == None:
   raise Exception("???")

screen.blit(x)
```

<br><br><br><br>
## metody zapisu

**MOŻE KIEDYŚ, AKTUALNIE BRAK**

<br><br><br><br>
## metody obróbki źródeł

<br><br>
### applyDarkToTexture()

**wymaga instancji:** nie

**argumenty (2):**
* image: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> pierwotny obraz
* lightValue: int -> wartość (zakres 16>i>=0)
  
**zwraca:** 
* result: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> wynik

Tworzy kopię przesłanego obrazu i nakłada na ten obraz ciemność z zakresu (0-15). Zwraca ten obraz. Zalecane jest korzystanie z innych metod takich jak [getTexture()](docs/pl/resourceManager.md#getTexture())

przykład użycia:
```python
jajko: pygame.surface.Surface = resourceManager.getTexture(name="resources/jajka/duzejajko.png")
jajkoCiemne: pygame.surface.Surface = resourceManager.applyDarkToTexture(jajko, 5)
screen.blit(jajkoCiemne, (0,0))
```

> [!IMPORTANT]  
> Zwracana rzecz nie jest tutaj cachowana!

<br><br><br><br>
## metody pozyskiwania źródeł oraz scachowanych informacji

<br><br>
### getTexture() **ZALECANE**

**wymaga instancji:** tak

**argumenty: (2+)**
* name: str -> nazwa zawartości, zwykle ścieżka do pliku
* disableTryingToGet: bool = False -> czy wyłączyć próbę pozyskiwania zawartości gdy tekstura nie zostanie znaleziona w cachu 
* other: kwargs -> dodatkowe opcje
  - lightValue: int -> czy pozyskiwać teksturę z nałożoną paletą ciemności (zakres 0-15)

**zwraca:**
* result: [pygame.surface.Surface](https://www.pygame.org/docs/ref/surface.html) -> gdy tekstura została scachowana wcześniej/udało się ją pozyskać
* result: None -> gdy nie udało się z jakiekolwiek powodu uzyskać grafiki

przykład użycia:
```python
jajko: pygame.surface.Surface = resourceManager.getTexture(name="resources/jajka/duzejajko.png")
screen.blit(jajko, (0,0))
```

<br><br>
### getBlockInformation()
**wymaga instancji:** tak
**argumenty:** name: str -> id bloku
**zwraca:** dict lub None

defacto działa praktycznie identycznie jak coś takiego:
```python
namespace: dict = resourceManager.getNameSpace()
blockData: dict = namespace['blocks'][ID]
return blockData
```
ale jest szybsze i znacznie bezpieczniejsze

przykład użycia:
```python
stone: dict = resourceManager.getBlockInformation(name="stone)
print(f"ścieżka do głównej tekstury stona to resources/{stone['class'].MAINTEXTURE})
```

pozyskuje informacje o danym bloku


<br><br>
### getNameSpace()
**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** dict 

zwraca przestrzeń nazw ([namespace](docs/pl/resourceManager.md#namespace)) zawierającą defacto wszystkie informacje o istniejących entity, blokach itd, liste wszystkich ID istniejących w grze itd.


przykład użycia
```python
namespace: dict = resourceManager.getNameSpace()
intIDStona: int = namespace['blocks']['stone']['intID']
print(f"int id stona to {intIDStona}")
```


<br><br><br><br>


## metody dostępu oraz uzyskiwania informacji

<br><br>
### getAmountOfResources()

**wymaga instancji:** tak
**argumenty:** brak
**zwraca:** int (zakres >=0)

Zwraca liczbe scachowanych źródeł (czyli pomijając scachowane dane bloków, entity i gui)

przykład:
```python
liczbaScachowanychRzeczy: int = resourceManager.getAmountOfResources()
print(f"liczba scachowanych rzeczy to {liczbaScachowanychRzeczy}")
```

<br><br>
### getAmountOfCached()

**wymaga instancji:** tak

**argumenty:** brak

**zwraca:** int (zakres >=0)

Zwraca liczbe scachowanych rzeczy.

przykład:
```python
liczbaScachowanychRzeczy: int = resourceManager.getAmountOfCached()
print(f"liczba scachowanych rzeczy to {liczbaScachowanychRzeczy}")
```


<br><br>
### getGame()

**wymaga instancji:** tak

**argumenty:** brak

**zwraca:** Game

Jest to metoda która pozwala na uzyskanie referencji do klas.

przykład użycia:

```python
# prosta funkcja zamieniająca blok na pozycji 0,0 na powietrze
game: 'Game' = resourceManager.getGame()
block: Block|None = game.getCurrentScene().getBlockByAbsPos(absolutePos=(0,0))

if Block != None: block.setToAir()
```
