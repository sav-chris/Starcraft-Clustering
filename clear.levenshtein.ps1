Get-ChildItem -Path '\levenshtein\' *.npy | foreach { Remove-Item -Path $_.FullName }
