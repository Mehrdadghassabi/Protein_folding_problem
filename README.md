# protein folding problem
The protein folding problem is a critical puzzle in biology, focusing on unraveling how a linear sequence of amino acids organizes into its functional,three-dimensional structure.
Proteins are vital molecules in living organisms, carrying out essential biological functions, and their precise folding is crucial for proper functionality.
The process involves intricate interactions between amino acids, influenced by physicochemical properties and environmental conditions. 
Predicting the final folded structure accurately is challenging due to the vast conformational space proteins can explore.
Understanding protein folding has broad implications for drug development, structural biology, and disease research, as misfolded proteins can lead to various disorders.
Experimental and computational methods are employed to study protein folding,
but accurately predicting structures from sequences remains a complex and unsolved problem with significant implications for biology and medicine.

# Set up
Here it is a list of important amino-acids in this <a href=http://cup.uni-muenchen.de/ch/compchem/tink/as.html> link </a> ,
choose the amino-acids you want to use and download its jason from this <a href=https://pubchem.ncbi.nlm.nih.gov/compound/tyrosine> link </a>
and put jasons in this <a href=https://github.com/Mehrdadghassabi/Protein_folding_problem/tree/main/Help/AminoAcids> directory </a>

# Solution
for solving this problem we used genetic algorithm,
having 3 population (HowSulfurCombined,HowTheyCombined,HowRotationAndDeltaOccured) we used linear multi-population optimization.

# Run 
to find your optimized molecule download files in this link
https://drive.google.com/file/d/1pYKXACVMCKPd5nOSfTGSqNLNgEauYnuh/view?usp=sharing
and together with files in this repository put them in a directory then load the docker image
```
    sudo docker load < HW2Image
    sudo  docker run -it -v ./:/Libraries --entrypoint bash chargefw2
    cd Libraries/
    cd Help/
```
and run main.py
```
    python3 main.py
```
# Result
your molecule would be saved as a .pdb file in this <a href=https://github.com/Mehrdadghassabi/Protein_folding_problem/tree/main/Help> directory </a>
if you want to see how does your molecule look like upload your .pdb file in <a href=https://github.com/Mehrdadghassabi/Protein_folding_problem/blob/main/Show_molecule.ipynb> this </a>
jupyter notebook and run it!
![Screenshot from 2024-03-01 05-22-11](https://github.com/Mehrdadghassabi/Protein_folding_problem/assets/53050138/726dd495-9a98-4b4c-8769-29c7bab088f0)



