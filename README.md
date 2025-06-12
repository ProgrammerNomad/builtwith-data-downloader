# BuiltWith Data Downloader

A Python application to download technology stack data from BuiltWith API with automatic pagination support.

## Setup

1. Clone the repository
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file and add your BuiltWith API key:
```properties
BUILTWITH_API_KEY=your_api_key_here
```
4. Ensure you have the `data/technologies.json` file with your target technologies:
```json
{
  "technologies": [
    {
      "RequestName": "Shopify"
    },
    {
      "RequestName": "Magento"
    }
  ]
}
```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. List available technologies from your technologies.json
2. Let you select a technology to download data for
3. Automatically fetch all pages of data using the API's pagination
4. Save results to CSV files in the `data/csv` directory
5. Store raw API responses in the `data/raw` directory for backup

### Features

- Automatic pagination handling
- Retry mechanism for failed requests
- CTRL+C support for graceful stopping
- CSV output with detailed website information
- Raw JSON backups of all API responses

### CSV Output Format

The CSV files include the following columns:
- Domain
- Social Links
- Company Name
- Telephone Numbers
- Email Addresses
- City
- State
- Postcode
- Country
- Vertical
- Titles
- First/Last Detection Dates
- First/Last Index Dates
- Score
- Rank

## Directory Structure

```
builtwith-data-downloader/
├── data/
│   ├── csv/           # CSV output files
│   ├── raw/           # Raw JSON responses
│   └── technologies.json
├── client.py          # API client implementation
├── main.py           # Main script
└── .env              # API key configuration
```

## Error Handling

- Automatic retry on failed requests (up to 3 attempts)
- 5-second delay between retries
- Clear error messages and progress reporting
- Graceful exit support with CTRL+C

## Notes

- API requests are rate-limited with a 2-second delay between successful requests
- Large datasets may take significant time to download completely
- Use CTRL+C to stop the download process at any time