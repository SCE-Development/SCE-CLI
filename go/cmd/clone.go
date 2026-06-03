package cmd

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/SCE-Development/SCE-CLI/internal"
	"github.com/spf13/cobra"
)

var sshFlag bool

var cloneCmd = &cobra.Command{
	Use:   "clone <repo>",
	Short: "Clone the given repo from GitHub",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		repo, ok := internal.ResolveAlias(args[0])
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown repo: %s\n", args[0])
			os.Exit(1)
		}

		var url string
		if sshFlag {
			url = internal.GithubBaseSSHURL + repo.RepoName + ".git"
		} else {
			url = internal.GithubBaseHTTPURL + repo.RepoName + ".git"
		}

		gitCmd := exec.Command("git", "clone", url)
		gitCmd.Stdout = os.Stdout
		gitCmd.Stderr = os.Stderr
		if err := gitCmd.Run(); err != nil {
			os.Exit(1)
		}
	},
}

func init() {
	cloneCmd.Flags().BoolVar(&sshFlag, "ssh", false, "clone using SSH instead of HTTPS")
	rootCmd.AddCommand(cloneCmd)
}
