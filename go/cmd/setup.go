package cmd

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"

	"github.com/SCE-Development/SCE-CLI/internal"
	"github.com/spf13/cobra"
)

var setupCmd = &cobra.Command{
	Use:   "setup <repo>",
	Short: "Copy config.example.json in a repo to config.json",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		repo, ok := internal.ResolveAlias(args[0])
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown repo: %s\n", args[0])
			os.Exit(1)
		}

		repoPath, err := internal.GetRepoPath(repo.RepoName)
		if err != nil {
			fmt.Printf("it looks like you haven't linked %s to the sce tool.\n", repo.RepoName)
			fmt.Println()
			fmt.Printf("either link the repo with sce link %s or clone it first with sce clone %s.\n", repo.RepoName, repo.RepoName)
			os.Exit(1)
		}

		if len(repo.ConfigPaths) == 0 {
			fmt.Printf("%s has no config files to set up.\n", repo.RepoName)
			return
		}

		for _, configPath := range repo.ConfigPaths {
			examplePath := filepath.Join(repoPath, strings.Replace(configPath, "config.json", "config.example.json", 1))
			targetPath := filepath.Join(repoPath, configPath)

			if err := copyFile(examplePath, targetPath); err != nil {
				fmt.Fprintf(os.Stderr, "error copying %s: %v\n", configPath, err)
				continue
			}
			fmt.Printf("copied %s → %s\n",
				strings.Replace(configPath, "config.json", "config.example.json", 1),
				configPath,
			)
		}
	},
}

func copyFile(src, dst string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}

func init() {
	rootCmd.AddCommand(setupCmd)
}
