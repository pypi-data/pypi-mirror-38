[![GitHub stars](https://img.shields.io/github/stars/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/network)
[![Coverage Status](https://coveralls.io/repos/github/cartologic/cartoview/badge.svg?branch=master&service=github)](https://coveralls.io/github/cartologic/cartoview?branch=master&service=github)
[![Build Status](https://travis-ci.org/cartologic/cartoview.svg?branch=master)](https://travis-ci.org/cartologic/cartoview)
[![GitHub license](https://img.shields.io/github/license/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cartologic/cartoview.svg)](https://github.com/cartologic/cartoview/issues)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/cartologic/cartoview.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fcartologic%2Fcartoview)
<p align="center">
  <img src="https://cartologic.github.io/img/cartoview-logo.png"/>
</p>

---
## What is Cartoview?
  - CartoView is a GIS Web Mapping Application Market.
  - Cartoview extends the popular [GeoNode](http://geonode.org/) SDI to provide the ability to create, share, and visualize GIS Web Mapping Applications very easily and very quickly from the browser without programming.

***

## Docker Installation:
  - install [docker](https://docs.docker.com/v17.12/install/#server) and [docker-compose](https://docs.docker.com/compose/install/#prerequisites)
  - clone cartoview and navigate to cartoview folder
  - on linux based OS use this command `make run` to setup and start cartoview in docker for the first time 
  - on windows run the following commands to setup and start cartoview in docker for the first time:
      ```sh
      $ docker-compose up
      $ docker-compose exec cartoview python manage.py makemigrations
      $ docker-compose exec cartoview python manage.py migrate
      $ docker-compose exec cartoview python manage.py loaddata sample_admin.json
      $ docker-compose exec cartoview python manage.py loaddata default_oauth_apps.json
      $ docker-compose exec cartoview python manage.py loaddata app_stores.json
      $ docker-compose exec cartoview python manage.py loaddata initial_data.json
      ```
  - open your browser and type the following address `10.5.0.4`
  - default user credentials `admin/admin` for cartoview and `admin/geoserver` for geoserver
  - you need to configure oauth in geonode and geoserver to do this please use this [link](http://docs.geonode.org/en/master/tutorials/admin/geoserver_geonode_security/index.html)
  - you can stop containers with `make down` or `docker-compose down`
  - you can get logs for each service in `docker-compose.yml` unsing the following command:
      - `docker-compose logs --follow --tail=100 <service_name>`
  - start the containers with `docker-compose up -d` or `make up`
  - stop the containers with `docker-compose down` or `make down`

***

## How To Add Cartoview To Existing Geonode:
  - install cartoview with pip:
      - `pip install cartoview==1.8.5 --no-cache-dir`
      - open geonode `settings.py` and add the following lines at the end of the file:
          ```python
            from cartoview import settings as cartoview_settings
            INSTALLED_APPS += cartoview_settings.CARTOVIEW_INSTALLED_APPS
            ROOT_URLCONF = cartoview_settings.ROOT_URLCONF

            APPS_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "apps"))
            PENDING_APPS = os.path.join(PROJECT_ROOT, "pendingOperation.yml")
            APPS_MENU = False
            # NOTE: please comment the following line of you want to use geonode templates
            TEMPLATES[0][
                "DIRS"] = cartoview_settings.CARTOVIEW_TEMPLATE_DIRS + TEMPLATES[0]["DIRS"]
            TEMPLATES[0]["OPTIONS"][
                'context_processors'] += cartoview_settings.CARTOVIEW_CONTEXT_PROCESSORS

            STATICFILES_DIRS += cartoview_settings.CARTOVIEW_STATIC_DIRS

            from cartoview import app_manager
            from past.builtins import execfile
            app_manager_settings = os.path.join(
                os.path.dirname(app_manager.__file__), "settings.py")
            execfile(os.path.realpath(app_manager_settings))
            load_apps(APPS_DIR)
            INSTALLED_APPS += CARTOVIEW_APPS
            for settings_file in APPS_SETTINGS:
                try:
                    execfile(settings_file)
                except Exception as e:
                    pass
          ```
      - **restart your server**

***


## How to run tests
- You Can run tests with the following command 
    ```sh
      paver run_test
    ```
