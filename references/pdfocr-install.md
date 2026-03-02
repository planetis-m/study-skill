# pdfocr Install Fallback

Use this only when `command -v pdfocr` fails.

Path policy:
- Use absolute user paths only (`$HOME/.local/...`).
- Never install into a relative workspace path such as `./.local/...`.
- Never create `.local` under the current project directory.

As of February 28, 2026 (`pdfocr` v0.2.6), release assets exist for:
- Linux `x86_64`
- macOS `arm64`
- Windows `x86_64`

Release page:
- `https://github.com/planetis-m/pdfocr/releases/latest`

## Linux x86_64

```bash
set -euo pipefail
mkdir -p "$HOME/.local/opt/pdfocr" "$HOME/.local/bin"
tmp_dir="$(mktemp -d)"
curl -fsSL -o "$tmp_dir/pdfocr.tar.gz" \
  "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-linux-x86_64.tar.gz"
rm -rf "$HOME/.local/opt/pdfocr/current"
mkdir -p "$HOME/.local/opt/pdfocr/current"
tar -xzf "$tmp_dir/pdfocr.tar.gz" -C "$HOME/.local/opt/pdfocr/current"
pdfocr_bin="$(find "$HOME/.local/opt/pdfocr/current" -type f -name pdfocr | head -n1)"
ln -sfn "$pdfocr_bin" "$HOME/.local/bin/pdfocr"
export PATH="$HOME/.local/bin:$PATH"
pdfocr --help >/dev/null
```

## macOS arm64

```bash
set -euo pipefail
mkdir -p "$HOME/.local/opt/pdfocr" "$HOME/.local/bin"
tmp_dir="$(mktemp -d)"
curl -fsSL -o "$tmp_dir/pdfocr.tar.gz" \
  "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-macos-arm64.tar.gz"
rm -rf "$HOME/.local/opt/pdfocr/current"
mkdir -p "$HOME/.local/opt/pdfocr/current"
tar -xzf "$tmp_dir/pdfocr.tar.gz" -C "$HOME/.local/opt/pdfocr/current"
pdfocr_bin="$(find "$HOME/.local/opt/pdfocr/current" -type f -name pdfocr | head -n1)"
ln -sfn "$pdfocr_bin" "$HOME/.local/bin/pdfocr"
export PATH="$HOME/.local/bin:$PATH"
pdfocr --help >/dev/null
```

## Windows x86_64 (PowerShell)

```powershell
$ErrorActionPreference = "Stop"
$dst = "$HOME\.local\opt\pdfocr"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$zip = Join-Path $env:TEMP "pdfocr.zip"
Invoke-WebRequest -Uri "https://github.com/planetis-m/pdfocr/releases/latest/download/pdfocr-windows-x86_64.zip" -OutFile $zip
Remove-Item -Recurse -Force (Join-Path $dst "current") -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $dst "current") | Out-Null
Expand-Archive -Path $zip -DestinationPath (Join-Path $dst "current") -Force
$exe = Get-ChildItem -Path (Join-Path $dst "current") -Recurse -Filter "pdfocr.exe" | Select-Object -First 1
$exeDir = Split-Path -Parent $exe.FullName
$env:Path = "$exeDir;$env:Path"
pdfocr --help | Out-Null
```

## DeepInfra API key configuration

`pdfocr` supports both env var and `config.json`:
- `DEEPINFRA_API_KEY` (recommended)
- `config.json` `api_key` field next to the `pdfocr` binary

Precedence:
- If `DEEPINFRA_API_KEY` is set, it overrides `config.json.api_key`.

### Recommended: environment variable

Linux/macOS (current shell):

```bash
export DEEPINFRA_API_KEY="your_deepinfra_api_key"
```

Windows PowerShell (current session):

```powershell
$env:DEEPINFRA_API_KEY = "your_deepinfra_api_key"
```

### Alternative: update config.json

Edit `config.json` in the same directory as the real `pdfocr` executable and set:

```json
{
  "api_key": "your_deepinfra_api_key"
}
```

### Credential detection rule

- Resolve `command -v pdfocr` to its real target path.
- Check `config.json` next to that real binary.
- If the PATH entry is a symlink, do not check `config.json` in the symlink directory.

## Notes

- Keep all extracted runtime files (`config.json`, `libpdfium`, and platform shared libs) with the real binary.
- Do not copy only `pdfocr`/`pdfocr.exe` into another directory without its bundled runtime files.
- Ensure install targets are under user home (`$HOME/.local` or `%USERPROFILE%\.local`), not the current workspace.
- If install fails due to permissions, retry in a user-writable location as shown above.
- If platform/architecture is unsupported, stop and ask the user for manual installation steps.
