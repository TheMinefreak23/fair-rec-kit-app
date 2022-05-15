# fair-rec-kit-app

[![Pylint](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pylint.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pylint.yml)
[![Server Pytest](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pytest.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pytest.yml)
[![Client Vitest](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/vitest.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/vitest.yml)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/TheMinefreak23/fair-rec-kit-app?label=Release)

The fairreckit application is a web-based tool intended to aid in the performing and analysing of recommender system computations. It utilises a custom library called [fairreckitlib](https://github.com/TheMinefreak23/fairreckitlib) to perform its computations.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.  
© Copyright Utrecht University (Department of Information and Computing Sciences)

## How to run client & server

### NOTE: These instructions are for Windows command prompt

(Install Node.js first and run npm install)
Either click the run.bat file in the app directory, or run (in cmd):

### `run`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view the client in your browser.
Open [http://localhost:5000](http://localhost:5000) for the server.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## How to run client separately

Run in the terminal:

### `npm run dev`

## How to run server separately

The easiest way is to install the prequisite packages with pip. In the server directory, either click the run batch file or run in the terminal:

## run

If you're using Anaconda, you need to install the package python-dotenv. Then use the Anaconda prompt and run: (Note: make sure you're in the right environment, using activate <env-name>)

### `flask run`

In all cases, you might want to add a configuration (to the .bat file) in PyCharm.

###########

## How to test client

Execute the run-test batch file, or run in the terminal:

### npm run test

## How to test server

Execute the run-test batch file, or run in the terminal:

### python -m pytest

###########

### Server requirements

flask
flask-cors
requests
pandas
pillow
fairreckitlib
