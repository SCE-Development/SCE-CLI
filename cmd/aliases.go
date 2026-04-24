package cmd

type RepoInfo struct {
	RepoName    string
	ConfigPaths []string
	MongoDBOnly bool
}

var aliasMap = map[string]RepoInfo{
	// Clark
	"clark": {RepoName: "Clark", ConfigPaths: []string{"src/config/config.json", "api/config/config.json"}},
	"dog":   {RepoName: "Clark", ConfigPaths: []string{"src/config/config.json", "api/config/config.json"}},
	"clrk":  {RepoName: "Clark", ConfigPaths: []string{"src/config/config.json", "api/config/config.json"}},
	"ck":    {RepoName: "Clark", ConfigPaths: []string{"src/config/config.json", "api/config/config.json"}},
	"c":     {RepoName: "Clark", ConfigPaths: []string{"src/config/config.json", "api/config/config.json"}},

	// MongoDB (uses Clark repo, only starts mongodb service)
	"mongo":   {RepoName: "Clark", MongoDBOnly: true},
	"db":      {RepoName: "Clark", MongoDBOnly: true},
	"mongodb": {RepoName: "Clark", MongoDBOnly: true},

	// Cleezy
	"cleezy": {RepoName: "cleezy"},
	"url":    {RepoName: "cleezy"},
	"z":      {RepoName: "cleezy"},

	// Quasar
	"quasar":  {RepoName: "Quasar", ConfigPaths: []string{"config/config.json"}},
	"q":       {RepoName: "Quasar", ConfigPaths: []string{"config/config.json"}},
	"idsmile": {RepoName: "Quasar", ConfigPaths: []string{"config/config.json"}},

	// SCE-discord-bot
	"sarah":           {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"sce-discord-bot": {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"discord-bot":     {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"discord":         {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"bot":             {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"s":               {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},
	"d":               {RepoName: "SCE-discord-bot", ConfigPaths: []string{"config.json"}},

	// SCEta
	"sceta":   {RepoName: "SCEta"},
	"transit": {RepoName: "SCEta"},
}

func resolveAlias(input string) (RepoInfo, bool) {
	info, ok := aliasMap[input]
	return info, ok
}

var repoNicknames = []string{
	"Clark: clark, dog, clrk, ck, c",
	"MongoDB (requires Clark linked): mongo, db, mongodb",
	"Quasar: quasar, q, idsmile",
	"SCE-discord-bot: sarah, sce-discord-bot, discord-bot, discord, bot, s, d",
	"cleezy: cleezy, url, z",
	"SCEta: sceta, transit",
}
