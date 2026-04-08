start cmd /k "title BACKEND & cd backend_bizon & call .venv\Scripts\activate & python manage.py runserver"
start cmd /k "title FRONTEND & cd frontend_bizon & npm run dev"
start cmd /k "title IMAGE & cd image_bizon & go run main.go"