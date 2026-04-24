package cmd

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/spf13/cobra"
)

var runCmd = &cobra.Command{
	Use:   "run <repo>",
	Short: "Run the repo using docker",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		repo, ok := resolveAlias(args[0])
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown repo: %s\n", args[0])
			os.Exit(1)
		}

		repoPath, err := getRepoPath(repo.RepoName)
		if err != nil {
			fmt.Printf("it looks like you haven't linked %s to the sce tool.\n", repo.RepoName)
			fmt.Println()
			fmt.Printf("either link the repo with sce link %s or clone it first with sce clone %s.\n", repo.RepoName, repo.RepoName)
			os.Exit(1)
		}

		// Check config files exist
		for _, configPath := range repo.ConfigPaths {
			fullPath := filepath.Join(repoPath, configPath)
			if _, err := os.Stat(fullPath); os.IsNotExist(err) {
				fmt.Println()
				fmt.Println("it seems like you forgot to create/configure the config.json file(s)")
				fmt.Println("follow the config.example.json as a template and add it at the following paths:")
				for _, p := range repo.ConfigPaths {
					fmt.Println(filepath.Join(repoPath, p))
				}
				fmt.Println()
				os.Exit(1)
			}
		}

		composeCmd := dockerComposeCommand()

		if repo.MongoDBOnly {
			dockerCmd := exec.Command(composeCmd[0], append(composeCmd[1:], "-f", dockerComposeFile, "up", "mongodb", "-d")...)
			dockerCmd.Dir = repoPath
			dockerCmd.Stdout = os.Stdout
			dockerCmd.Stderr = os.Stderr
			if err := dockerCmd.Run(); err != nil {
				os.Exit(1)
			}
		} else {
			dockerCmd := exec.Command(composeCmd[0], append(composeCmd[1:], "-f", dockerComposeFile, "up", "--build")...)
			dockerCmd.Dir = repoPath
			dockerCmd.Stdout = os.Stdout
			dockerCmd.Stderr = os.Stderr
			dockerCmd.Stdin = os.Stdin
			if err := dockerCmd.Run(); err != nil {
				os.Exit(1)
			}
		}
	},
}

func dockerComposeCommand() []string {
	// Try docker compose v2 first
	if err := exec.Command("docker", "compose", "version").Run(); err == nil {
		return []string{"docker", "compose"}
	}
	return []string{"docker-compose"}
}

func init() {
	rootCmd.AddCommand(runCmd)
}
