# BuiltWith Data Downloader

A Python application to download technology stack data from BuiltWith API.

## Setup

1. Clone the repository
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file and add your BuiltWith API key:
```
BUILTWITH_API_KEY=your_api_key_here
```

## Usage

Run the main script:
```bash
python src/main.py
```

The script will:
1. Fetch data for specified domains from BuiltWith API
2. Process the response
3. Save the results in the `data` directory as JSON files

## Testing

Run the tests:
```bash
python -m unittest tests/test_client.py
```