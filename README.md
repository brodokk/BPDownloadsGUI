# downloadui respositories version
This is the repository is a fork of Bob Pony's downloader UI. Its add the ability to have differents repository, local, distant or proxy. There is only one local repository for now.

## Installation

For the webUI you will just need to have a webserver like Apache or Nginx its just a javacript website. There is not much configuration available for now. But you can still modify the style of the webpage.

### Files formats

The file `repositories.json` is a json file contains the list of the repositories available:

```
{
    "Bob Pony": { // This is the name of the repository. `Local` or `local` defined if the repository is local or no
        "website": "https://downloadui.bobpony.com/", // The url of the website this is purely informative and not used at all for now
        "note": "If you need to enter a password, try bigcdn.", // A not who will be showed on the UI if there is.
        "README": "https://dl.bobpony.com/README.txt", // A README file of the repository who will be present in the folder where the file are if the repository is a local proxy
        "repository": "repositories/bob_pony.json" // The path of the repository, could be a local path on your system (relative or absolute) or an url
    },
    ...
}
```

The folder `repositories` contains all the file of each repository, the name is the same of the one declared in the `repositories` file in lowercase. All space in the name of the repository will be replaces by underscores by the webUI. This file is a json file. The file have a special format who is a 4 level nested dict. The first one will be the category of the file,
the second one will be the version or the type and the third on the option. The last level take a string as a value who is the uri of the file. This should be the download path.

## Mirroring

If you want to mirror a repository you can keep set downloaded path of the url in the json file in the folder `repositories` and add it to the `repositories.json` file. The webUI will automatically remove the domain from the `repositories` and replace it by the local path for you for being able to download it directly from the local server instead of the distant server.

For update the local mirrored file you can use the script `update_repositories.py` it will download the files in the same architecture as the mirrored server. You can set the path of the mirror folder directly in the script. If you change the value it will need to also be changed in the `listing.js` file. There is no configuration file for the moment. The update date is save each time in the file `version.txt` and will be display on the webUI.

### Installation

For using the script its a good idea to create a virtualenv first. There is some required package that you can find in the `requirements.txt` file.

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 update_repositories.py
```

## How can I contribute?
Fork the repository, edit what you need, and [submit a pull request!](https://github.com/TheBobPony/BPDownloadsGUI/pulls)
