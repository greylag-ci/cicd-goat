<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI to szybki, prosty w nauce i gotowy do użycia w produkcji framework</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Dokumentacja**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Kod żródłowy**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI to nowoczesny, wydajny framework webowy do budowania API z użyciem Pythona 3.6+ bazujący na standardowym typowaniu Pythona.

Kluczowe cechy:

* **Wydajność**: FastAPI jest bardzo wydajny, na równi z **NodeJS** oraz **Go** (dzięki Starlette i Pydantic). [Jeden z najszybszych dostępnych frameworków Pythonowych](#wydajnosc).
* **Szybkość kodowania**: Przyśpiesza szybkość pisania nowych funkcjonalności o około 200% do 300%. *
* **Mniejsza ilość błędów**: Zmniejsza ilość ludzkich (dewelopera) błędy o około 40%. *
* **Intuicyjność**: Wspaniałe wsparcie dla edytorów kodu. Dostępne wszędzie <abbr title="znane jako auto-complete, autocompletion, IntelliSense">automatyczne uzupełnianie</abbr> kodu. Krótszy czas debugowania.
* **Łatwość**: Zaprojektowany by być prosty i łatwy do nauczenia. Mniej czasu spędzonego na czytanie dokumentacji.
* **Kompaktowość**: Minimalizacja powtarzającego się kodu. Wiele funkcjonalności dla każdej deklaracji parametru. Mniej błędów.
* **Solidność**: Kod gotowy dla środowiska produkcyjnego. Wraz z automatyczną interaktywną dokumentacją.
* **Bazujący na standardach**: Oparty na (i w pełni kompatybilny z) otwartych standardach API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (wcześniej znane jako Swagger) oraz <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* oszacowania bazowane na testach wykonanych przez wewnętrzny zespół deweloperów, budujących aplikacie używane na środowisku produkcyjnym.</small>

## Sponsorzy

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Inni sponsorzy</a>

## Opinie

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI aplikacji konsolowych

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Jeżeli tworzysz aplikacje <abbr title="aplikacja z interfejsem konsolowym">CLI</abbr>, która ma być używana w terminalu zamiast API, sprawdź <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** to młodsze rodzeństwo FastAPI. Jego celem jest pozostanie **FastAPI aplikacji konsolowych** . ⌨️ 🚀

## Wymagania

Python 3.6+

FastAPI oparty jest na:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> dla części webowej.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> dla części obsługujących dane.

## Instalacja

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Na serwerze produkcyjnym będziesz także potrzebował serwera ASGI, np. <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> lub <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Przykład

### Stwórz

* Utwórz plik o nazwie `main.py` z:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Albo użyj <code>async def</code>...</summary>

Jeżeli twój kod korzysta z `async` / `await`, użyj `async def`:

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Przypis**:

Jeżeli nie znasz, sprawdź sekcję _"In a hurry?"_ o <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` i `await` w dokumentacji</a>.

</details>

### Uruchom

Uruchom serwer używając:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>O komendzie <code>uvicorn main:app --reload</code>...</summary>
Komenda `uvicorn main:app` odnosi się do:

* `main`: plik `main.py` ("moduł" w Pythonie).
* `app`: obiekt stworzony w `main.py` w lini `app = FastAPI()`.
* `--reload`: spraw by serwer resetował się po każdej zmianie w kodzie. Używaj tego tylko w środowisku deweloperskim.

</details>

### Wypróbuj

Otwórz link <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> w przeglądarce.

Zobaczysz następującą odpowiedź JSON:

```JSON
{"item_id": 5, "q": "somequery"}
```

Właśnie stworzyłeś API które:

* Otrzymuje żądania HTTP w _ścieżce_ `/` i `/items/{item_id}`.
* Obie _ścieżki_ używają <em>operacji</em> `GET` (znane także jako _metody_ HTTP).
* _Ścieżka_ `/items/{item_id}` ma _parametr ścieżki_ `item_id` który powinien być obiektem typu `int`.
* _Ścieżka_ `/items/{item_id}` ma opcjonalny _parametr zapytania_ typu `str` o nazwie `q`.

### Interaktywna dokumentacja API

Otwórz teraz stronę <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Zobaczysz automatyczną interaktywną dokumentację API (dostarczoną z pomocą <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatywna dokumentacja API

Otwórz teraz <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Zobaczysz alternatywną, lecz wciąż automatyczną dokumentację (wygenerowaną z pomocą <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Aktualizacja przykładu

Zmodyfikuj teraz plik `main.py`, aby otrzmywał treść (body) żądania `PUT`.

Zadeklaruj treść żądania, używając standardowych typów w Pythonie dzięki Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Serwer powinien przeładować się automatycznie (ponieważ dodałeś `--reload` do komendy `uvicorn` powyżej).

### Zaktualizowana interaktywna dokumentacja API

Wejdź teraz na <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Interaktywna dokumentacja API zaktualizuje sie automatycznie, także z nową treścią żądania (body):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Kliknij przycisk "Try it out" (wypróbuj), pozwoli Ci to wypełnić parametry i bezpośrednio użyć API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Kliknij potem przycisk "Execute" (wykonaj), interfejs użytkownika połączy się z API, wyśle parametry, otrzyma odpowiedź i wyświetli ją na ekranie:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Zaktualizowana alternatywna dokumentacja API

Otwórz teraz <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Alternatywna dokumentacja również pokaże zaktualizowane parametry i treść żądania (body):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Podsumowanie

Podsumowując, musiałeś zadeklarować typy parametrów, treści żądania (body) itp. tylko **raz**, i są one dostępne jako parametry funkcji.

Robisz to tak samo jak ze standardowymi typami w Pythonie.

Nie musisz sie uczyć żadnej nowej składni, metod lub klas ze specyficznych bibliotek itp.

Po prostu standardowy **Python 3.6+**.

Na przykład, dla danych typu `int`:

```Python
item_id: int
```

albo dla bardziej złożonego obiektu `Item`:

```Python
item: Item
```

...i z pojedyńczą deklaracją otrzymujesz:

* Wsparcie edytorów kodu, wliczając:
    * Auto-uzupełnianie.
    * Sprawdzanie typów.
* Walidacja danych:
    * Automatyczne i przejrzyste błędy gdy dane są niepoprawne.
    * Walidacja nawet dla głęboko zagnieżdżonych obiektów JSON.
* <abbr title="znane również jako: serializacja, przetwarzanie, marshalling">Konwersja</abbr> danych wejściowych: przychodzących z sieci na Pythonowe typy. Pozwala na przetwarzanie danych:
    * JSON.
    * Parametrów ścieżki.
    * Parametrów zapytania.
    * Dane cookies.
    * Dane nagłówków (headers).
    * Formularze.
    * Pliki.
* <abbr title="znane również jako: serializacja, przetwarzanie, marshalling">Konwersja</abbr> danych wyjściowych: wychodzących z Pythona do sieci (jako JSON):
    * Przetwarzanie Pythonowych typów (`str`, `int`, `float`, `bool`, `list`, itp).
    * Obiekty `datetime`.
    * Obiekty `UUID`.
    * Modele baz danych.
    * ...i wiele więcej.
* Automatyczne interaktywne dokumentacje API, wliczając 2 alternatywne interfejsy użytkownika:
    * Swagger UI.
    * ReDoc.

---

Wracając do poprzedniego przykładu, **FastAPI** :

* Potwierdzi, że w ścieżce jest `item_id` dla żądań `GET` i `PUT`.
* Potwierdzi, że `item_id` jest typu `int` dla żądań `GET` i `PUT`.
    * Jeżeli nie jest, odbiorca zobaczy przydatną, przejrzystą wiadomość z błędem.
* Sprawdzi czy w ścieżce jest opcjonalny parametr zapytania `q` (np. `http://127.0.0.1:8000/items/foo?q=somequery`) dla żądania `GET`.
    * Jako że parametr `q` jest zadeklarowany jako `= None`, jest on opcjonalny.
    * Gdyby tego `None` nie było, parametr ten byłby wymagany (tak jak treść żądania w żądaniu `PUT`).
* Dla żądania `PUT` z ścieżką `/items/{item_id}`, odczyta treść żądania jako JSON:
    * Sprawdzi czy posiada wymagany atrybut `name`, który powinien być typu `str`.
    * Sprawdzi czy posiada wymagany atrybut `price`, który musi być typu `float`.
    * Sprawdzi czy posiada opcjonalny atrybut `is_offer`, który (jeżeli obecny) powinien być typu `bool`.
    * To wszystko będzie również działać dla głęboko zagnieżdżonych obiektów JSON.
* Automatycznie konwertuje z i do JSON.
* Dokumentuje wszystko w OpenAPI, które może być używane przez:
    * Interaktywne systemy dokumentacji.
    * Systemy automatycznego generowania kodu klienckiego, dla wielu języków.
* Dostarczy bezpośrednio 2 interaktywne dokumentacje webowe.

---

To dopiero początek, ale już masz mniej-więcej pojęcie jak to wszystko działa.

Spróbuj zmienić linijkę:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...z:

```Python
        ... "item_name": item.name ...
```

...na:

```Python
        ... "item_price": item.price ...
```

...i zobacz jak edytor kodu automatycznie uzupełni atrybuty i będzie znał ich typy:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Dla bardziej kompletnych przykładów posiadających więcej funkcjonalności, zobacz <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Uwaga Spoiler**: tutorial - user guide zawiera:

* Deklaracje **parametrów** z innych miejsc takich jak: **nagłówki**, **pliki cookies**, **formularze** i **pliki**.
* Jak ustawić **ograniczenia walidacyjne** takie jak `maksymalna długość` lub `regex`.
* Potężny i łatwy w użyciu system **<abbr title="znane jako komponenty, resources, providers, services, injectables">Dependency Injection</abbr>**.
* Zabezpieczenia i autentykacja, wliczając wsparcie dla **OAuth2** z **tokenami JWT** oraz autoryzacją **HTTP Basic**.
* Bardziej zaawansowane (ale równie proste) techniki deklarowania **głęboko zagnieżdżonych modeli JSON** (dzięki Pydantic).
* Wiele dodatkowych funkcji (dzięki Starlette) takie jak:
    * **WebSockety**
    * **GraphQL**
    * bardzo proste testy bazujące na `requests` oraz `pytest`
    * **CORS**
    * **Sesje cookie**
    * ...i więcej.

## Wydajność

Niezależne benchmarki TechEmpower pokazują, że **FastAPI** (uruchomiony na serwerze Uvicorn) <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">jest jednym z najszybszych dostępnych Pythonowych frameworków</a>, zaraz po Starlette i Uvicorn (używanymi wewnątrznie przez FastAPI). (*)

Aby dowiedzieć się o tym więcej, zobacz sekcję <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Opcjonalne zależności

Używane przez Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - dla szybszego <abbr title="przetwarzania stringa który przychodzi z żądaniem HTTP na dane używane przez Pythona">"parsowania"</abbr> danych JSON.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - dla walidacji adresów email.

Używane przez Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Wymagane jeżeli chcesz korzystać z `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Wymagane jeżeli chcesz korzystać z `FileResponse` albo `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Wymagane jeżeli chcesz używać domyślnej konfiguracji szablonów.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Wymagane jeżelich chcesz wsparcie <abbr title="przetwarzania stringa którzy przychodzi z żądaniem HTTP na dane używane przez Pythona">"parsowania"</abbr> formularzy, używając `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Wymagany dla wsparcia `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Wymagane dla wsparcia `SchemaGenerator` z Starlette (z FastAPI prawdopodobnie tego nie potrzebujesz).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Wymagane dla wsparcia `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Wymagane jeżeli chcesz korzystać z `UJSONResponse`.

Używane przez FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - jako serwer, który ładuje i obsługuje Twoją aplikację.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Wymagane jeżeli chcesz używać `ORJSONResponse`.

Możesz zainstalować wszystkie te aplikacje przy pomocy `pip install fastapi[all]`.

## Licencja

Ten projekt jest na licencji MIT.
