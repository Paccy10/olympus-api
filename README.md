[![Build Status](https://travis-ci.com/Paccy10/olympus-api.svg?branch=master)](https://travis-ci.com/Paccy10/olympus-api) ![Code Climate coverage](https://img.shields.io/codeclimate/coverage/Paccy10/olympus-api) ![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/Paccy10/olympus-api) ![GitHub language count](https://img.shields.io/github/languages/count/Paccy10/olympus-api) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Paccy10/olympus-api/flask)

# Olympus App API

A vacation rental online marketplace app API.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

```
- Python 3.7.3
- pip
- pipenv
```

## Installation and setup

- Download Python

```
https://www.python.org/downloads/
```

- Install pipenv

```
pip install pipenv
```

- Clone the repository

```
git clone https://github.com/Paccy10/olympus-api.git
```

- Create the virtual environment

```
pipenv shell
```

- Install dependencies

```
pipenv install
```

- Make a copy of the .env.sample file and rename it to .env and update the variables accordingly

- Apply migrations

```
flask db upgrade
```

- Should you make changes to the database models, run migrations as follows

  - Migrate database

  ```
  flask db migrate
  ```

  - Upgrade to the new structure

  ```
  flask db upgrade
  ```

## Running

- Running app

```
flask run
```
