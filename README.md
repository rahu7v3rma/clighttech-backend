# C. Light Backend Service

## CLightTech CMS
CLightTech CMS is an application that manages CLightTech content.

## Launching the development environment

### Clone and install dependencies

```bash
$ git clone https://github.com/beehive-software/clighttech-backend.git
$ cd clighttech-backend
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Define environment variables

```bash
$ cp .env.dist .env
```

Update environment variables

### Setup a local database

SQLite is currently used as a database, so no action is needed to setup a new one.

### Run the service

```bash
$ python src/manage.py runserver
```

## Run tests

Install test dependencies
```bash
$ pip install -r test_requirements.txt
```

Make sure your .env file is set to use the `root` database user to run tests
```bash
$ python src/manage.py test
```

## Run pylint and code formatter

Install test dependencies
```bash
$ pip install -r test_requirements.txt
```

To run pylint execute
```bash
$ PYTHONPATH=$(pwd)/src:$PYTHONPATH DJANGO_SETTINGS_MODULE=clighttech_cms.settings pylint src
```

For blue in check mode
```bash
$ blue --check --diff src
```

If you want blue to auto-format your code use
```bash
$ blue src
````
