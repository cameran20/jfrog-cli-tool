import dotenv
import os
import requests
import typer
import re

from enum import Enum
from requests.auth import HTTPBasicAuth
from typing import List

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app = typer.Typer()

jfrog_host = os.environ.get("HOST")

class RClass(str, Enum):
    local = "local"
    remote = "remote"
    virtual = "virtual"

class PackageType(str, Enum):
    all=''
    alpine='alpine'
    bower='bower'
    cargo='cargo'
    chef='chef'
    cocoapods='cocoapods'
    composer='composer'
    conan='conan'
    cran='cran'
    debian='debian'
    docker='docker'
    gems='gems'
    generic='generic'
    gitlfs='gitlfs'
    go='go'
    gradle='gradle'
    helm='helm'
    ivy='ivy'
    maven='maven'
    npm='npm'
    nuget='nuget'
    opkg='opkg'
    pub='pub'
    puppet='puppet'
    pypi='pypi'
    rpm='rpm'
    sbt='sbt'
    swift='swift'
    terraform='terraform'
    vagrant='vagrant'
    yum='yum'

class RepositoryType(str, Enum):
    all = ""
    local = "local"
    remote = "remote"
    virtual = "virtual"
    distribution = "distribution"

def get_headers(content_type="application/x-www-form-urlencoded"):
    headers = {
        "X-JFrog-Art-Api": os.environ.get("X-JFrog-Art-Api"),   
        "Content-type": f"{content_type}"}
    return headers

@app.command()
def login(username: str=typer.Option(..., prompt=True, help="username used to login"),
    password: str=typer.Option(..., prompt=True, help="password used to login")):
    response = requests.get(f'{jfrog_host}api/security/apiKey', auth=HTTPBasicAuth(username, password))
    if (response.status_code==200):
        try:
            response_api_key = response.json()['apiKey']
            print(response.json())
            print("Login Sucessful")
            os.environ["X-JFrog-Art-Api"] = response_api_key
            dotenv.set_key(dotenv_file, "X-JFrog-Art-Api", os.environ["X-JFrog-Art-Api"])
        except Exception as ex:
            print(f"Could not get apiKey from response: {response.json()}")
    else:
        print(f"status code: {response.status_code}")
        print(response.json())

@app.command()
def ping():
    """
    Get a simple status response about the state of Artifactory
    """
    response = requests.get(f'{jfrog_host}api/system/ping', headers=get_headers())
    print(f'{response.status_code}: {response.reason}')

@app.command()
def version():
    """
    Retrieve information about the current Artifactory version
    """
    response = requests.get(f'{jfrog_host}api/system/version', headers=get_headers())
    if (response.status_code==200):
        try:
            print(response.json()['version'])
        except Exception as ex:
            print(f"Could not get version from response: {response.json}")
    else:
        print(f"status code: {response.status_code}")
        print(response.json())

@app.command()
def create_user(username: str=typer.Option(..., prompt=True, help="username of user to be created"),
    email: str=typer.Option("", help="email of user to be created"),
    password: str=typer.Option("", help="password of user to be created")):
    """
    Creates a new user in Artifactory or replaces an existing user
    """ 
    email=email if email else typer.prompt("email")
    while (not validate_email(email)):
        email = typer.prompt("email")
    password=password if password else typer.prompt("password")
    while (not validate_password(password)):
        password = typer.prompt("password")
    data={
    "name": username,
    "email": email,
    "password": password
    }
    response = requests.put(f'{jfrog_host}api/security/users/{username}', headers=get_headers("application/json"), json=data)
    if (response.status_code==201):
        print(f"User {username} was sucessfully created")
    else:
        print(f"There was an error creating the user: {response.status_code} {response.reason}")

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

def validate_password(password):
    """ 
    Password must include:
    At least 1 upper case letter 
    At least 1 lower case letter
    At least 1 digits
    At least 1 special character
    At least 8 characters long
    """
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.fullmatch(regex, password)

@app.command()
def delete_user(username: str=typer.Option(..., prompt=True, confirmation_prompt=False, help="username of user to be deleted")):
    """
    Removes an Artifactory user.
    """
    response = requests.delete(f'{jfrog_host}api/security/users/{username}', headers=get_headers())
    if (response.status_code==200):
        print(f"User {username} was sucessfully deleted")
    else:
        print(f"There was an error deleting the user: {response.status_code} {response.reason}")

@app.command()
def get_storage_info():
    """
    Returns storage summary information regarding binaries, file store and repositories.
    """
    response = requests.get(f'{jfrog_host}api/storageinfo', headers=get_headers())
    if (response.status_code==200):
        print(response.json())
    else:
        print(f"There was an error fetching the storage info: {response.status_code} {response.reason}")

@app.command()
def create_repo(repo_key: str=typer.Option(..., prompt=True, help="key for repository to be created"),
    rclass: RClass=typer.Option(RClass.local, prompt=True, case_sensitive=False, help="repository type to be created"),
    package_type: PackageType=typer.Option(PackageType.generic, case_sensitive=False, help="package type of repository to be created"),
    externalDependenciesEnabled: bool=typer.Option(False, help="Applies to Docker repositories only"),
    remote_url: str=typer.Option("", help="url of remote repository to be created")):
    """
    Creates a new repository in Artifactory with the provided configuration. Supported by local, remote and virtual repositories. 
    """
    data=fill_repo_json(repo_key, rclass, package_type, externalDependenciesEnabled, remote_url)
    response = requests.put(f'{jfrog_host}api/repositories/{repo_key}', headers=get_headers("application/json"), json=data)
    if (response.status_code==200):
        print(f"Repo {repo_key} was sucessfully created")
    else:
        print(f"There was an error creating the repository: {response.status_code} {response.reason}")

@app.command()
def update_repo(repo_key: str=typer.Option(..., prompt=True, help="key for repository to be created"),
    rclass: RClass=typer.Option(RClass.local, prompt=True, case_sensitive=False, help="repository type to be created"),
    package_type: PackageType=typer.Option(PackageType.generic, case_sensitive=False, help="package type of repository to be created"),
    externalDependenciesEnabled: bool=typer.Option(False, help="Applies to Docker repositories only"),
    remote_url: str=typer.Option("", help="url of remote repository to be created")):
    """
    Updates an exiting repository configuration in Artifactory with the provided configuration elements. Supported by local, remote and virtual repositories.
    """
    data=fill_repo_json(repo_key, rclass, package_type, externalDependenciesEnabled, remote_url)
    response = requests.post(f'{jfrog_host}api/repositories/{repo_key}', headers=get_headers("application/json"), json=data)
    if (response.status_code==200):
        print(f"Repo {repo_key} was sucessfully updated")
    else:
        print(f"There was an error updating the repository: {response.status_code} {response.reason}")

@app.command()
def list_repos(repository_type: RepositoryType=typer.Option(RepositoryType.all, case_sensitive=False, help="type of repo to fetch"),
    package_type: RepositoryType=typer.Option(RepositoryType.all, case_sensitive=False, help="repo package type to fetch")):
    """
    Returns storage summary information regarding binaries, file store and repositories.
    """
    response = requests.get(f'{jfrog_host}api/repositories?type={repository_type}&packageType={package_type}', headers=get_headers())
    if (response.status_code==200):
        print(response.json())
    else:
        print(f"There was an error fetching the repositories: {response.status_code} {response.reason}")

def fill_repo_json(repo_key, rclass, package_type, externalDependenciesEnabled, remote_url):
    data={}
    if rclass=="local":
        data={
            "key": f"{repo_key}",
            "rclass" : f"{rclass}"
        }
    elif rclass=="remote":
        remote_url=remote_url if remote_url else typer.prompt("url")
        externalDependenciesEnabled=externalDependenciesEnabled if externalDependenciesEnabled else typer.confirm("externalDependenciesEnabled")
        data={
            "key": f"{repo_key}",
            "rclass" : f"{rclass}",
            "url": f"{remote_url}",
            "externalDependenciesEnabled": f"{externalDependenciesEnabled}"
        }
    elif rclass=="virtual":
        package_type = None
        while (package_type == None):
            input = typer.prompt("package type")
            try:
                if (input != ""):
                    package_type = PackageType(input)
            except:
                print("Please enter a valid package type. (maven|gradle|ivy|sbt|helm|rpm|nuget|cran|gems|npm|bower|pypi|docker|p2|yum|go|chef|puppet|generic)")
        externalDependenciesEnabled=externalDependenciesEnabled if externalDependenciesEnabled else typer.confirm("externalDependenciesEnabled")
        data={
            "key": f"{repo_key}",
            "rclass" : f"{rclass}",
            "packageType": f"{package_type}",
            "externalDependenciesEnabled": f"{externalDependenciesEnabled}"
        }
    return data

if __name__ == "__main__":
    app()