package internal

import (
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const (
	latestReleaseURL = "https://api.github.com/repos/SCE-Development/SCE-CLI/releases/latest"
	cacheFileName    = ".version-check.json"
	cacheTTL         = 24 * time.Hour
	httpTimeout      = 1500 * time.Millisecond
)

type versionCache struct {
	Latest    string    `json:"latest"`
	CheckedAt time.Time `json:"checked_at"`
}

// LatestRelease returns the most recent release tag, using a 24h on-disk cache.
// Returns an empty string on any failure (network, parse, fs) — callers must
// treat "" as "unknown" and stay silent.
func LatestRelease() string {
	cachePath, err := cachePath()
	if err == nil {
		if cached, ok := readCache(cachePath); ok {
			return cached
		}
	}

	latest := fetchLatest()
	if latest == "" {
		return ""
	}

	if cachePath != "" {
		writeCache(cachePath, latest)
	}
	return latest
}

func cachePath() (string, error) {
	dir, err := GetLinkDirectory()
	if err != nil {
		return "", err
	}
	return filepath.Join(dir, cacheFileName), nil
}

func readCache(path string) (string, bool) {
	data, err := os.ReadFile(path)
	if err != nil {
		return "", false
	}
	var c versionCache
	if err := json.Unmarshal(data, &c); err != nil {
		return "", false
	}
	if time.Since(c.CheckedAt) > cacheTTL {
		return "", false
	}
	return c.Latest, c.Latest != ""
}

func writeCache(path, latest string) {
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return
	}
	data, err := json.Marshal(versionCache{Latest: latest, CheckedAt: time.Now()})
	if err != nil {
		return
	}
	_ = os.WriteFile(path, data, 0644)
}

func fetchLatest() string {
	client := &http.Client{Timeout: httpTimeout}
	req, err := http.NewRequest("GET", latestReleaseURL, nil)
	if err != nil {
		return ""
	}
	req.Header.Set("Accept", "application/vnd.github+json")
	resp, err := client.Do(req)
	if err != nil {
		return ""
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return ""
	}
	var payload struct {
		TagName string `json:"tag_name"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		return ""
	}
	return payload.TagName
}
