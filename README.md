# FairRecKit App
[![Pylint](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pylint.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pylint.yml)
[![PEP257](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pydoctest.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pydoctest.yml)
[![Server Pytest](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pytest.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/pytest.yml)
[![Client Vitest](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/vitest.yml/badge.svg)](https://github.com/TheMinefreak23/fair-rec-kit-app/actions/workflows/vitest.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/TheMinefreak23/fair-rec-kit-app?label=Release)

The fairreckit application is a web-based tool intended to aid in the performing and analysing of recommender system computations. It utilises a custom library called [fairreckitlib](https://github.com/TheMinefreak23/fairreckitlib) to perform its computations.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course, commissioned by dr. Christine Bauer. 

Lennard Chung           Aleksej Cornelissen
Isabelle van Driessel   Diede van der Hoorn
Yme de Jong             Lan Le
Sanaz Najiyan Tabriz    Roderick Spaans
Casper Thijsen          Robert Verbeeten
Vos Wesseling           Fern Wieland           

© Copyright Utrecht University (Department of Information and Computing Sciences)

## Running the client & server

### NOTE: These instructions are for Windows command prompt

- Install Node.js first and run `npm install`
- Either click the run.bat file in the app directory, or run `run` in cmd.

This runs the app in the development mode.  
Open [http://localhost:3000](http://localhost:3000) to view the client in your browser.  
Open [http://localhost:5000](http://localhost:5000) for the server.

The page will reload when you make changes.  
You can also see any lint errors in the console.

## Running the client separately

- Use `npm i` first to install the needed packages.
- In the client folder, run `npm run dev` the terminal.  

## Running the server separately

- Install the prerequisite packages with pip (e.g. by running `pip install -r requirements.txt` in the server directory).  
- In the server directory, either execute run.bat or enter `run` in the terminal.

If you're using Anaconda, you need to install the package python-dotenv. Then use the Anaconda prompt and run the `flask run` command.  
(Note: make sure you're in the right environment, using `activate <env-name>`)

In all cases, you might want to add a configuration (pointing to the .bat file) in PyCharm.

## Testing the client

- Execute the run-test.bat file in the client folder, or run `npm run test` in the terminal.

## Testing the server

- Execute the run-test batch file in the server directory, or run `python -m pytest` in the terminal.
