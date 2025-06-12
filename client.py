import os
import json
import requests
from dotenv import load_dotenv
import time
import csv
import urllib.parse

class BuiltWithClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('BUILTWITH_API_KEY')
        self.base_url = 'https://api.builtwith.com/lists11/api.json'
        self.technologies = self.load_technologies()

    def load_technologies(self):
        """Load technologies from local JSON file"""
        json_path = os.path.join('data', 'technologies.json')
        with open(json_path, 'r') as f:
            return json.load(f)['technologies']

    def list_technologies(self):
        """Display available technologies with index numbers"""
        for idx, tech in enumerate(self.technologies, 1):
            print(f"[{idx}] {tech['name']} ({tech['RequestName']})")
            
    def get_technology_data(self, tech_index, offset=''):
        """Get data for a specific technology"""
        if not 1 <= tech_index <= len(self.technologies):
            raise ValueError("Invalid technology index")
            
        tech = self.technologies[tech_index - 1]
    
        # Construct URL manually to avoid double encoding
        url = f"{self.base_url}?KEY={self.api_key}&TECH={tech['RequestName']}&META=yes"
    
        # Add offset if provided (without additional encoding)
        if offset and offset != 'END':
            url += f"&OFFSET={offset}"

        # Print URL for debugging
        print(f"\nRequesting URL: {url}")
        
        # Make the request with the manually constructed URL
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"API Error (Status {response.status_code}): {response.text}")
        
        try:
            data = response.json()
        except ValueError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

        # Save raw JSON response for backup
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        self._save_raw_response(tech['RequestName'], data, timestamp)
        
        return data

    def _save_raw_response(self, tech_name, data, timestamp):
        """Save raw API response as JSON backup"""
        os.makedirs('data/raw', exist_ok=True)
        
        # Save JSON file with timestamp
        filename = f"data/raw/{tech_name}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Saved raw data to {filename}")

    def save_results_to_csv(self, data, tech_name, create_new=False):
        """Save API results to CSV file"""
        if not data or 'Results' not in data:
            raise ValueError("Invalid data format")
            
        os.makedirs('data/csv', exist_ok=True)
        
        # Add timestamp to filename to keep all versions
        timestamp = time.strftime('%Y%m%d')
        filename = f"data/csv/{tech_name}_{timestamp}.csv"
        
        mode = 'a'  # Always append to preserve all data
        file_exists = os.path.exists(filename)
        
        with open(filename, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow([
                    'Timestamp',          # When this batch was saved
                    'Domain',             # D
                    'Social',            # META.Social
                    'CompanyName',       # META.CompanyName
                    'Telephones',        # META.Telephones
                    'Emails',            # META.Emails
                    'City',              # META.City
                    'State',             # META.State
                    'Postcode',          # META.Postcode
                    'Country',           # META.Country
                    'Vertical',          # META.Vertical
                    'Titles',            # META.Titles
                    'FirstDetected',     # FD
                    'LastDetected',      # LD
                    'FirstIndexed',      # FI
                    'LastIndexed',       # LI
                    'Score',             # S
                    'Rank',             # R
                    'BatchOffset'        # Offset used for this batch
                ])

            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            results = data.get('Results', [])
            
            for result in results:
                if not isinstance(result, dict):
                    continue
                    
                meta = result.get('META') or {}
                if meta is None:
                    meta = {}
                    
                row = [
                    current_time,  # Add timestamp to each row
                    result.get('D', ''),
                    '|'.join(filter(None, meta.get('Social', []) or [])),
                    meta.get('CompanyName', ''),
                    '|'.join(filter(None, meta.get('Telephones', []) or [])),
                    '|'.join(filter(None, meta.get('Emails', []) or [])),
                    meta.get('City', ''),
                    meta.get('State', ''),
                    meta.get('Postcode', ''),
                    meta.get('Country', ''),
                    meta.get('Vertical', ''),
                    '|'.join(filter(None, meta.get('Titles', []) or [])),
                    result.get('FD', ''),
                    result.get('LD', ''),
                    result.get('FI', ''),
                    result.get('LI', ''),
                    result.get('S', ''),
                    result.get('R', ''),
                    data.get('NextOffset', '')  # Add offset to track batches
                ]
                writer.writerow(row)

        print(f"Saved {len(results)} results to {filename}")
        return data.get('NextOffset', 'END')

    def _save_offset(self, tech_name, offset):
        """Save the offset for a technology to track progress"""
        os.makedirs('data/offsets', exist_ok=True)
        offset_file = f'data/offsets/{tech_name}.txt'
        
        # Store the raw offset value without any modifications
        with open(offset_file, 'w', encoding='utf-8') as f:
            f.write(str(offset))
        
        print(f"Saved offset: {offset}")

    def get_saved_offset(self, tech_name):
        """Get the saved offset for a technology"""
        offset_file = f'data/offsets/{tech_name}.txt'
        if os.path.exists(offset_file):
            with open(offset_file, 'r') as f:
                return f.read().strip()
        return ''