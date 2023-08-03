function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    $isAdmin = $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
    return $isAdmin
}

Set-ExecutionPolicy Bypass -Scope Process

function Test-ChocolateyInstallation {
    $chocoCommand = 'choco'
    $installed = $false

    try {
        $null = Get-Command -Name $chocoCommand -ErrorAction Stop
        $installed = $true
    }
    catch {
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
    Read-Host -Prompt "Press Enter to exit"
}
else {
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Read-Host -Prompt "Press Enter to exit"
}
