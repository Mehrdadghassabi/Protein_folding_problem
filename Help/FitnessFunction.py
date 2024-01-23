from AminoAcidsControl import AminoAcis
from ReadAminoAcidJsonFileExceptForTrp import *
import chargefw2_python
from writepdbFile import MakePDBFileSeq
import os
from ReadAtomProperties import AtomProperties
from PreprocessOnCombinationsAtom import PreProcessOnCombinaions
import pandas as pd
import CaculateEnergyLib.ecalc as e
import random


class FitnessFunction:
    def __init__(self, SequenceOfAminoObjects=[], 
                 ResNames=[]):
        self.AtomPropertiesobj = AtomProperties("AtomsProperties.csv")
        self.ResNames=ResNames
        HowmanyAtoms=0
        self.SequenceOfAminoObjects = SequenceOfAminoObjects
        for AminoId in range(len(self.SequenceOfAminoObjects)):
            self.SequenceOfAminoObjects[AminoId].Find_Allname()
            self.SequenceOfAminoObjects[AminoId].CaculateCombinations(HowmanyAtoms, LastAmino=False)
            HowmanyAtoms=HowmanyAtoms+len(self.SequenceOfAminoObjects[AminoId].atom_elements)-1 
            
        
        for AminoId in range(len(self.SequenceOfAminoObjects)-1):
            del self.SequenceOfAminoObjects[AminoId].atom_coords[0][self.SequenceOfAminoObjects[AminoId].atom_elements.index("OXT")]
            del self.SequenceOfAminoObjects[AminoId].atom_coords[1][self.SequenceOfAminoObjects[AminoId].atom_elements.index("OXT")]
            del self.SequenceOfAminoObjects[AminoId].atom_coords[2][self.SequenceOfAminoObjects[AminoId].atom_elements.index("OXT")]
            del self.SequenceOfAminoObjects[AminoId].AtomsCombination[self.SequenceOfAminoObjects[AminoId].atom_elements.index("OXT")]
            self.SequenceOfAminoObjects[AminoId].atom_elements.remove("OXT")
            
        HowManyCombinationsCanWeHave = 0
        self.HowManyCombinationsCanWeHaveForSulfur = 0
        self.AminoAcisobj = AminoAcis(self.SequenceOfAminoObjects)
        self.AminoAcisobj.NitrogensAndOxygensDetection()
        for AminoId in range(1, len(self.SequenceOfAminoObjects)+1):
            for NIndex in self.AminoAcisobj.GiveMeAllNitrogensOfThisAminoId(AminoId):
                for OIndex in self.AminoAcisobj.GiveMeAllPossibleOxygenIndexCombinationFromThisAminoId(AminoId):
                    HowManyCombinationsCanWeHave+=1
        self.HowManyCombinationsCanWeHave = HowManyCombinationsCanWeHave
        
        for AminoId in range(1, len(self.SequenceOfAminoObjects)+1):
            for SulfureIndex in self.AminoAcisobj.GiveMeAllSulfursOfThisAminoId(AminoId):
                for SIndex in self.AminoAcisobj.GiveMeAllPossibleSulfurIndexCombinationFromThisAminoId(AminoId):
                    self.HowManyCombinationsCanWeHaveForSulfur+=1
    def TempInput(self, ):
        return [0]*self.HowManyCombinationsCanWeHave, [0]*6*len(self.SequenceOfAminoObjects)
    def TempInputForSulfur(self, ):
        return [0]*self.HowManyCombinationsCanWeHaveForSulfur
    def caculateEnergy(self, Combinations, DeltaPosition, SulfurCombinations=[]):
        destinationPDBFileName = str(Combinations)+str(DeltaPosition)+".pdb"
        index = -1
        AminoAcidsObjects = self.SequenceOfAminoObjects
        for AminoIdForNitrogen in range(1, len(self.SequenceOfAminoObjects)+1):
            index+=1
            for NIndex in self.AminoAcisobj.GiveMeAllNitrogensOfThisAminoId(AminoIdForNitrogen):
                for OIndex in self.AminoAcisobj.GiveMeAllPossibleOxygenIndexCombinationFromThisAminoId(AminoIdForNitrogen):
                    if Combinations[index]==1:
                        AminoIdForOxygen = self.AminoAcisobj.AminoOxygenIndexes[self.AminoAcisobj.OxygenIndexes.index(OIndex)]
                        if NIndex < OIndex:
                            AminoAcidsObjects[AminoIdForNitrogen-1].\
                                AtomsCombination[NIndex-AminoAcidsObjects[AminoIdForNitrogen-1].\
                                    FirstAtomIndex].append(OIndex)
                        elif OIndex < NIndex:
                            AminoAcidsObjects[AminoIdForOxygen-1].\
                                AtomsCombination[OIndex-AminoAcidsObjects[AminoIdForOxygen-1].\
                                    FirstAtomIndex].append(NIndex)
        if len(SulfurCombinations) and sum(SulfurCombinations)>0:
            for AminoIdForNitrogen in range(1, len(self.SequenceOfAminoObjects)+1):
                index+=1
                for SSIndex in self.AminoAcisobj.GiveMeAllSulfursOfThisAminoId(AminoIdForNitrogen):
                    for SIndex in self.AminoAcisobj.GiveMeAllPossibleSulfurIndexCombinationFromThisAminoId(AminoIdForNitrogen):
                        if Combinations[index]==1:
                            AminoIdForSulfur = self.AminoAcisobj.AminoSulfurIndexes[self.AminoAcisobj.SulfurIndexes.index(SIndex)]
                            if SIndex < SSIndex:
                                AminoAcidsObjects[AminoIdForSulfur-1].\
                                    AtomsCombination[SIndex-AminoAcidsObjects[AminoIdForSulfur-1].\
                                        FirstAtomIndex].append(SSIndex)
            
        chromosomeFor3DPred = []
        eachRowDeltaR = []
        eachRowDelta = []
        
        for i in DeltaPosition:
            if len(eachRowDeltaR)<3:
                eachRowDeltaR.append(i)
            elif len(eachRowDeltaR)==3 and len(eachRowDelta)<3:
                eachRowDelta.append(i)
            if len(eachRowDelta)==3:
                chromosomeFor3DPred.append([eachRowDeltaR.copy(), eachRowDelta[0], eachRowDelta[1], eachRowDelta[2]])
                eachRowDeltaR = []
                eachRowDelta = []
                
        AminosAtomsNewPosition = []
        atom_elements = []
        for AminoId in range(len(AminoAcidsObjects)):
            AminoAcidsObjects[AminoId].ChangeInitialVecTo(chromosomeFor3DPred[AminoId])
            AminoAtomsNewPosition = []
            for Atom in AminoAcidsObjects[AminoId].atom_elements:
                AminoAtomsNewPosition.append(AminoAcidsObjects[AminoId].GiveMeAtomPositionWithNewStartAndEndpoint(Atom))
            AminosAtomsNewPosition.append(AminoAtomsNewPosition)
            atom_elements.append(AminoAcidsObjects[AminoId].atom_elements)
        Atm_name, Res_name, Ress, X, Y, Z = \
                        MakePDBFileSeq(destinationPDBFileName, atom_elements,
                                        AminosAtomsNewPosition,
                                        self.ResNames)
        molecules = chargefw2_python.Molecules(destinationPDBFileName)
        charges_sqeqp = chargefw2_python.calculate_charges(molecules, 'sqeqp', 'SQEqp_10_Schindler2021_CCD_gen')
        for i in charges_sqeqp:
            charges_sqeqp = charges_sqeqp[i]
        try:
            os.remove(destinationPDBFileName)
        except:
            pass
        AtomIndexes = list(range(len(Atm_name)))
        
        Epsilon = []
        Sigma = []
        ASP = []
        Combined = []
        R = []
        for index in range(len(Atm_name)):
            props = self.AtomPropertiesobj.GiveMeAtomProps(Atm_name[index], Res_name[index])
            Epsilon.append(props[2])
            Sigma.append(props[3])
            ASP.append(props[4])
            R.append(props[1])
        for AminoId in range(len(AminoAcidsObjects)):
            for i in AminoAcidsObjects[AminoId].AtomsCombination:
                Combined.append(i)
        Combined, NextClue = PreProcessOnCombinaions(Combined)
        ProteinBigProps = {
            "i": AtomIndexes,
            "X": X,
            "Y": Y,
            "Z": Z,
            "R": R,
            "Epsilon": Epsilon,
            "Sigma": Sigma,
            "Charge": charges_sqeqp,
            "ASP": ASP,
            "Atm_name": Atm_name,
            "Res_name": Res_name,
            "Res": Ress,
            "Nexclude": NextClue,
            "Combined": Combined
        }
        df = pd.DataFrame(ProteinBigProps)
        protein_energy, vdw_energies, solvation_energies = e.energy(df)
        return protein_energy
        
        
if __name__=="__main__":
    with open("AminoAcids/M.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    M_Amino = ReadJsonFile(data)
    
    with open("AminoAcids/F.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    F_Amino = ReadJsonFile(data)
    with open("AminoAcids/K.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    K_Amino = ReadJsonFile(data)
    with open("AminoAcids/C.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    C_Amino = ReadJsonFile(data)
    ResNames = ["Met", "Phe", "Lys", "Cys"]
    FitnessFunctionObj = FitnessFunction(\
                    [M_Amino, F_Amino, K_Amino, C_Amino], ResNames)
    HowTheyCombined, HowRotationAndDeltaOccured = FitnessFunctionObj.TempInput()
    HowSulfurCombined = FitnessFunctionObj.TempInputForSulfur()
    print(HowTheyCombined, HowRotationAndDeltaOccured)
    print(HowSulfurCombined)
    HowTheyCombined = [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0] 
    HowRotationAndDeltaOccured = [65, 70, 300, 200, 10, 20, 110, 230, 300, 20, 20, 600, 290, 120, 260, 100, 290, 600, 100, 220, 190, 700, 400, 120]
    print(FitnessFunctionObj.caculateEnergy(HowTheyCombined, HowRotationAndDeltaOccured, SulfurCombinations=HowSulfurCombined))
