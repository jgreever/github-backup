# Changelog

---

## [0.0.0]: (2022-03-13)

> Added

- [x] Initial version from [fork](https://github.com/abusesa/github-backup)

---

## [1.0.0]: (2022-03-14)

> Added

- [x] Added the ability to 'clone' or 'backup' a repository in config.json
- [x] Added the ability to read the settings from config.json
- [x] Added the ability to read the settings from the command line
- [x] Added a CHANGELOG.md file
- [x] Added the license (MIT) to the script.
- [x] Added a help message to the script and added a --help option.
- [x] Added a --version option

> Fixed

- [x] Refactored the mirror() function to backup() to handle clone/backup
- [x] Bumped the version to 1.0.0. (First Major Release)
- [x] Renamed the file LICENSE to LICENSE.md
- [x] Cleaned up the output of the script and added some phrasing

---

## [1.1.0]: (2022-03-16)

> Added

- [x] Added pip requirements into the requirements.txt file
- [x] Added the ability to check for user input first, then config.json, and
      if neither are provided, ask user for the values
- [x] Added check to see if the backup() function should clone or pull to update
      existing cloned directories (backup option handles this automatically)

> Fixed

- [x] Bumped the version to 1.1.0 (First Minor Release)
- [x] Refactored the mkdir() function to display a message if directory exists
      instead of raising an error
- [x] Changed command line options for providing values (simplified)
- [x] Updated README.md to reflect new command line options and fix language
      type for example code in it
- [x] Updated urllib3 to version 1.26.9

> Testing

- [ ] Add support for .env file to store GitHub credentials instead of using
      the config.json file (help prevent credentials from being stored in the
      source code)

---

> TODO

- [ ] Simplify the code
- [ ] Get user input before running the script on large repositories or when
      there are many repositories within a user account or organization
- [ ] Create unit tests for the script

---
