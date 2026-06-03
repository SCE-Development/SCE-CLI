package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "sce",
	Short: "CLI tool for managing SCE Development projects",
	Long:  "Command line tool to run any of the SCE projects. Works on Windows, Mac and Linux.",
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
