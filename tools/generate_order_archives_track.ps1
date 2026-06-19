$ErrorActionPreference = "Stop"

$sampleRate = 22050
$duration = 132.0
$count = [int]($sampleRate * $duration)
$random = [Random]::new(1437)
$samples = [double[]]::new($count)

function Add-Tone {
    param(
        [double]$Start,
        [double]$Length,
        [double[]]$Frequencies,
        [double]$Amp,
        [double]$Attack,
        [double]$Release
    )

    $startIndex = [Math]::Max(0, [int]($Start * $script:sampleRate))
    $endIndex = [Math]::Min($script:count, [int](($Start + $Length) * $script:sampleRate))
    for ($i = $startIndex; $i -lt $endIndex; $i++) {
        $localTime = ($i - $startIndex) / $script:sampleRate
        $globalTime = $i / $script:sampleRate
        $env = [Math]::Min(1.0, [Math]::Min($localTime / $Attack, ($Length - $localTime) / $Release))
        if ($env -le 0.0) { continue }

        $tone = 0.0
        foreach ($frequency in $Frequencies) {
            $wobble = 1.0 + 0.0025 * [Math]::Sin(2.0 * [Math]::PI * 0.017 * $globalTime + $frequency)
            $phase = 2.0 * [Math]::PI * $frequency * $wobble * $globalTime
            $tone += [Math]::Sin($phase) + 0.28 * [Math]::Sin(2.0 * $phase + 0.4)
        }

        $script:samples[$i] += $Amp * $env * $tone / [Math]::Max(1, $Frequencies.Count)
    }
}

function Add-Bell {
    param(
        [double]$Start,
        [double]$Frequency,
        [double]$Amp,
        [double]$Decay
    )

    $startIndex = [Math]::Max(0, [int]($Start * $script:sampleRate))
    $length = [int]($Decay * 7.0 * $script:sampleRate)
    $phase = $script:random.NextDouble() * 2.0 * [Math]::PI
    for ($j = 0; $j -lt $length; $j++) {
        $i = $startIndex + $j
        if ($i -ge $script:count) { break }

        $time = $j / $script:sampleRate
        $env = [Math]::Exp(-$time / $Decay) * [Math]::Min(1.0, $time / 0.018)
        $partials =
            [Math]::Sin(2.0 * [Math]::PI * $Frequency * $time + $phase) +
            0.63 * [Math]::Sin(2.0 * [Math]::PI * $Frequency * 2.01 * $time + 0.3 * $phase) +
            0.34 * [Math]::Sin(2.0 * [Math]::PI * $Frequency * 2.92 * $time + 1.7) +
            0.18 * [Math]::Sin(2.0 * [Math]::PI * $Frequency * 4.16 * $time + 0.2)
        $script:samples[$i] += $Amp * $env * $partials
    }
}

# Subterranean drone in D with fifths and minor color.
for ($i = 0; $i -lt $count; $i++) {
    $t = $i / $sampleRate
    $fadeIn = [Math]::Min(1.0, $t / 10.0)
    $fadeOut = [Math]::Min(1.0, ($duration - $t) / 12.0)
    $breath = 0.55 + 0.45 * [Math]::Sin(2.0 * [Math]::PI * 0.027 * $t)

    $s = 0.0
    foreach ($layer in @(
        @(73.42, 0.30, 0.000),
        @(73.42, 0.16, 0.006),
        @(110.00, 0.18, -0.004),
        @(146.83, 0.11, 0.003),
        @(174.61, 0.06, -0.002)
    )) {
        $frequency = $layer[0]
        $amp = $layer[1]
        $detune = $layer[2]
        $phase = 2.0 * [Math]::PI * $frequency * (1.0 + $detune * [Math]::Sin(2.0 * [Math]::PI * 0.011 * $t)) * $t
        $s += $amp * [Math]::Sin($phase)
        $s += $amp * 0.22 * [Math]::Sin(2.0 * $phase + 0.7)
    }

    $samples[$i] += $fadeIn * $fadeOut * $breath * 0.66 * $s
}

$chords = @(
    @(73.42, 110.00, 146.83, 174.61),
    @(65.41, 98.00, 130.81, 164.81),
    @(58.27, 87.31, 116.54, 146.83),
    @(73.42, 98.00, 146.83, 196.00)
)

for ($start = 0; $start -lt $duration; $start += 24) {
    Add-Tone -Start $start -Length 26.0 -Frequencies ([double[]]$chords[($start / 24) % $chords.Count]) -Amp 0.095 -Attack 7.0 -Release 8.0
}

$scale = @(73.42, 82.41, 87.31, 98.00, 110.00, 116.54, 130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 233.08, 261.63, 293.66)
$eventTime = 8.0
while ($eventTime -lt ($duration - 7.0)) {
    $frequency = $scale[$random.Next(4, $scale.Count)]
    if ($random.NextDouble() -lt 0.28) { $frequency *= 0.5 }
    if ($random.NextDouble() -lt 0.18) { $frequency *= 2.0 }
    Add-Bell -Start $eventTime -Frequency $frequency -Amp (0.045 + $random.NextDouble() * 0.075) -Decay (2.2 + $random.NextDouble() * 3.2)
    $eventTime += 3.5 + $random.NextDouble() * 7.5
}

foreach ($eventTime in @(18.0, 42.0, 67.0, 96.0, 119.0)) {
    Add-Bell -Start $eventTime -Frequency @(55.00, 61.74, 73.42)[$random.Next(0, 3)] -Amp 0.23 -Decay 8.5
}

# Dust and room air.
$noise = 0.0
for ($i = 0; $i -lt $count; $i++) {
    $t = $i / $sampleRate
    $white = $random.NextDouble() * 2.0 - 1.0
    $noise = 0.992 * $noise + 0.008 * $white
    $samples[$i] += $noise * (0.015 + 0.011 * [Math]::Sin(2.0 * [Math]::PI * 0.006 * $t + 0.4))
}

# Cavern-like feedback delays.
foreach ($delay in @(
    @(0.173, 0.42, 0.38),
    @(0.389, 0.35, 0.28),
    @(0.727, 0.25, 0.22),
    @(1.113, 0.18, 0.15)
)) {
    $offset = [int]($delay[0] * $sampleRate)
    $feedback = $delay[1]
    $gain = $delay[2]
    for ($i = $offset; $i -lt $count; $i++) {
        $samples[$i] += $samples[$i - $offset] * $feedback * $gain
    }
}

$peak = 0.001
for ($i = 0; $i -lt $count; $i++) {
    $abs = [Math]::Abs($samples[$i])
    if ($abs -gt $peak) { $peak = $abs }
}

$outPath = Join-Path $PSScriptRoot "..\game\audio\order_archives_dark_ambient.wav"
$outPath = [IO.Path]::GetFullPath($outPath)
$bytes = [byte[]]::new(44 + $count * 2)
$dataSize = $count * 2
$riffSize = 36 + $dataSize

function Write-Ascii([byte[]]$Buffer, [int]$Offset, [string]$Text) {
    $chars = [Text.Encoding]::ASCII.GetBytes($Text)
    [Array]::Copy($chars, 0, $Buffer, $Offset, $chars.Length)
}

function Write-Int16([byte[]]$Buffer, [int]$Offset, [int]$Value) {
    $b = [BitConverter]::GetBytes([int16]$Value)
    [Array]::Copy($b, 0, $Buffer, $Offset, 2)
}

function Write-Int32([byte[]]$Buffer, [int]$Offset, [int]$Value) {
    $b = [BitConverter]::GetBytes([int32]$Value)
    [Array]::Copy($b, 0, $Buffer, $Offset, 4)
}

Write-Ascii $bytes 0 "RIFF"
Write-Int32 $bytes 4 $riffSize
Write-Ascii $bytes 8 "WAVE"
Write-Ascii $bytes 12 "fmt "
Write-Int32 $bytes 16 16
Write-Int16 $bytes 20 1
Write-Int16 $bytes 22 1
Write-Int32 $bytes 24 $sampleRate
Write-Int32 $bytes 28 ($sampleRate * 2)
Write-Int16 $bytes 32 2
Write-Int16 $bytes 34 16
Write-Ascii $bytes 36 "data"
Write-Int32 $bytes 40 $dataSize

$level = 0.82 / $peak
for ($i = 0; $i -lt $count; $i++) {
    $t = $i / $sampleRate
    $fade = [Math]::Min(1.0, [Math]::Min($t / 10.0, ($duration - $t) / 12.0))
    $y = [Math]::Tanh($samples[$i] * $level * $fade * 1.25) * 0.82
    $value = [int16]([Math]::Max(-1.0, [Math]::Min(1.0, $y)) * 32767)
    $sampleBytes = [BitConverter]::GetBytes($value)
    $bytes[44 + $i * 2] = $sampleBytes[0]
    $bytes[45 + $i * 2] = $sampleBytes[1]
}

[IO.File]::WriteAllBytes($outPath, $bytes)
$sizeMiB = [Math]::Round((Get-Item $outPath).Length / 1MB, 1)
Write-Output "$outPath"
Write-Output "$([int]$duration)s, mono, $sampleRate Hz, $sizeMiB MiB"
