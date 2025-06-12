from client import BuiltWithClient
from website import Website
import os

def main():
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    client = BuiltWithClient()

    # Example domains to scan
    domains = [
        'example.com',
        'google.com',
        # Add more domains here
    ]

    results = []
    for domain in domains:
        try:
            data = client.get_website_data(domain)
            website = Website(
                domain=domain,
                technologies=data.get('Results', [{}])[0].get('Result', []),
                meta=data.get('Meta', {})
            )
            results.append(website.__dict__)
        except Exception as e:
            print(f"Error processing {domain}: {str(e)}")

    # Save all results to JSON file
    client.save_to_json(results, 'websites.json')

if __name__ == "__main__":
    main()