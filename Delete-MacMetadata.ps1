# Define the target directory
$TargetDirectory = " D:\Files" # Replace with your directory path

# Check if the directory exists
if (-Not (Test-Path -Path $TargetDirectory)) {
    Write-Host "The specified directory does not exist: $TargetDirectory" -ForegroundColor Red
    exit
}

# Find and delete ._ files
Get-ChildItem -Path $TargetDirectory -Recurse -File -Include "._*", ".DS_Store" |
    ForEach-Object {
        try {
            # Delete the file
            Remove-Item -Path $_.FullName -Force
            Write-Host "Deleted: $($_.FullName)" -ForegroundColor Green
        } catch {
            Write-Host "Failed to delete: $($_.FullName). Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }

Write-Host "Cleanup completed." -ForegroundColor Cyan
