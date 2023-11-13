
from happi import Client

location_data={"lm1k4":"IP1","lm2k4":"DREAM","lm2k2":"chemRIXS", "lm1k2":"qRIXS"}

def add_location(location_code, location_name):
	if location_code not in location_data:
		location_data[location_code]=location_name
		print(f"Location '{location_name}' with code '{location_code}' added successfully.")
	else:
		print(f"Location code '{location_code}' already exists. Please choose a different code.")



# Define the get_boolean_input function first
def get_boolean_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ('true', 't', 'yes', 'y'):
            return True
        elif user_input in ('false', 'f', 'no', 'n'):
            return False
        else:
            print("Invalid input. Please enter 'true/t/yes/y' or 'false/f/no/n'.")
            return get_boolean_input(prompt)

#def main():
#	# Initialize the Happi client
#	client = Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
#	
#	# Ask the user for the device name
#	device_name = input("Enter the device name: ")
#	active_status(device_name)


def active_status(device_name):
	# Search for devices by name
	devices = client.search(name=device_name)
	
	if not devices:
	    print(f"No devices found with the name '{device_name}'.")
	else:
		for device in devices:
	       		 print(type(device))
	       		 #print(device.__dict__)
	       		 # Display the current 'Active' status
	       		 try:
	       		 	current_active_status = device['active']
	       		 	print(f"Current 'Active' status for '{device_name}': {current_active_status}")
	       		 except KeyError:
	       		 	print(f"No 'Active' status found for '{device_name}'.")
	
	       		 # Ask the user for the new 'Active' status
	       		 new_active_status = get_boolean_input(f"Set 'Active' status (true/false) for '{device_name}': ")
	
	       		 if new_active_status in [True, False]:
	       		     # Update the 'Active' status in the database
	       		     if 'active' in device:
	       		         device.item.active = new_active_status
	       		         device.item.save()
	       		         print(f"'Active' status for '{device_name}' set to {new_active_status}.")
	       		     else:
	       		         print(f"'Active' status not found for '{device_name}'.")
	       		 else:
	       		     print(f"Invalid input for '{device_name}'. Please enter 'true/t/yes/y' or 'false/f/no/n'.")
def validate_entry(device_name):
	# check ensures same name is mentioned in all fields of the entry
	entries_to_modify= client.search(name=device_name)
	loc_code= entries_to_modify.split('_')[0]
	if loc_code not in location_data:
		print(f"Invalid location code: device name not found in dict. Please add")
	else:
		for entry in entries_to_modify:
			try:
				cat_ioc_alias=entry.item.ioc-alias.split(':')[0]
				if loc_code.upper() is not cat_ioc_alias:
					return False
				cat_ioc_base=entry.item.ioc_base.split(':')[1]
				if loc_code.upper() is not cat_ioc_base:
					return False
				cat_prefix=entry.item.prefix.split('_')[0]
				if loc_code.upper() is not cat_prefix:
					return False
				cat_ioc_name=entry.item.ioc_name.split('-')[0]
				if loc_code.lower() is not cat_ioc_name:
					return False
				cat_location_group=entry.item.location_group.split('_')[1]
				if loc_code.lower() is not cat_location_group:
					return False
				cat_name=entry.item.name.split('_')[0]
				if loc_code.lower() is not cat_name:
					return False
				if loc_code.lower() is not in location_data:
					return False
				else:
					return True
			except Exception as e:
				print(f"Error! entry returned error {e}")
def main():
        # Initialize the Happi client
        client = Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        
        # Ask the user for the device name
        device_name = input("Enter the location group code: ")
        devices=client.search(location_group=device_name)
        for device in devices:
            if validate_entry(device) is False:
                print(f"Invalid entry for {device.item.name}")
            else:
                
                
        if validate_entry(device_name) is True:
		active_status(device_name)
