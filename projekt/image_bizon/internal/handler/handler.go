package handler

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"

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

var allowedExtensions = map[string]bool{".jpg": true, ".jpeg": true, ".png": true, ".gif": true, ".webp": true}

func (h *ImageHandler) ServeImage(w http.ResponseWriter, r *http.Request) {
	imageName := chi.URLParam(r, "imageName")
	if imageName == "" {
		http.Error(w, "Blank image name", http.StatusBadRequest)
		return
	}

	safeFilename := filepath.Base(imageName)
	ext := strings.ToLower(filepath.Ext(safeFilename))
	if !allowedExtensions[ext] {
		http.Error(w, "File type not allowed", http.StatusBadRequest)
		return
	}

	filePath := filepath.Join(h.StaticPath, safeFilename)

	http.ServeFile(w, r, filePath)
}

func (h *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request) {
	forcedFilename, ok := r.Context().Value(FilenameKey).(string)
	if !ok {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	r.ParseMultipartForm(10 << 20) // maks 10MB

	file, handler, err := r.FormFile("file")
	if err != nil {
		log.Println("Error while reciving a file:", err)
		http.Error(w, "Error retrieving file from form", http.StatusBadRequest)
		return
	}
	defer file.Close()

	log.Printf("Uploaded File: %+v\n", handler.Filename) //log
	log.Printf("File Size: %+v\n", handler.Size)
	log.Printf("MIME Header: %+v\n", handler.Header)

	// sprawdz mime by sie upewnic ze to na pewno jpg czy inne
	buff := make([]byte, 512)
	_, err = file.Read(buff)
	if err != nil {
		log.Println("Error:", err)
		http.Error(w, "Failed to check mime type", http.StatusInternalServerError)
		return
	}
	// czy ja sprawdzam dwa razy to samo
	filetype := http.DetectContentType(buff)
	if _, err := file.Seek(0, 0); err != nil {
		log.Println("Error:", err)
		http.Error(w, "Server error", http.StatusInternalServerError)
		return
	}

	allowedMimes := map[string]bool{
		"image/jpeg": true, "image/png": true, "image/gif": true, "image/webp": true,
	}
	if !allowedMimes[filetype] {
		log.Println("Error:", err)
		http.Error(w, "File type not allowed", http.StatusBadRequest)
		return
	}

	// ------------------------- SAFE ----------------------------------------
	safeFilename := filepath.Base(handler.Filename) // ostatni element sciezki

	ext := strings.ToLower(filepath.Ext(safeFilename))
	if !allowedExtensions[ext] {
		log.Println("Error:", err)
		http.Error(w, "File ext not allowed", http.StatusBadRequest)
		return
	}

	// NAZWA NADANA NIE DANA
	finalName := forcedFilename + ext

	destPath := filepath.Join(h.StaticPath, finalName)

	dst, err := os.Create(destPath)
	if err != nil {
		log.Println("Error:", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		log.Println("Error:", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fileURL := fmt.Sprintf("http://%s/%s", r.Host, finalName)
	response := fmt.Sprintf(`{"success": true, "message": "File %s uploaded successfully", "url": "%s"}`, handler.Filename, fileURL)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(response))
}

func (h *ImageHandler) DeleteImage(w http.ResponseWriter, r *http.Request) {
	imageName := chi.URLParam(r, "imageName")
	if imageName == "" {
		log.Println("Error blank image name")
		http.Error(w, "Blank image name", http.StatusBadRequest)
		return
	}

	log.Printf("Http Header: %+v", r.Header)

	safeFilename := filepath.Base(imageName)

	ext := strings.ToLower(filepath.Ext(safeFilename))
	if !allowedExtensions[ext] {
		log.Println("Error file type not allowed")
		http.Error(w, "File type not allowed", http.StatusBadRequest)
		return
	}

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
