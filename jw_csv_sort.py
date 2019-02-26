#!/usr/bin/env python3

#try to import pandas module, if this fails it probably isn't installed and therefore a warning message to install is displayed and programed in terminated.
try:
    import pandas
except:
    print('You need to install `Pandas` package to run this program. Run `pip install pandas` and try again, please!')
    exit()
#sys is needed to input what file to parse.
import sys

#function to convert csv to pandas datagram
def csv_to_pandas():
    #If there is a sys aruguement assign to variable.
    if len(sys.argv) > 1:
        vf_str_filename = sys.argv[1]
    #imports to pandas dataframe from csv, header=1 to skip first row.  Only need to include certain columns.
    #try to import csv from sys arguement filename.
    try:
        vf_pand_main = pandas.read_csv(vm_str_filename,header=1,usecols=['Device Name','Vendor','Model','Operating System','Device End-of-Service'])
    #if this fails, print error and then try default file ('NPL_Feb_Inventory.csv').
    except:
        print('Inputed file not found, trying default file')
        try:
           vf_pand_main = pandas.read_csv('NPL_Feb_Inventory.csv',header=1,usecols=['Device Name','Vendor','Model','Operating System','Device End-of-Service'])
        #If that fails, print error and exit program.
        except:
            print('Inputted and default files not found, please run program again and select correct file/directory!')
            exit()
    #if successful, return dataframe back to main.
    return(vf_pand_main)

#function to find unique vendor/model/OS combinations within the entire csv. These are then stored as list of dictionaries and passed back to main.
def extract_data(vf_pand_main):
    #Make the panda model into dictionary grouped by Model type.
    vf_dict_model = dict(tuple(vf_pand_main.groupby('Model')))
    #Make a list of different models.
    vf_list_model = vf_dict_model.keys()
    #final list to store final set of data to be printed.
    vf_list_final = []
    #iterate over list of models to create separate dictionaries for each OS type and append to final list.
    for vf_str_model in vf_list_model:
        vf_pand_model = vf_dict_model[vf_str_model]
        vf_dict_OS = dict(tuple(vf_pand_model.groupby('Operating System')))
        #for each OS/Model combo, add a new entry to final list - list of dictionaries.  Each dictionary will keep the rest of the info of the dataframe to extract other data later.
        for vf_str_OS in vf_dict_OS.keys():
            vf_list_final.append({'Model':vf_str_model,'OS':vf_str_OS,'Count':'','Vendor':'','EoL':'','Rest':vf_dict_OS[vf_str_OS]})
    #This for loop iterates over entries in list of dictionaries and adds the vendor and OS count entries.
    for vf_dict_entry in vf_list_final:
        vf_dict_entry['Vendor'] = vf_dict_entry['Rest']['Vendor'].values[0]
        vf_dict_entry['EoL'] = vf_dict_entry['Rest']['Device End-of-Service'].values[0]
        #Needed in case the EoL section is empty in that case input 'N/A'.
        if type(vf_dict_entry['EoL']) is str:    
            vf_dict_entry['EoL'] = vf_dict_entry['EoL'][:-5]
        else:
            vf_dict_entry['EoL'] = 'N/A'
        vf_dict_entry['Count'] = vf_dict_entry['Rest']['Operating System'].value_counts().tolist()[0]
    #return final list of dictionaries.
    return(vf_list_final) 

#function to print information in final list of dictionaries and format.
def print_stuff(vf_list_final):
    print('{:<6} {:<9} {:<20} {:<20} {:<20}'.format('Count','Vendor','Model','Software','End of Service'))
    for vf_dict_entry in vf_list_final:
        print('{:<6} {:<9} {:<20} {:<20} {:<20}'.format(vf_dict_entry['Count'],vf_dict_entry['Vendor'],vf_dict_entry['Model'],vf_dict_entry['OS'],vf_dict_entry['EoL']))

#main program.       
if __name__ == '__main__':
    #first import csv to pandas dataframe.
    vm_pand_main = csv_to_pandas()
    #next organize material to print in list of dictionaries.
    vm_list_final = extract_data(vm_pand_main)
    #finally print list of dictionaries.
    print_stuff(vm_list_final)
