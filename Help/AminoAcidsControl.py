import copy

class AminoAcis():
    def __init__(self, AminoAcidsObjects=[]):
        self.AminoAcidsObjects = AminoAcidsObjects
        pass
    def NitrogensAndOxygensDetection(self, ):
        self.NitrogenIndexes = []
        self.AminoNitrogenIndexes = []
        self.OxygenIndexes = []
        self.AminoOxygenIndexes = []
        self.SulfurIndexes = []
        self.AminoSulfurIndexes = []
        atomIndex = -1
        AminoId = 0
        justLastCRelativeIndex = []
        for Amino in self.AminoAcidsObjects:
            AminoId+=1
            atomrelativeIndex = -1
            for Atom in Amino.atom_elements:
                atomrelativeIndex+=1
                atomIndex+=1
                if Atom == "N" and AminoId>1:
                    self.AminoAcidsObjects[AminoId-2].\
                        AtomsCombination[justLastCRelativeIndex[AminoId-2]].append(atomIndex)
                if Atom[0]=="N":
                    self.NitrogenIndexes.append(atomIndex)
                    self.AminoNitrogenIndexes.append(AminoId)
                elif Atom[0]=="O":
                    self.OxygenIndexes.append(atomIndex)
                    self.AminoOxygenIndexes.append(AminoId)
                elif Atom[0]=="S":
                    self.SulfurIndexes.append(atomIndex)
                    self.AminoSulfurIndexes.append(AminoId)
                if Atom=="C":
                    justLastCRelativeIndex.append(atomrelativeIndex)
        # print(self.AminoSulfurIndexes)
    def GiveMeAllPossibleOxygenIndexCombinationFromThisAminoId(self, AminoId):
        OxygenPossibleIndexes = []
        for i in range(len(self.AminoOxygenIndexes)):
            if self.AminoOxygenIndexes[i]!=AminoId:
                OxygenPossibleIndexes.append(self.OxygenIndexes[i])
                
        return OxygenPossibleIndexes
    
    
    def GiveMeAllPossibleSulfurIndexCombinationFromThisAminoId(self, AminoId):
        SulfurPossibleIndexes = []
        for i in range(len(self.AminoSulfurIndexes)):
            if self.AminoSulfurIndexes[i]!=AminoId:
                SulfurPossibleIndexes.append(self.SulfurIndexes[i])
                
        return SulfurPossibleIndexes
    
    
    def GiveMeAllSulfursOfThisAminoId(self, AminoId):
        SulfurIndexes = []
        for i in range(len(self.AminoSulfurIndexes)):
            if self.AminoSulfurIndexes[i]==AminoId:
                SulfurIndexes.append(self.SulfurIndexes[i])
                
        return SulfurIndexes
        
    def GiveMeAllNitrogensOfThisAminoId(self, AminoId):
        NitrogenIndexes = []
        for i in range(len(self.AminoNitrogenIndexes)):
            if self.AminoNitrogenIndexes[i]==AminoId:
                NitrogenIndexes.append(self.NitrogenIndexes[i])
                
        return NitrogenIndexes
    
    def DecodeCombination(self, Chrom):
        AminoAcidsObjects = self.AminoAcidsObjects.copy()
        for i in range(len(self.NitrogenIndexes)):
            AminoIdForNitrogen = self.AminoNitrogenIndexes[i]
            NitrogenIndex = self.NitrogenIndexes[i]
            PossOxygenComb = self.GiveMeAllPossibleOxygenIndexCombinationFromThisAminoId(AminoIdForNitrogen)
            for genIndex in range(len(Chrom[i])):
                gen = Chrom[i][genIndex]
                if gen <= len(PossOxygenComb):
                    OxygenIndex = PossOxygenComb[gen-1]
                    AminoIdForOxygen = self.AminoOxygenIndexes[gen-1]
                    if NitrogenIndex < OxygenIndex:
                        AminoAcidsObjects[AminoIdForNitrogen-1].\
                            AtomsCombination[NitrogenIndex-AminoAcidsObjects[AminoIdForNitrogen-1].\
                                FirstAtomIndex].append(OxygenIndex)
                    elif OxygenIndex < NitrogenIndex:
                        AminoAcidsObjects[AminoIdForOxygen-1].\
                            AtomsCombination[OxygenIndex-AminoAcidsObjects[AminoIdForOxygen-1].\
                                FirstAtomIndex].append(NitrogenIndex)
                else:
                    break
        return AminoAcidsObjects