from happi import Client
from happi.errors import DuplicateError
def initialize_client():
    # Initialize the Happi client
    client = Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')

def location_group_change():
    device_name = input("Enter the location group: ")
    loc_code = device_name.split('_')[1]
    new_name = input("Enter the new device location code: ")
    
    # Search for entries by name 
    entries_to_modify = client.search(location_group=device_name)
    
    if not entries_to_modify:
    	print("No entries found for the search criteria.")
    else:
    	for entry in entries_to_modify:
    		try:
    			entry.item.ioc_alias=entry.item.ioc_alias.replace(loc_code.upper(), new_name.upper())
    			entry.item.save()
    			entry.item.ioc_base=entry.item.ioc_base.replace(loc_code.upper(), new_name.upper())
    			entry.item.save()
    			entry.item.prefix=entry.item.prefix.replace(loc_code.upper(), new_name.upper())
    			entry.item.save()
    			entry.item.ioc_name=entry.item.ioc_name.replace(loc_code.lower(), new_name.lower())
    			entry.item.save()
    			entry.item.location_group=entry.item.location_group.replace(loc_code.lower(), new_name.lower())
    			entry.item.save()
    			entry.item.name=entry.item.name.replace(loc_code.lower(), new_name.lower())
    			entry.item.save()
    		except DuplicateError as e:
    			print(f"An entry with the same name already exists: {e}")		
    		else:
    			print("Modification complete. Entries updated in the database.")
def main():
    initialize_client()
    location_group_change()

