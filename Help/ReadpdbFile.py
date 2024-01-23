import pdbreader

pdb = pdbreader.read_pdb("AF-A0A2K5QXN6-F1-model_v4.pdb")
from Bio.PDB import PDBParser
import xpdb 
sloppyparser = PDBParser(
    PERMISSIVE=True, structure_builder=xpdb.SloppyStructureBuilder()
)
structure = sloppyparser.get_structure("./", "AF-A0A2K5QXN6-F1-model_v4.pdb")

# if you wonna write this 
sloppyio = xpdb.SloppyPDBIO()
sloppyio.set_structure(structure)
sloppyio.save("AF-A0A2K5QXN6-F1-model_v4-Cleared.pdb")