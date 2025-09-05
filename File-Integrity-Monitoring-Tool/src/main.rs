use chrono::{DateTime, Local}; // For formatting date-time stamps
use csv; // For CSV file handling
use sha2::{Digest, Sha256}; // For hashing files
use std::collections::HashMap; // For structure for storing key information about files in logs
use std::fs::{self, File};
use std::io::Read;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use walkdir::WalkDir; // For directory traversal

// This stores the important information about each file
// Citation: [2]
#[derive(Debug, Clone)]
struct FileData {
    path: String,
    name: String,
    size: u64,
    modified: u64,
    hash: String,
}

impl FileData {
    // Create FileData from the file path, collecting data and hashing file content
    // Citation: [8]
    fn get_file_data(path: &Path) -> Option<Self> {
        let metadata = fs::metadata(path).ok()?;
        let modified = metadata.modified().ok()?; // Get the last modified time
        let modified_secs = Self::system_time_to_secs(modified);
        let size = metadata.len(); 
        let hash = Self::generate_hash(path); 

        Some(FileData {
            path: path.to_string_lossy().to_string(), // Converts the path to a string
            name: path.file_name()?.to_string_lossy().to_string(), // Gets the file name as a string
            size,
            modified: modified_secs,
            hash,
        })
    }

    // Get seconds since the Unix epoch for time calculations
    fn system_time_to_secs(time: SystemTime) -> u64 {
        time.duration_since(UNIX_EPOCH).unwrap_or_default().as_secs()    }

    // Converts SystemTime to a readable date and time string format
    // Citation: [3]
    fn format_time(&self) -> String {
        let datetime = DateTime::<Local>::from(UNIX_EPOCH + std::time::Duration::from_secs(self.modified));
        datetime.format("%Y-%m-%d %H:%M:%S").to_string()
    }

    // Create a SHA-256 hash of the file’s contents
    // Citation: [7]
    fn generate_hash(path: &Path) -> String {
        let mut file = match File::open(path) {
            Ok(file) => file,
            Err(_) => return String::new(), // Return empty string if file cannot be opened
        };
        
        let mut hasher = Sha256::new();
        let mut buffer = [0; 1024]; // Buffer for reading the file in chunks to avoid loading it all into memory

        loop {
            let content = match file.read(&mut buffer)  {
                Ok(n) => n,
                Err(_) => return String::new(), // Return empty string if read fails
            };
            if content == 0 {
                break;
            }
            hasher.update(&buffer[..content]); // Updates the hasher with the bytes read
        }

        format!("{:x}", hasher.finalize()) // Returns the hash as a lowercase hexadecimal string
    }

    // Check if file content is modified compared to another FileData
    fn is_modified(&self, other: &FileData) -> bool {
        self.hash != other.hash
    }

    // Return path as string
    fn path_str(&self) -> String {
        self.path.clone()
    }
}

// Scanning directories and collecting file data
struct DirectoryScanner {
    folder: PathBuf,
}

impl DirectoryScanner {
    fn new(folder: &str) -> Self {
        DirectoryScanner {
            folder: PathBuf::from(folder),
        }
    }

    // Scans the directory and returns a HashMap of FileData
    // Citation: [10]
    fn scan(&self) -> HashMap<String, FileData> {
        WalkDir::new(&self.folder)
            .into_iter()
            .filter_map(Result::ok) // Ignore errors
            .filter(|entry| entry.path().is_file()) // Only get files
            .filter_map(|entry| FileData::get_file_data(entry.path())) // Store FileData if possible
            .map(|file_data| (file_data.path_str(), file_data)) // Create map entries
            .collect()
    }
}

// Saving and loading file data logs to and from CSV
struct LogManager {
    filename: PathBuf,
}

impl LogManager {
    fn new(filename: &str) -> Self {
        LogManager {
            filename: PathBuf::from(filename),
        }
    }

    // Save the log HashMap to CSV file
    // Citation: [5]
    fn save(&self, log: &HashMap<String, FileData>) {
        let mut writer = csv::Writer::from_path(&self.filename).expect("Could not open log file to write");

        writer.write_record(&["path", "name", "size", "modified", "hash"]).expect("Failed to write CSV header");

        for file_data in log.values() {  // Loops through the HashMap
            writer
                .write_record(&[   // Writes data to the CSV file
                    &file_data.path_str(),
                    &file_data.name,
                    &file_data.size.to_string(),
                    &file_data.modified.to_string(),
                    &file_data.hash,
                ])
                .expect("Failed to write CSV record");
        }

        writer.flush().expect("Failed to flush CSV writer");
    }

    // Load the log from CSV file into a HashMap
    // Citation: [6]
    fn load(&self) -> HashMap<String, FileData> {
        let mut log = HashMap::new(); // Creates HashMap to store data about files

        if let Ok(mut reader) = csv::Reader::from_path(&self.filename) {
            // Tries to open the CSV file
            for record in reader.records() {
                // Loops through the records in the CSV file
                if let Ok(data) = record {
                    if data.len() == 5 {
                        let file_data = FileData {
                            // Creates a FileData struct to hold the data
                            path: data[0].to_string(),
                            name: data[1].to_string(),
                            size: data[2].parse().unwrap_or(0),
                            modified: data[3].parse().unwrap_or(0),
                            hash: data[4].to_string(),
                        };
                        log.insert(file_data.path_str(), file_data); // Inserts the data into the HashMap
                    }
                }
            }
        }

        log
    }
}

// Manages scanning, comparing and logging
struct IntegrityChecker {
    scanner: DirectoryScanner,
    log_manager: LogManager,
}

impl IntegrityChecker {
    fn new(folder: &str, log_file: &str) -> Self {
        IntegrityChecker {
            scanner: DirectoryScanner::new(folder),
            log_manager: LogManager::new(log_file),
        }
    }

    fn run(&self) {
        println!("\nScanning folder: {}\n", self.scanner.folder.to_string_lossy());

        // Load old log and scan current directory
        let old_log = self.log_manager.load();
        let new_log = self.scanner.scan();

        // Vectors to store created and deleted files
        let mut created_files = Vec::new();
        let mut deleted_files = Vec::new();

        // Detect created and modified files
        // Citation: [9]
        for (path, new_file) in &new_log {
            // Check for file in the old log
            match old_log.get(path) {
                None => {
                    println!("File created since last run: {}", path);
                    created_files.push(new_file);
                }
                // If the file exists in old log but its contents have changed
                Some(old_file) if new_file.is_modified(old_file) => {
                    println!(
                        "File modified since last run: {} at {}", path, new_file.format_time());
                }
                _ => {}
            }
        }

        // Detect deleted files
        for (path, old_file) in &old_log {
            if !new_log.contains_key(path) {
                println!("File deleted since last run: {}", path);
                deleted_files.push(old_file);
            }
        }

        // Detect likely renames by matching created and deleted files with same hash and size
        for old_file in &deleted_files {
            for new_file in &created_files {
                if old_file.hash == new_file.hash && old_file.size == new_file.size {
                    println!("Likely renamed: {} To {}", old_file.path_str(), new_file.path_str());
                }
            }
        }

        // Save the new log to CSV
        self.log_manager.save(&new_log);
        print!("\n No other changes detected.\n");
        println!("\nLog saved.\n");
    }
}

// Main function to run the integrity checker
fn main() {
    let folder = "test_directory";
    let log_file = "integrity_log.csv";

    let checker = IntegrityChecker::new(folder, log_file);
    checker.run();
}
