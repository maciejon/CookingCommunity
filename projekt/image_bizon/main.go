// File: main.go
package main

import (
	"fmt"
	"log"
	"net/http"

	"image_bizon/internal/config"
	"image_bizon/internal/handler"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

func main() {
	cfg := config.New()

	imageHandler := handler.NewImageHandler(cfg.StaticPath)

	rout := chi.NewRouter()

	rout.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"http://localhost:5173", "http://localhost:8000"},
		AllowedMethods:   []string{"GET", "POST", "DELETE"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "Upload-Token", "API-Key"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300,
	}))

	rout.Use(middleware.Logger)

	rout.Get("/{imageName}", imageHandler.ServeImage)

	// chronione, wymagaja podania api key
	rout.Group(func(rout chi.Router) {
		rout.Use(handler.AuthMiddleware(cfg.APIKey))
		rout.Delete("/{imageName}", imageHandler.DeleteImage)
	})

	rout.Group(func(rout chi.Router) {
		rout.Use(handler.ValidateUploadToken(cfg.APIKey))
		rout.Post("/upload", imageHandler.UploadImage)
	})

	addr := fmt.Sprintf(":%s", cfg.Port)
	log.Printf("Listen on http://localhost%s", addr)

	err := http.ListenAndServe(addr, rout)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}
}
