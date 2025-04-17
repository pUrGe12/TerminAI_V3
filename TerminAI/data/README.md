The `commands.yaml` file contains all the necessary information including the descriptions and the flags for every linux command. This will be further expanded (or a new file created) for windows and mac.

## Structure

```yaml
Command: ls
	desc: list directory contents
	flags: List information about the FILEs (the current directory by default).  Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
		flag_1: -a
			desc: do not ignore entries starting with .
		flag_2: --author
			desc: with -l, print the author of each file
```

This is scraped using the man pages of each file. 