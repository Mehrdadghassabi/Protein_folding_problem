import numpy as np
import pandas as pd
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
    # df3.drop(['i'],axis = 1,inplace = True)
    return df3
