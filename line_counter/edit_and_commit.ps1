$currLocation = Get-Location
python .\line_counter.py
# Directory of the readme file.
Set-Location $Env:ReadmeDir
git add .
$randCommitMess = Get-Random
git commit -m "$randCommitMess"
# Master or any name of the banch.
git push origin master
Set-Location $currLocation