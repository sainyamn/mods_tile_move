from happi import Client
from happi.errors import DuplicateError
from validate import validate

def initialize_client():
    # Initialize the Happi client
    client = Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
    return client

#do we want a confirmation prompt for each entry or once for all in the location_group?
def display_changes(entry):
    #print(f"You are about to change device location for {device_name}")
    #print(f"Destination location for {device_name} is {new_name}")
    #print(f"Following parameters will be updated:")
    #for entry in entries_to_modify:
    #for entry in entry:    
        #print(entry.metadata)
        print("The device info is as follows:")
        if 'ioc_alias' in entry: print(entry.metadata['ioc_alias'])
        if 'ioc_type' in entry:print(entry.metadata['ioc_type'])
        if 'ioc_name' in entry:print(entry.metadata['ioc_name'])
        if 'ioc_base' in entry:print(entry.metadata['ioc_base'])
        if 'prefix' in entry:print(entry.metadata['prefix'])
        if 'location_group' in entry:print(entry.metadata['location_group'])
       # print(entry[0].metadata['ioc_alias'])
       # print(f"IOC Alias: {entry['ioc_alias']}")
       # print(f"IOC Base: {entry.metadata['ioc_base']}")
       # print(f"Prefix: {entry.metadata['prefix']}")
       # print(f"IOC Name: {entry.metadata['ioc_name']}")
       # print(f"Location Group: {entry.metadata['location_group']}")
       # print(f"Name: {entry.metadata['name']}")
       # print("------------------------------")


def location_group_change():
    loc_grp = input("Enter the location group: ")
    loc_code = loc_grp.split('_')[1]
    new_name = input("Enter the new device location code: ")
    validator=validate()
    # Search for entries by name 
    client=initialize_client()
    entries_to_modify = client.search(location_group=loc_grp)
    print(len(entries_to_modify))
    #print(f"{entries_to_modify}")
    #display_changes(loc_grp, loc_code, new_name, entries_to_modify)    
    if not entries_to_modify:
        print("No entries found for the search criteria.")
    else:
        for entry in entries_to_modify:
            try:
                    #print(f"{entry}")
                    #print(f"{entry.metadata['name']}")
                    #print(len(entry))
                    display_changes(entry)
                    
                    if 'ioc_alias' in entry: 
                        old_ioc_alias=entry.item.ioc_alias
                        entry.item.ioc_alias=entry.item.ioc_alias.replace(loc_code.upper(), new_name.upper())
                    if 'ioc_base' in entry: 
                        old_ioc_base=entry.item.ioc_base
                        entry.item.ioc_base=entry.item.ioc_base.replace(loc_code.upper(), new_name.upper())
                    if 'prefix' in entry: 
                        old_prefix=entry.item.prefix
                        entry.item.prefix=entry.item.prefix.replace(loc_code.upper(), new_name.upper())
                    if 'ioc_name' in entry: 
                        old_ioc_name=entry.item.ioc_name
                        entry.item.ioc_name=entry.item.ioc_name.replace(loc_code.lower(), new_name.lower())
                    if 'location_group' in entry: 
                        old_location_grp=entry.item.location_group
                        entry.item.location_group=entry.item.location_group.replace(loc_code.lower(), new_name.lower())
                    if 'name' in entry: 
                        old_name=entry.item.name
                        entry.item.name=entry.item.name.replace(loc_code.lower(), new_name.lower())
                    entry.item.save()
                    print(f"The new parameters for the device are:")
                    display_changes(entry)
                    if validator.get_boolean_input("Enter Yes/No (y/n) true/false (t/f) to confirm changes:"):
                        entry.item.save()
                        print(f"Location successfully changed for {entry.item.name}")
                    else:
                        if 'ioc_alias' in entry: entry.item.ioc_alias=old_ioc_alias
                        if 'ioc_base' in entry: entry.item.ioc_base=old_ioc_base
                        if 'prefix' in entry: entry.item.prefix=old_prefix
                        if 'ioc_name' in entry: entry.item.ioc_name=old_ioc_name
                        if 'location_group' in entry: entry.item.location_group=old_location_grp
                        if 'name' in entry: entry.item.name=old_name
                        entry.item.save()
                        print(f"No changes made to device entry")
            except DuplicateError as e:
                print(f"An entry with the same name already exists: {e}")
            #print("Modification complete. Entries updated in the database.")
def main():
    initialize_client()

    location_group_change()
if __name__ == "__main__":
    main()
