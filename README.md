## dermaval
![img](app/static/img/Geo-Krishi-logo.png)
Nepal has an immense diversity in terms of geographic, topographic and climatic conditions. However, intervention to increase crop productivity with pest/diseases control, randomly promote cash crop and over utilization of fertilizer are not sufficient in the context of changing climate, population growth and degradation of resources. More specifically and importantly, information such as bio-physical, climatic and agro economic information are useful but contextualize them to get the relevant information is harder to find.

dermaval provides an intelligent digital agriculture platform built to solve challenges faced by commercial and smallholder farmers. dermaval applies a data-driven system approach to translate knowledge into actionable, timely and context-specific advisories, covering all stages of the crop value chain.

## Mission
Our mission is to simplify and amplify the work of farmer/intermediator by adopting scientific methodology to provide location specific-timely actionable information to increase farm productivity and maximize profitability.

## Objective
1. Establish agricultural data infrastructure incorporating several data, products and tools useful for overall agricultural stages.
2. Remove technical and cultural barrier in the most simple and cost-effective way such that anyone can monitor real-time information from the farm.
3. Empower extension worker to provide better recommendation to the farmer through our district level agriculture advisory services center.

## Project Setup
1. Create virtual using pipenv and sync dependencies.
   If you do not have pipenv, you can use virtualenv to create environment as well.
   (pipenv preferred). Please scroll down the page to know installation for pipenv.
   First upgrade setuptools and pip,
   ```
   pipenv shell
   pip install --upgrade pip
   pip install --upgrade setuptools 
   ```
   If any issue regarding pip arises. 
   Remove the existing virtual environment and create a new virtual environment. 
   Activate the virtual environment and then follow the steps below.
   ```
   # To remove pipenv created virutal env.
   pipenv --rm
   
   # Install specific verion of python using pipenv.
   pipenv --python <PYTHON-VERSION>
   
   # Activate pipenv environment.
   pipenv shell
   
   # After activating virtual env follow below steps.
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python get-pip.py --force-reinstall
   rm get-pip.py
   pip install --upgrade pip
   pip install --upgrade setuptools
   ```
   For production,
   ```
   pipenv sync
   ```
   For development,
   ```
   pipenv sync --dev
   ```
   
2. Add .env file in the root folder.
   ```
   DEBUG= False
   SECRET_KEY= YOUR_SECRET_KEY
   ALLOWED_HOSTS = YOUR_ALLOWED_HOSTS
   ADMINS = Admin, admin@email.com
   MANAGERS = Admin, admin@email.com
   
   # Environment - development or production
   ENVIRONMENT = development
   
   # Database
   DEFAULT_DATABASE = DEFAULT_DATABASE_NAME
   DEFAULT_DATABASE_USER = DEFAULT_DATABASE_USER
   DEFAULT_DATABASE_PASSWORD = DEFAULT_DATABASE_PASSWORD
   DEFAULT_DATABASE_HOST = DEFAULT_DATABASE_HOST
   DEFAULT_DATABASE_PORT = DEFAULT_DATABASE_PORT
   DEFAULT_OPTIONS = DEFAULT_OPTIONS
   
   # ODK Database
   ODK_DATABASE = ODK_DATABASE
   ODK_DATABASE_USER = ODK_DATABASE_USER
   ODK_DATABASE_PASSWORD = ODK_DATABASE_PASSWORD
   ODK_DATABASE_HOST = ODK_DATABASE_HOST
   ODK_DATABASE_PORT = ODK_DATABASE_PORT
   ODK_OPTIONS = ODK_OPTIONS

   # EMAIL SETTINGS
   DEFAULT_FROM_EMAIL= dermaval <no-reply>
   EMAIL_USE_TLS= True
   EMAIL_HOST= smtp.gmail.com
   EMAIL_HOST_USER= EMAIL_HOST_USER
   EMAIL_HOST_PASSWORD= EMAIL_HOST_PASSWORD
   EMAIL_PORT=587
   
   PROTOCOL = http or https
   DOMAIN = www.dermaval.farm
   
   TASK_DEFAULT_QUEUE = dermaval
   
   ADBL_TEST_SERVER = False
   ADBL_USERNAME = ADBL_USERNAME # Provided by ADBL team.
   ADBL_PASSWORD = ADBL_PASSWORD # Provided by ADBL team.
   
   ADBL_SECRET_KEY_TEST = ADBL_SECRET_KEY_TEST # Provided by ADBL team.
   ADBL_SECRET_KEY = ADBL_SECRET_KEY # Provided by ADBL team.
   
   ADBL_FIREBASE_KEY = ADBL_FIREBASE_KEY # Provided by dermaval team.

   FCM_SERVER_KEY = FCM_SERVER_KEY
   GOOGLE_MAP_API_KEY = GOOGLE_MAP_API_KEY
   OPEN_WEATHER_MAP_APP_ID = OPEN_WEATHER_MAP_APP_ID
   
   SEND_ADD_FARM_NOTIFICATION = True
   SEND_ADD_CROP_NOTIFICATION = True
   ```
   Generate SECRET_KEY using python shell and replace YOUR_SECRET_KEY.
   ```
   from django.core.management.utils import get_random_secret_key
   get_random_secret_key()
   ```
   
3. Restore database.
   Restore database from latest backup.

4. To run server
   ```
   python manage.py runserver
   ```

## Internationalization and Localization

To localize the text, first message must be made then compiled.

```
python manage.py makemessages
python manage.py compilemessages
```

## Testing

Djanto test with no migrations is used for testing. For more info, visit https://pypi.org/project/django-test-without-migrations/. It simply creates all models without running migrations.

Also, custom runner has been created in order to handle models with managed false.
To run test

```
python manage.py test --nomigrations
python manage.py test app --nomigrations # Testing particular app
```
## Other Setup

##### Maintenance Mode
In maintenance mode, all the web pages and apis will be restricted. No operation can be done. 

To enable maintenance mode, set MAINTENANCE_MODE = True in settings.py

##### Pipenv Install
To install pipenv
```
sudo apt install pipenv
pip install pipenv
```
If your system's python version doesn't match the required python version, then install pyenv.
To install pyenv, please follow the steps provided in https://github.com/pyenv/pyenv or https://realpython.com/intro-to-pyenv/.
If any issue arises, please find solutions in https://github.com/pyenv/pyenv/wiki/Common-build-problems or any other sites.

##### Auto Generate Doc with Sphinx

View this link http://www.columbia.edu/~alan/django-jsonapi-training/sphinx.html, https://www.freecodecamp.org/news/sphinx-for-django-documentation-2454e924b3bc/, https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/ to know more about django sphinx doc.
To generate auto doc with sphinx, follow the following steps:
```
# Go to root of the project and create a folder named docs
mkdir docs
cd docs
# To activate environment
pipenv shell
sphinx-quickstart
# > Separate source and build directories (y/n) [n]: y
# > Project name: dermaval
# > Author name(s): Pathway Technologies
```

Open conf.py file in docs and paste the following below the #import os line.
```
import os
import sys
import django
sys.path.insert(0, os.path.abspath('../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Your_project_name.settings'
django.setup()
```

In conf.py, to autodoc add the following
```
extensions = [
   ...
   'sphinx.ext.autodoc'
]
```

```
sphinx-apidoc -o source/app .. --force
make html
make linkcheck

# To rebuild doc
make clean
make html
```

###### Optional

To view doc in read the doc theme.
For more info visit https://sphinx-rtd-theme.readthedocs.io/en/stable/.

```
pipenv install sphinx-rtd-theme

# Open conf.py file in docs and find extensions add the following
import sphinx_rtd_theme

extensions = [
    ...
    "sphinx_rtd_theme",
]

html_theme = "sphinx_rtd_theme"
```