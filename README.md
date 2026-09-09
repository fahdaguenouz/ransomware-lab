# Ransomware-Lab

Ransomware-Lab is a deliberately limited ransomware simulation for learning how
file encryption and recovery work. It contains an encryption program, a
decryption program, safety controls, and automated tests.

This project is for an isolated Windows virtual machine and disposable test
files only. It does **not** contain persistence, spreading, privilege
escalation, obfuscation, antivirus bypass, networking, or payment handling.

## What is included

| File | Purpose |
|---|---|
| `setup_lab.py` | Creates a test folder and the required safety marker. |
| `encrypt.py` | Generates a random code and encrypts files in that marked folder. |
| `decrypt.py` | Accepts the code and restores the encrypted files. |
| `ransomlab/common.py` | Shared safety, file, key-derivation, and AES-GCM logic. |
| `tests/test_roundtrip.py` | Tests recovery, wrong codes, notes, and safety checks. |
| `requirements.txt` | Python dependency list. |

## Safety rules

The simulator only operates when all of these conditions are met:

1. A target directory is provided explicitly with `--target`.
2. The target contains `.ransomware_lab_safe`, created by `setup_lab.py`.
3. The encryption command includes `--i-understand-this-is-a-lab`.
4. The target is not the filesystem root or the current user's home directory.
5. Symbolic links are ignored, so traversal cannot escape through a link.

The marker and previously encrypted `.ransomlab` files are not encrypted. Never
put real or irreplaceable data in the lab folder. Take a VM snapshot first.

## Requirements

- An isolated Windows 10 or Windows 11 virtual machine
- Python 3.10 or newer
- The `cryptography` Python package
- VirtualBox or VMware on an x86/x64 host, or UTM/Parallels with Windows 11 ARM
  on Apple Silicon

Configure the VM network as **Internal Network** or **Host-Only**. Disable
shared folders, clipboard sharing, drag-and-drop, and USB passthrough for the
test. Do not test on the host computer or upload the program to public scanning
services.

## Installation on Windows

Open PowerShell inside the project directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the virtual environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Safe demonstration

### 1. Prepare disposable files

Create a dedicated test directory. The setup command creates it if needed and
adds the opt-in safety marker:

```powershell
py setup_lab.py C:\RansomwareLab\test-data
Set-Content C:\RansomwareLab\test-data\example.txt "Disposable example"
New-Item -ItemType Directory C:\RansomwareLab\test-data\nested
Set-Content C:\RansomwareLab\test-data\nested\second.txt "Another example"
```

### 2. Encrypt the test files

```powershell
py encrypt.py --target C:\RansomwareLab\test-data --i-understand-this-is-a-lab
```

The program:

- generates a new random 24-character recovery code;
- encrypts every regular file below the marked target directory;
- changes each encrypted name by adding `.ransomlab`;
- prints the recovery code; and
- writes `RANSOM_NOTE.txt` on the current user's Desktop.

Copy the recovery code for the next step. A new code is generated on every run.
For an audit-only note location, add `--note-dir C:\RansomwareLab`.

### 3. Restore the files

The safest option is the hidden interactive prompt:

```powershell
py decrypt.py --target C:\RansomwareLab\test-data
```

For an automated demonstration, the code can be passed as an argument:

```powershell
py decrypt.py --target C:\RansomwareLab\test-data --code ABC123-DEF456-GHI789-JKL012
```

The example code above is only a placeholder. Use the code printed by your own
encryption run. The decryptor first authenticates every encrypted file. If the
code is wrong or a file was damaged, it reports an error and leaves the
encrypted set in place. It also refuses to overwrite an existing restored file.

### 4. Run the automated tests

```powershell
py -m unittest discover -v
```

The tests use temporary directories and verify text, empty, binary, and nested
files; wrong-code behavior; marker enforcement; note creation; and random code
format.

## Technical explanation

### Encryption model

This mandatory implementation uses a **symmetric-only** design:

1. `secrets.choice` creates 24 random uppercase letters/digits. Hyphens are
   added only to make the code easier to read.
2. Each file gets a fresh random 16-byte salt.
3. Scrypt derives a 256-bit key from the entered code and salt. Its parameters
   are `N=16384`, `r=8`, and `p=1`.
4. Each file gets a fresh random 12-byte nonce.
5. AES-256-GCM encrypts and authenticates the content.
6. The output stores `RANSIM01`, the salt, the nonce, and the authenticated
   ciphertext. The code itself is not stored inside the encrypted file.

The file layout is:

```text
RANSIM01 | 16-byte salt | 12-byte nonce | ciphertext and 16-byte GCM tag
```

AES-GCM was selected because it provides confidentiality and integrity. A
changed file or wrong code fails authentication instead of producing corrupted
plaintext. Scrypt makes guessing a code more expensive. Temporary files and an
atomic replace reduce the chance of leaving a half-written output.

### Decryption model

The decryptor reads the salt and nonce from each `.ransomlab` file, derives the
same AES key from the user-supplied code, verifies the GCM tag, and writes the
original bytes back under the original name. Nothing is hardcoded or tied to a
specific computer, so the correct code can restore files on another system.

### Symmetric-only limitation

While a file is being encrypted or decrypted, its AES key necessarily exists in
the process memory. A capable analyst could potentially extract it. Real
ransomware often uses a hybrid model: a random AES key encrypts files, and an
attacker's RSA public key encrypts that AES key. The RSA private key never
appears on the affected computer. That design makes unauthorized recovery more
difficult, so it is intentionally outside this simple educational project.

## Audit checklist

Before the audit:

- Show that the Windows VM is isolated and has no shared host directories.
- Take a clean snapshot and prepare only disposable random files.
- Show both source programs and this README.
- Run `py -m unittest discover -v`.
- Demonstrate that an unmarked folder is rejected.
- Encrypt the marked folder and show that each file has `.ransomlab`.
- Show `RANSOM_NOTE.txt` and its newly generated code.
- Try a wrong code and show that restoration is rejected.
- Enter the correct code and compare the restored files with the originals.
- Repeat with a new folder/run to show that a different code is generated.

Be ready to explain that ransomware denies access to data, that AES-GCM performs
authenticated symmetric encryption, that Scrypt derives the key dynamically,
and that backups and rapid isolation are essential defenses.

### About the antivirus-evasion rubric

The subject asks for Windows Defender and VirusTotal avoidance. This repository
does not attempt to bypass security products. Evasion would make the sample more
dangerous, conflicts with the defensive purpose of the lab, and is not required
to explain the encryption lifecycle. Detection by a security product is an
expected and acceptable outcome for this safe simulation. Do not disable
Defender or add exclusions to conceal it.

## Defensive recommendations

Organizations should:

- keep versioned, offline, immutable backups and test restoration regularly;
- use least privilege and separate administrator accounts;
- patch operating systems, browsers, VPNs, and exposed services quickly;
- enable endpoint detection, tamper protection, and centralized logging;
- restrict script interpreters and application execution where practical;
- segment networks and limit SMB/RDP access;
- use phishing-resistant MFA and train users to report suspicious messages;
- alert on rapid file rewrites, unusual extension changes, ransom-note creation,
  and deletion of backups or shadow copies; and
- isolate affected systems immediately while preserving forensic evidence.

For this sample specifically, defenders can detect the `.ransomlab` extension,
the `RANSIM01` header, the note name, and a process rapidly reading, writing, and
deleting many files.

## Ethical and legal report

Encryption code becomes ransomware when it is used without informed permission
to deny someone access to their data. Testing must therefore be authorized,
limited to disposable data, and contained in an isolated VM. The operator is
responsible for the scope, local law, evidence handling, and cleanup.

Do not deploy this project on another person's computer, production equipment,
school or employer systems, cloud-synced folders, shared drives, or public
networks. Do not demand payment, collect data, add persistence, or modify the
code to evade defenses. If an accidental execution affects real data, stop the
process, disconnect the machine from networks, preserve the recovery code and
logs, and contact the responsible security team.

## Cleanup

After demonstrating successful recovery, delete the disposable test directory
and desktop note inside the VM, then revert the VM to its clean snapshot. Keep
the source in the authorized course repository only.

