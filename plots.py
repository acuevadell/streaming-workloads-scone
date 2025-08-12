import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt

########################################################################
# Cumulative Distribution Function (CDF) Plots by Event Size
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

def format_label(size):
    if int(size) == 100:
        return '100B'
    elif int(size) == 1024:
        return '1KB'
    elif int(size) == 10240:
        return '10KB'
    elif int(size) == 102400:
        return '100KB'

def subplot_cdf(data1, data2, row, title):
    fig, axs = plt.subplots(2, 2)

    spr1 = split_event_size(data1)
    spr2 = split_event_size(data2)
    a = 0
    for i in range(2):
        for j in range(2):
            lbl = 'Event Size = ' + format_label(spr1[a]['Message_Size'].iloc[0])
            
            count, bins_count = np.histogram(spr1[a][row], bins=10)
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            axs[i][j].plot(bins_count[1:], cdf, label='Non-Secured')
            
            count, bins_count = np.histogram(spr2[a][row], bins=10)
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            axs[i][j].plot(bins_count[1:], cdf, label='Secured')

            axs[i][j].set_xlabel('Time (ms)')
            axs[i][j].set_title(lbl)
            axs[i][j].set_ylim(0, 1)
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;

    fig.suptitle(title)
    plt.tight_layout()
    #plt.show()
    plt.savefig(title + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot ' + title + '.png generated')


df = pd.read_csv('result.csv')
df1, df2 = get_dfs(df)

subplot_cdf(df1, df2, 'OMB_Latency_50', 'CDF Write Latencies 50 pct')
subplot_cdf(df1, df2, 'OMB_Latency_75', 'CDF Write Latencies 75 pct')
subplot_cdf(df1, df2, 'OMB_Latency_95', 'CDF Write Latencies 95 pct')
subplot_cdf(df1, df2, 'OMB_Latency_99', 'CDF Write Latencies 99 pct')

########################################################################
# Mean Plots by Event Size
########################################################################

def get_dfs(data):
    data1 = data[ data['Security'] == 'Non-Secure' ]
    data2 = data[ data['Security'] == 'Secure' ]
    return data1, data2

def get_security(data):
    return data['Security'].iloc[0]

def split_event_size(data):
    data1 = data[ data['Message_Size'] == 100 ]
    data2 = data[ data['Message_Size'] == 1024 ]
    data3 = data[ data['Message_Size'] == 10240 ]
    data4 = data[ data['Message_Size'] == 102400 ]
    return [data1, data2, data3, data4]

def format_label(size):
    if int(size) == 100:
        return '100B'
    elif int(size) == 1024:
        return '1KB'
    elif int(size) == 10240:
        return '10KB'
    elif int(size) == 102400:
        return '100KB'

def get_label(row):
    return str(int(row['Producer_Rate'])) + ' e/s'

def subplot_cdf(data1, data2, row, title, autolimit=False):
    fig, axs = plt.subplots(2, 2)
    
    spr1 = split_event_size(data1)
    spr2 = split_event_size(data2)
    a = 0
    for i in range(2):
        for j in range(2):
            labels = list(spr1[i].apply(get_label, axis=1))
            
            lbl = 'Event Size = ' + format_label(spr1[a]['Message_Size'].iloc[0])
            axs[i][j].plot(labels, spr1[a][row], label=get_security(spr1[a]) )
            axs[i][j].plot(labels, spr2[a][row], label=get_security(spr2[a]) )

            axs[i][j].set_yscale('log')
            if autolimit:
                axs[i][j].set_ylim(0.001, 1000)
            else:
                axs[i][j].set_ylim(1, 10000)
            axs[i][j].set_title(lbl)
            axs[i][j].legend()
            axs[i][j].grid(True)
            a += 1;

    fig.suptitle(title)
    plt.tight_layout()
    #plt.show()
    plt.savefig(title + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot ' + title + '.png generated')

df = pd.read_csv('result_mean.csv')
df1, df2 = get_dfs(df)

subplot_cdf(df1, df2, 'OMB_Latency_50', 'Write Latency 50 pct')
subplot_cdf(df1, df2, 'OMB_Latency_75', 'Write Latency 75 pct')
subplot_cdf(df1, df2, 'OMB_Latency_95', 'Write Latency 95 pct')
subplot_cdf(df1, df2, 'OMB_Latency_99', 'Write Latency 99 pct')

########################################################################
# Percentiles
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

def get_title(data):
    pr = data['Producer_Rate'].iloc[0]
    mz = data['Message_Size'].iloc[0]
    return 'Event Size ' + format_label(mz) + ' | Producer Rate ' + str(pr) + ' e/s'

def plot_histogram(data, test_case, execution=1):
    f1 = data[ (data['Test_Case'] == test_case) & (data['Execution'] == execution) & (data['Security'] == 'Non-Secure') ]
    f2 = data[ (data['Test_Case'] == test_case) & (data['Execution'] == execution) & (data['Security'] == 'Secure') ]
    title = get_title(f1)
    
    plt.scatter(f1['Latency'], f1['Percentile'], label='Non-Secure')
    plt.scatter(f2['Latency'], f2['Percentile'], label='Secure')
    
    plt.xlabel('Write Latency (Ms)')
    plt.ylabel('Percentile')
    plt.xscale('log')
    plt.xlim(0.1, 10000)
    plt.legend()
    plt.grid(True)
    plt.title(title)
    #plt.show()
    plt.savefig(test_case + '.png', bbox_inches='tight')
    plt.clf()
    print('Plot ' + test_case + '.png generated')

df = pd.read_csv('percentiles.csv')
plot_histogram(df, 'TC01')
#plot_histogram(df, 'TC02')
#plot_histogram(df, 'TC03')
#plot_histogram(df, 'TC04')
#plot_histogram(df, 'TC05')
#plot_histogram(df, 'TC06')
#plot_histogram(df, 'TC07')
#plot_histogram(df, 'TC08')
#plot_histogram(df, 'TC09')
#plot_histogram(df, 'TC10')
#plot_histogram(df, 'TC11', execution=2)
#plot_histogram(df, 'TC12')

########################################################################
# Percentiles by Producer Rate
########################################################################



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

def format_label(size):
    if int(size) == 100:
        return '100B'
    elif int(size) == 1024:
        return '1KB'
    elif int(size) == 10240:
        return '10KB'
    elif int(size) == 102400:
        return '100KB'

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
            
            lbl = 'Event Size = ' + format_label(spr1[a]['Message_Size'].iloc[0])
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

