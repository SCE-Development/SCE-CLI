package cmd

import (
	"os"
	"os/exec"
	"runtime"

	"github.com/spf13/cobra"
)

const (
	unixInstallURL    = "https://raw.githubusercontent.com/SCE-Development/SCE-CLI/master/go/install.sh"
	windowsInstallURL = "https://raw.githubusercontent.com/SCE-Development/SCE-CLI/master/go/install.ps1"
)

var updateCmd = &cobra.Command{
	Use:   "update",
	Short: "Update the SCE CLI to the latest version",
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		var c *exec.Cmd
		if runtime.GOOS == "windows" {
			c = exec.Command("powershell", "-Command",
				"Invoke-WebRequest -Uri \""+windowsInstallURL+"\" -UseBasicParsing | Invoke-Expression")
		} else {
			c = exec.Command("sh", "-c", "curl -sSL "+unixInstallURL+" | sh")
		}
		c.Stdout = os.Stdout
		c.Stderr = os.Stderr
		c.Stdin = os.Stdin
		if err := c.Run(); err != nil {
			os.Exit(1)
		}
	},
}

func init() {
	rootCmd.AddCommand(updateCmd)
}
