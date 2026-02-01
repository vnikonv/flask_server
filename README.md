![](app/static/favicon.ico)
## A home-use Flask app for file transfer between multiple devices.
### Install the [dependencies](requirements.txt) and execute the [entry point](run.py).
```bash
python run.py
```
### Features:
* Flask application to upload and download files by client devices of a local access network.
* No JavaScript is used, no cache is saved on client devices except for cookies.
* It is possible to upload, download, and delete multiple files at once.
* When folders are uploaded with either webkit/folder or archive mode, the file structure is preserved.
* When archives are uploaded in the archive upload mode, the files are extracted to the server.
### Short Todo:
Implement archive upload/download modes; multiple file and folder downloads/deletes/mutations. Write a class for simplifying upload history management. Figure out ways of increasing file transfer speed on local network.
### Long Todo:
Introduce a feature to take a uniform action (upload/download/delete) on all files that follow a specified filename patter. Connect a database to Flask app for an optional account feature that includes a personal, user-specific, storage (+ uploads history will be saved in the account DB). Introduce optional Dockerization. Connect the Flask app to a configured Nginx on a VPS for fun.
