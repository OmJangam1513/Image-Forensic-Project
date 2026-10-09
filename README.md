# 🔍 Digital Image Forensics Tool

A Python-based digital forensics application built with **Streamlit** to analyze digital images and identify potential signs of image manipulation. The tool extracts image metadata (EXIF), calculates cryptographic hashes, performs Error Level Analysis (ELA), analyzes pixel intensity statistics, and generates downloadable forensic reports.

## 🚀 Features

- **Image Upload:** Upload images in supported formats for forensic analysis.
- **Metadata Extraction:** Extract image properties, including format, dimensions, color mode, and available EXIF metadata.
- **Hash Generation:** Calculate MD5 and SHA-256 hashes for file integrity verification.
- **Error Level Analysis (ELA):** Highlight compression differences in JPEG images for further investigation.
- **Pixel Analysis:** Calculate mean, minimum, and maximum pixel intensity values.
- **Forensic Reports:** Generate and download detailed JSON reports containing analysis results.
- **Interactive Interface:** User-friendly web interface powered by Streamlit.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Streamlit** – Web application interface
- **Pillow (PIL)** – Image processing and metadata extraction
- **NumPy** – Pixel intensity analysis
- **Hashlib** – Cryptographic hash generation
- **JSON** – Forensic report generation

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd Digital_Image_Forensics
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL displayed in the terminal to access the application.

## 📂 Project Structure

```text
Digital_Image_Forensics/
├── app.py
├── forensics.py
└── requirements.txt
```

## ⚠️ Disclaimer

This tool is intended for educational and investigative purposes. ELA results and metadata inconsistencies are indicators for further examination and do not independently prove image manipulation. Reliable forensic conclusions require additional evidence and validation.

## 👨‍💻 Author

**Om Jangam**
