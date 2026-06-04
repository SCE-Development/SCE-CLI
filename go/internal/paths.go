package internal

import (
	"fmt"
	"os"
	"path/filepath"
)

func GetLinkDirectory() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	return filepath.Join(home, ".sce"), nil
}

func GetRepoPath(repoName string) (string, error) {
	linkDir, err := GetLinkDirectory()
	if err != nil {
		return "", err
	}
	linkPath := filepath.Join(linkDir, repoName)

	info, err := os.Lstat(linkPath)
	if err != nil {
		return "", fmt.Errorf("repo %s is not linked", repoName)
	}

	// Follow symlink if it is one
	if info.Mode()&os.ModeSymlink != 0 {
		resolved, err := filepath.EvalSymlinks(linkPath)
		if err != nil {
			return "", err
		}
		return resolved, nil
	}

	return linkPath, nil
}

func CreateLink(repoName string, targetDir string) error {
	linkDir, err := GetLinkDirectory()
	if err != nil {
		return err
	}
	if err := os.MkdirAll(linkDir, 0755); err != nil {
		return err
	}
	linkPath := filepath.Join(linkDir, repoName)

	// Remove existing symlink if present
	os.Remove(linkPath)

	return os.Symlink(targetDir, linkPath)
}
