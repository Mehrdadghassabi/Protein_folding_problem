from ReadAminoAcidJsonFileExceptForTrp import *
import FitnessFunction as ff
from Optimizer import *

def get_Aminoacids_information():
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
    with open("AminoAcids/I.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    I_Amino = ReadJsonFile(data)
    with open("AminoAcids/S.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    S_Amino = ReadJsonFile(data)
    with open("AminoAcids/V.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    V_Amino = ReadJsonFile(data)
    with open("AminoAcids/T.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    T_Amino = ReadJsonFile(data)
    with open("AminoAcids/P.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    P_Amino = ReadJsonFile(data)
    with open("AminoAcids/L.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    L_Amino = ReadJsonFile(data)
    with open("AminoAcids/H.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    H_Amino = ReadJsonFile(data)
    with open("AminoAcids/Q.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    Q_Amino = ReadJsonFile(data)
    with open("AminoAcids/E.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    E_Amino = ReadJsonFile(data)
    with open("AminoAcids/D.json", 'r') as file:
        son_data = file.read()
    data = json.loads(json_data)
    D_Amino = ReadJsonFile(data)
    with open("AminoAcids/N.json", 'r') as file:
        son_data = file.read()
    data = json.loads(json_data)
    N_Amino = ReadJsonFile(data)
    with open("AminoAcids/A.json", 'r') as file:
        son_data = file.read()
    data = json.loads(json_data)
    A_Amino = ReadJsonFile(data)
    ResNames = ["Met", "Phe", "Lys", "Cys","Ile","Ser","Val","Thr","Pro",
                "Leu","His","Gln","Gln","Asp","Asn","Ala"]
    return (M_Amino,F_Amino,K_Amino,C_Amino,I_Amino,S_Amino,V_Amino,T_Amino,
            P_Amino,L_Amino,H_Amino,Q_Amino,E_Amino,D_Amino,N_Amino,A_Amino,ResNames)

if __name__=="__main__":
    (M_Amino,F_Amino,K_Amino,C_Amino,I_Amino,S_Amino,V_Amino,T_Amino,P_Amino,L_Amino,
     H_Amino,Q_Amino,E_Amino,D_Amino,N_Amino,A_Amino,ResNames) = get_Aminoacids_information()
    FitnessFunctionObj = ff.FitnessFunction([M_Amino,F_Amino,K_Amino,C_Amino,I_Amino,S_Amino,
                                             V_Amino,T_Amino,P_Amino,L_Amino,H_Amino,Q_Amino,
                                             E_Amino,D_Amino,N_Amino,A_Amino], ResNames)
    good_fitness = 100                                        
    optimize_solution(FitnessFunctionObj,good_fitness)
