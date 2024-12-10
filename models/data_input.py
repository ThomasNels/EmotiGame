import pandas as pd
import matplotlib.pyplot as plt

class LoadData():
    def __init__(self, file_HR, file_EDA):
        self.file_HR = file_HR
        self.file_EDA = file_EDA
        self.dataframe = self.create_dataframe()

    def create_dataframe(self):
        columns_HR = ['LocalTimestamp', 'EmotiBitTimestamp', 'HR']
        # columns_BI = ['LocalTimestamp', 'EmotiBitTimestamp', 'BI']
        columns_EA = ['LocalTimestamp', 'EmotiBitTimestamp', 'DataLength', 'EA']
        # columns_EL = ['LocalTimestamp', 'EmotiBitTimestamp', 'DataLength', 'EL']

        # NOTE: Next semester we will decide on specific features we want to focus on, may change based on the model accuracies
        dataframe_HR = pd.read_csv(self.file_HR, usecols=columns_HR)
        # dataframe_BI = pd.read_csv('2024-11-23_23-37-50-480147_BI.csv', usecols=columns_BI)
        # dataframe_HR = pd.merge(dataframe_HR, dataframe_BI, on=['LocalTimestamp', 'EmotiBitTimestamp'])

        # print(dataframe_HR)
        # NOTE: Work on Spring Semester to decide on exact features we want to use
        dataframe_EA = pd.read_csv(self.file_EDA, usecols=columns_EA)
        # dataframe_EL = pd.read_csv('2024-11-23_23-37-50-480147_EL.csv', usecols=columns_EL)
        # dataframe_EDA = pd.merge(dataframe_EL, dataframe_EA, on=['LocalTimestamp', 'EmotiBitTimestamp'])
        dataframe_EA = dataframe_EA[dataframe_EA['DataLength'] == 1]
        dataframe_EA = dataframe_EA.drop(columns=['DataLength'])
        # dataframe_EL = pd.read_csv('2024-11-23_23-37-50-480147_EL.csv', usecols=columns_EL)
        # dataframe_EL = dataframe_EL[dataframe_EL['DataLength'] == 1]
        # dataframe_EL = dataframe_EL.drop(columns=['DataLength'])
        # dataframe_EDA = pd.merge(dataframe_EL, dataframe_EA, on=['LocalTimestamp', 'EmotiBitTimestamp'])
        dataframe_EDA = dataframe_EA

        # print(dataframe_EDA)

        # NOTE: Time is in ms
        # NOTE: likely will be used to find EmotiBitTimestamp for key events next semester
        # dataframe_times = pd.read_csv('2024-11-23_23-37-50-480147_timesyncmap.csv')
        # start_time = dataframe_times.iloc[0]['EmotiBitStartTime']
        # end_time = dataframe_times.iloc[0][' EmotiBitEndTime']

        start_dataframe_time = max(dataframe_HR.iloc[0]['EmotiBitTimestamp'], dataframe_EDA.iloc[0]['EmotiBitTimestamp'])
        # print(start_dataframe_time)
        # end_dataframe_time = min(dataframe_HR.iloc[-1]['EmotiBitTimestamp'], dataframe_EDA.iloc[-1]['EmotiBitTimestamp'])
        # print(end_dataframe_time)

        # NOTE: 10 s intervals (modify for interval duration)
        interval = 10000

        # NOTE: only here for testing purposes during this semester
        key_event_time = 528939
        key_event_interval = ((key_event_time - start_dataframe_time) // interval).astype(int)
        # print(key_event_interval)

        dataframe_HR['Interval'] = ((dataframe_HR['EmotiBitTimestamp'] - start_dataframe_time) // interval).astype(int)
        dataframe_HR = dataframe_HR.groupby('Interval')['HR'].mean().reset_index()
        # print(dataframe_HR)
        dataframe_EDA['Interval'] = ((dataframe_EDA['EmotiBitTimestamp'] - start_dataframe_time) // interval).astype(int)
        dataframe_EDA = dataframe_EDA.groupby('Interval')['EA'].mean().reset_index()
        # print(dataframe_EDA)

        merged_dataframe = pd.merge(dataframe_HR, dataframe_EDA, on=['Interval'])

        # NOTE: key event = 1, else -1
        merged_dataframe['EventLabel'] = -1
        for index, row in merged_dataframe.iterrows():
            if row['Interval'] == key_event_interval:
                merged_dataframe.at[index, 'EventLabel'] = 1

                # NOTE: Next semester decide on how to label events after test run of study and monitoring live data
                merged_dataframe.at[index+1, 'EventLabel'] = 1
                break
        # print(merged_dataframe)

        # NOTE: label applied to entire dataframe (1 = skilled, -1 = unskilled player)
        merged_dataframe['label'] = 1

        return merged_dataframe

# NOTE: temporary for this semester
HR_file = '2024-11-23_23-37-50-480147_HR.csv'
EA_file = '2024-11-23_23-37-50-480147_EA.csv'
df = LoadData(HR_file, EA_file).dataframe
print(df)

plt.title('Heart Rate Vs Time')
plt.plot(df['Interval'], df['HR'], label='Heart Rate')
plt.xlabel('Time (10s intervals)')
plt.ylabel('Heart Rate')
plt.legend()
plt.savefig('HR_sample.jpg')
plt.show()

plt.title('EDA Vs Time')
plt.plot(df['Interval'], df['EA'], label='EDA')
plt.xlabel('Time (10s intervals)')
plt.ylabel('EDA')
plt.legend()
plt.savefig('EDA_sample.jpg')
plt.show()