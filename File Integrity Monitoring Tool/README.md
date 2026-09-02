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

The Cargo.toml file contains dependency version the program needs.

An empty folder labelled test_directory is attached in the program folder. New files can be created in here to test the functionality of the program.

## How To Run:
1. Ensure integrity_log.csv exist
2. Ensure Rust and Cargo are installed to run the rust file.
3. Ensure test_directory folder exists.
4. Run the main.rs code.
5. Make changes to the test_directory folder with new files.
6. Repeat step 4 and 5 to test different functionalities.

## System Screenshot

