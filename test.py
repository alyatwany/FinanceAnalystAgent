import os
from bs4 import BeautifulSoup
import json
import requests
import time
import re

def get_sec_filings(formtype: str, ticker: str, amount: int):
    """
    Get the latest filings (10-K, 10-Q, 8-K) for a ticker.
    Returns a json.
    """
    
    cik = get_cik(ticker)
    if not cik:
        return json.dumps({"error": f"Could not find CIK for ticker {ticker}"})
    
    print(f"Found CIK {cik} for {ticker}")
    
    filings = get_filing_urls(cik, formtype, amount)
    
    if not filings:
        return json.dumps({"error": f"No {formtype} filings found for {ticker}"})
    
    print(f"Found {len(filings)} {formtype} filings")
    
    all_filings_json = []
    
    for filing in filings:
        print(f"Processing {filing['accession']}...")
        
        text = download_filing_text(filing, cik)
        
        filing_data = {
            "ticker": ticker,
            "formtype": formtype,
            "accession_number": filing['accession'],
            "filing_date": filing['filing_date'],
            "text": text
        }
        all_filings_json.append(filing_data)
        
        time.sleep(0.2)
    
    print(f"Successfully processed {len(all_filings_json)} filings")
    return json.dumps(all_filings_json, separators=(",", ":"))


def get_cik(ticker):
    """Get CIK number for a ticker symbol."""
    try:
        url = "https://www.sec.gov/files/company_tickers.json"
        headers = {'User-Agent': 'Mozilla/5.0 (bastion.reyniel@fontfee.com)'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for item in data.values():
            if item['ticker'].upper() == ticker.upper():
                return str(item['cik_str']).zfill(10)
        
        return None
    except Exception as e:
        print(f"Error getting CIK: {e}")
        return None


def get_filing_urls(cik, form_type, limit):
    """Get URLs for recent filings of a specific type."""
    try:
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        headers = {'User-Agent': 'Mozilla/5.0 (bastion.reyniel@fontfee.com)'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        filings = []
        recent_filings = data['filings']['recent']
        
        for i, form in enumerate(recent_filings['form']):
            if form == form_type:
                accession = recent_filings['accessionNumber'][i]
                filing_date = recent_filings['filingDate'][i]
                
                filings.append({
                    'accession': accession,
                    'filing_date': filing_date,
                })
                
                if len(filings) >= limit:
                    break
        
        return filings
    
    except Exception as e:
        print(f"Error getting filing URLs: {e}")
        return []


def download_filing_text(filing, cik):
    """Download filing and extract text from any HTML document found."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (bastion.reyniel@fontfee.com)'}
        
        accession_no_dash = filing['accession'].replace('-', '')
        txt_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dash}/{filing['accession']}.txt"
        
        print(f"  Downloading from: {txt_url}")
        response = requests.get(txt_url, headers=headers)
        response.raise_for_status()
        
        content = response.text
        
        # Split by <DOCUMENT> tags
        documents = re.split(r'<DOCUMENT>', content)
        
        all_text = []
        
        for doc in documents:
            if not doc.strip() or '</DOCUMENT>' not in doc:
                continue
            
            # Extract document content (everything before </DOCUMENT>)
            doc_content = doc.split('</DOCUMENT>')[0]
            
            # Check the filename - skip exhibits and XML files
            filename_match = re.search(r'<FILENAME>([^\n]+)', doc_content)
            if filename_match:
                filename = filename_match.group(1).strip().lower()
                # Skip exhibits, XML files, and certain other files
                if any(skip in filename for skip in ['ex-', '.xml', '.xsd', 'excel', 'graphic']):
                    continue
            
            # Look for HTML content
            html_match = re.search(r'<html.*?>(.*)</html>', doc_content, re.DOTALL | re.IGNORECASE)
            if html_match:
                html_content = html_match.group(0)
                
                # Parse and clean
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Remove unwanted tags
                for tag in soup(['script', 'style', 'head', 'meta', 'link', 'title']):
                    tag.decompose()
                
                # Also remove ix:hidden sections (inline XBRL hidden content)
                for tag in soup.find_all(attrs={'style': re.compile(r'display:\s*none', re.I)}):
                    tag.decompose()
                
                # Get text
                text = soup.get_text(separator='\n')
                
                # Clean up
                lines = []
                for line in text.splitlines():
                    line = line.strip()
                    # Skip empty lines, URLs, and CIK numbers
                    if (line and 
                        not line.startswith('http://') and 
                        not re.match(r'^\d{10}$', line) and
                        not line.startswith('xmlns') and
                        len(line) > 2):
                        lines.append(line)
                
                section_text = '\n'.join(lines)
                
                # Only add if it has substantial content
                if len(section_text) > 1000:
                    all_text.append(section_text)
        
        if all_text:
            combined = '\n\n--- DOCUMENT SECTION ---\n\n'.join(all_text)
            return combined
        else:
            return "No readable HTML content found in filing. May be inline XBRL only."
    
    except Exception as e:
        return f"Error downloading filing: {str(e)}"


# Test it
result = get_sec_filings("10-K", "AAPL", 2)  # Start with just 1 to test

filings = json.loads(result)
print(f"\n{'='*80}")
print(f"Retrieved {len(filings)} filings")
print(f"{'='*80}\n")

for i, filing in enumerate(filings, 1):
    print(f"Filing {i}:")
    print(f"  Accession: {filing['accession_number']}")
    print(f"  Date: {filing['filing_date']}")
    print(f"  Text length: {len(filing['text']):,} characters")
    print(f"\n  First 2000 characters:\n")
    print(filing['text'][:2000])
    print(f"\n{'-'*80}\n")