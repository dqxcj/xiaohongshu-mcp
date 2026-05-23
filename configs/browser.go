package configs

var sidecarURL = "http://127.0.0.1:18061"

func SetSidecarURL(u string) {
	sidecarURL = u
}

func GetSidecarURL() string {
	return sidecarURL
}
