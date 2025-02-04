# Set the input and output file paths
$inputFile = "BebrData.js"
$outputFile1 = "BebrP1.js"
$outputFile2 = "BebrP2.js"

# Read the file content
$lines = Get-Content $inputFile -Encoding UTF8

# Initialize flags
$foundPolygon = $false

# Open the output files
$out1 = New-Object System.IO.StreamWriter($outputFile1, $false, [System.Text.Encoding]::UTF8)
$out2 = New-Object System.IO.StreamWriter($outputFile2, $false, [System.Text.Encoding]::UTF8)

# Process the lines
foreach ($line in $lines) {
    if (-not $foundPolygon) {
        # Write the line to the first file until "let polygon" is found
        $out1.WriteLine($line)
        if ($line -match "let pointUppsala") {
            $foundPolygon = $true
        }
    } else {
        # Write the rest of the lines to the second file
        $out2.WriteLine($line)
    }
}

# Close the output files
$out1.Close()
$out2.Close()

Write-Host "File has been split successfully."
