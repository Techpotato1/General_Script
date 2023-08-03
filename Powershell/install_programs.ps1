if ($null = Get-Command -Name 'choco' -ErrorAction Stop) {
    choco install 7zip -y
    choco install vlc -y

}
else {
    Read-Host "Chocolaty is not installed, please install"
    exit 1
}