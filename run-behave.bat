@echo on
echo Run scenario test

@echo off
set /p TestPath=Test file path (ex: features\steps\tutorial.feature):

behave -i "%TestPath%"
pause