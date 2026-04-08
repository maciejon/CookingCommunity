package config

import (
	"os"
	"github.com/joho/godotenv"
)

type Config struct {
	Port       string
	StaticPath string
	APIKey     string
}

func New() *Config {
	godotenv.Load() 
	apiKey := os.Getenv("API_SECRET_KEY")
	return &Config{
		Port:       "8080",
		StaticPath: "./static",
		APIKey:     apiKey,
	}
}
