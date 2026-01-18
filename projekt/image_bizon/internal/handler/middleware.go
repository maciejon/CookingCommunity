package handler

import (
	"context"
	"crypto/subtle"
	"fmt"
	"net/http"

	"github.com/golang-jwt/jwt/v5"
)

// autoryzacja z api key, w headarze żądania trzeba podac "API-Key"
func AuthMiddleware(secretKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			providedKey := r.Header.Get("API-Key")
			if subtle.ConstantTimeCompare([]byte(providedKey), []byte(secretKey)) != 1 {
				http.Error(w, "Invalid API-Key", http.StatusForbidden)
				return
			}
			// to jest rzekomo głupie
			// if providedKey == "" || providedKey != secretKey {
			// 	fmt.Printf("Invalid or missing API-Key\n")
			// 	http.Error(w, "Invalid or missing API-Key", http.StatusForbidden)
			// 	return
			// }
			next.ServeHTTP(w, r)
		})
	}
}

type key int

const FilenameKey key = 0

func ValidateUploadToken(secretKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			tokenString := r.Header.Get("Upload-Token")
			if tokenString == "" {
				http.Error(w, "Upload-Token: ???", http.StatusUnauthorized)
				return
			}

			token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
				if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
					return nil, fmt.Errorf("wrong signing method")
				}
				return []byte(secretKey), nil
			})

			if err != nil || !token.Valid {
				http.Error(w, "invalid token", http.StatusForbidden)
				return
			}

			claims, ok := token.Claims.(jwt.MapClaims)
			if !ok {
				http.Error(w, "claims error", http.StatusForbidden)
				return
			}

			filename := claims["filename"].(string)

			// przerzucic w contextcie
			ctx := context.WithValue(r.Context(), FilenameKey, filename)

			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
