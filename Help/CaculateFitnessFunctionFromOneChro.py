from ReadAminoAcidJsonFileExceptForTrp import *
import chargefw2_python


with open("AminoAcids/M.json", 'r') as file:
    json_data = file.read()
data = json.loads(json_data)
M_Amino = ReadJsonFile(data)
M_Amino.Find_Allname()

with open("AminoAcids/F.json", 'r') as file:
    json_data = file.read()
data = json.loads(json_data)
F_Amino = ReadJsonFile(data)
F_Amino.Find_Allname()


with open("AminoAcids/K.json", 'r') as file:
    json_data = file.read()
data = json.loads(json_data)
K_Amino = ReadJsonFile(data)
K_Amino.Find_Allname()
with open("AminoAcids/C.json", 'r') as file:
    json_data = file.read()
data = json.loads(json_data)
ReadJsonFileObj = ReadJsonFile(data)
C_Amino = ReadJsonFile(data)
C_Amino.Find_Allname()
ResNames = ["Met", "Phe", "Lys", "Cys"]


HowmanyAtoms=0
M_Amino.CaculateCombinations(HowmanyAtoms, LastAmino=False)
HowmanyAtoms=HowmanyAtoms+len(M_Amino.atom_elements)-1 # except OXT
F_Amino.CaculateCombinations(HowmanyAtoms, LastAmino=False)
HowmanyAtoms=HowmanyAtoms+len(F_Amino.atom_elements)-1 # except OXT
K_Amino.CaculateCombinations(HowmanyAtoms, LastAmino=False)
HowmanyAtoms=HowmanyAtoms+len(K_Amino.atom_elements)-1 # except OXT
C_Amino.CaculateCombinations(HowmanyAtoms, LastAmino=True)

del M_Amino.atom_coords[0][M_Amino.atom_elements.index("OXT")]
del M_Amino.atom_coords[1][M_Amino.atom_elements.index("OXT")]
del M_Amino.atom_coords[2][M_Amino.atom_elements.index("OXT")]
del M_Amino.AtomsCombination[M_Amino.atom_elements.index("OXT")]
M_Amino.atom_elements.remove("OXT")
del F_Amino.atom_coords[0][F_Amino.atom_elements.index("OXT")]
del F_Amino.atom_coords[1][F_Amino.atom_elements.index("OXT")]
del F_Amino.atom_coords[2][F_Amino.atom_elements.index("OXT")]
del F_Amino.AtomsCombination[F_Amino.atom_elements.index("OXT")]
F_Amino.atom_elements.remove("OXT")
del K_Amino.atom_coords[0][K_Amino.atom_elements.index("OXT")]
del K_Amino.atom_coords[1][K_Amino.atom_elements.index("OXT")]
del K_Amino.atom_coords[2][K_Amino.atom_elements.index("OXT")]
del K_Amino.AtomsCombination[K_Amino.atom_elements.index("OXT")]
K_Amino.atom_elements.remove("OXT")

from AminoAcidsControl import AminoAcis
AmoniAcids = [M_Amino, F_Amino, K_Amino, C_Amino]
AminoAcisobj = AminoAcis(AmoniAcids)
AminoAcisobj.NitrogensAndOxygensDetection()
# print(AminoAcisobj.GiveMeAllPossibleOxygenIndexCombinationFromThisAminoId(1))
# print(AminoAcisobj.GiveMeAllNitrogensOfThisAminoId(3))
# exit()
ChromHowAtomsGetCombination = [[3, 5, 4, 2, 1],
                               [4, 5, 3, 1, 2],
                               [1,2, 5, 3, 4],
                               [1, 5, 4, 1, 3],
                               [2, 4, 2, 3]]

AmoniAcids = AminoAcisobj.DecodeCombination(ChromHowAtomsGetCombination)
[M_Amino, F_Amino, K_Amino, C_Amino] = AmoniAcids



chromosomeFor3DPred = [[[100, 200, 777], 30, 40, 55],
                       [[102, 60, 20], 10, 60, 70],
                       [[180, 80, 830], 0, 15, 10],
                       [[160, 250, 105], 10, 78, 120]]


M_Amino.ChangeInitialVecTo(chromosomeFor3DPred[0])
M_AminoAtomsNewPos=[]
for Atom in M_Amino.atom_elements:
    M_AminoAtomsNewPos.append(M_Amino.GiveMeAtomPositionWithNewStartAndEndpoint(Atom))

    
F_Amino.ChangeInitialVecTo(chromosomeFor3DPred[1])
F_AminoAtomsNewPos=[]
for Atom in F_Amino.atom_elements:
    F_AminoAtomsNewPos.append(F_Amino.GiveMeAtomPositionWithNewStartAndEndpoint(Atom))

K_Amino.ChangeInitialVecTo(chromosomeFor3DPred[2])
K_AminoAtomsNewPos=[]
for Atom in K_Amino.atom_elements:
    K_AminoAtomsNewPos.append(K_Amino.GiveMeAtomPositionWithNewStartAndEndpoint(Atom))
    
    
C_Amino.ChangeInitialVecTo(chromosomeFor3DPred[2])
C_AminoAtomsNewPos = []
for Atom in C_Amino.atom_elements:
    C_AminoAtomsNewPos.append(C_Amino.GiveMeAtomPositionWithNewStartAndEndpoint(Atom))
    
from writepdbFile import MakePDBFileSeq

DesPath = "ForTest.pdb"
Atm_name, Res_name, Ress, X, Y, Z = MakePDBFileSeq(DesPath, [M_Amino.atom_elements, F_Amino.atom_elements, K_Amino.atom_elements, C_Amino.atom_elements],
               [M_AminoAtomsNewPos, F_AminoAtomsNewPos, K_AminoAtomsNewPos, C_AminoAtomsNewPos],
               ResNames)
molecules = chargefw2_python.Molecules(DesPath)
charges_sqeqp = chargefw2_python.calculate_charges(molecules, 'sqeqp', 'SQEqp_10_Schindler2021_CCD_gen')
charges_sqeqp = charges_sqeqp[DesPath[:-4]]
AtomIndexes = list(range(len(Atm_name)))

from ReadAtomProperties import AtomProperties
AtomPropertiesobj = AtomProperties("AtomsProperties.csv")
Epsilon = []
Sigma = []
ASP = []
Combined = []
R = []
for index in range(len(Atm_name)):
    props = AtomPropertiesobj.GiveMeAtomProps(Atm_name[index], Res_name[index])
    Epsilon.append(props[2])
    Sigma.append(props[3])
    ASP.append(props[4])
    R.append(props[1])
for i in M_Amino.AtomsCombination:
    Combined.append(i)
for i in F_Amino.AtomsCombination:
    Combined.append(i)
for i in K_Amino.AtomsCombination:
    Combined.append(i)
for i in C_Amino.AtomsCombination:
    Combined.append(i)
from PreprocessOnCombinationsAtom import PreProcessOnCombinaions
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
import pandas as pd
import CaculateEnergyLib.ecalc as e
df = pd.DataFrame(ProteinBigProps)
protein_energy, vdw_energies, solvation_energies = e.energy(df)
print(protein_energy)