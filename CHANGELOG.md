# Changelog

---
## [0.0.0]: (2022-03-13):

### Added:

- [x] Initial version from [fork](https://github.com/abusesa/github-backup)
---

## [1.0.0]: (2022-03-14):

### Added:

- [x] Added the ability to 'clone' or 'backup' a repository in config.json.
- [x] Added the ability to read the settings from config.json.
- [x] Added the ability to read the settings from the command line.
- [x] Added a CHANGELOG.md file
- [x] Added the license (MIT) to the script.
- [x] Added a help message to the script and added a --help option.
- [x] Added a --version option.

### Fixed:

- [x] Refactored the mirror() function to backup() to handle clone/backup
- [x] Bumped the version to 1.0.0. (First Major Release)
- [x] Renamed the file LICENSE to LICENSE.md
- [x] Cleaned up the output of the script and added some phrasing.
---

# TODO:

- [ ] Simplify the code
- [ ] Get user input before running the script on large repositories or when
      there are many repositories within a user account or organization
- [ ] Add support for .env file to store GitHub credentials instead of using
      the config.json file (help prevent credentials from being stored in the
      source code)
- [ ] Create unit tests for the script
---