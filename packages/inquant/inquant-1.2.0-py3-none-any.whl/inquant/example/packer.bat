@echo off

echo ����Anaconda��Ŀ¼��(��C:\ProgramData\Anaconda3��: 
set /p anacondapath=%~1

echo ����python�ļ�·����(��C:\inquant\example\MyStrategy.py��: 
set /p pythonfile= %~2

echo ��ʼ���
pyinstaller -F --add-data=%anacondapath%\Lib\site-packages\inquant\libs\InQuant.OpenApi.dll;. --add-data=%anacondapath%\Lib\site-packages\inquant\libs\Newtonsoft.Json.dll;. --add-data=%anacondapath%\Lib\site-packages\Python.Runtime.dll;. %pythonfile%

echo ����json�ļ�
xcopy %pythonfile%\..\*.json  dist /dy

pause