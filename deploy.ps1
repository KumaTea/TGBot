Set-Location 'C:\Program Files (x86)\Proxifier'
start Proxifier.exe
Start-Sleep -Seconds 1
Set-Location 'D:\Games\GitHub\TGBot'
gcloud app deploy -q
echo 'Manually exit Proxifier.'
