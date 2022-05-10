# fair-rec-kit-app

## NOTE: These instructions are for Windows command prompt

## How to run client & server

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

The easiest way is to install the packages (flask, flask-cors) with pip. Either click the run-api batch file or run in the terminal:

## run-api

If you're using Anaconda, you need to install the package python-dotenv. Then use the Anaconda prompt and run: (Note: make sure you're in the right environment, using activate <env-name>)

### `flask run`

You can also use the run-anaconda batch file from Discord.

In all cases, you might want to add a configuration (to the .bat file) in PyCharm.

###########

## How to test client

Execute the run-test batch file, or run in the terminal:

### npm run test

## How to test server

Execute the run-test batch file, or run in the terminal:

### python -m pytest