Włączenie serwera backend:
wejść do .venv (macOS: source .venv/bin/activate Windows(cmd): .venv\Scripts\Activate)
backend_bizon > py (albo python3) manage.py runserver

Włączenie serwera frontend (2 cmd):
frontend_bizon > npm run dev

Włączenie mikroserwisu zdjęć (3 cmd):
image_bizon > go run main.go

# Dokumentacja Backend API

## 1. Logowanie i rejestracja

### Rejestracja
Rejestruje użytkownika, wysyła e-mail powitalny i **automatycznie loguje** (zwraca ciasteczka sesyjne).

*   **URL:** `/register/`
*   **Metoda:** `POST`
*   **Body:**
    ```json
    {
      "username": "jan123",
      "email": "jan@example.com",
      "password": "strongpassword"
    }
    ```

### Logowanie
*   **URL:** `/token/`
*   **Metoda:** `POST`
*   **Body:**
    ```json
    {
      "username": "jan123",
      "password": "strongpassword"
    }
    ```
*   **Sukces (200 OK):** Odpowiedź pusta lub ze szczątkowymi danymi, kluczowe są nagłówki `Set-Cookie`.

### Odświeżanie tokena (Refresh)
Należy wywołać ten endpoint, gdy API zwróci błąd `401 Unauthorized` (wygasł access token). Endpoint pobiera `refresh_token` z ciasteczek i ustawia nowy `access_token`.

*   **URL:** `/token/refresh/`
*   **Metoda:** `POST`

### Wylogowanie
Unieważnia token refresh i usuwa ciasteczka z przeglądarki.

*   **URL:** `/logout/`
*   **Metoda:** `POST`

---

## 2. Przepisy - Publiczne

### Top 5 Przepisów
Zwraca 5 najczęściej wyświetlanych przepisów.

*   **URL:** `/top5/`
*   **Metoda:** `GET`
*   **Odpowiedź (200 OK):**
    ```json
    {
      "top5": [
        {
          "id": 1,
          "title": "Jajecznica",
          "slug": "jajecznica",
          "image": "r_1_123456",
          "category": { ... }
        },
        ...
      ]
    }
    ```

### Szczegóły Przepisu
Pobiera jeden przepis. Automatycznie inkrementuje licznik wyświetleń.

*   **URL:** `/recipe/<slug>/`
*   **Metoda:** `GET`
*   **Odpowiedź (200 OK):**
    ```json
    {
      "id": 10,
      "title": "Pizza",
      "ingredients": [...],
      "steps": "...",
      "requesting_user": "...",
      "can_delete": 1              
    }
    ```
*   **Błędy:** `404` jeśli przepis nie istnieje.

### Wyszukiwanie
Szuka w nazwie, opisie i składnikach. Wyniki są sortowane według trafności (nazwa > opis > składnik).

*   **URL:** `/search/`
*   **Metoda:** `GET`
*   **Parametry:** `?query=pomidorowa`
*   **Odpowiedź (200 OK):**
    ```json
    [
      {
        "id": 5,
        "title": "Zupa pomidorowa",
        "relevance": 10
      },
      ...
    ]
    ```

### Szczegóły Kategorii
*   **URL:** `/category/<slug>/`
*   **Metoda:** `GET`

## 3. Zarządzanie Przepisami

### Pobieranie danych do uploadu
Pobiera listy potrzebne do zbudowania selectów w formularzu dodawania/edycji.

*   **URL:** `/recipe/upload/`
*   **Metoda:** `GET`
*   **Wymaga logowania:** Tak
*   **Odpowiedź (200 OK):**
    ```json
    {
      "categories": [{"id": 1, "name": "Obiad"}, ...],
      "ingredients": [{"id": 50, "name": "Mąka"}, ...],
      "units": [{"value": "g", "label": "Gramy"}, ...]
    }
    ```

### Dodawanie Przepisu
Tworzy wpis w bazie i zwraca token pozwalający na wysłanie zdjęcia na zewnętrzny serwer.

*   **URL:** `/recipe/upload/`
*   **Metoda:** `POST`
*   **Body:**
    ```json
    {
      "title": "Nowe Ciasto",
      "description": "Opis...",
      "category": 1,
      "ingredients": [...]
    }
    ```
*   **Odpowiedź (201 Created):**
    ```json
    {
      "id": 15,
      "title": "Nowe Ciasto",
      "Upload-Token": "eyJhbGciOiJI...",  
      "Upload-Url": "https://.../upload"
    }
    ```
    > **Uwaga:** Frontend po otrzymaniu tej odpowiedzi musi wysłać plik graficzny `PUT` na adres `Upload-Url` z nagłówkiem autoryzacji `Upload-Token`.

### Usuwanie Przepisu
Usuwa przepis z bazy oraz wysyła żądanie usunięcia zdjęcia z zewnętrznego serwisu.

*   **URL:** `/recipe/upload/`
*   **Metoda:** `DELETE`
*   **Parametry:** `?id=15` (lub w body `{ "id": 15 }`)

## 4. Reszta

## Reviews
Jeden użytkownik może dodać tylko jedną opinię do danego przepisu.

*   **URL:** `/create_review/`
*   **Metoda:** `POST`
*   **Wymaga logowania:** Tak
*   **Body:**
    ```json
    {
      "recipe_id": 10,
      "stars": 5,
      "text": "Super smakuje!"
    }
    ```
*   **Błędy:** `409 Conflict` (jeśli opinia już istnieje).

### Usuwanie samego zdjęcia
Usuwa zdjęcie z przepisu, ale zostawia sam przepis.

*   **URL:** `/images/`
*   **Metoda:** `DELETE`
*   **Body:** `{ "id": 10 }` (ID przepisu)

## 5. IMAGE server

## Pobranie zdjęcia

*   **URL:** `/{imageName}`
*   **Metoda:** `GET`

## Usuwanie zdjęcia

*   **URL:** `/{imageName}`
*   **Metoda:** `GET`
*   **Header:** `API-Key` : `...`

## Upload zdjęcia

*   **URL:** `/upload`
*   **Metoda:** `POST`
*   **Nagłówki:**
    *   `Content-Type: multipart/form-data`
*   **Body (Multipart):**
    *   `headers`: { `Upload-Token`: `...` },
    *   `file`: (plik binarny)
