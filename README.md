Rozbudowany opis instalacji i uruchomienia aplikacji:

# Instrukcja instalacji oraz uruchomienia aplikacji
Aby uruchomić aplikację, wykonaj poniższe kroki. Zakłada się, że użytkownik korzysta z systemu operacyjnego zgodnego z Dockerem (Linux, macOS, Windows z zainstalowanym Dockerem).

## Krok 1: Instalacja oprogramowania Docker i Docker Compose

Aplikacja jest uruchamiana za pomocą kontenerów, co upraszcza zarządzanie zależnościami oraz konfiguracją środowiska. Do tego celu wykorzystany zostanie Docker oraz Docker Compose. Upewnij się, że masz zainstalowane następujące oprogramowanie:

1. **Docker**
2. **Docker Compose**

## Krok 2: Sklonowanie repozytorium z kodem źródłowym

Po zainstalowaniu Dockera i Docker Compose, należy sklonować repozytorium z aplikacją. Wykonaj to za pomocą komendy `git clone`:

1. Otwórz terminal.
2. Przejdź do katalogu, w którym chcesz umieścić projekt.
3. Wpisz poniższą komendę, aby sklonować repozytorium:

```bash
git clone https://github.com/PJWSTK-Data-Science-Dojo/fintax-hackyeah-2024
```

4. Przejdź do katalogu projektu:

```bash
cd fintax-hackyeah-2024
```

## Krok 3: Ustawienie klucza dostępu OpenAI

Aplikacja korzysta z API OpenAI, co wymaga posiadania odpowiedniego klucza API. Należy go uzyskać z serwisu OpenAI, a następnie skonfigurować go w aplikacji.

1. Załóż konto lub zaloguj się do [OpenAI](https://platform.openai.com/).
2. Utwórz klucz API.
3. W otwartym projekcie przejdź do pliku `docker-compose.yml`. Możesz to zrobić za pomocą edytora tekstu lub dowolnego IDE.

4. Otwórz plik i znajdź linię 24. Powinna wyglądać mniej więcej tak:

```yaml
OPENAI_API_KEY: "YOUR_OPENAI_API_KEY"
```

5. Zamień `"YOUR_OPENAI_API_KEY"` na swój rzeczywisty klucz API otrzymany z OpenAI:

```yaml
OPENAI_API_KEY: "Twój_Klucz_API"
```

Zapisz plik i zamknij edytor.

## Krok 4: Uruchomienie aplikacji za pomocą Docker Compose

Po skonfigurowaniu klucza API jesteś gotów, aby uruchomić aplikację.

1. W terminalu, będąc w katalogu projektu, uruchom komendę:

```bash
docker-compose up -d
```

Opcja `-d` uruchamia kontenery w trybie "detached", co oznacza, że aplikacja będzie działać w tle. Jeżeli chcesz zobaczyć logi w czasie rzeczywistym, możesz pominąć flagę `-d`.

2. Docker Compose pobierze wszystkie niezbędne obrazy oraz uruchomi kontenery zgodnie z konfiguracją zawartą w pliku `docker-compose.yml`.

## Krok 5: Dostęp do aplikacji

Po uruchomieniu kontenerów, aplikacja będzie dostępna w przeglądarce. Otwórz przeglądarkę internetową i wpisz poniższy adres:

```
http://localhost:8501/
```

Aplikacja powinna się załadować, a Ty będziesz mógł rozpocząć interakcję z interfejsem użytkownika.

---

### Dodatkowe informacje:

- Jeśli chcesz zatrzymać aplikację, użyj komendy:

```bash
docker-compose down
```

- Aby sprawdzić logi działania aplikacji, możesz użyć:

```bash
docker-compose logs
```

- W razie problemów z uruchomieniem aplikacji sprawdź, czy wszystkie kontenery działają poprawnie za pomocą:

```bash
docker ps
```

Jeśli napotkasz problemy z konfiguracją, warto przejrzeć dokumentację Dockera lub skontaktować się z administratorem projektu.