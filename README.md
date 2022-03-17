# GitHub backup script

This directory contains a script, `backup.py`, for backing up GitHub repositories.

The script requires a GitHub token and a destination directory. It then uses the token to populate the destination directory with clones of all the repositories the token can access.

Repeated runs only update the already existing backups and add new repositories, if any.

## Installation

Install the required Python dependencies using `pip3`:

```bash
pip3 install -r requirements.txt
```

## Configuring

### Create a token

For authorization, you need to create a new personal GitHub token. You can do this from the GitHub settings, under the **Personal Access Tokens** tab.

![Step 1](images/new-token-1.png)

When you click the **Generate new token** button you enter the token creation screen. Here you should give the token a descriptive name and choose its *scopes*, which basically determine what the token is allowed to do.

![Step 2](images/new-token-2.png)

To back up public and private repositories you need to select only the **repo** scope. If you have no need for private repositories just choose the **public_repo** scope.

![Step 3](images/new-token-3.png)

After clicking the **Generate token** button you're presented with the generated token. Remember to store it now, as GitHub won't show it to you anymore!

In the next example let's assume your token is `6b86190dd45c57c1a1b039a5a54d892e019102f7` as in the above image.

### Create a configuration file

To run the script you need a JSON configuration file. For an example see the included file `config.json.example`.

As an example let's create a file, `config.json`. This file should contain the token we just created and the destination directory where we want to back up the repositories:

```json
{
    "token": "GITHUB_TOKEN_HERE",
    "directory": "~/backups/github.com",
    "type": "backup",
    "owners": []
}
```

#### Choose users and organizations to back up

By default, all repositories you have read access to are backed up. To choose which users' and organizations' repos are backed up, add `owners` to `config.json`:

```json
{
    "token": "GITHUB_TOKEN_HERE",
    "directory": "~/backups/github.com",
    "type": "backup",
    "owners": ["username", "another-username"]
}
```

## Running

After preparing the token and the configuration file you now can run the script:

```bash
./backup.py
```

If you want to manually pass the options instead of using the config.json file, you can use the following command:

```bash
./backup.py --config=<CONFIG> --token=<TOKEN> --directory=<DIRECTORY> --owners=<OWNER,OWNER> --type={backup,clone}
```

For help, type:

```bash
./backup.py --help
```
