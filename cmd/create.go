package cmd

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/spf13/cobra"
)

var createCmd = &cobra.Command{
	Use:   "create [level]",
	Short: "Create a test user for the SCE website",
	Long: `Create a test user for the SCE website.
Levels: admin (default), officer, member, nonmember, pending, banned.`,
	Args: cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		levelName := "admin"
		if len(args) > 0 {
			levelName = args[0]
		}

		level, ok := accessLevels[levelName]
		if !ok {
			fmt.Fprintf(os.Stderr, "unknown access level: %s\n", levelName)
			keys := make([]string, 0, len(accessLevels))
			for k := range accessLevels {
				keys = append(keys, k)
			}
			fmt.Fprintf(os.Stderr, "valid options: %s\n", strings.Join(keys, ", "))
			os.Exit(1)
		}

		suffix := randomHex(2)
		email := fmt.Sprintf("test_%s@one.sce", suffix)

		mongoScript := fmt.Sprintf(`use sce_core
db.User.insertOne({
    emailVerified: true,
    accessLevel: %d,
    pagesPrinted: 0,
    password: '%s',
    firstName: 'Development',
    lastName: 'Account',
    email: '%s',
})`, level, bcryptHash, email)

		dockerCmd := exec.Command("docker", "exec", "-i", mongoDBContainer, "mongosh", "--shell", "--norc", "--quiet")
		dockerCmd.Stdin = strings.NewReader(mongoScript)
		dockerCmd.Stdout = os.Stdout
		dockerCmd.Stderr = os.Stderr
		if err := dockerCmd.Run(); err != nil {
			fmt.Fprintf(os.Stderr, "error creating user: %v\n", err)
			os.Exit(1)
		}

		fmt.Printf("created %s user for the SCE website with:\n", levelName)
		fmt.Printf("email:    %s\n", email)
		fmt.Println("password: sce")
	},
}

func randomHex(n int) string {
	bytes := make([]byte, n)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

func init() {
	rootCmd.AddCommand(createCmd)
}
