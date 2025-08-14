import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt

########################################################################
# General function
########################################################################

def format_label(size):
    if int(size) == 100:
        return '100B'
    elif int(size) == 1024:
        return '1KB'
    elif int(size) == 10240:
        return '10KB'
    elif int(size) == 102400:
        return '100KB'

########################################################################
# CDF by Producer Rate
########################################################################

def get_title(data):
    pr = data['Producer_Rate'].iloc[0]
    mz = data['Message_Size'].iloc[0]
    return 'Event Size ' + format_label(mz) + ' | Producer Rate ' + str(pr) + ' e/s'

def split_data(data, test_cases):
    res = []
    for test_case in test_cases:
        tmp = data[ (data['Test_Case'] == test_case) ]
        res.append(tmp)
    return res

def subplot_cdf_percentile(data, test_cases):
    fig, axs = plt.subplots(2, 2)

    a = 0
    data_list = split_data(data, test_cases)
    
    for i in range(2):
        for j in range(2):
            f1 = data_list[a][ data_list[a]['Security'] == 'Non-Secure' ]
            f2 = data_list[a][ data_list[a]['Security'] == 'Secure' ]
            message_size = f1['Message_Size'].iloc[0]
            
            axs[i][j].plot(f1['Latency'], f1['Percentile'], label='STANDARD')
            axs[i][j].plot(f2['Latency'], f2['Percentile'], label='SCONE')
            axs[i][j].set_xscale('log')
            axs[i][j].set_xlim(0.1, 10000)
            axs[i][j].set_title('Event Size ' + format_label(message_size))
            axs[i][j].set_xlabel('Write Latency (ms)')
            axs[i][j].set_ylabel('Percentage')
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;

    producer_rate = data_list[0]['Producer_Rate'].iloc[0]
    #fig.suptitle('Producer Rate ' + str(producer_rate) + ' e/s')
    plt.tight_layout()
    #plt.show()
    plt.savefig('img/Percentile_PM' + str(producer_rate) + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot img/Percentile_PM' + str(producer_rate) + '.png generated')

df = pd.read_csv('percentiles.csv')
subplot_cdf_percentile(df, ['TC01', 'TC02', 'TC03', 'TC04'])
subplot_cdf_percentile(df, ['TC05', 'TC06', 'TC07', 'TC08'])
subplot_cdf_percentile(df, ['TC09', 'TC10', 'TC11', 'TC12'])

########################################################################
# Throughout by Event Size
########################################################################

def get_dfs(data):
    data1 = data[ data['Security'] == 'Non-Secure' ]
    data2 = data[ data['Security'] == 'Secure' ]
    return data1, data2

def split_event_size(data):
    data1 = data[ data['Message_Size'] == 100 ]
    data2 = data[ data['Message_Size'] == 1024 ]
    data3 = data[ data['Message_Size'] == 10240 ]
    data4 = data[ data['Message_Size'] == 102400 ]
    return [data1, data2, data3, data4]

def get_label(row):
    return str(int(row['Producer_Rate']))

def throughout_subplot(data1, data2, row):
    fig, axs = plt.subplots(2, 2)
    
    spr1 = split_event_size(data1)
    spr2 = split_event_size(data2)
    a = 0
    for i in range(2):
        for j in range(2):
            labels = list(spr1[i].apply(get_label, axis=1))
            
            lbl = 'Event Size ' + format_label(spr1[a]['Message_Size'].iloc[0])
            axs[i][j].plot(labels, spr1[a][row], label="Standard")
            axs[i][j].plot(labels, spr2[a][row], label="Secured")

            axs[i][j].set_yscale('log')
            axs[i][j].set_ylim(0.001, 1000)
            axs[i][j].set_title(lbl)
            axs[i][j].set_xlabel('Producer Rate (e/s)')
            axs[i][j].set_ylabel('Throughout (MB/s)')
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;
    
    plt.tight_layout()
    #plt.show()
    plt.savefig('img/Throughout.png', bbox_inches='tight')
    plt.clf()
    print('Plot img/Throughout.png generated')

df = pd.read_csv('result_mean.csv')
df1, df2 = get_dfs(df)

throughout_subplot(df1, df2, 'OMB_Throughout')

