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
)

func main() {
	cfg := config.New()

	imageHandler := handler.NewImageHandler(cfg.StaticPath)

	rout := chi.NewRouter()

	rout.Use(middleware.Logger)

	rout.Get("/{imageName}", imageHandler.ServeImage)

	// chronione, wymagaja podania api key
	rout.Group(func(rout chi.Router) {
		rout.Use(handler.AuthMiddleware(cfg.APIKey))
		rout.Post("/upload", imageHandler.UploadImage)
		rout.Delete("/{imageName}", imageHandler.DeleteImage)
	})

	addr := fmt.Sprintf(":%s", cfg.Port)
	log.Printf("Listen on http://localhost%s", addr)

	err := http.ListenAndServe(addr, rout)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}
}
