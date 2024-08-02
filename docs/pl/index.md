## [◀️](/docs/index.md) [📑](/docs/index.md) /[docs](/docs/index.md)/[pl](/docs/pl/index.md) [🇵🇱](/docs/pl/index.md) 󠁧[🇺🇸](/docs/en/index.md)
<br><br><br><br>


# **Główne klasy silnika gry**

## [Game](/docs/pl/gameClass.md)

Jest to główna klasa odpowiedzialna za realizację głównej komunikacji z [Pygamem](https://www.pygame.org/) (oraz możliwe że w przyszłości z opengl'em). Umożliwia obsługę myszki i klawiatury oraz zarządzanie podstawami gry. W jednym procesie ta klasa może zostać utworzona jedna raz i nie ma gwarancji działania w przypadku utworzenia ponownie jej (nawet po usunięciu instancji tej klasy). Zwykle możesz uzyskać instancję tej klasy używając obiekt.getGame().

> [!CAUTION]
> Podpowiedzi w różnych programach mogą źle podpowiadać! Używanie dokumentacji zalecane!

## [ResourceManager](/docs/pl/resourceManager.md)

Jest to klasa która odpowiada za cachowanie grafik, entity, gui oraz bloków oraz ładowanie ich do silnika gry. Zalecane jest posiadanie maksymalnie jednej instancji na instancje [Game](/docs/pl/gameClass.md). ResourceManager możesz uzyskać za pomocą [Game](/docs/pl/gameClass.md).[getResourceManager()](/docs/pl/gameClass.md#getResourceManager) po zainicjalizowaniu silnika (resourceManager jest automatycznie inicjalizowany).

> [!CAUTION]
> Wszystkie dane gui, entity oraz bloków są automatycznie wczytywane podczas ładowania gry.

> [!TIP]
> Zalecane jest ładowanie większych oraz ważniejszych informacji w czasie ładowania gry/mapy. Spowoduje to stabilizowanie fpsów.

> [!TIP]
> Zalecane jest czyszczenie cachu z zbędnych informacji. Chociaż nie jest to wymagane

## [Scene](/docs/pl/sceneClass.md)

Scena przedstawia jeden wymiar w mapie. Jedna scena jest główna (ustanowiona przez metodę [setMainScene](/docs/pl/gameClass.md#addScene) i jest ona traktowana jako priorytetowa w obliczeniach i tylko ona jest renderowana przez klasę [Camera](/docs/pl/cameraClass.md) oraz ma gracza głównego który automatycznie powoduje ładowanie chunków (dla innych scen wymagane jest robienie tego ręcznie)

Każda scena by była rozpoznawana przez silnik gry musi zostać dodana przez instancję klasy [Game](/docs/pl/index.md#game) poprzez metodę [addScene](/docs/pl/gameClass.md#addScene).
Wiele scen może być dodana do silnika i aktywnie obliczanych, jednak wiąże się to ze spadkiem wydajności. Każda scena może być aktywnie usypiana i wznawiana poprzz atrybut [idle](/docs/pl/sceneClass.md#idle).

> [!CAUTION]
> Możliwa zmiana nazwy klasy z Scene na SceneMap w przyszłości, by umożliwić dodanie Scene bez obsługi bloków by zrobić menu w grze

> [!CAUTION]
> Nie posiadanie żadnej sceny ustawionej jako główna w instancji klasy [Game](/docs/pl/index.md#game) może spowodować crasha gry!
