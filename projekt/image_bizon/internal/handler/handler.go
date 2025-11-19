package handler

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"

	"github.com/go-chi/chi/v5"
)

type ImageHandler struct {
	StaticPath string
}

func NewImageHandler(staticPath string) *ImageHandler {
	return &ImageHandler{
		StaticPath: staticPath,
	}
}

func (h *ImageHandler) ServeImage(w http.ResponseWriter, r *http.Request) {
	imageName := chi.URLParam(r, "imageName")
	if imageName == "" {
		http.Error(w, "Blank image name", http.StatusBadRequest)
		return
	}

	filePath := filepath.Join(h.StaticPath, imageName)

	http.ServeFile(w, r, filePath)
}

func (h *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(10 << 20) // maks 10MB

	file, handler, err := r.FormFile("file")
	if err != nil {
		fmt.Println("Error while reciving a file:", err)
		http.Error(w, "Error retrieving file from form", http.StatusBadRequest)
		return
	}
	defer file.Close()

	fmt.Printf("Uploaded File: %+v\n", handler.Filename)
	fmt.Printf("File Size: %+v\n", handler.Size)
	fmt.Printf("MIME Header: %+v\n", handler.Header)

	safeFilename := filepath.Base(handler.Filename)
	destPath := filepath.Join(h.StaticPath, safeFilename)
	dst, err := os.Create(destPath)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fileURL := fmt.Sprintf("http://%s/%s", r.Host, safeFilename)
	response := fmt.Sprintf(`{"success": true, "message": "File %s uploaded successfully", "url": "%s"}`, handler.Filename, fileURL)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(response))
}

func (h *ImageHandler) DeleteImage(w http.ResponseWriter, r *http.Request) {
	imageName := chi.URLParam(r, "imageName")
	if imageName == "" {
		http.Error(w, "Blank image name", http.StatusBadRequest)
		return
	}

	safeFilename := filepath.Base(imageName)
	filePath := filepath.Join(h.StaticPath, safeFilename)

	err := os.Remove(filePath)

	if os.IsNotExist(err) {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := fmt.Sprintf(`{"success":"true", "message":"File %s deleted successfully"}`, safeFilename)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(response))
}

// autoryzacja z api key, w headarze żądania trzeba podac "API-Key"
func AuthMiddleware(secretKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			providedKey := r.Header.Get("API-Key")
			if providedKey == "" || providedKey != secretKey {
				fmt.Printf("Invalid or missing API Key\n")
				http.Error(w, "Invalid or missing API Key", http.StatusForbidden)
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}
