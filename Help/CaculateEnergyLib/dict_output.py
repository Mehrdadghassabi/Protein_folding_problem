# Module for applying the energy calculation on single files and directories of varying depths, depending on user input.
# Returns a dictionary with the energy of each .crd file present in a given folder. 
from CaculateEnergyLib.protein_class import Protein
from CaculateEnergyLib.dataframefunction import check_if_crd
import pandas as pd
import CaculateEnergyLib.ecalc as e
from functools import reduce
import os

# Creates a nested dictionary that represents the folder structure of the input directory. 
def make_dictionary(rootdir, subfolders: bool):
    dir1 = {}
    # The following line makes the input flexible as to whether or not the user passes a "/" at the end of their path name.
    rootdir = rootdir.rstrip(os.sep)
    print(f"This is rootdir: {rootdir}")
    start = rootdir.rfind(os.sep) + 1
    print(f"This is start: {start}")
    values = list()
    indexes = list()
    for path, dirs, files in os.walk(rootdir, topdown=True):
        energies = list()
        folders = path[start:].split(os.sep)
        print(f"These are the folders: {folders}")
        # The following section allows the program to read in only .crd files when passed a folder containing mixed file types.
        sort_files = sorted(files, key =lambda x: x)
        check, mod_files, types = check_if_crd(sort_files)
        crd_files = [i for i,j in zip(sort_files,check) if j] # Using list comprehension create a 

        # If we have walked the first parent folder and are looping through the subfolders, calculate energies
        if((len(folders)>1 and subfolders)): 
            sub_path = os.path.join(rootdir, folders[1]+os.sep)
            print(f"This is the sub_path: {sub_path}")
            for j in range(0, len(crd_files)):
                protein = Protein(filePath = sub_path, name = crd_files[j])
                energies.append(e.energy(protein)[0])

            # Dictionary comprehension to initialize dictionary with a list of values
            tuples = tuple(zip(crd_files, energies))
            print("Unordered tuples: {tuples}")
            tuples = sorted(tuples, key=lambda x: x[1])
            indexes.append(folders[1])
            values.append(tuples[0])
            print(f"Ordered tuples: {tuples}")
            subdir = {key:value for key, value in tuples}
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
            print(f"This is types: {types}")
            print(f"These are the modfiles: {mod_files}")
            
        # Else if no subfolders
        elif(subfolders == False): 
            # Instead of getting a subpath, we just use the passed in file path
            # [NOTE] sub_path = os.path.join(rootdir, folders[1]+os.sep) ---> Returns an error if run here
            for j in range(0, len(crd_files)):
                protein = Protein(filePath = path+os.sep, name = crd_files[j])
                energies.append(e.energy(protein)[0])

            # Dictionary comprehension to initialize dictionary with a list of values
            subdir = {key:value for key, value in zip(files, energies)}
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
            print(f"These are the types: {types}")
            print(f"These are the modfiles: {mod_files}")
            
        # Do this first if there are subfolders. Since we are walking the directory topdown, 
        # we must decend past the first directory layer to then access the folders and files inside. 
        else: 
            subdir = dict.fromkeys(files)
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
    
    # Creates a dataframe summarizing the information present in the output dictionary. Sorts this information
    # so that the .crd file with the lowest energy is presented as the first row of the dataframe. This is 
    # important for our application of oru model for further downstream protein structure analysis.
    df = pd.DataFrame(data=values, index=indexes, columns = ["Model", "Energy (kcal/mol)"])
    df = pd.DataFrame.sort_index(df, axis=0)
        
    return dir1, df
