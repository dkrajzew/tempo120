erase build
erase dist
erase tempo120

pyinstaller --onefile tempo120.py
mkdir dist\muzak
xcopy muzak dist\muzak /I /E /K
mkdir dist\gfx
xcopy gfx dist\gfx /I /E /K
mkdir dist\scores
xcopy scores dist\scores /I /E /K
xcopy LICENSE dist\ /I /K
xcopy README.md dist /I /K
rename dist tempo120

python -m build
rem python -m twine upload --repository pypi dist/*
python -m twine upload --repository testpypi dist/*
