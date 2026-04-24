package cmd

const (
	githubBaseHTTPURL = "https://github.com/SCE-Development/"
	githubBaseSSHURL  = "git@github.com:SCE-Development/"

	mongoDBContainer   = "sce-mongodb-dev"
	dockerComposeFile  = "docker-compose.dev.yml"

	bcryptHash = "$2a$10$HWbBiWRso1IUgqnuV6t1hO6lCBWO7KTC/E3G1MsFoXKH7/l/4FVK2"
)

var accessLevels = map[string]int{
	"admin":     3,
	"officer":   2,
	"member":    1,
	"nonmember": 0,
	"pending":   -1,
	"banned":    -2,
}

type lintTarget struct {
	Container    string
	EslintConfig string
}

var lintContainers = map[string][]lintTarget{
	"Clark": {
		{Container: "sce-frontend-dev", EslintConfig: "/frontend/.eslintrc.json"},
		{Container: "sce-main-endpoints-dev", EslintConfig: "/app/.eslintrc.json"},
		{Container: "sce-cloud-api-dev", EslintConfig: "/app/.eslintrc.json"},
	},
	"SCE-discord-bot": {
		{Container: "sarah", EslintConfig: "/sarah/.eslintrc.json"},
	},
}
