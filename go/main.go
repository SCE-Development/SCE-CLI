package main

import "github.com/SCE-Development/SCE-CLI/cmd"

var version = "dev"

func main() {
	cmd.SetVersion(version)
	cmd.Execute()
}
