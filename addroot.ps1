$x = Get-ChildItem  -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -Match "Steve's RDP Manager"} | Select-Object Thumbprint
$x = $x.thumbprint

if (-not (Test-Path -path Cert:\CurrentUser\Root\$x))
	{
	$cert = Get-Item -Path Cert:\CurrentUser\My\$x
	$store = Get-Item -Path Cert:\CurrentUser\Root
	$store.open("ReadWrite")
	$store.add($cert)
	$store.Close()
	}
