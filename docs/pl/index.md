## [◀️](/docs/index.md) [📑](/docs/index.md) /[docs](/docs/index.md)/[pl](/docs/pl/index.md) [🇵🇱](/docs/pl/index.md) 󠁧[🇺🇸](/docs/en/index.md)
<br><br><br><br>


# **Główne klasy silnika gry**

## [Game](/docs/pl/gameClass.md)

Jest to główna klasa odpowiedzialna za realizację głównej komunikacji z [Pygamem](https://www.pygame.org/) (oraz możliwe że w przyszłości z opengl'em). Umożliwia obsługę myszki i klawiatury oraz zarządzanie podstawami gry. W jednym procesie ta klasa może zostać utworzona jedna raz i nie ma gwarancji działania w przypadku utworzenia ponownie jej (nawet po usunięciu instancji tej klasy)

> [!CAUTION]
> Podpowiedzi w różnych programach mogą źle podpowiadać! Używanie dokumentacji zalecane!

## [Scene](/docs/pl/sceneClass.md)

Scena przedstawia jeden wymiar w mapie. Jedna scena jest główna (ustanowiona przez metodę [setMainScene](/docs/pl/gameClass.md#addScene) i jest ona traktowana jako priorytetowa w obliczeniach i tylko ona jest renderowana przez klasę [Camera](/docs/pl/cameraClass.md) oraz ma gracza głównego który automatycznie powoduje ładowanie chunków (dla innych scen wymagane jest robienie tego ręcznie)

Każda scena by była rozpoznawana przez silnik gry musi zostać dodana przez instancję klasy [Game](/docs/pl/index.md#game) poprzez metodę [addScene](/docs/pl/gameClass.md#addScene).
Wiele scen może być dodana do silnika i aktywnie obliczanych, jednak wiąże się to ze spadkiem wydajności. Każda scena może być aktywnie usypiana i wznawiana poprzz atrybut [idle](/docs/pl/sceneClass.md#idle).

> [!CAUTION]
> Możliwa zmiana nazwy klasy z Scene na SceneMap w przyszłości, by umożliwić dodanie Scene bez obsługi bloków by zrobić menu w grze

> [!CAUTION]
> Nie posiadanie żadnej sceny ustawionej jako główna w instancji klasy [Game](/docs/pl/index.md#game) może spowodować crasha gry!
