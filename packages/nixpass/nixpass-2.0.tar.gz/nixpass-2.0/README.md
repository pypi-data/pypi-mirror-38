Hello fellow person,

nixpass was created to help organize, generate, and store passwords. It allows password workspaces to be encrypted with AES-256 and decrypted with a single password, giving access to all entered credentials within that workspace.

Work flow was designed to create organized spaces called password files. The designed workflow is as follows:

Home


which has entries

Google

 -username
 -password

Reddit

 -username
 -password



These entries are stored in JSON format, encrypted with AES-256, encoded with base64 and written to a file.

To open a workspace, enter the name of the Workspace and authenticate. This will decode and decrypt the JSON in the file that has all the entries.



To view the username/password of a password file entry, enter the entry name:


Reddit


This will provide the username/password


foo bar





---Installation---

-Via Pip-

1.Create virtual environment, was developed with python 3.6 modules

2.pip install nixpass

3.run nixpass  from virtual environment



-Via Standalone-

1. Download stand-alone-nixpass.py from github - https://github.com/gatovato/nixpass

2. Rename to whatever

3. Create virtual environment - developed using standard python 3.6 modules and pycrypto 2.6.1

4. Include path to your virtual environment in the !# at the top




Hope this helps in your password management/storage needs

-Shane Guymon, aka. gatovato 😸  11/1/2018
