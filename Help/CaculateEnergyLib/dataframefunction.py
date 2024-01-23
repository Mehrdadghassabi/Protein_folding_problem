# Module for processing and managing dataframes and files
import pandas as pd
import os

# Reads an input .crd filepath and creates a conveniently formatted dataframe which is used for calculating the energy of a protein. 
def frames(filePath, name):
    file = open(filePath+name)
    number_of_rows =int(file.readline())
    file.close()
    df = (pd.read_csv(filePath+name, skiprows = 2,delim_whitespace=True,header=None, index_col=None)).head(number_of_rows)
    df2 = (pd.read_csv(filePath+name, delim_whitespace=True,skiprows=2,header=None)).tail(number_of_rows)
    # Checks that the .crd file input has either 12 or 13 columns, to account for variance in the number of columns in the crd files provided.
    try:
        if len(df.columns) == 13 and len(df2.columns) == 13:
            df.drop(df.columns[-2],axis=1,inplace=True)
            df2.drop(df.columns[-2],axis=1,inplace=True)
        elif len(df.columns) == 12 and len(df2.columns) == 12:
            pass
    except ValueError:
        raise "[ERROR] Please keep a constant input shape"
    df.columns = ['i','X','Y','Z','R','Epsilon','Sigma','Charge','ASP','Atm_name','Res_name','Res']
    realcolumns = ['i','Nexclude','E_list','NA1','NA2','NA3','NA4','NA5','NA6','NA7','NA8','NA9']
    df2.columns = realcolumns
    df.Res = df['Res'].astype(int)
    df2['Combined'] = df2[realcolumns[2:]].apply(lambda x: [(int(val)-1) for val in x if not pd.isnull(val)], axis=1)
    df2.drop(realcolumns[2:12],axis  = 1, inplace=True)
    df3 = pd.merge(df,df2,on = ['i'])
    df3.drop(['i'],axis = 1,inplace = True)
    return df3

# Used to replicate our platform wide analysis. Compares two input dataframes of the same length 
# from analysis of two different platforms. 
def final_comparison_df(df1, df2):
    concat_output = pd.DataFrame()
    for i in range(0, (len(df1))):
       value1 = df1.iloc[i, 1] 
       value2 = df2.iloc[i, 1]
       if(value1<value2):
           concat_output = concat_output.append(df1.iloc[[i]])
       elif(value1>value2):
           concat_output = concat_output.append(df2.iloc[[i]])
    return concat_output

# Uses os.path.splitext to create a logical array indicating which files are of type .crd out of 
# a sorted list of potentially different file types. Also returns the name and type of each for 
# debugging purposes.
def check_if_crd(file_list):
    # If file_list is passed as a non-iterable string, converts that string into an iterable list.
    if isinstance(file_list, str):
        file_list = [file_list]
    mod_files = list() # 
    types = list()
    crd_check = list()
    for i in range(0, len(file_list)):
        split = os.path.splitext(file_list[i]) # Split "model1.crd" into "model1" and ".crd"
        mod_files.append(split[0])
        types.append(split[1])
        if types[i]==".crd":
            crd_check.append(True)
        else:
            crd_check.append(False)
    return crd_check, mod_files, types 