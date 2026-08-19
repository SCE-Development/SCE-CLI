package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/SCE-Development/SCE-CLI/internal"
	"github.com/spf13/cobra"
)

var currentVersion = "dev"

func SetVersion(v string) {
	currentVersion = v
}

var skipVersionCheck = map[string]bool{
	"update":     true,
	"completion": true,
	"help":       true,
}

var rootCmd = &cobra.Command{
	Use:   "sce",
	Short: "CLI tool for managing SCE Development projects",
	Long:  "Command line tool to run any of the SCE projects. Works on Windows, Mac and Linux.",
	PersistentPreRun: func(cmd *cobra.Command, args []string) {
		if currentVersion == "" || currentVersion == "dev" {
			return
		}
		if skipVersionCheck[cmd.Name()] {
			return
		}
		// release tags are prefixed with a v (v0.5) but goreleaser strips it
		// from the injected version (0.5), so compare without the prefix.
		latest := strings.TrimPrefix(internal.LatestRelease(), "v")
		current := strings.TrimPrefix(currentVersion, "v")
		if latest == "" || latest == current {
			return
		}
		fmt.Fprintf(os.Stderr, "your cli is outdated (%s → %s). run `sce update` to get the latest version\n\n", current, latest)
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
