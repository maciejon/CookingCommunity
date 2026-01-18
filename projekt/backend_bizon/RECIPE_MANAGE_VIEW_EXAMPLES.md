# RecipeManageView - Przykładowe zapytania REST i JSON

**Endpoint:** `/recipe/upload/`

**Wymagane uwierzytelnienie:** Token JWT (cookies)

---

## 1. GET - Pobranie kategorii, składników i jednostek

### Zapytanie:
```http
GET /recipe/upload/
Host: localhost:8000
Cookie: access_token=<jwt_token>
```

### Odpowiedź (200 OK):
```json
{
    "categories": [
        {"id": 1, "name": "Śniadania", "slug": "sniadania"},
        {"id": 2, "name": "Obiady", "slug": "obiady"},
        {"id": 3, "name": "Kolacje", "slug": "kolacje"},
        {"id": 4, "name": "Desery", "slug": "desery"},
        {"id": 5, "name": "Zupy", "slug": "zupy"}
    ],
    "ingredients": [
        {"id": 1, "name": "Mąka"},
        {"id": 2, "name": "Jajka"},
        {"id": 3, "name": "Mleko"},
        {"id": 4, "name": "Masło"},
        {"id": 5, "name": "Cukier"},
        {"id": 6, "name": "Sól"},
        {"id": 7, "name": "Pieprz"},
        {"id": 8, "name": "Kurczak"},
        {"id": 9, "name": "Cebula"},
        {"id": 10, "name": "Czosnek"}
    ],
    "units": [
        {"value": "łyżka", "label": "łyżka"},
        {"value": "łyżeczka", "label": "łyżeczka"},
        {"value": "szklanka", "label": "szklanka"},
        {"value": "sztuka", "label": "sztuka"},
        {"value": "szczypta", "label": "szczypta"},
        {"value": "ml", "label": "ml"},
        {"value": "l", "label": "l"},
        {"value": "g", "label": "g"},
        {"value": "kg", "label": "kg"},
        {"value": "", "label": ""}
    ]
}
```

---

## 2. POST - Utworzenie nowego przepisu

### Zapytanie:
```http
POST /recipe/upload/
Host: localhost:8000
Content-Type: application/json
Cookie: access_token=<jwt_token>

{
    "name": "Naleśniki",
    "description": "Tradycyjne polskie naleśniki z dżemem lub śmietaną",
    "preparation_time": 30,
    "categories": [1],
    "steps": [
        {"step_number": 1, "text": "W misce wymieszaj mąkę z jajkami i mlekiem.", "image": ""},
        {"step_number": 2, "text": "Dodaj szczyptę soli i oleju.", "image": ""},
        {"step_number": 3, "text": "Smaż na rozgrzanej patelni z obu stron.", "image": ""}
    ],
    "ingredients": [
        {"ingredient": 1, "quantity": "2.5", "unit_choice": "szklanka"},
        {"ingredient": 2, "quantity": "3", "unit_choice": "sztuka"},
        {"ingredient": 3, "quantity": "500", "unit_choice": "ml"},
        {"ingredient": 5, "quantity": "2", "unit_choice": "łyżka"},
        {"ingredient": 6, "quantity": "1", "unit_choice": "szczypta"}
    ]
}
```

### Odpowiedź (201 Created):
```json
{
    "Upload-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "Upload-Url": "http://localhost:8080/upload"
}
```

### Następny krok - upload obrazka:
```http
POST http://localhost:8080/upload
Content-Type: multipart/form-data
Upload-Token: <image_secret_key>

multipart/form-data z plikiem obrazka
```

---

## 3. PUT - Aktualizacja przepisu

### Zapytanie:
```http
PUT /recipe/upload/
Host: localhost:8000
Content-Type: application/json
Cookie: access_token=<jwt_token>

{
    "id": 1,
    "name": "Naleśniki (wersja 2)",
    "description": "Zaktualizowany przepis na puszyste naleśniki",
    "preparation_time": 25,
    "categories": [1, 4],
    "steps": [
        {"step_number": 1, "text": "Ubij jajka z cukrem na puszystą masę.", "image": ""},
        {"step_number": 2, "text": "Dodaj mleko i wymieszaj.", "image": ""},
        {"step_number": 3, "text": "Stopniowo dodawaj przesianą mąkę.", "image": ""},
        {"step_number": 4, "text": "Smaż na małym ogniu.", "image": ""}
    ],
    "ingredients": [
        {"ingredient": 1, "quantity": "2", "unit_choice": "szklanka"},
        {"ingredient": 2, "quantity": "4", "unit_choice": "sztuka"},
        {"ingredient": 3, "quantity": "400", "unit_choice": "ml"},
        {"ingredient": 4, "quantity": "50", "unit_choice": "g"},
        {"ingredient": 5, "quantity": "3", "unit_choice": "łyżka"}
    ]
}
```

### Odpowiedź (200 OK):
```json
{
    "id": 1,
    "name": "Naleśniki (wersja 2)",
    "description": "Zaktualizowany przepis na puszyste naleśniki",
    "preparation_time": 25,
    "categories": [1, 4]
}
```

### Z aktualizacją obrazka (dodaj `update_image: true`):
```http
PUT /recipe/upload/
Host: localhost:8000
Content-Type: application/json
Cookie: access_token=<jwt_token>

{
    "id": 1,
    "update_image": true,
    "name": "Naleśniki z nowym zdjęciem",
    "description": "Przepis ze świeżym zdjęciem",
    "preparation_time": 30,
    "categories": [1]
}
```

### Odpowiedź z tokenem upload:
```json
{
    "id": 1,
    "name": "Naleśniki z nowym zdjęciem",
    "description": "Przepis ze świeżym zdjęciem",
    "preparation_time": 30,
    "categories": [1],
    "Upload-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "Upload-Url": "http://localhost:8080/upload"
}
```

---

## 4. DELETE - Usunięcie przepisu

### Zapytanie (via request.data):
```http
DELETE /recipe/upload/
Host: localhost:8000
Content-Type: application/json
Cookie: access_token=<jwt_token>

{"id": 1}
```

### Zapytanie (via query params):
```http
DELETE /recipe/upload/?id=1
Host: localhost:8000
Cookie: access_token=<jwt_token>
```

### Odpowiedź (200 OK):
```json
{
    "status": 200
}
```

---

## 5. Przykład pełnego przepisu (kompleksowy JSON)

### Pełny POST do tworzenia przepisu:
```json
{
    "name": "Kurczak w sosie cytrynowym",
    "description": "Pysny kurczak w kremowym sosie cytrynowym z ziołami. Podawaj z ryżem lub makaronem.",
    "preparation_time": 45,
    "categories": [2],
    "steps": [
        {
            "step_number": 1,
            "text": "Pokrój kurczaka na kawałki i dopraw solą oraz pieprzem.",
            "image": ""
        },
        {
            "step_number": 2,
            "text": "Na patelni rozgrzej masło i smaż kurczaka na złoty kolor.",
            "image": ""
        },
        {
            "step_number": 3,
            "text": "Drobno pokrojoną cebulę i czosnek podsmaż przez 2 minuty.",
            "image": ""
        },
        {
            "step_number": 4,
            "text": "Wlej śmietanę i sok z cytryny, dopraw ziołami.",
            "image": ""
        },
        {
            "step_number": 5,
            "text": "Duś pod przykryciem przez 20 minut aż sos zgęstnieje.",
            "image": ""
        }
    ],
    "ingredients": [
        {
            "ingredient": 8,
            "quantity": "500",
            "unit_choice": "g"
        },
        {
            "ingredient": 9,
            "quantity": "1",
            "unit_choice": "sztuka"
        },
        {
            "ingredient": 10,
            "quantity": "3",
            "unit_choice": "ząbek"
        },
        {
            "ingredient": 4,
            "quantity": "3",
            "unit_choice": "łyżka"
        },
        {
            "ingredient": 3,
            "quantity": "250",
            "unit_choice": "ml"
        }
    ]
}
```

---

## Uwagi:

1. Wszystkie zapytania (POST, PUT, DELETE) wymagają tokena JWT w cookies (`access_token`)
2. Użytkownik może modyfikować/usuwać tylko własne przepisy (`created_by=request.user`)
3. Po utworzeniu przepisu (`POST`) należy przesłać obrazek na serwer obrazków używając otrzymanego `Upload-Token`
4. `ingredient` w JSON to ID składnika z odpowiedzi GET
5. `categories` to lista ID kategorii
6. `unit_choice` musi być jedną z wartości: `łyżka`, `łyżeczka`, `szklanka`, `sztuka`, `szczypta`, `ml`, `l`, `g`, `kg`, ``

