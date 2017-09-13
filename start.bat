REM start ENV\Scripts\activate.bat  
cd py
REM
REM libs folder would contain following packages:
REM   - pyHook
REM   - SendKeys 
REM   - wx 
REM 
set PYTHONPATH=%PYTHONPATH%;.\libs
pythonw main.py 