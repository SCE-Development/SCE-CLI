package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Show the version of the SCE CLI",
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println(currentVersion)
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)
}
