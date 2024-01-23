from Bio.PDB import PDBIO, Model, Atom, Chain, Residue

def MakePDBFileSeq(DestinationPathPDBFile="", AtomsName=[[]], AtomsCoords=[[]], AminoAcidName=""):
    io = PDBIO()
    Atm_name = []
    Res_name = []
    X = []
    Y = []
    Z = []
    Ress=[]
    model = Model.Model(0)
    chain_A = Chain.Chain("A")
    for aminoacidIndex in range(len(AminoAcidName)):
        Res = Residue.Residue((" ", aminoacidIndex+1, " "), AminoAcidName[aminoacidIndex], " ")
        for atomIndex in range(len(AtomsName[aminoacidIndex])):
            Res.add(Atom.Atom(AtomsName[aminoacidIndex][atomIndex], AtomsCoords[aminoacidIndex][atomIndex], 0.0, 1., " ", AtomsName[aminoacidIndex][atomIndex], aminoacidIndex, AtomsName[aminoacidIndex][atomIndex][0]))
            Atm_name.append(AtomsName[aminoacidIndex][atomIndex])
            Res_name.append(AminoAcidName[aminoacidIndex])
            X.append(AtomsCoords[aminoacidIndex][atomIndex][0])
            Y.append(AtomsCoords[aminoacidIndex][atomIndex][1])
            Z.append(AtomsCoords[aminoacidIndex][atomIndex][2])
            Ress.append(aminoacidIndex+1)
        chain_A.add(Res)
    model.add(chain_A)
    io.set_structure(model)
    io.save(DestinationPathPDBFile)
    return Atm_name, Res_name, Ress, X, Y, Z
    