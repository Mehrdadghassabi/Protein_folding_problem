from CaculateEnergyLib.dataframefunction import frames
import os

# Creates a protein class object to store the head and tail of the full  query 
# path referred to here as "filePath" and "name" respectively.
class Protein:
    # Initializer / Instance attributes
    def __init__(self, filePath, name): #Default directory is current working directory
        self.filePath = filePath
        self.name = name 

    # Returns the name of the protein and the file path associated with it
    # just print the object that been assigned with the class
    def __repr__(self):
        return f"{self.filePath}: {self.name}"
    
    # Create datafreame from file, calling dataframefunction.py
    def dataframe(self):
        return frames(self.filePath, self.name)
    
    # Development method
    def setPath(self, filePath):
        try:
            with os.path.exists(filePath):
                self.filePath = filePath
        except IOError:
            return f"Please pass a valid file path, {filePath} does not exist"
    
    # Development method
    def rename(self, name):
        self.name = input("Please enter a new name for this protein: ")