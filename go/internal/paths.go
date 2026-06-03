package internal

import (
	"fmt"
	"os"
	"path/filepath"
)

func GetCliDirectory() (string, error) {
	exe, err := os.Executable()
	if err != nil {
		return "", err
	}
	resolved, err := filepath.EvalSymlinks(exe)
	if err != nil {
		return "", err
	}
	return filepath.Dir(resolved), nil
}

func GetRepoPath(repoName string) (string, error) {
	cliDir, err := GetCliDirectory()
	if err != nil {
		return "", err
	}
	linkPath := filepath.Join(cliDir, repoName)

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
	cliDir, err := GetCliDirectory()
	if err != nil {
		return err
	}
	linkPath := filepath.Join(cliDir, repoName)

	// Remove existing symlink if present
	os.Remove(linkPath)

	return os.Symlink(targetDir, linkPath)
}
