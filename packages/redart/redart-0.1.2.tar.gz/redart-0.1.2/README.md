# redart

A CLI for publishing und fetching REDmine ARTifacts.

## How to use?

Initialising a project, using redart for managing artifacts. will place a .redart file in the root of your project folder. 

Also places as .redart-auth file in your root folder, which will contain your secret credentials, which will be used for authentication in later commands. Do not add this file to your Source Code Management Tool.

```
redart init --redmine https://redmine-base-url.com
```

Publishing a folder by compressing the build folder first, and then pushing it to redmine:

```
redart pub --compress <redmine-project>/<artifact-file-name>:<version-inside-redmine-project>
                      <local-path-to-folder>
```

Publishing a file to redmine:

```
redart pub <redmine-project>/<artifact-file-name>:<version-inside-redmine-project>
           <local-path-to-file>
```

Fetching an artifact from redmine, and extracting it; placing all files inside the destination folder:

```
redart fetch --extract <redmine-project>/<artifact-file-name>:<version-inside-redmine-project>
                       <local-path-to-folder>
```

Fetching an artifact from redmine, placing it inside the destination folder (optionaly renaming it)

```
redart fetch --target-name <new-filename> <redmine-project>/<artifact-file-name>:<version-inside-redmine-project>
                           <local-path-to-folder>
```


## Development

* pip3 install click python-redmine
* python3 redart <arguments>

## Deployment

First time:

```
pip install twine
``` 

Updating:

* Change version inside setup.py
* Then run:

```
python setup.py sdist
twine upload dist/*
```

## License

see [License](LICENSE).