import os
import pandas as pd
import cymetric as cym
from cymetric import graphs
from cymetric import timeseries

def get_data(file):
    db = cym.dbopen(file)
    evaler = cym.Evaluator(db)
    
    name = os.path.splitext(file)[0]
    
    tr = evaler.eval('Transactions')
    mat = evaler.eval('Resources')
    transactions = pd.merge(mat, tr, on=['SimId', 'ResourceId'], how='inner')
    agents = evaler.eval('Agents')
    ei = evaler.eval('ExplicitInventory')
    

    
    data = {'ev': evaler,
            'agents': agents,
            'transactions': transactions,
            'ei': ei}
    
    return name, data