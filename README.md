# Ransomware-Lab

Ransomware-Lab is a controlled educational simulation of file encryption and
recovery. The Python source is split into small files for readability, but the
project builds to **one executable file** containing all three commands:

```text
ransomware-lab setup
ransomware-lab encrypt
ransomware-lab decrypt
```

The Windows build produces `release\ransomware-lab.exe`. The Linux build
produces `release/ransomware-lab`. Python is not required on the computer that
runs the finished executable.

Use this project only in an isolated virtual machine with disposable files. It
does not include spreading, persistence, privilege escalation, networking,
obfuscation, antivirus bypass, or payment handling.

## Project structure

| File | Purpose |
|---|---|
| `ransomware_lab.py` | Unified entry point packaged into the executable. |
| `encrypt.py` | Encryption and note-creation functions. |
| `decrypt.py` | File-restoration functions. |
| `setup_lab.py` | Standalone source version of the setup command. |
| `ransomlab/common.py` | Shared cryptography, file, and safety functions. |
| `build.py` | Builds the unified one-file executable. |
| `requirements.txt` | Runtime Python dependency. |
| `requirements-build.txt` | Runtime dependency plus PyInstaller. |
| `tests/` | Automated tests. |

Only the single file under `release/` is the distributable build. The source
files, build directory, spec file, and virtual environment are not needed to
run it.

## Safety controls

The executable only encrypts a directory when:

1. The directory is explicitly passed with `--target`.
2. The `setup` command has added `.ransomware_lab_safe` to that directory.
3. The `--i-understand-this-is-a-lab` flag is supplied.
4. The target is not the filesystem root or the current user's home directory.

Symbolic links are ignored. Never use real, important, shared, mounted, or
cloud-synchronized data.

## Important build rule

PyInstaller is not a cross-compiler:

- Build the Windows `.exe` on Windows.
- Build the Linux executable on Linux.

Running `build.py` on Kali cannot create a Windows `.exe`.

## Build one executable on Windows

### 1. Install Python

Install Python 3.10 or newer and enable **Add Python to PATH** in the installer.
Open PowerShell and verify it:

```powershell
py --version
```

### 2. Open the project

Change this example path if your project is elsewhere:

```powershell
cd C:\Ransomware-Lab
```

### 3. Create the build environment

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
```

If activation is blocked, run this once in the current PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 4. Run the one-file build

```powershell
python build.py
```

The final executable is:

```text
release\ransomware-lab.exe
```

Confirm that it starts:

```powershell
.\release\ransomware-lab.exe --version
.\release\ransomware-lab.exe --help
```

The entire runnable application is that one `.exe` file.

## Use the executable on Windows

Run these commands only inside an isolated Windows VM.

### 1. Prepare the test directory

```powershell
.\release\ransomware-lab.exe setup C:\RansomwareLab\test-data
```

### 2. Create disposable files

```powershell
Set-Content C:\RansomwareLab\test-data\example.txt "Disposable example"
New-Item -ItemType Directory -Force C:\RansomwareLab\test-data\nested
Set-Content C:\RansomwareLab\test-data\nested\second.txt "Second example"
```

### 3. Encrypt the marked test directory

```powershell
.\release\ransomware-lab.exe encrypt `
  --target C:\RansomwareLab\test-data `
  --note-dir C:\RansomwareLab\note `
  --i-understand-this-is-a-lab
```

Example output:

```text
Encrypted 2 file(s) inside: C:\RansomwareLab\test-data
Recovery code: ABC123-DEF456-GHI789-JKL012
Ransomware-Lab note: C:\RansomwareLab\note\RANSOM_NOTE.txt
```

Save the exact recovery code printed by your run. Every run generates a new
code. Encrypted file names end in `.ransomlab`.

### 4. Restore the files

```powershell
.\release\ransomware-lab.exe decrypt --target C:\RansomwareLab\test-data
```

Paste the generated code when prompted. You can provide it directly for an
automated demonstration, although it will remain visible in terminal history:

```powershell
.\release\ransomware-lab.exe decrypt `
  --target C:\RansomwareLab\test-data `
  --code ABC123-DEF456-GHI789-JKL012
```

Replace the example code with the real code from the encryption output.

## Build one executable on Linux

From Kali, Ubuntu, or another Linux system:

```bash
cd ~/Desktop/ransomware-lab
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-build.txt
python3 build.py
```

The final executable is:

```text
release/ransomware-lab
```

Confirm that it starts:

```bash
./release/ransomware-lab --version
./release/ransomware-lab --help
```

If virtual-environment creation fails on Kali or Debian:

```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

## Use the executable on Linux

### 1. Prepare the test directory

```bash
./release/ransomware-lab setup /tmp/ransomware-lab-test
```

### 2. Create disposable files

```bash
printf 'First disposable example\n' > /tmp/ransomware-lab-test/example.txt
mkdir -p /tmp/ransomware-lab-test/nested
printf 'Second disposable example\n' > /tmp/ransomware-lab-test/nested/second.txt
```

### 3. Encrypt the files

```bash
./release/ransomware-lab encrypt \
  --target /tmp/ransomware-lab-test \
  --note-dir /tmp/ransomware-lab-note \
  --i-understand-this-is-a-lab
```

Save the generated recovery code.

### 4. Restore the files

```bash
./release/ransomware-lab decrypt --target /tmp/ransomware-lab-test
```

Paste the recovery code at the hidden prompt. For an automated demonstration:

```bash
./release/ransomware-lab decrypt \
  --target /tmp/ransomware-lab-test \
  --code ABC123-DEF456-GHI789-JKL012
```

## Run from Python without building

The same unified interface can be run directly from source:

```bash
python3 ransomware_lab.py --help
python3 ransomware_lab.py setup /tmp/ransomware-lab-test
python3 ransomware_lab.py encrypt \
  --target /tmp/ransomware-lab-test \
  --note-dir /tmp/ransomware-lab-note \
  --i-understand-this-is-a-lab
python3 ransomware_lab.py decrypt --target /tmp/ransomware-lab-test
```

On Windows, replace `python3` with `python` and use Windows paths.

## Run the tests

Tests run against temporary directories and do not use the executable:

```bash
python3 -m unittest discover -v
```

On Windows:

```powershell
python -m unittest discover -v
```

The six tests cover nested, binary, and empty files; successful restoration;
incorrect codes; safety-marker enforcement; note creation; unique codes; and
the unified setup command.

## Command reference

```text
ransomware-lab setup TARGET
ransomware-lab encrypt --target TARGET --i-understand-this-is-a-lab
ransomware-lab encrypt --target TARGET --note-dir DIRECTORY --i-understand-this-is-a-lab
ransomware-lab decrypt --target TARGET
ransomware-lab decrypt --target TARGET --code CODE
```

Use `ransomware-lab COMMAND --help` for command-specific options.

## Common errors

### `No module named PyInstaller`

Activate `.venv` and install `requirements-build.txt`, not only
`requirements.txt`.

### `Safety marker missing`

Run the `setup` command on the exact target path before encryption.

### `Wrong recovery code or damaged encrypted file`

Use the code generated during that encryption run. A code from another run will
not work. The encrypted files remain unchanged after a failed attempt.

### `Restore destination already exists`

A plaintext file already has the name needed by the decryptor. Move that
disposable file outside the test directory before retrying. The program refuses
to overwrite it.

### Windows `.exe` does not appear after a Linux build

Build on Windows. PyInstaller packages for the operating system on which it is
running.

## Technical explanation

The project uses a symmetric-only design:

1. Python's `secrets` module generates a random 24-character recovery code.
2. Every file receives a new random 16-byte salt.
3. Scrypt derives a 256-bit key from the code and salt.
4. Every file receives a random 12-byte nonce.
5. AES-256-GCM encrypts and authenticates the file content.

The encrypted format is:

```text
RANSIM01 | 16-byte salt | 12-byte nonce | ciphertext and 16-byte GCM tag
```

The decrypt command reads the salt and nonce, derives the same key from the
entered code, verifies the GCM tag, and restores the original bytes and name.
The key is dynamic and not hardcoded or tied to one computer.

A symmetric key exists in memory while the application works, so this simpler
model is potentially vulnerable to memory analysis. A hybrid AES/RSA model
would keep an RSA private key off the affected machine, but that more dangerous
design is intentionally outside this project.

## Defensive recommendations

- Maintain tested, offline, immutable backups.
- Use least privilege and network segmentation.
- Patch operating systems and exposed services.
- Enable endpoint protection, tamper protection, and centralized logging.
- Alert on rapid file rewrites, extension changes, and ransom-note creation.
- Isolate affected systems while preserving forensic evidence.

This simulation can be identified by `.ransomlab`, the `RANSIM01` header,
`RANSOM_NOTE.txt`, and rapid file modifications. It does not attempt to bypass
security products.

## Ethical and legal considerations

Testing must be authorized, restricted to disposable data, and contained in an
isolated VM. Never deploy this project on another person's computer, production
equipment, school or employer systems, shared drives, host-mounted directories,
cloud-synchronized folders, or public networks. Do not add persistence,
spreading, data collection, payment demands, or defense evasion.

## Cleanup

After verifying restoration, delete only the disposable lab data and note. Then
revert the VM to its clean snapshot.
