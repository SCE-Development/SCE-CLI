package cmd

import (
	"fmt"

	"github.com/SCE-Development/SCE-CLI/internal"
	"github.com/spf13/cobra"
)

var nicknamesCmd = &cobra.Command{
	Use:   "nicknames",
	Short: "Show repo nicknames",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println()
		fmt.Println("each repo has nicknames:")
		for _, line := range internal.RepoNicknames {
			fmt.Printf("  %s\n", line)
		}
		fmt.Println()
	},
}

func init() {
	rootCmd.AddCommand(nicknamesCmd)
}
