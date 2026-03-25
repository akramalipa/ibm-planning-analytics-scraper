# IBM Planning Analytics Workspace Feature Scraper

A Python web scraper designed to extract feature information from IBM Planning Analytics Workspace support pages and export the data to CSV and Excel formats.

## Features

- ✅ Scrapes IBM support pages with table data
- ✅ Extracts page metadata (title, description, last updated date)
- ✅ Exports data to both CSV and Excel formats
- ✅ Comprehensive error handling and retry logic
- ✅ Rate limiting to respect website policies
- ✅ Detailed logging for debugging and monitoring
- ✅ Automatic timestamp-based file naming

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this project**

2. **Run the setup script** (Unix/Linux/macOS):
   ```bash
   cd web-scraper-project
   chmod +x setup_environment.sh
   ./setup_environment.sh
   ```

   For Windows, manually create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Activate the virtual environment**:
   - Unix/Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python scraper.py
```

This will:
- Scrape the IBM Planning Analytics Workspace feature page
- Generate two output files with timestamps:
  - `ibm_features_YYYYMMDD_HHMMSS.csv`
  - `ibm_features_YYYYMMDD_HHMMSS.xlsx`
- Create a log file: `scraper.log`

### Output Files

#### CSV File
Contains the scraped table data in comma-separated format, suitable for data analysis and processing.

#### Excel File
Contains three sheets:
1. **Features**: Main table data
2. **Metadata**: Page metadata (title, description, last updated)
3. **Scraping Info**: Scraping timestamp, source URL, and record count

### Customization

To scrape a different URL, modify the `url` variable in the `main()` function:

```python
def main():
    url = "https://your-target-url.com"
    scraper = IBMFeatureScraper(url, delay=2.0)
    # ... rest of the code
```

To adjust the delay between requests (default is 2 seconds):

```python
scraper = IBMFeatureScraper(url, delay=3.0)  # 3 second delay
```

## Project Structure

```
web-scraper-project/
├── scraper.py              # Main scraper script
├── requirements.txt        # Python dependencies
├── setup_environment.sh    # Setup script for Unix/Linux/macOS
├── README.md              # This file
├── venv/                  # Virtual environment (created after setup)
├── scraper.log            # Log file (created when running)
└── ibm_features_*.csv     # Output CSV files (created when running)
└── ibm_features_*.xlsx    # Output Excel files (created when running)
```

## Dependencies

- **requests**: HTTP library for fetching web pages
- **beautifulsoup4**: HTML parsing library
- **lxml**: Fast XML/HTML parser
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file handling
- **matplotlib**: Data visualization (optional)
- **seaborn**: Statistical data visualization (optional)

## Logging

The scraper creates a `scraper.log` file with detailed information about:
- Page fetching attempts and results
- Number of tables and rows found
- Extraction progress
- Errors and warnings
- File save operations

## Error Handling

The scraper includes robust error handling:
- **Retry Logic**: Automatically retries failed requests up to 3 times
- **Timeout Protection**: 30-second timeout for HTTP requests
- **Rate Limiting**: Configurable delay between requests
- **Graceful Degradation**: Continues processing even if some elements fail

## Best Practices

1. **Respect robots.txt**: Always check the website's robots.txt file
2. **Rate Limiting**: Use appropriate delays between requests (default: 2 seconds)
3. **User Agent**: The scraper uses a standard browser user agent
4. **Error Monitoring**: Check `scraper.log` for any issues
5. **Data Validation**: Review output files to ensure data quality

## Troubleshooting

### Import Errors
If you see import errors, ensure the virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### No Data Extracted
- Check `scraper.log` for detailed error messages
- Verify the target URL is accessible
- Ensure the page structure hasn't changed

### Connection Errors
- Check your internet connection
- Verify the URL is correct
- The scraper will automatically retry failed requests

## License

This project is for educational and personal use. Always respect website terms of service and robots.txt files.

## Author

Created with Bob - AI Software Engineer

---

**Note**: This scraper is designed for the IBM Planning Analytics Workspace support page. For other websites, you may need to modify the parsing logic in the `parse_table()` method.