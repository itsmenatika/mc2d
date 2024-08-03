## [◀️](/docs/index.md) [📑](/docs/index.md) /[docs](/docs/index.md)/[pl](/docs/pl/index.md)/[resourceManager](/docs/pl/resourceManager.md) [🇵🇱](/docs/pl/resourceManager.md) 󠁧[🇺🇸](/docs/en/resourceManager.md)
<br><br><br><br>

# Podstawy

## Czym jest resource Manager?

Resource Manager jest narzędziem które ma za cel cachowanie wszelkich danych które muszą być ładowane z pliku lub przerabiane. Wszystkie twoje grafiki, dane gui, dane o blokach oraz entity powinny być ładowane własnie poprzez jego, zwłaszcza jeśli dana rzecz jest używana dość często. Cachowanie w ten sposób pozwala uniknąć niepotrzebnego ładowania dysku lub ponownego jego odrabiania oraz tworzenia kopii tych samych rzeczy (resource Manager zwróci referencję tego samego obiektu jeśli się poprosi o ten sam (jeśli chcesz kopię, należy to powiedzieć jasno resource Managerowi). 

## Gdzie jest zlokalizowany?

Całość resource Managera jest zlokalizowana w **bin/namespace.py**, głównie w klasie **resourceManager**



# Metody

## metody dostępu



### self.getGame() -> Game

Jest to metoda która pozwala na uzyskanie referencji do klas
