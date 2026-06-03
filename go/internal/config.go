package internal

const (
	GithubBaseHTTPURL = "https://github.com/SCE-Development/"
	GithubBaseSSHURL  = "git@github.com:SCE-Development/"

	MongoDBContainer  = "sce-mongodb-dev"
	DockerComposeFile = "docker-compose.dev.yml"

	BcryptHash = "$2a$10$HWbBiWRso1IUgqnuV6t1hO6lCBWO7KTC/E3G1MsFoXKH7/l/4FVK2"
)

var AccessLevels = map[string]int{
	"admin":     3,
	"officer":   2,
	"member":    1,
	"nonmember": 0,
	"pending":   -1,
	"banned":    -2,
}

type LintTarget struct {
	Container    string
	EslintConfig string
}

var LintContainers = map[string][]LintTarget{
	"Clark": {
		{Container: "sce-frontend-dev", EslintConfig: "/frontend/.eslintrc.json"},
		{Container: "sce-main-endpoints-dev", EslintConfig: "/app/.eslintrc.json"},
		{Container: "sce-cloud-api-dev", EslintConfig: "/app/.eslintrc.json"},
	},
	"SCE-discord-bot": {
		{Container: "sarah", EslintConfig: "/sarah/.eslintrc.json"},
	},
}
