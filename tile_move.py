#!/cds/group/pcds/pyps/conda/py39/envs/pcds-5.8.1/bin/python3
import argparse

from happi import Client
from happi.errors import DuplicateError
from validate import validate
import pandas as pd


class GroupChange:
    def __init__(self, db_path):
        self.client=Client(path='/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        self.validator =validate()

    #do we want a confirmation prompt for each entry or once for all in the location_group?
    def display_changes(self, entry):
            entry.item.show_info()
            
    def location_group_change(self, loc_grp, new_name):
        loc_code = loc_grp.split('_')[1]
        
        entries_to_modify = self.client.search(location_group=loc_grp)
        print(f"Number of entries that will be modified are {len(entries_to_modify)}")
        

        if not entries_to_modify:
            print("No entries found for the search criteria.")
        else:
            globalFlag=0
            confirm_ALL=input("\n Do you want to skip verification and confirm changes for all devices (y/N)").strip().lower()
            # set flag=1 if we want to skip verification for all devices
            if confirm_ALL == 'y':
                globalFlag=1

            for entry in entries_to_modify:
                inital_values={}
                final_values={}
                #some device may miss fields hence the use of if statements below
                try:
                        if 'ioc_alias' in entry: 
                            old_ioc_alias=entry.item.ioc_alias
                            inital_values['ioc_alias']=old_ioc_alias
                            new_ioc_alias=old_ioc_alias.replace(loc_code.upper(), new_name.upper())
                            entry.item.ioc_alias=new_ioc_alias
                            final_values['ioc_alias']=entry.item.ioc_alias
                        if 'ioc_base' in entry: 
                            old_ioc_base=entry.item.ioc_base
                            inital_values['ioc_base']=old_ioc_base
                            new_ioc_base=old_ioc_base.replace(loc_code.upper(), new_name.upper())
                            entry.item.ioc_base=new_ioc_base
                            final_values['ioc_base']=entry.item.ioc_base
                        if 'prefix' in entry: 
                            old_prefix=entry.item.prefix
                            inital_values['prefix']=old_prefix
                            new_prefix=old_prefix.replace(loc_code.upper(), new_name.upper())
                            entry.item.prefix=new_prefix
                            final_values['prefix']=entry.item.prefix
                        if 'ioc_name' in entry: 
                            old_ioc_name=entry.item.ioc_name
                            inital_values['ioc_name']=old_ioc_name
                            new_ioc_name=old_ioc_name.replace(loc_code.lower(), new_name.lower())
                            entry.item.ioc_name=new_ioc_name
                            final_values['ioc_name']=entry.item.ioc_name
                        if 'location_group' in entry: 
                            old_location_grp=entry.item.location_group
                            inital_values['location_group']=old_location_grp
                            new_loc_grp=old_location_grp.replace(loc_code.lower(), new_name.lower())
                            entry.item.location_group=new_loc_grp
                            final_values['location_group']=entry.item.location_group
                        if 'name' in entry: 
                            old_name=entry.item.name
                            inital_values['name']=old_name
                            final_name=old_name.replace(loc_code.lower(), new_name.lower())
                            entry.item.name=final_name
                            final_values['name']=entry.item.name
                        
                        df_initial=pd.DataFrame.from_dict(inital_values, orient='index', columns=['Old Value'])
                        df_initial.index.name='Device parameter'

                        df_final=pd.DataFrame.from_dict(final_values, orient='index', columns=['New Value'])
                        df_final.index.name='Device parameter'

                        df_compare=pd.concat([df_initial, df_final], axis=1)
                        print(df_compare)
                        #changes are displayed in a dataframe for easy comparision with previous values
                        if globalFlag == 1:
                            entry.item.save()
                            continue
                        if  globalFlag == 0:
                            confirmation = input("Confirm changes (y/N): ").strip().lower()
                            
                            if confirmation == 'y':
                                entry.item.save()
                                print(f"Location successfully changed for {entry.item.name}")
                                #entry.item.show_info()
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
                
    def main(self, loc_grp, new_name):
        if not loc_grp or not new_name:
                print("Please provide both location group (--loc_grp) and new name (--new_name)")
                return
        self.location_group_change(loc_grp, new_name)

        
if __name__ == "__main__":
        #conda_activate_cmd="source pcds_conda"
        #subprocess.run(conda_activate_cmd, shell=True, executable="/bin/sh")

        parser = argparse.ArgumentParser()
        parser.add_argument("--i", help="intial location group for devices to be shifted")
        parser.add_argument("--f", help="final destination location code for the devices after shifting")

        args = parser.parse_args()
        loc_grp = args.i
        new_name = args.f

        group_change = GroupChange('/reg/g/pcds/epics-dev/nagar123/mods/db.json')
        group_change.main(loc_grp, new_name)
        #conda_env_path = "/cds/group/pcds/pyps/conda/py39/envs/pcds-5.8.1"