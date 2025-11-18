package handler

import (
	"net/http"
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

// func (h *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request) {
// 	r.ParseMultipartForm(10 << 20) // maks 10MB

// 	file, handler, err := r.FormFile("file")
// 	if err != nil {
// 		fmt.Println("Error Retrieving the File:", err)
// 		http.Error(w, "Error retrieving file from form", http.StatusBadRequest)
// 		return
// 	}
// 	defer file.Close()

// 	fmt.Printf("Uploaded File: %+v\n", handler.Filename)
// 	fmt.Printf("File Size: %+v\n", handler.Size)
// 	fmt.Printf("MIME Header: %+v\n", handler.Header)

// 	safeFilename := filepath.Base(handler.Filename)
// 	destPath := filepath.Join(h.StaticPath, safeFilename)

// 	dst, err := os.Create(destPath)
// 	if err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	defer dst.Close()

// 	if _, err := io.Copy(dst, file); err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}

// 	fileURL := fmt.Sprintf("http://%s/%s", r.Host, safeFilename)
// 	response := fmt.Sprintf(`{"success": true, "message": "File uploaded successfully", "url": "%s"}`, fileURL)

// 	w.Header().Set("Content-Type", "application/json")
// 	w.WriteHeader(http.StatusCreated)
// 	w.Write([]byte(response))
// }
