import json
import numpy as np


def angle_to_xy_and_z(vector):
    angle_xy = np.degrees(np.arctan2(np.linalg.norm(vector[:2]), vector[2]))
    angle_z = np.degrees(np.arctan2(vector[1], vector[0]))
    return angle_xy, angle_z
def vector_from_angles(angle_xy, angle_z, r, InitialPoint):
    # Convert angles from degrees to radians
    angle_xy_rad = np.radians(angle_xy)
    angle_z_rad = np.radians(angle_z)

    # Calculate the endpoint of the vector
    x = r * np.cos(angle_z_rad) * np.sin(angle_xy_rad) + InitialPoint[0]
    y = r * np.sin(angle_z_rad) * np.sin(angle_xy_rad) + InitialPoint[1]
    z = r * np.cos(angle_xy_rad) + InitialPoint[2]

    return np.array([x, y, z])

class ReadJsonFile():
    def __init__(self, JsonData):
        self.atom_names = []
        self.atom_elements = JsonData['PC_Compounds'][0]['atoms']['element']
        atom_coords = JsonData['PC_Compounds'][0]['coords'][0]['conformers'][0]
        atomcordsX = atom_coords["x"]
        atomcordsY = atom_coords["y"]
        atomcordsZ = atom_coords["z"]
        self.atom_coords = [atomcordsX, atomcordsY, atomcordsZ]
        self.atomsName = []
        for atomid in self.atom_elements:
            if atomid == 1:
                self.atomsName.append("H")
            elif atomid == 8:
                self.atomsName.append("O")
            elif atomid==7:
                self.atomsName.append("N")
            elif atomid==6:
                self.atomsName.append("C")
            elif atomid==16:
                self.atomsName.append("S")
        self.Combinations = []
        for index in range(len(JsonData['PC_Compounds'][0]['bonds']['aid1'])):
            self.Combinations.append({"AtomName1": self.atomsName[JsonData['PC_Compounds'][0]['bonds']['aid1'][index]-1],\
                                "RelativeAtomIndex1": str(JsonData['PC_Compounds'][0]['bonds']['aid1'][index]), \
                                "AtomName2": self.atomsName[JsonData['PC_Compounds'][0]['bonds']['aid2'][index]-1], \
                                "RelativeAtomIndex2": str(JsonData['PC_Compounds'][0]['bonds']['aid2'][index])})
    def CombinationOfAtomRelativeIndexToReltiveIndexes(self, RelativeIndex):
        RelativeIndexes = []
        for combine in self.Combinations:
            if combine["RelativeAtomIndex1"]==str(RelativeIndex):
                RelativeIndexes.append(combine["RelativeAtomIndex2"])
            elif combine["RelativeAtomIndex2"]==str(RelativeIndex):
                RelativeIndexes.append(combine["RelativeAtomIndex1"])
        return RelativeIndexes
    
    def WhichRelativeIndexCombinedIsThisAtom(self, RelativeIndex=5, Atomname="O"):
        RelativeIndexes = []
        for combine in self.Combinations:
            if combine["RelativeAtomIndex1"]==str(RelativeIndex):
                if combine["AtomName2"]==Atomname:
                    RelativeIndexes.append(combine["RelativeAtomIndex2"])
            elif combine["RelativeAtomIndex2"]==str(RelativeIndex):
                if combine["AtomName1"]==Atomname:
                    RelativeIndexes.append(combine["RelativeAtomIndex1"])
        return RelativeIndexes
    def CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex(self, KnownRelativeIndexes, ExcecptRelativeIndexes):
        RelativeIndexes = []
        for combine in self.Combinations:
            if combine["RelativeAtomIndex1"] in KnownRelativeIndexes and combine["RelativeAtomIndex2"] not in ExcecptRelativeIndexes:
                if combine["AtomName2"]!="H":
                    RelativeIndexes.append(combine["RelativeAtomIndex2"])
            elif combine["RelativeAtomIndex2"] in KnownRelativeIndexes and combine["RelativeAtomIndex1"] not in ExcecptRelativeIndexes:
                if combine["AtomName1"]!="H":
                    RelativeIndexes.append(combine["RelativeAtomIndex1"])
        return RelativeIndexes
    
    
    def Find_Allname(self, ):
        OxygensRelativeIndexea = []
        for combine in self.Combinations:
            if combine["AtomName1"]=="O":
                OxygensRelativeIndexea.append(combine["RelativeAtomIndex1"])
            elif combine["AtomName2"]=="O":
                OxygensRelativeIndexea.append(combine["RelativeAtomIndex2"])
        OxygensRelativeIndexea = np.array(OxygensRelativeIndexea)
        for i in range(len(OxygensRelativeIndexea)):
            if len(np.where(OxygensRelativeIndexea==OxygensRelativeIndexea[i])[0])==1:
                self.atom_elements[int(OxygensRelativeIndexea[i])-1] = "O"
        RelativeIndexes = self.CombinationOfAtomRelativeIndexToReltiveIndexes(self.atom_elements.index("O")+1)
        self.atom_elements[int(RelativeIndexes[0])-1] = "C"
        RelativeIndexes = self.WhichRelativeIndexCombinedIsThisAtom(self.atom_elements.index("C")+1, "O")
        for RelativeIndexe in RelativeIndexes:
            if self.atom_elements[int(RelativeIndexe)-1] != "O":
                self.atom_elements[int(RelativeIndexe)-1] = "OXT"
        RelativeIndexes = self.WhichRelativeIndexCombinedIsThisAtom(self.atom_elements.index("C")+1, "C")
        self.atom_elements[int(RelativeIndexes[0])-1] = "CA"
        RelativeIndexes = self.WhichRelativeIndexCombinedIsThisAtom(self.atom_elements.index("CA")+1, "N")
        self.atom_elements[int(RelativeIndexes[0])-1] = "N"
        RelativeIndexes = self.WhichRelativeIndexCombinedIsThisAtom(self.atom_elements.index("CA")+1, "C")
        prevRelativeIndexes = []
        for RelativeIndexe in RelativeIndexes:
            if self.atom_elements[int(RelativeIndexe)-1] != "C":
                prevRelativeIndexes.append(RelativeIndexe)
                self.atom_elements[int(RelativeIndexe)-1] = "CB"

        RelativeIndexes = self.CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex([str(self.atom_elements.index("CB")+1)], [str(self.atom_elements.index("CA")+1)])
        if len(RelativeIndexes)>1:
            index = 1
            for i in RelativeIndexes:
                self.atom_elements[int(i)-1] = self.atomsName[int(i)-1]+"G"+str(index)
                index+=1
        else:
            self.atom_elements[int(RelativeIndexes[0])-1] = self.atomsName[int(RelativeIndexes[0])-1]+"G"
        index = -1
        for i in self.atom_elements:
            index+=1
            try:
                i = int(i)
                if i ==1:
                    self.atom_elements=self.atom_elements[:index]
                    self.atom_coords[0]=self.atom_coords[0][:index]
                    self.atom_coords[1]=self.atom_coords[1][:index]
                    self.atom_coords[2]=self.atom_coords[2][:index]
                    return 1
                else:
                    break
            except:
                pass
        RelativeIndexess = self.CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex(RelativeIndexes, prevRelativeIndexes)
        prevRelativeIndexes = RelativeIndexes.copy()
        RelativeIndexes = RelativeIndexess
        if len(RelativeIndexes)>1:
            index = 1
            for i in RelativeIndexes:
                self.atom_elements[int(i)-1] = self.atomsName[int(i)-1]+"D"+str(index)
                index+=1
        else:
            self.atom_elements[int(RelativeIndexes[0])-1] = self.atomsName[int(RelativeIndexes[0])-1]+"D"
        index = -1
        for i in self.atom_elements:
            index+=1
            try:
                i = int(i)
                if i ==1:
                    self.atom_elements=self.atom_elements[:index]
                    self.atom_coords[0]=self.atom_coords[0][:index]
                    self.atom_coords[1]=self.atom_coords[1][:index]
                    self.atom_coords[2]=self.atom_coords[2][:index]
                    return 1
                else:
                    break
            except:
                pass
        RelativeIndexess = self.CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex(RelativeIndexes, prevRelativeIndexes)
        prevRelativeIndexes = RelativeIndexes.copy()
        RelativeIndexes = RelativeIndexess
        if len(RelativeIndexes)>1:
            index = 1
            for i in RelativeIndexes:
                self.atom_elements[int(i)-1] = self.atomsName[int(i)-1]+"E"+str(index)
                index+=1
        else:
            self.atom_elements[int(RelativeIndexes[0])-1] = self.atomsName[int(RelativeIndexes[0])-1]+"E"
        
        index =-1
        for i in self.atom_elements:
            index+=1
            try:
                i = int(i)
                if i ==1:
                    self.atom_elements=self.atom_elements[:index]
                    self.atom_coords[0]=self.atom_coords[0][:index]
                    self.atom_coords[1]=self.atom_coords[1][:index]
                    self.atom_coords[2]=self.atom_coords[2][:index]
                    return 1
                else:
                    break
            except:
                pass
            
        RelativeIndexess = self.CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex(RelativeIndexes, prevRelativeIndexes)
        prevRelativeIndexes = RelativeIndexes.copy()
        RelativeIndexes = RelativeIndexess
        if len(RelativeIndexes)>1:
            index = 1
            for i in RelativeIndexes:
                self.atom_elements[int(i)-1] = self.atomsName[int(i)-1]+"Z"+str(index)
                index+=1
        else:
            self.atom_elements[int(RelativeIndexes[0])-1] = self.atomsName[int(RelativeIndexes[0])-1]+"Z"
        index = -1
        for i in self.atom_elements:
            index+=1
            try:
                i=int(i)
                if i ==1:
                    self.atom_elements=self.atom_elements[:index]
                    self.atom_coords[0]=self.atom_coords[0][:index]
                    self.atom_coords[1]=self.atom_coords[1][:index]
                    self.atom_coords[2]=self.atom_coords[2][:index]
                    return 1
                else:
                    break
            except:
                pass
            
        RelativeIndexess = self.CombinationOfAtomRelativeIndexToReltiveIndexesExceptWhatRelativeIndex(RelativeIndexes, prevRelativeIndexes)
        prevRelativeIndexes = RelativeIndexes.copy()
        RelativeIndexes = RelativeIndexess
        if len(RelativeIndexes)>1:
            index = 1
            for i in RelativeIndexes:
                self.atom_elements[int(i)-1] = self.atomsName[int(i)-1]+"H"+str(index)
                index+=1
        else:
            self.atom_elements[int(RelativeIndexes[0])-1] = self.atomsName[int(RelativeIndexes[0])-1]+"H"
    def ChangeInitialVecTo(self, ChromosomeInput):
        DeltaSourcePoint, dRx, dRy, dRz = ChromosomeInput
        dRx = np.radians(dRx)
        dRy = np.radians(dRy)
        dRz = np.radians(dRz)
        deltaxyz = np.array([[1, 0, 0, DeltaSourcePoint[0]],
                             [0, 1, 0, DeltaSourcePoint[1]],
                             [0, 0, 1, DeltaSourcePoint[2]],
                             [0, 0, 0, 1]])
        RotationOnZ = np.array([[np.cos(dRz), -np.sin(dRz), 0, 0], 
                                [np.sin(dRz), np.cos(dRz), 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        RotationOny = np.array([[np.cos(dRy), 0, np.sin(dRy), 0], 
                                [0, 1, 0, 0],
                                [-np.sin(dRy), 0, np.cos(dRy), 0],
                                [0, 0, 0, 1]])
        RotationOnx = np.array([[1, 0, 0, 0], 
                                [0, np.cos(dRx), -np.sin(dRx), 0],
                                [0, np.sin(dRx), np.cos(dRx), 0],
                                [0, 0, 0, 1]])
        self.TransposeMatrix = np.dot(deltaxyz, RotationOnx)
        self.TransposeMatrix = np.dot(self.TransposeMatrix, RotationOny)
        self.TransposeMatrix = np.dot(self.TransposeMatrix, RotationOnZ)
    def GiveMeAtomPositionWithNewStartAndEndpoint(self, Atomname="O"):
        AtomIndex = self.atom_elements.index(Atomname)
        Atomcords = np.array([[self.atom_coords[0][AtomIndex]],
                              [self.atom_coords[1][AtomIndex]],
                              [self.atom_coords[2][AtomIndex]],
                              [1]])
        newAtomCords = np.dot(self.TransposeMatrix, Atomcords)[:-1, 0]
        return newAtomCords
    
    def CaculateCombinations(self, MaxIndexThatAdded, LastAmino=False):
        self.FirstAtomIndex = MaxIndexThatAdded
            
        AtomsCombination=[[] for _ in range(len(self.atom_elements))]
        OXTINdex = self.atom_elements.index("OXT")
        for combine in self.Combinations:
            if int(combine["RelativeAtomIndex1"])<=len(self.atom_elements) and int(combine["RelativeAtomIndex2"])<=len(self.atom_elements):
                if int(combine["RelativeAtomIndex2"]) not in AtomsCombination[int(combine["RelativeAtomIndex1"])-1]:
                    AtomsCombination[int(combine["RelativeAtomIndex1"])-1].append(int(combine["RelativeAtomIndex2"]))
                if int(combine["RelativeAtomIndex1"]) not in AtomsCombination[int(combine["RelativeAtomIndex2"])-1]:
                    AtomsCombination[int(combine["RelativeAtomIndex2"])-1].append(int(combine["RelativeAtomIndex1"]))
        index=0
        for Combs in AtomsCombination:
            index+=1
            subIndex = -1
            for comb in Combs:
                subIndex+=1
                if comb<index:
                    del AtomsCombination[index-1][subIndex]
        self.AtomsCombination = AtomsCombination
        for i in range(len(self.AtomsCombination)):
            for j in range(len(self.AtomsCombination[i])):
                if self.AtomsCombination[i][j]>OXTINdex+1 and not LastAmino:
                    self.AtomsCombination[i][j]=self.AtomsCombination[i][j]+self.FirstAtomIndex-1-1 # id to index, remove OXT of This Amino id
                elif LastAmino:
                    self.AtomsCombination[i][j]=self.AtomsCombination[i][j]+self.FirstAtomIndex-1

if __name__=="__main__":
    with open("Conformer3D_COMPOUND_CID_6057.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    ReadJsonFileObj = ReadJsonFile(data)
    ReadJsonFileObj.Find_Allname()
    print(ReadJsonFileObj.atom_elements)