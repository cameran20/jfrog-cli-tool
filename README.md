# `jfrog-cli`

This project waS created to allow users to use a command line interface to manage an Artifactory SaaS instance via its API

**Set Up**:

* To use this cli begin by downloading the files in the repository
* This project has a few required python packages which can be downloaded using the following command 
    
    ```pip install -r requirements.txt```
* For the application a .env file must be created with the following fields
    ```
    HOST=https://cameran.jfrog.io/artifactory/
    X-JFrog-Art-Api=
    ```
* Finally login in to the account to populate the api key in the .env using this commmand
    
    ```python jfrog.py login --username=admin --password=Password1!```

**Usage**:

```console
$ python jfrog.py [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create-repo`: Creates a new repository in Artifactory with...
* `create-user`: Creates a new user in Artifactory or replaces...
* `delete-user`: Removes an Artifactory user.
* `get-storage-info`: Returns storage summary information regarding...
* `list-repos`: Returns storage summary information regarding...
* `login`
* `ping`: Get a simple status response about the state...
* `update-repo`: Updates an exiting repository configuration...
* `version`: Retrieve information about the current...

## `python jfrog.py login`

**Usage**:

```console
$ python jfrog.py login [OPTIONS]
```

**Options**:

* `--username TEXT`: username used to login  [required]
* `--password TEXT`: password used to login  [required]
* `--help`: Show this message and exit.

**Notes**:

* The username `admin` and password `Password1!` were used to sign in for this account

## `python jfrog.py create-user`

Creates a new user in Artifactory or replaces an existing user

**Usage**:

```console
$ python jfrog.py create-user [OPTIONS]
```

**Options**:

* `--username TEXT`: username of user to be created  [required]
* `--email TEXT`: email of user to be created  [default: ]
* `--password TEXT`: password of user to be created  [default: ]
* `--help`: Show this message and exit.

**Notes**:

* This command will continue to prompt the user to input the email until a valid email is entered
* This command will continue to prompt the user to input a password until it has proper security formatting
        
        Password must include:
        At least 1 upper case letter 
        At least 1 lower case letter
        At least 1 digits
        At least 1 special character
        At least 8 characters long

## `python jfrog.py delete-user`

Removes an Artifactory user.

**Usage**:

```console
$ python jfrog.py delete-user [OPTIONS]
```

**Options**:

* `--username TEXT`: username of user to be deleted  [required]
* `--help`: Show this message and exit.

## `python jfrog.py get-storage-info`

Returns storage summary information regarding binaries, file store and repositories.

**Usage**:

```console
$ python jfrog.py get-storage-info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `python jfrog.py list-repos`

Returns storage summary information regarding binaries, file store and repositories.

**Usage**:

```console
$ python jfrog.py list-repos [OPTIONS]
```

**Options**:

* `--repository-type [|local|remote|virtual|distribution]`: type of repo to fetch  [default: ]
* `--package-type [|local|remote|virtual|distribution]`: repo package type to fetch  [default: ]
* `--help`: Show this message and exit.

**Notes**:

* The default values for `respository-type` and `package-type` are set to a blank value which will get off that type

## `python jfrog.py create-repo`

Creates a new repository in Artifactory with the provided configuration. Supported by local, remote and virtual repositories. 

**Usage**:

```console
$ python jfrog.py create-repo [OPTIONS]
```

**Options**:

* `--repo-key TEXT`: key for repository to be created  [required]
* `--rclass [local|remote|virtual]`: repository type to be created  [default: local]
* `--package-type [|alpine|bower|cargo|chef|cocoapods|composer|conan|cran|debian|docker|gems|generic|gitlfs|go|gradle|helm|ivy|maven|npm|nuget|opkg|pub|puppet|pypi|rpm|sbt|swift|terraform|vagrant|yum]`: package type of repository to be created  [default: generic]
* `--externaldependenciesenabled / --no-externaldependenciesenabled`: Applies to Docker repositories only  [default: False]
* `--remote-url TEXT`: url of remote repository to be created  [default: ]
* `--help`: Show this message and exit.

## `python jfrog.py update-repo`

Updates an exiting repository configuration in Artifactory with the provided configuration elements. Supported by local, remote and virtual repositories.

**Usage**:

```console
$ python jfrog.py update-repo [OPTIONS]
```

**Options**:

* `--repo-key TEXT`: key for repository to be created  [required]
* `--rclass [local|remote|virtual]`: repository type to be created  [default: local]
* `--package-type [|alpine|bower|cargo|chef|cocoapods|composer|conan|cran|debian|docker|gems|generic|gitlfs|go|gradle|helm|ivy|maven|npm|nuget|opkg|pub|puppet|pypi|rpm|sbt|swift|terraform|vagrant|yum]`: package type of repository to be created  [default: generic]
* `--externaldependenciesenabled / --no-externaldependenciesenabled`: Applies to Docker repositories only  [default: False]
* `--remote-url TEXT`: url of remote repository to be created  [default: ]
* `--help`: Show this message and exit.

## `python jfrog.py ping`

Get a simple status response about the state of Artifactory

**Usage**:

```console
$ python jfrog.py ping [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `python jfrog.py version`

Retrieve information about the current Artifactory version

**Usage**:

```console
$ python jfrog.py version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
