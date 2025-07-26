![](app/static/favicon.ico)
## A home-use Flask app for file transfer between multiple devices.
### Install the [dependencies](requirements.txt) and execute the [entry point](run.py).
### Features:
* Flask application to upload and download files by client devices of a local access network.
* No JavaScript is used, no cache is saved on client devices; only cookies.
* It is possible to upload, download and delete multiple files at once.
* When folders are uploaded with either webkit/folder or archive mode, the file structure is preserved.
* When archives are uploaded in the archive upload mode, the files are extracted on the server.
### Short Todo:
Write a class for cookies. Implement archiving files in OOP. Implement archive upload/download modes; multiple file and folder downloads/deletes. Draw own icon (icicle).
### Long Todo:
Make home page entertaining with arts. Introduce a feature to take a uniform action (upload/download/delete) on all files that follow a specified filename patter. Connect a database to Flask app for an optional account feature that includes a personal, user-specific, storage. Introduce optional Dockerization. Connect the Flask app to a configured Nginx on a VPS for production use.