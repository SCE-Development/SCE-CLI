package cmd

import (
	"fmt"
	"os"

	"github.com/SCE-Development/SCE-CLI/internal"
	"github.com/spf13/cobra"
)

var linkCmd = &cobra.Command{
	Use:   "link <repo>",
	Short: "Tell the sce tool where to find the repo on your computer",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		repo, ok := internal.ResolveAlias(args[0])
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown repo: %s\n", args[0])
			os.Exit(1)
		}

		cwd, err := os.Getwd()
		if err != nil {
			fmt.Fprintf(os.Stderr, "error getting current directory: %v\n", err)
			os.Exit(1)
		}

		if err := internal.CreateLink(repo.RepoName, cwd); err != nil {
			fmt.Fprintf(os.Stderr, "error creating link: %v\n", err)
			os.Exit(1)
		}

		fmt.Printf("linked %s → %s\n", repo.RepoName, cwd)
	},
}

func init() {
	rootCmd.AddCommand(linkCmd)
}
