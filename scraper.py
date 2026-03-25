#!/usr/bin/env python3
"""
IBM Planning Analytics Workspace Feature Scraper
Scrapes feature information from IBM support pages and exports to CSV/Excel
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class IBMFeatureScraper:
    """Scraper for IBM Planning Analytics Workspace feature pages"""
    
    def __init__(self, url: str, delay: float = 2.0):
        """
        Initialize the scraper
        
        Args:
            url: Target URL to scrape
            delay: Delay between requests in seconds (default: 2.0)
        """
        self.url = url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Fetch HTML content from URL with retry logic
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            
        Returns:
            HTML content as string or None if failed
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching URL: {url} (Attempt {attempt + 1}/{max_retries})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                logger.info(f"Successfully fetched page (Status: {response.status_code})")
                time.sleep(self.delay)  # Rate limiting
                return response.text
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page (Attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries reached. Failed to fetch page.")
                    return None
    
    def parse_table(self, html: str) -> List[Dict]:
        """
        Parse HTML table content
        
        Args:
            html: HTML content as string
            
        Returns:
            List of dictionaries containing table data
        """
        soup = BeautifulSoup(html, 'lxml')
        data = []
        
        # Find all tables on the page
        tables = soup.find_all('table')
        logger.info(f"Found {len(tables)} table(s) on the page")
        
        if not tables:
            logger.warning("No tables found on the page")
            return data
        
        # Process the first table (or modify to process all tables)
        for table_idx, table in enumerate(tables):
            logger.info(f"Processing table {table_idx + 1}")
            
            # Extract headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            else:
                # Try to get headers from first row if no thead
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            
            logger.info(f"Table headers: {headers}")
            
            # Extract rows
            tbody = table.find('tbody')
            rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]  # Skip header row
            
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_data = {}
                    for idx, cell in enumerate(cells):
                        header = headers[idx] if idx < len(headers) else f"Column_{idx + 1}"
                        row_data[header] = cell.get_text(strip=True)
                    
                    data.append(row_data)
            
            logger.info(f"Extracted {len(rows)} rows from table {table_idx + 1}")
        
        return data
    
    def extract_metadata(self, html: str) -> Dict:
        """
        Extract page metadata
        
        Args:
            html: HTML content as string
            
        Returns:
            Dictionary containing metadata
        """
        soup = BeautifulSoup(html, 'lxml')
        metadata = {
            'title': '',
            'description': '',
            'last_updated': '',
            'keywords': ''
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)
        
        # Extract meta tags
        meta_tags = {
            'description': soup.find('meta', attrs={'name': 'description'}),
            'keywords': soup.find('meta', attrs={'name': 'keywords'}),
            'date': soup.find('meta', attrs={'name': 'dcterms.date'})
        }
        
        for key, tag in meta_tags.items():
            if tag and tag.get('content'):
                if key == 'date':
                    metadata['last_updated'] = tag.get('content')
                else:
                    metadata[key] = tag.get('content')
        
        logger.info(f"Extracted metadata: {metadata['title']}")
        return metadata
    
    def scrape(self) -> tuple[List[Dict], Dict]:
        """
        Main scraping method
        
        Returns:
            Tuple of (data list, metadata dict)
        """
        logger.info("=" * 60)
        logger.info("Starting scraping process")
        logger.info("=" * 60)
        
        html = self.fetch_page(self.url)
        if not html:
            logger.error("Failed to fetch page content")
            return [], {}
        
        metadata = self.extract_metadata(html)
        data = self.parse_table(html)
        
        logger.info(f"Scraping complete. Extracted {len(data)} records")
        return data, metadata
    
    def save_to_csv(self, data: List[Dict], filename: str = None):
        """
        Save data to CSV file
        
        Args:
            data: List of dictionaries to save
            filename: Output filename (default: auto-generated)
        """
        if not data:
            logger.warning("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ibm_features_{timestamp}.csv"
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Data saved to CSV: {filename}")
            logger.info(f"Total records: {len(df)}")
            logger.info(f"Columns: {', '.join(df.columns)}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_to_excel(self, data: List[Dict], metadata: Dict, filename: str = None):
        """
        Save data to Excel file with metadata sheet
        
        Args:
            data: List of dictionaries to save
            metadata: Metadata dictionary
            filename: Output filename (default: auto-generated)
        """
        if not data:
            logger.warning("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ibm_features_{timestamp}.xlsx"
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Write main data
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name='Features', index=False)
                
                # Write metadata
                meta_df = pd.DataFrame([metadata])
                meta_df.to_excel(writer, sheet_name='Metadata', index=False)
                
                # Add scraping info
                info_data = {
                    'Scraped Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Source URL': [self.url],
                    'Total Records': [len(df)]
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='Scraping Info', index=False)
            
            logger.info(f"Data saved to Excel: {filename}")
            logger.info(f"Total records: {len(df)}")
            logger.info(f"Columns: {', '.join(df.columns)}")
        except Exception as e:
            logger.error(f"Error saving to Excel: {e}")


def main():
    """Main execution function"""
    # Target URL
    url = "https://www.ibm.com/support/pages/node/6999675"
    
    # Initialize scraper
    scraper = IBMFeatureScraper(url, delay=2.0)
    
    # Scrape data
    data, metadata = scraper.scrape()
    
    if data:
        # Save to both CSV and Excel
        scraper.save_to_csv(data)
        scraper.save_to_excel(data, metadata)
        
        # Display summary
        print("\n" + "=" * 60)
        print("SCRAPING SUMMARY")
        print("=" * 60)
        print(f"Page Title: {metadata.get('title', 'N/A')}")
        print(f"Last Updated: {metadata.get('last_updated', 'N/A')}")
        print(f"Total Records Extracted: {len(data)}")
        if data:
            print(f"Columns: {', '.join(data[0].keys())}")
        print("=" * 60)
    else:
        logger.error("No data was extracted. Please check the logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
