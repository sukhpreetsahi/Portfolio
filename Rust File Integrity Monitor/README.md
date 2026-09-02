# File Integrity Monitoring Tool
This project develops a cybersecurity tool using the Rust programming language to monitor the integrity of files within the chosen directory and its subdirectories. It detects changes by storing a snapshot of files and comparing them across runs.

This tool is crucial for organisations, as suspicious changes can be detected and attacks could be stopped earlier.

## Key Features
1. Detection of file creation.
2. Detection of file deletion.
3. Detection of file modification (by comparing the SHA-256 hash value).
4. Detection of possible renames (if size and hashes stay the same, but a file seems to be deleted and a new one is created).

---
The folder should consist of the main.rs code file. In this file, the directory to be searched can be set on line 245. (Currently set to search the test_directory folder.)

An empty integrity log file with headers (integrity_log.csv) will also be attached.

The Cargo.toml file contains the dependency version the program needs.

An empty folder labelled test_directory is attached in the program folder. New files can be created in here to test the functionality of the program.

## How To Run:
1. Ensure integrity_log.csv exist
2. Ensure Rust and Cargo are installed to run the rust file.
3. Ensure test_directory folder exists.
4. Run the main.rs code.
5. Make changes to the test_directory folder with new files.
6. Repeat step 4 and 5 to test different functionalities.

## System Screenshot
<img width="561" height="164" alt="blank" src="https://github.com/user-attachments/assets/e77fe36a-6229-4627-a366-c9d54ccb443a" />
<img width="531" height="153" alt="delete" src="https://github.com/user-attachments/assets/9104e7a5-9af7-4950-994d-ff9e5b42a059" />
<img width="703" height="355" alt="modified" src="https://github.com/user-attachments/assets/63e68e62-351f-4a0b-8537-8f71391b7c5a" />
<img width="630" height="201" alt="rename" src="https://github.com/user-attachments/assets/8b3ec77b-7a66-48c6-9fd2-2285a5c4a1b4" />


