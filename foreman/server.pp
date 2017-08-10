
# hammer config file
file { "/etc/hammer/cli_config.yml":
	ensure	=> present,
	source	=> "/home/server/git/foreman-poc/hammer/cli_config.yml",

}

exec { "hammer execution":
	command	=> "/home/server/git/foreman-poc/hammer/hammer.sh",
	path	=> "/usr/local/bin/",

#	user	=> "server",
	environment	=> ["HOME=/home/server"],
}















