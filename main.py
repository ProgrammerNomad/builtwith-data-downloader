from client import BuiltWithClient
import time
import os
import urllib.parse

def main():
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
        
        while True:
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
                
                print(f"Batch processed. Next offset: {next_offset}")
                first_batch = False
                
                # Check if we're done
                if next_offset == 'END':
                    print(f"\nCompleted downloading data for {tech['name']}!")
                    break
                
                # Use the next_offset for subsequent requests
                offset = next_offset
                
                # Add delay between requests
                time.sleep(2)
                
                # Ask user before continuing
                user_input = input("\nPress Enter to continue, or 'q' to quit: ")
                if user_input.lower() == 'q':
                    break
                
            except Exception as e:
                print(f"\nError during batch: {str(e)}")
                retry = input("Retry this batch? (y/n): ")
                if retry.lower() != 'y':
                    break
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()