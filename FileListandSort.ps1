Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
Get-ChildItem -Path "D:\Files" -Recurse |
    Where-Object { -not $_.PSIsContainer -and $_.Length -lt 204800 } |
    Sort-Object Length |
    Select-Object FullName, Length |
    Out-File "D:\Files\sorted_files.txt"