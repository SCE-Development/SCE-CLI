package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var completionCmd = &cobra.Command{
	Use:   "completion",
	Short: "Output shell alias/completion for the sce command",
	Run: func(cmd *cobra.Command, args []string) {
		fishVersion := os.Getenv("FISH_VERSION")
		if fishVersion != "" {
			exe, _ := os.Executable()
			fmt.Println("# add this to your fish config")
			fmt.Printf("function sce; %s $argv; end\n", exe)
			return
		}

		shell := os.Getenv("SHELL")
		exe, _ := os.Executable()
		if shell != "" {
			fmt.Println("# add this to your shell config")
			fmt.Printf("alias sce=\"%s\"\n", exe)
		} else {
			fmt.Printf("# alias sce to: %s\n", exe)
		}
	},
}

func init() {
	rootCmd.AddCommand(completionCmd)
}
