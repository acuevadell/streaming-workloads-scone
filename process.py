import os
import json
import glob
import statistics
import pandas as pd
from matplotlib import pyplot as plt

########################################################################
# Results
########################################################################

def get_duration(testcase, execution, secure):
    df = pd.read_csv('times_' + secure + '.csv')
    df = df[ (df['Test_Case'] == testcase) & (df['Exec'] == execution) ]['Time']
    return df.iloc[0]

report_data = {
    'Test_Case': [],
    'Producer_Rate': [],
    'Security': [],
    'Message_Size': [],
    'Execution': [],
    
    'OMB_Latency_50': [],
    'OMB_Latency_75': [],
    'OMB_Latency_95': [],
    'OMB_Latency_99': [],
    'OMB_Messages': [],
    'OMB_Bytes': [],
    'OMB_Duration': [],
    'OMB_Throughout': [],
}

df = pd.read_csv('test_cases.csv')
for index, row in df.iterrows():
    for i in range(1, 11):
        file_path = row['Test_Case'] + '-' + str(i) + '-OMB-UNSECURE.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        report_data['Test_Case'].append( row['Test_Case'] )
        report_data['Producer_Rate'].append( row['Production_Rate'] )
        report_data['Security'].append( 'Non-Secure' )
        report_data['Message_Size'].append( row['Size'] )
        report_data['Execution'].append( i )
        report_data['OMB_Latency_50'].append( data.get('aggregatedPublishLatency50pct') )
        report_data['OMB_Latency_75'].append( data.get('aggregatedPublishLatency75pct') )
        report_data['OMB_Latency_95'].append( data.get('aggregatedPublishLatency95pct') )
        report_data['OMB_Latency_99'].append( data.get('aggregatedPublishLatency99pct') )
        report_data['OMB_Messages'].append( data.get('totalMessagesSent') )
        sntbytes = data.get('totalBytesSent') * 0.000001
        duration = get_duration(row['Test_Case'], i, 'unsecure')
        report_data['OMB_Bytes'].append( sntbytes )
        report_data['OMB_Duration'].append( duration )
        report_data['OMB_Throughout'].append( sntbytes/duration )
        
        file_path = row['Test_Case'] + '-' + str(i) + '-OMB-SECURE.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        report_data['Test_Case'].append( row['Test_Case'] )
        report_data['Producer_Rate'].append( row['Production_Rate'] )
        report_data['Security'].append( 'Secure' )
        report_data['Message_Size'].append( row['Size'] )
        report_data['Execution'].append( i )
        report_data['OMB_Latency_50'].append( data.get('aggregatedPublishLatency50pct') )
        report_data['OMB_Latency_75'].append( data.get('aggregatedPublishLatency75pct') )
        report_data['OMB_Latency_95'].append( data.get('aggregatedPublishLatency95pct') )
        report_data['OMB_Latency_99'].append( data.get('aggregatedPublishLatency99pct') )
        report_data['OMB_Messages'].append( data.get('totalMessagesSent') )
        sntbytes = data.get('totalBytesSent') * 0.000001
        duration = get_duration(row['Test_Case'], i, 'secure')
        report_data['OMB_Bytes'].append( sntbytes )
        report_data['OMB_Duration'].append( duration )
        report_data['OMB_Throughout'].append( sntbytes/duration )

res = pd.DataFrame(report_data)
res.to_csv('result.csv', index=False)
print('Metrics written in result.csv')

########################################################################
# Mean Results
########################################################################

res_mean = res.groupby(['Test_Case', 'Security']).mean()
res_mean.pop('Execution')
res_mean.to_csv('result_mean.csv')
print('Metrics written in result_mean.csv')

########################################################################
# Histograms
########################################################################

report_data = {
    'Test_Case': [],
    'Producer_Rate': [],
    'Security': [],
    'Message_Size': [],
    'Execution': [],
    'Percentile': [],
    'Latency': [] 
}

df = pd.read_csv('test_cases.csv')
for index, row in df.iterrows():
    for i in range(1, 11):
        # Non-Secure
        file_path = row['Test_Case'] + '-' + str(i) + '-OMB-UNSECURE.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        latencies = data.get('aggregatedPublishLatencyQuantiles')
        for key, value in latencies.items():
            report_data['Test_Case'].append( row['Test_Case'] )
            report_data['Producer_Rate'].append( row['Production_Rate'] )
            report_data['Security'].append( 'Non-Secure' )
            report_data['Message_Size'].append( row['Size'] )
            report_data['Execution'].append( i )
            report_data['Percentile'].append( key )
            report_data['Latency'].append( value )
        # Secure
        file_path = row['Test_Case'] + '-' + str(i) + '-OMB-SECURE.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        latencies = data.get('aggregatedPublishLatencyQuantiles')
        for key, value in latencies.items():
            report_data['Test_Case'].append( row['Test_Case'] )
            report_data['Producer_Rate'].append( row['Production_Rate'] )
            report_data['Security'].append( 'Secure' )
            report_data['Message_Size'].append( row['Size'] )
            report_data['Execution'].append( i )
            report_data['Percentile'].append( key )
            report_data['Latency'].append( value )
    
res = pd.DataFrame(report_data)
res.to_csv('percentiles.csv', index=False)
print('Metrics written in percentiles.csv')
