#### General

##### Check the Repo Content

Files that must be present in the repository:

- Source code for both the ransomware and decryption programs.
- Detailed documentation in the `README.md` file containing program overviews, technical explanations, testing instructions, and ethical considerations.

###### Are all the required files present?

##### Verify Setup

Confirm that the student is using an isolated **Windows-based virtual machine** for development and testing. This is required because the project involves testing against Windows Defender and understanding Windows file system behavior.

**For Windows/Linux users:**

1. Verify VirtualBox or VMware is installed and running.
2. Confirm the student is using a Windows 10/11 VM.
3. Ensure network isolation is configured (Host-Only or Internal Network mode).

**For Apple Silicon (M1/M2/M3/M4) users:**

1. Verify UTM or Parallels is installed and running.
2. Confirm the student is using a **Windows 11 ARM** VM (not Linux or macOS).
3. Ensure network isolation is configured appropriately.

> **Note:** VirtualBox does not support Apple Silicon. Apple Silicon users must use UTM or Parallels with Windows 11 ARM. A standard Windows x86/x64 ISO will not work on Apple Silicon.

###### Is virtualization software (VirtualBox, VMware, UTM, or Parallels) properly installed?

###### Is the student using an isolated Windows-based virtual machine?

###### Is the environment properly isolated from the host system and external networks?

##### Play the Role of a Stakeholder

Conduct a simulated scenario where the student acts as a **Malware Developer** presenting their ransomware simulation to a hypothetical team of stakeholders. Evaluate their understanding, communication skills, and depth of knowledge.

Suggested questions include:

- What is ransomware, and how does it operate on a system?
- How does your ransomware encrypt files and generate the unique encryption code?
- How does your decryption program restore the encrypted files?
- What techniques did you use to bypass antivirus detections?
- What ethical considerations should be addressed when working with ransomware simulations?
- How can organizations protect themselves against ransomware attacks?

###### Did the student demonstrate a thorough understanding of ransomware mechanics and encryption techniques?

###### Was the student able to communicate effectively and explain their programs?

###### Did the student discuss the ethical and real-world implications of ransomware?

###### Was the student able to justify their program's design and implementation?

##### Review the Student Documentation

Verify that the `README.md` file contains:

- **Ransomware Program Overview**: Explanation of how the ransomware operates.
- **Decryption Program Overview**: Description of how the decryption program restores encrypted files.
- **Technical Explanation**: Details about encryption, code generation, and decryption logic.
- **Testing and Usage Instructions**: Clear steps for safely testing the ransomware and decryption tools in a secure environment.
- **Defensive Recommendations**: Explanation of how organizations can detect and defend against ransomware.
- **Ethical and Legal Report**: Discussion of ethical responsibilities and legal considerations.

###### Does the documentation provide a clear and complete overview of the ransomware and decryption programs?

###### Are the technical details of encryption and decryption well-explained?

###### Does the documentation explain whether the student used symmetric-only encryption (e.g., AES) or a hybrid model (e.g., AES + RSA)?

###### Does the documentation explain why the chosen encryption model was selected and its security implications (e.g., why hybrid encryption prevents key extraction from binary memory)?

###### Does the documentation include defensive recommendations for organizations?

###### Does the documentation highlight the importance of ethical and legal practices?

##### Check the Detection Avoidance

Scan the ransomware program in **Windows Defender** and **VirusTotal**.

###### Does the ransomware bypass detection in Windows Defender?

###### Does the ransomware bypass detection in more than 80% of security vendors on VirusTotal?

##### Check the File Encryption

Create files with random data in the virtual machine and run the ransomware program.

###### Does the ransomware encrypt all files in the specified directory or with the targeted extension?

###### Does the ransomware create a text file on the desktop with the encryption code and contact information?

##### Check the File Decryption

Test the decryption program to ensure it works dynamically and does not rely on hardcoded keys.

1. **Dynamic Key Derivation Test:**
   - Run the decryption program and provide the encryption code as input.
   - The decryption program should accept the randomly generated code and use it to derive the decryption key.

###### Does the decryption program accept the encryption code as input (not hardcoded)?

###### Does the decryption program successfully restore all encrypted files using the provided encryption code?

###### Can the decryption program work on different systems with different encryption codes (proving it's dynamic, not machine-specific)?

##### Manual Verification and Cryptographic Architecture

Ask the student to explain how the encryption code is generated and used. Verify that the encryption code is random and unique for each affected system.

Additionally, ask the student to explain their cryptographic approach:

- **Symmetric-only (e.g., AES with password-derived key)**: Simpler but vulnerable to key extraction from binary memory.
- **Hybrid model (e.g., AES for file encryption + RSA for key encryption)**: More secure as the private key is never stored on the victim's machine.

###### Is the encryption code unique for each affected system?

###### Is the encryption code generation method random and effective?

###### Can the student explain whether they used symmetric-only or hybrid encryption?

###### Does the student understand why a hybrid model (AES + RSA) is more secure and prevents key extraction from the binary's memory?

###### If using symmetric-only encryption, does the student acknowledge its limitations and potential vulnerabilities?

#### Bonus

###### + Did the student extend the ransomware functionality to support multiple file types?

###### + Did the student implement advanced stealth techniques?

###### + Did the student develop a custom encryption algorithm?

###### + Did the student implement a hybrid encryption model (AES + RSA) for enhanced security?

###### + Did the student build a detection tool for the ransomware techniques they implemented?

###### + Is this project an outstanding submission that exceeds the basic requirements?
