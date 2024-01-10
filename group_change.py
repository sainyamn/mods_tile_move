import argparse

from happi import Client
from happi.errors import DuplicateError
from validate import validate
import pandas as pd


class GroupChange:
    def __init__(self, db_path):
        self.client=Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        self.validator =validate()

    '''
    def initialize_client():
        # Initialize the Happi client
        client = Client()
        return client
    '''
    #do we want a confirmation prompt for each entry or once for all in the location_group?
    def display_changes(self, entry):
            entry.item.show_info()
            '''
            if 'ioc_alias' in entry: print(entry.metadata['ioc_alias'])
            if 'ioc_type' in entry:print(entry.metadata['ioc_type'])
            if 'ioc_name' in entry:print(entry.metadata['ioc_name'])
            if 'ioc_base' in entry:print(entry.metadata['ioc_base'])
            if 'prefix' in entry:print(entry.metadata['prefix'])
            if 'location_group' in entry:print(entry.metadata['location_group'])
            '''
    def location_group_change(self, loc_grp, new_name):
        loc_code = loc_grp.split('_')[1]
        #print(f"There are "loc_code)
        #validator=validate() 
        #client=initialize_client()
        entries_to_modify = self.client.search(location_group=loc_grp)
        print(f"Number of entries that will be modified are {len(entries_to_modify)}")
        #print(f"{entries_to_modify}")
        #display_changes(loc_grp, loc_code, new_name, entries_to_modify)    
        

        if not entries_to_modify:
            print("No entries found for the search criteria.")
        else:
            globalFlag=0
            confirm_ALL=input("\n Do you want to skip verification and confirm changes for all devices (Y/n)").strip().lower()
            if confirm_ALL == 'y':
                globalFlag=1

            for entry in entries_to_modify:
                inital_values={}
                final_values={}
                try:
                        #print(f"{entry}")
                        #print(f"{entry.metadata['name']}")
                        #print(len(entry))
                        #display_changes(entry)
                        #print("\nInitial State: ")
                        #entry.item.show_info()
                        if 'ioc_alias' in entry: 
                            old_ioc_alias=entry.item.ioc_alias
                            inital_values['ioc_alias']=old_ioc_alias
                            #print(old_ioc_alias)
                            new_ioc_alias=old_ioc_alias.replace(loc_code.upper(), new_name.upper())
                            entry.item.ioc_alias=new_ioc_alias
                            final_values['ioc_alias']=entry.item.ioc_alias
                            #print("Initial State".ljust(20), "Final State".ljust(20))
                            #print(f"IOC Alias: {old_ioc_alias}".ljust(20), f"IOC Alias: {new_ioc_alias}")
                            #print(entry.item.ioc_alias)
                        if 'ioc_base' in entry: 
                            old_ioc_base=entry.item.ioc_base
                            #print(old_ioc_base)
                            inital_values['ioc_base']=old_ioc_base
                            new_ioc_base=old_ioc_base.replace(loc_code.upper(), new_name.upper())
                            entry.item.ioc_base=new_ioc_base
                            final_values['ioc_base']=entry.item.ioc_base
                            #print(entry.item.ioc_base)
                        if 'prefix' in entry: 
                            old_prefix=entry.item.prefix
                            #print(old_prefix)
                            inital_values['prefix']=old_prefix
                            new_prefix=old_prefix.replace(loc_code.upper(), new_name.upper())
                            entry.item.prefix=new_prefix
                            final_values['prefix']=entry.item.prefix
                            #print(entry.item.prefix)
                        if 'ioc_name' in entry: 
                            old_ioc_name=entry.item.ioc_name
                            inital_values['ioc_name']=old_ioc_name
                            new_ioc_name=old_ioc_name.replace(loc_code.lower(), new_name.lower())
                            entry.item.ioc_name=new_ioc_name
                            final_values['ioc_name']=entry.item.ioc_name
                            #print(entry.item.ioc_name)
                        if 'location_group' in entry: 
                            old_location_grp=entry.item.location_group
                            inital_values['location_group']=old_location_grp
                            new_loc_grp=old_location_grp.replace(loc_code.lower(), new_name.lower())
                            entry.item.location_group=new_loc_grp
                            final_values['location_group']=entry.item.location_group
                            #print(entry.item.location_group)
                        if 'name' in entry: 
                            old_name=entry.item.name
                            inital_values['name']=old_name
                            final_name=old_name.replace(loc_code.lower(), new_name.lower())
                            entry.item.name=final_name
                            final_values['name']=entry.item.name
                            #print(entry.item.name)
                        
                        #entry.item.save()
                        #print("\nThe new parameters for the device are:")
                        #entry.item.show_info()
                        #display_changes(entry)
                        df_initial=pd.DataFrame.from_dict(inital_values, orient='index', columns=['Old Value'])
                        df_initial.index.name='Device parameter'

                        df_final=pd.DataFrame.from_dict(final_values, orient='index', columns=['New Value'])
                        df_final.index.name='Device parameter'

                        df_compare=pd.concat([df_initial, df_final], axis=1)
                        print(df_compare)

                        '''
                        if validator.get_boolean_input():
                            entry.item.save()
                            print(f"Location successfully changed for {entry.item.name}")
                            display_changes(entry)
                        '''
                        if globalFlag == 1:
                            entry.item.save()
                            continue
                        if  globalFlag == 0:
                            confirmation = input("Confirm changes (Y/n): ").strip().lower()
                            if confirmation == 'y':
                                entry.item.save()
                                print(f"Location successfully changed for {entry.item.name}")
                                entry.item.show_info()
                            else:
                                if 'ioc_alias' in entry: entry.item.ioc_alias=old_ioc_alias
                                if 'ioc_base' in entry: entry.item.ioc_base=old_ioc_base
                                if 'prefix' in entry: entry.item.prefix=old_prefix
                                if 'ioc_name' in entry: entry.item.ioc_name=old_ioc_name
                                if 'location_group' in entry: entry.item.location_group=old_location_grp
                                if 'name' in entry: entry.item.name=old_name
                                entry.item.save()
                                print(f"No changes made to device entry {entry.item.name}")
                        new_ioc_alias=new_ioc_base=new_ioc_name=new_loc_grp=final_name=new_prefix=''
                        old_ioc_alias=old_ioc_base=old_ioc_name=old_location_grp=old_name=old_prefix=''

                except DuplicateError as e:
                    print(f"An entry with the same name already exists: {e}")
                #print("Modification complete. Entries updated in the database.")
    def main(self, loc_grp, new_name):
        if not loc_grp or not new_name:
                print("Please provide both location group (--loc_grp) and new name (--new_name)")
                return
        self.location_group_change(loc_grp, new_name)

        
if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--loc_grp", help="location group for devices to be shifted")
        parser.add_argument("--new_name", help="destination code for the devices after shifting")

        args = parser.parse_args()
        loc_grp = args.loc_grp
        new_name = args.new_name

        group_change = GroupChange('/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        group_change.main(loc_grp, new_name)
