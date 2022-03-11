@echo on
call C:\ProgramData\Anaconda3\Scripts\activate.bat
set FLASK_APP=flaskr 
set FLASK_ENV=development 
flask run
pause