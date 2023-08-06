# lhclient

This utility connects to a deployment to

* Import scripts
* Import modules
* Import flow
* Create an Event Type from a CSV file

## Parameters

All actions expect the following parameters

* origin: eg. https://<yourdeployment>/api
* username
* password (prompted interactively if missing)

The last argument is either a file or a directory. If a directory is provided, the script will apply the action to all the files in the directory with suffixes .json, .py, .sh, .csv.

## Actions

### Import a script

Uploads either a python or a bash script. If a script with the same name already exists, its contents are overwritten with the new contents (that's how the backend works, nothing specific to this script).

#### Syntax

```
python lhclient.py import script --origin https://<deployment_host>/api --username <username> <the py/sh file or folder>
```

### Import a module

Imports a module from its JSON representation. If a module with the same ID already exists, it will fail with the `DuplicateModuleIdException` exception. 

#### Syntax

```
python lhclient.py import module --origin https://<deployment_host>/api --username <username> <the json file or folder>
```

### Import a flow

Imports a flow from its JSON representation. We are currently using the legacy API, so import will fail if a flow with the same name already exists.

#### Syntax

```
python lhclient.py import flow --origin https://<deployment_host>/api --username <username> <the json file or folder>
```

### Create Event Type from CSV

Uploads a CSV file, creates a new FileConnection (named as the file, without the extension) and creates a new EventType (named as the file, without the extension as well). If the CSV file already exists, its contents will NOT be overwritten on the server. If an EventType already has the name of the filename, the creation will fail (we can't have two EventTypes with the same name).

You can optionally use the --name argument to specify the name to use for both the FileConnection and the EventType

#### Syntax

```
python lhclient.py create event-type from-csv --origin https://<deployment_host>/api --username <username> <the csv file or folder>
```
