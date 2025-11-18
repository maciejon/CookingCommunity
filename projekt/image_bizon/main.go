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

	r := chi.NewRouter()

	r.Use(middleware.Logger)

	r.Get("/{imageName}", imageHandler.ServeImage)
	// r.Post("/upload", imageHandler.UploadImage)

	addr := fmt.Sprintf(":%s", cfg.Port)
	log.Printf("Listen on http://localhost%s", addr)

	err := http.ListenAndServe(addr, r)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}
}
