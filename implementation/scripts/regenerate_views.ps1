param(
    [string]$Dataset = ""
)

Add-Type -AssemblyName System.Drawing

$root = (Get-Location).Path
$views = Join-Path $root "data\views"
$stores = Join-Path $root "data\stores"

function Save-View {
    param(
        [object[]]$Rows,
        [string]$Path,
        [string]$Title,
        [ValidateSet("top", "front", "side", "3d")]
        [string]$Mode
    )

    $bitmap = New-Object System.Drawing.Bitmap(900, 760)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([System.Drawing.Color]::White)
    $axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Black, 2)
    $gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Gainsboro, 1)
    $font = New-Object System.Drawing.Font("Arial", 12)
    $titleFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
    $left = 90
    $top = 75
    $plotWidth = 730
    $plotHeight = 600

    $graphics.DrawString($Title, $titleFont, [System.Drawing.Brushes]::Black, 20, 20)
    if ($Mode -ne "3d") {
        $graphics.DrawRectangle($axisPen, $left, $top, $plotWidth, $plotHeight)
        for ($index = 1; $index -lt 5; $index++) {
            $gridX = $left + ($plotWidth * $index / 5)
            $gridY = $top + ($plotHeight * $index / 5)
            $graphics.DrawLine($gridPen, $gridX, $top, $gridX, $top + $plotHeight)
            $graphics.DrawLine($gridPen, $left, $gridY, $left + $plotWidth, $gridY)
        }
    }

    if ($Mode -eq "top") {
        $xLabel = "X (m)"
        $yLabel = "Y (m)"
    } elseif ($Mode -eq "front") {
        $xLabel = "X (m)"
        $yLabel = "Z (m)"
    } elseif ($Mode -eq "side") {
        $xLabel = "Y (m)"
        $yLabel = "Z (m)"
    } else {
        $xLabel = "X/Y depth projection (m)"
        $yLabel = "Z altitude (m)"
    }

    if ($Mode -ne "3d") {
        $graphics.DrawString($xLabel, $font, [System.Drawing.Brushes]::Black, $left + 280, $top + $plotHeight + 18)
        $graphics.DrawString($yLabel, $font, [System.Drawing.Brushes]::Black, 12, $top + 280)
    }

    foreach ($row in $Rows) {
        $x = [double]$row.x_m
        $y = [double]$row.y_m
        $z = [double]$row.z_m
        if ($Mode -eq "top") {
            $pixelX = $left + ($x / 1000 * $plotWidth)
            $pixelY = $top + $plotHeight - ($y / 1000 * $plotHeight)
        } elseif ($Mode -eq "front") {
            $pixelX = $left + ($x / 1000 * $plotWidth)
            $pixelY = $top + $plotHeight - ([math]::Min($z, 120) / 120 * $plotHeight)
        } elseif ($Mode -eq "side") {
            $pixelX = $left + ($y / 1000 * $plotWidth)
            $pixelY = $top + $plotHeight - ([math]::Min($z, 120) / 120 * $plotHeight)
        } else {
            # Project the complete 1000m x 1000m area into one parallelogram.
            # Its lower corner is the origin; every user remains inside it.
            $originX = $left + ($plotWidth * 0.50)
            $originY = $top + ($plotHeight * 0.38)
            $xVectorX = -0.36 * $plotWidth
            $xVectorY = 0.24 * $plotHeight
            $yVectorX = 0.36 * $plotWidth
            $yVectorY = 0.24 * $plotHeight
            $groundX = $originX + ($x / 1000 * $xVectorX) + ($y / 1000 * $yVectorX)
            $groundY = $originY + ($x / 1000 * $xVectorY) + ($y / 1000 * $yVectorY)
            $pixelX = $groundX
            $pixelY = $groundY - ([math]::Min($z, 120) / 120 * 260)
            $graphics.DrawLine(
                [System.Drawing.Pens]::LightSteelBlue,
                [float]$groundX,
                [float]$groundY,
                [float]$pixelX,
                [float]$pixelY
            )
        }

        $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 105, 175))
        $graphics.FillEllipse($brush, [float]($pixelX - 3), [float]($pixelY - 3), 6, 6)
        $brush.Dispose()
    }

    if ($Mode -eq "3d") {
        $groundPen = New-Object System.Drawing.Pen([System.Drawing.Color]::LightGray, 1)
        for ($index = 0; $index -le 10; $index++) {
            $ratio = $index / 10
            $originX = $left + ($plotWidth * 0.50)
            $originY = $top + ($plotHeight * 0.38)
            $xScale = 0.36 * $plotWidth
            $yScale = 0.24 * $plotHeight
            $x1 = $originX + ($ratio * $xScale)
            $y1 = $originY + ($ratio * $yScale)
            $x2 = $originX - $xScale + ($ratio * $xScale)
            $y2 = $originY + $yScale + ($ratio * $yScale)
            $graphics.DrawLine($groundPen, [float]$x1, [float]$y1, [float]$x2, [float]$y2)

            $x3 = $originX - ($ratio * $xScale)
            $y3 = $originY + ($ratio * $yScale)
            $x4 = $originX + $xScale - ($ratio * $xScale)
            $y4 = $originY + ($ratio * $yScale) + $yScale
            $graphics.DrawLine($groundPen, [float]$x3, [float]$y3, [float]$x4, [float]$y4)
        }
        $groundPen.Dispose()

        $axisLengthX = 0.36 * $plotWidth
        $axisLengthY = 0.24 * $plotHeight
        $axisLengthZ = 260
        $originX = $left + ($plotWidth * 0.50)
        $originY = $top + ($plotHeight * 0.38)
        $xPen = New-Object System.Drawing.Pen([System.Drawing.Color]::Crimson, 4)
        $yPen = New-Object System.Drawing.Pen([System.Drawing.Color]::ForestGreen, 4)
        $zPen = New-Object System.Drawing.Pen([System.Drawing.Color]::LightSalmon, 4)
        $xEndX = $originX - $axisLengthX * 1.45
        $xEndY = $originY + $axisLengthY * 1.45
        $yEndX = $originX + $axisLengthX * 1.45
        $yEndY = $originY + $axisLengthY * 1.45
        $graphics.DrawLine($xPen, $originX, $originY, $xEndX, $xEndY)
        $graphics.DrawLine($yPen, $originX, $originY, $yEndX, $yEndY)
        $zEndX = $originX
        $zEndY = $originY - $axisLengthZ * 0.78
        $graphics.DrawLine($zPen, $originX, $originY, $zEndX, $zEndY)
        $graphics.DrawString("X (m)", $font, [System.Drawing.Brushes]::Crimson, $xEndX - 45, $xEndY + 5)
        $graphics.DrawString("Y (m)", $font, [System.Drawing.Brushes]::ForestGreen, $yEndX + 5, $yEndY + 5)
        $graphics.DrawString("Z (m)", $font, [System.Drawing.Brushes]::LightSalmon, $zEndX + 8, $zEndY - 20)
        $graphics.DrawString("Origin (0,0,0)", $font, [System.Drawing.Brushes]::Black, $originX + 8, $originY + 5)
        $graphics.DrawString("Axes: X = red, Y = green, Z = blue", $font, [System.Drawing.Brushes]::DimGray, 20, 45)
        $xPen.Dispose()
        $yPen.Dispose()
        $zPen.Dispose()

        # Redraw user markers last so axes and projection lines never cover them.
        foreach ($row in $Rows) {
            $x = [double]$row.x_m
            $y = [double]$row.y_m
            $z = [double]$row.z_m
            $originX = $left + ($plotWidth * 0.50)
            $originY = $top + ($plotHeight * 0.38)
            $xVectorX = -0.36 * $plotWidth
            $xVectorY = 0.24 * $plotHeight
            $yVectorX = 0.36 * $plotWidth
            $yVectorY = 0.24 * $plotHeight
            $groundX = $originX + ($x / 1000 * $xVectorX) + ($y / 1000 * $yVectorX)
            $groundY = $originY + ($x / 1000 * $xVectorY) + ($y / 1000 * $yVectorY)
            $pixelX = $groundX
            $pixelY = $groundY - ([math]::Min($z, 120) / 120 * 260)
            $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 105, 175))
            $graphics.FillEllipse($brush, [float]($pixelX - 4), [float]($pixelY - 4), 8, 8)
            $brush.Dispose()
        }
    }

    $graphics.DrawString(("Mode: " + $Mode), $font, [System.Drawing.Brushes]::DimGray, 20, $top + $plotHeight + 50)
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $font.Dispose()
    $titleFont.Dispose()
    $axisPen.Dispose()
    $gridPen.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()
}

foreach ($csv in Get-ChildItem $stores -Filter "*.csv" -File) {
    if ($Dataset -and $csv.BaseName -ne $Dataset -and $csv.Name -ne $Dataset) {
        continue
    }
    $rows = @(Import-Csv $csv.FullName)
    $output = Join-Path $views $csv.BaseName
    New-Item -ItemType Directory -Force -Path $output | Out-Null
    Save-View $rows (Join-Path $output "top.png") ($csv.BaseName + " - Top X-Y") "top"
    Save-View $rows (Join-Path $output "front.png") ($csv.BaseName + " - Front X-Z") "front"
    Save-View $rows (Join-Path $output "side.png") ($csv.BaseName + " - Side Y-Z") "side"
    Save-View $rows (Join-Path $output "3d.png") ($csv.BaseName + " - 3D X-Y-Z") "3d"
}
