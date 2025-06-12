from client import BuiltWithClient
import time
import os
import signal
import sys

def signal_handler(sig, frame):
    print('\nCTRL+C detected. Gracefully stopping...')
    sys.exit(0)

def main():
    # Setup CTRL+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    client = BuiltWithClient()
    
    print("\nAvailable Technologies:")
    client.list_technologies()
    
    try:
        choice = int(input("\nEnter technology number to download: "))
        tech = client.technologies[choice - 1]
        
        offset = ''  # Start with no offset
        first_batch = True
        max_retries = 3
        
        while True:
            retries = 0
            success = False
            
            while not success and retries < max_retries:
                try:
                    print(f"\nFetching data for {tech['name']}" + 
                          (f" (offset: {offset})" if offset else "..."))
                    
                    # Get data from API
                    data = client.get_technology_data(choice, offset)
                    
                    # Save results and get next offset
                    next_offset = client.save_results_to_csv(
                        data, 
                        tech['RequestName'],
                        create_new=first_batch
                    )
                    
                    # Check if we've reached the end (NextOffset is END)
                    if next_offset == 'END':
                        print(f"\nCompleted downloading data for {tech['name']}!")
                        return
                    
                    # Use the next_offset for subsequent requests
                    offset = next_offset
                    first_batch = False
                    success = True
                    
                    # Add delay between requests
                    time.sleep(2)
                    
                except Exception as e:
                    retries += 1
                    print(f"\nError during batch (attempt {retries}/{max_retries}): {str(e)}")
                    if retries < max_retries:
                        print("Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        print("\nMax retries reached. Use CTRL+C to stop or press Enter to continue anyway...")
                        input()
                        retries = 0  # Reset retries counter
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()