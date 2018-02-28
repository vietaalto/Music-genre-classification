import numpy as np 
import pandas as pd
from IPython.display import display

def list_xls_sheet(dict):
	for i in range(len(dict.keys())):
		print('\033[1m Sheet %d: %s \033[0m' % ((i+1),list(dict.keys())[i]));
		
def view_xls_sheet(dict,sheetnumber = 'all'):
	if sheetnumber == 'all':	
		for i in range(len(dict.keys())):
			print('\033[1m Sheet %d: %s \033[0m' % ((i+1),list(dict.keys())[i]))
			with pd.option_context("display.max_colwidth",1000):
				display(list(dict.values())[i])
	else:
		for i in sheetnumber:
			print('\033[1m Sheet %d: %s \033[0m' % (i,list(dict.keys())[i-1]))
			with pd.option_context("display.max_colwidth",1000): 
				display(list(dict.values())[i-1]);
	

def freq(df, sort = 'count'):
    """
    Frequency table of each variable, either sorted by values or counts
    Input: dataframe
    Args:
        Sort: 'value' will display the frequency table by sorted values
              'count' (default) will display the frequency table by sorted frequency  
    Output: batch of frequency tables
    """
    print('\033[1m' + 'Frequency table of each variable:' + '\033[0m')
    for x in df.columns: 
        freq = df[x].value_counts(dropna = False).to_frame()
        if sort == "value" :
            freq.columns = ['Count'] 
            freq.index.names=[x] 
            display(freq.sort_index(axis=0).T)
        elif sort == 'count' :
            display(freq.sort_values(by = [x], ascending = False).T)
    # Ipython.display will display the dataframe in a nice tabular format
	
def freq_trans(series):
    """
    Return frequency of each element in a series (same index as original series)
    """
    return series.fillna('999').groupby(series.fillna('999')).transform('count') / len(series); 
	
def high_cardinality(df, how, threshold = 200, exception = []):
    """
    Processing high cardinality features
    Args:
    * Input: Dataframe
    * how: 'freq': change each value into its frequency
           'drop': delete the feature
           'label_encode': label encoding the features
           'label_encode_na': label encoding the features and keep NAs
    * threshold (default = 200): minimum number of different values that a feature 
    must have in order to be a high cardinality feature
    * exception (list): features that are unaffected by this function
    Output: no output. The function makes direct change to the dataframe
    """
    print ('Processing high-cardinality features:')
    for x in df.columns:
        if (df[x].dtype == 'O') and (len(df[x].unique()) > threshold) and (x not in exception):
            print (x, len(df[x].unique()))
            if how == 'freq': df[x] = freq_trans(df[x])
            elif how =='drop': del df[x]
            elif how == 'label_encode': df[x] = pd.factorize(df[x])[0]
            elif how == 'label_encode_na': df[x] = pd.factorize(df[x])[0].replace(-1,np.nan)
        else: df[x] = df[x]
    return df;
	
def label_encoding(df, na = -1):
    """
    Label encoding categorical features
    Args:
    * Input: Dataframe
    * na: True: keep NAs
          int: value to replace NAs 
    """
    print ('Label encoding categorical features:')
    for x in df.select_dtypes(include=[object]).columns:
        print (' ',x, len(df[x].unique()))
        if na == True:
            df[x] = pd.factorize(df[x])[0]
            df[x] = df[x].replace(-1,np.nan)
        else: df[x] = pd.factorize(df[x], na_sentinel=na)[0]
    return df;
	
def one_hot_encoding(df, na = False):
    """
    One hot encoding categorical features:
    Args:
    * Input: Dataframe
    * na: True: Add a column to indicate NaNs
          False: NaNs are ignored
    """
    print ('One hot encoding categorical features:')
    print ('Total original features (will be dropped after encoding): ',len(df.select_dtypes(include=[object]).columns))
    s = 0
    for x in df.select_dtypes(include=[object]).columns:
        print ('  ',x, len(df[x].unique()))
        s += len(df[x].unique());
    print ('Total new features will be added: ', s)
    print ('Data shape before encoding: ',df.shape)
    if na == True:
        df = pd.get_dummies(df,dummy_na=True)
    else: 
        print ('Total NAs cols will be dropped: ',
               df.select_dtypes(include=[object]).isnull().any().sum())
        df = pd.get_dummies(df);
    print ('Data shape after encoding: ',df.shape)
    return df;