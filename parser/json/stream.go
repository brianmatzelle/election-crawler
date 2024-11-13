package stream

import (
	"encoding/json"
	"os"
)

const POSTS_FILE = "./posts-11-13-2024.json"

// OpenPostsStream opens the posts.json file and returns a decoder for streaming JSON data
func OpenPostsStream() (*json.Decoder, error) {
	// Open the file
	file, err := os.Open(POSTS_FILE)
	if err != nil {
		return nil, err
	}

	// Create a new decoder
	decoder := json.NewDecoder(file)
	return decoder, nil
}
