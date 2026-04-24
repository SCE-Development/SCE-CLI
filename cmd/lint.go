package cmd

import (
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/spf13/cobra"
)

var lintCmd = &cobra.Command{
	Use:   "lint <repo>",
	Short: "Run eslint --fix on running containers (Clark and SCE-discord-bot only)",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		repo, ok := resolveAlias(args[0])
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown repo: %s\n", args[0])
			os.Exit(1)
		}

		targets, ok := lintContainers[repo.RepoName]
		if !ok {
			fmt.Fprintf(os.Stderr, "lint is not supported for %s\n", repo.RepoName)
			fmt.Fprintln(os.Stderr, "lint is only available for Clark and SCE-discord-bot.")
			os.Exit(1)
		}

		for _, target := range targets {
			fmt.Printf("linting in %s...\n", target.Container)
			lintCommand := fmt.Sprintf("npm run lint -- -c %s --fix", target.EslintConfig)
			dockerCmd := exec.Command("docker", "exec", "-i", target.Container, "/bin/sh")
			dockerCmd.Stdin = strings.NewReader(lintCommand)
			dockerCmd.Stdout = os.Stdout
			dockerCmd.Stderr = os.Stderr
			if err := dockerCmd.Run(); err != nil {
				fmt.Fprintf(os.Stderr, "error linting in %s: %v\n", target.Container, err)
			}
		}
	},
}

func init() {
	rootCmd.AddCommand(lintCmd)
}
