@echo off
echo Running PDF extraction on all files in input folder...

for %%f in ("../input/*.pdf") do (
    echo Processing %%~nxf ...
    python main.py "../input/%%~nxf" -o "../output/%%~nf.txt"
)

echo All done!
pause
