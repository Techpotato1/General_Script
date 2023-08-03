function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    $isAdmin = $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
    return $isAdmin
}

function Test-ChocolateyInstallation {
    $chocoCommand = 'choco'
    $installed = $false

    try {
        $null = Get-Command -Name $chocoCommand -ErrorAction Stop
        $installed = $true
    } catch {
        $installed = $false
    }

    return $installed
}

if (-Not (Test-Administrator)) {
    Write-Host "Please run the script as an administrator to check Chocolatey installation."
    exit 1
}

$chocoInstalled = Test-ChocolateyInstallation

if ($chocoInstalled) {
    Write-Host "Chocolatey is installed on this system."
} else {
    Write-Host "Chocolatey is not installed on this system."
}
