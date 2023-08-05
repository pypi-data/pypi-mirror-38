# flask-tunnel

Using this extension, your flask application will create an SSH tunnel and destroy it with each new request made 
to a remote resource. Personally, I use an app factory that configures a tunnel if I am using Flask
in a specific development mode. I find it useful to run/debug on my flask application locally without
having to leave a tunnel open. This makes your app more portable and is helpful if your database is too large
to be considered portal

## Example

This example assumes you're trying to access a postgresql server. Initialize a `Tunnel` object.
``` python
if app.config['DEVELOPMENT']:
    tunn = Tunnel(app, ssh_host='example.com', \
    ssh_username='user', ssh_pkey='~/.ssh/id_rsa', \
    remote_bind_address=('127.0.0.1', 5432), local_bind_address=('localhost', 5432))
```

Use it elsewhere in your code:
`tunn.connect.start()` before accessing your database or other resource,
and that's it. The tunnel will close automatically during `app.teardown_appcontext`.
Add a check to make sure you're running in development mode if that's when you intend to use it using
something like `if app.config['PRODUCTION'] is None`.

## TODO
* Write tests
* Add documentation (Sphinx?)
* Add link to dev version
* Add support for 2.6/2.7

## Done
* License Added
* Using factory-pattern/supports multiple apps
* Add to pypi

## Other Documentation
[tldr mit](https://tldrlegal.com/license/mit-license#fulltext)

[pypi sshtunnel](https://pypi.python.org/pypi/sshtunnel)

[packaging tutorial](https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi)

