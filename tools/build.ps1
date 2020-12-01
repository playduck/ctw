$name = "ctw"
$build = ".\build"
$dist = ".\dist"
$spec = ".\ctw.spec"
$flags = $("--clean --noconfirm --onedir --name $name --distpath $dist --workpath $build")

$command = $(".\venv\Scripts\Activate.ps1; pyinstaller $flags $spec")
$remove = $("-rmdir $build -r -fo; rmdir $dist -r -fo")

Invoke-Expression $("$remove")
Invoke-Expression $command
