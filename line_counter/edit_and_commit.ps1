$currLocation = Get-Location
python .\line_counter.py
# Directory of the readme file.
Set-Location $Env:ReadmeDir
git add .
$randCommitMess = Get-Random
git commit -m "$randCommitMess"
git push origin main
Set-Location $currLocation