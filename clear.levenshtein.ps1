Get-ChildItem -Path 'levenshtein\' *.npy | foreach { Remove-Item -Path $_.FullName }
Get-ChildItem -Path 'build.orders\' *.npy | foreach { Remove-Item -Path $_.FullName }
