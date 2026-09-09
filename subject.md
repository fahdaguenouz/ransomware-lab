## Ransomware-Lab

### Introduction

To effectively defend against ransomware attacks, it's essential to understand their mechanics. This project challenges you to think like a black hat and develop a controlled ransomware simulation. By creating both encryption and decryption programs, you'll gain insight into how ransomware like WannaCry operates.

This exercise is conducted in a secure virtual machine environment to ensure safety and controlled experimentation.

### Why This Project Matters

Ransomware attacks cost organizations billions of dollars annually and can cripple critical infrastructure, hospitals, and businesses. Understanding how ransomware works is essential for building effective defenses. This project teaches you to "think like an attacker" so you can:

- **Build Better Defenses**: By understanding encryption and evasion techniques, you can design more robust detection systems and backup strategies.
- **Conduct Effective Security Assessments**: Red team exercises require knowledge of real-world ransomware tactics to test organizational resilience.
- **Improve Incident Response**: When a ransomware attack occurs, understanding the mechanics helps you respond faster, potentially recover data, and contain the threat.
- **Develop Security Tools**: Many EDR (Endpoint Detection and Response) and anti-ransomware solutions are built by professionals who deeply understand ransomware behavior.

The knowledge gained here should be used to **protect organizations, improve security products, and conduct authorized security testing** — never for malicious purposes.

### Objective

The goal of this project is to develop a ransomware simulation and a corresponding decryption tool to understand ransomware mechanics. By completing this project, you will:

- Learn the core principles of file encryption and decryption.
- Understand how ransomware manipulates files and affects systems.
- Gain hands-on experience in developing secure cryptographic programs.
- Enhance your understanding of how to defend against such attacks in real-world scenarios.
- Learn how to detect and prevent ransomware in production environments.

### Role Play

As part of the project, you will participate in a role-play session where you act as a **Malware Developer** presenting your ransomware simulation to a team of stakeholders. Be prepared to:

- Explain the design and functionality of your ransomware and decryption tool.
- Discuss how ransomware can bypass antivirus detection and the challenges involved.
- Analyze the ethical considerations and potential risks of working with ransomware simulations.
- Provide recommendations for improving ransomware detection and system security.
- Explain how organizations can protect themselves against ransomware attacks.

### Project Requirements

#### Setup and Environment

You are required to use a **Windows-based virtual machine** as your development and testing environment. This is mandatory because the project requires testing against Windows Defender and understanding Windows file system behavior. Ensure proper isolation to prevent unintended consequences.

**For Windows/Linux users:**

- Install [VirtualBox](https://www.virtualbox.org/) (free) or [VMware Workstation](https://www.vmware.com/products/workstation-pro.html).
- Download a [Windows 10/11 ISO](https://www.microsoft.com/software-download/windows11) and create a Windows VM.
- Ensure network isolation by using "Host-Only" or "Internal Network" mode.

**For Apple Silicon (M1/M2/M3/M4) users:**

- Install [UTM](https://mac.getutm.app/) (free) or [Parallels Desktop](https://www.parallels.com/) (paid).
- Download [Windows 11 ARM](https://www.microsoft.com/en-us/software-download/windowsinsiderpreviewarm64) from Microsoft's Insider Preview program.
- Create a **Windows 11 ARM** VM using UTM or Parallels.
- Ensure network isolation by configuring network settings appropriately.

> **Note:** VirtualBox does not support Apple Silicon. Apple Silicon users **must** use UTM or Parallels with Windows 11 ARM. A standard Windows x86/x64 ISO will not work on Apple Silicon.

> **Important:** Ensure that the environment is isolated to prevent accidental damage or spread of the ransomware!

#### The Challenge

1. **Ransomware Development**:
   - Develop a ransomware program that encrypts all files.
   - Place a text file on the desktop with the following message:
     ```
     All of your files have been encrypted.
     To unlock them, contact me with your encryption code at email@email.com.
     Your encryption code is: {randomly_generated_code}
     ```
   - Generate a unique random encryption code for each affected system.

2. **Decryption Program**:
   - Develop a decryption program that uses the encryption code to restore the encrypted files.
   - Ensure the decryption program works reliably for each affected system based on their encryption code.

3. **Detection Avoidance**:
   - Your ransomware program must use advanced techniques to avoid detection by antivirus software.
   - Ensure the ransomware bypasses detection in **Windows Defender** and more than 80% of security vendors on [VirusTotal](https://www.virustotal.com/).

### Documentation

Create a `README.md` file that includes:

- **Ransomware Program Overview**: Explain how your program works and its intended functionality.
- **Decryption Program Overview**: Describe how the decryption program works and how it interacts with the encryption tool.
- **Technical Explanation**: Provide details on the encryption algorithm used, how the encryption code is generated, and how files are decrypted.
- **Testing and Usage Instructions**: Include clear instructions for testing the ransomware and decryption tools in the virtual machine.
- **Defensive Recommendations**: Explain how organizations can detect and defend against ransomware attacks.
- **Ethical and Legal Report**: Discuss the ethical responsibilities of developing ransomware simulations and the importance of using such knowledge to improve security defenses.

### Bonus

If you complete the mandatory part successfully, and you still have free time, you can implement additional features, such as:

- **Multiple File Type Support**: Expand the ransomware to encrypt multiple file types (e.g., images, videos).
- **Stealth Techniques**: Implement advanced techniques to improve ransomware stealth.
- **Custom Encryption Algorithms**: Develop your own encryption algorithm for enhanced security.
- **Detection Tool**: Build a companion tool that detects the ransomware techniques you implemented.

Challenge yourself!

### Ethical and Legal Considerations

This project is for educational purposes only. The skills you learn here are the same skills used by:

- **Red Team Professionals** who help organizations test their ransomware defenses.
- **Malware Analysts** who reverse-engineer ransomware to develop decryption tools for victims.
- **Security Researchers** who discover ransomware vulnerabilities and help law enforcement.
- **Incident Responders** who analyze ransomware during active attacks to contain and remediate threats.

You are responsible for ensuring all ransomware testing is conducted within a secure, isolated environment. Do not use or share ransomware outside of this project. Misuse of these techniques is strictly prohibited and may violate local laws.

> **Disclaimer**: This project is for educational purposes only. Unauthorized use of these techniques is prohibited and may be illegal.

> **Disclaimer**: Unauthorized development or deployment of ransomware outside of this controlled project environment is strictly prohibited. Misuse may result in severe legal consequences.

### Submission and Audit

Submit the following:

- Source code for both the ransomware and decryption programs.
- `README.md` file with detailed documentation.

Ensure that your virtualization software (VirtualBox, VMware, UTM, or Parallels) is installed and your **Windows VM** is ready for the audit demonstration.

### Resources

Some useful resources:

- [Windows Cryptographic Functions](https://docs.microsoft.com/en-us/windows/win32/api/bcrypt/): Learn about cryptographic APIs in Windows.
- [File Management Functions](https://docs.microsoft.com/en-us/windows/win32/fileio/file-management-functions): Understand file manipulation in Windows.
- [VirusTotal](https://www.virustotal.com/): Check your ransomware against antivirus detections.
- [Microsoft Security Basics](https://docs.microsoft.com/en-us/windows/security/): Learn about Windows security features.
- [VirtualBox Downloads](https://www.virtualbox.org/): Virtualization for Windows/Linux users.
- [UTM for macOS](https://mac.getutm.app/): Free virtualization for Apple Silicon users.
- [Windows 11 ARM Download](https://www.microsoft.com/en-us/software-download/windowsinsiderpreviewarm64): Windows for Apple Silicon users.
- [MITRE ATT&CK - Ransomware](https://attack.mitre.org/techniques/T1486/): Understanding ransomware tactics for better defense.
- [No More Ransom Project](https://www.nomoreransom.org/): Learn how security professionals help ransomware victims.
