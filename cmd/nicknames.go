package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var nicknamesCmd = &cobra.Command{
	Use:   "nicknames",
	Short: "Show repo nicknames",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println()
		fmt.Println("each repo has nicknames:")
		for _, line := range repoNicknames {
			fmt.Printf("  %s\n", line)
		}
		fmt.Println()
	},
}

func init() {
	rootCmd.AddCommand(nicknamesCmd)
}
