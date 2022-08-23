package config

import (
	"fmt"
	"sync"

	"github.com/spf13/viper"
)

type Config struct {
	Account      string `yaml:"account"`
	Password     string `yaml:"password"`
	ProductUrl   string `yaml:"productUrl"`
	Chromedriver string `yaml:"chromedriver"`
	Port         int    `yaml:"port"`
	Quantity     uint8  `yaml:"quantity"`
}

var (
	config Config
	once   sync.Once
)

func New() *Config {
	once.Do(func() {
		if err := viper.Unmarshal(&config); err != nil {
			panic(fmt.Errorf("config generate failed: %w", err))
		}
	})

	return &config
}
