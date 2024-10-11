import os
import pandas as pd
import cymetric as cym
from cymetric import graphs
from cymetric import timeseries

def get_data(file, ignore_commods=[]):
    db = cym.dbopen(file)
    evaler = cym.Evaluator(db)
    
    name = os.path.splitext(file)[0].split('/')[0]
    
    tr = evaler.eval('Transactions')
    mat = evaler.eval('Resources')
    transactions = pd.merge(mat, tr, on=['SimId', 'ResourceId'], how='inner')
    agents = evaler.eval('Agents')
    facilities = agents.loc[agents['Kind'] == "Facility"]
    ei = evaler.eval('ExplicitInventory')
    
    transactions = clean_transactions(transactions, agents, ignore_commods)
    
    data = {'ev': evaler,
            'agents': agents,
            'facilities': facilities,
            'transactions': transactions,
            'resources': mat,
            'ei': ei}
    
    return name, data

def clean_transactions(tr, agents, ignore_commods):
    tr = pd.merge(tr, 
                  agents, 
                  left_on=['SenderId', 'SimId'],
                  right_on=['AgentId', 'SimId'],
                  how='left'
        ).rename(columns={'Prototype':'SenderPrototype', 'Spec':'SenderSpec'}).drop(
        columns=[
            'AgentId',
            'EnterTime',
            'ExitTime',
            'ParentId',
            'Lifetime',
            'Kind'])
    tr = pd.merge(tr, 
                  agents,
                  left_on=['ReceiverId', 'SimId'],
                  right_on=['AgentId', 'SimId'],
                  how='left'
        ).rename(columns={'Prototype':'ReceiverPrototype', 'Spec':'ReceiverSpec'}).drop(
        columns=[
            'AgentId',
            'EnterTime',
            'ExitTime',
            'ParentId',
            'Lifetime',
            'Kind'])

    tr['SenderProtAgentId'] = tr['SenderPrototype'] + \
        tr['SenderId'].astype('str')
    tr['ReceiverProtAgentId'] = tr['ReceiverPrototype'] + \
        tr['ReceiverId'].astype('str')

    # drop all commodities that should be ignored
    tr=tr.loc[~tr['Commodity'].isin(ignore_commods)]

    tr['CumQuantityReceived'] = tr.groupby(by='ReceiverId')['Quantity'].cumsum()
    tr['CumQuantitySent'] = tr.groupby(by='SenderId')['Quantity'].cumsum()
    
    return tr