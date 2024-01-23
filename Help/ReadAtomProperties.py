import csv
import numpy as np
class AtomProperties():
    def __init__(self, csvFilePath="AtomsProperties.csv"):
        self.AtomsProb = []
        with open(csvFilePath, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.AtomsProb.append(row)
        self.AtomsProb = np.array(self.AtomsProb)
        self.AtomsName = self.AtomsProb[:, 0]
        self.WhatResAtomsInclude = self.AtomsProb[:, -1]
        self.Criclist = np.reshape(self.AtomsName, (len(self.AtomsName), 1))
        self.Criclist =np.append(self.Criclist, np.reshape(self.WhatResAtomsInclude, (len(self.WhatResAtomsInclude), 1)), -1)
    def GiveMeAtomProps(self, AtomName="", AtomResInclude=""):
        index = -1
        for i in self.Criclist:
            index+=1
            if AtomName == i[0] and AtomResInclude==i[1]:
                return self.AtomsProb[index, :]
        index = -1
        for i in self.Criclist:
            index+=1
            if AtomName[0] == i[0][0] and AtomResInclude==i[1]:
                return self.AtomsProb[index, :]
            
        index = -1
        for i in self.Criclist:
            index+=1
            if AtomName == i[0]:
                return self.AtomsProb[index, :]
            

            
        index = -1
        for i in self.Criclist:
            index+=1
            if AtomName[0] == i[0][0]:
                return self.AtomsProb[index, :]
            
            
            
            
if __name__=="__main__":
    AtomPropertiesobj = AtomProperties()
    print(AtomPropertiesobj.GiveMeAtomProps("CE", "MET"))