# load data in from parsed EmotiBit CSV files, mouse/keyboard tracking, and timestamp file
# used by SVM and Random Forest models

import pandas as pd
import matplotlib.pyplot as plt

class LoadData():
    def __init__(self, file_HR, file_mouse, file_time):
        self.file_HR = file_HR
        self.file_mouse = file_mouse
        self.file_time = file_time
        self.dataframe = self.create_dataframe()

    # used the webpage below for help with pandas and creating the final dataframe (merging)
    # https://www.geeksforgeeks.org/python-pandas-merging-joining-and-concatenating/ 
    def create_dataframe(self):
        columns_HR = ['LocalTimestamp', 'EmotiBitTimestamp', 'HR']
        columns_mouse = ['Timestamp', 'APM', 'Erratic Score']
        columns_timestamp = ['Timestamp', 'Event']

        # NOTE: Next semester we will decide on specific features we want to focus on, may change based on the model accuracies
        dataframe_HR = pd.read_csv(self.file_HR, usecols=columns_HR)
        dataframe_mouse = pd.read_csv(self.file_mouse, usecols=columns_mouse)
        dataframe_time = pd.read_csv(self.file_time, usecols=columns_timestamp)

        # sync timestamps
        dataframe_time['Timestamp'] = pd.to_datetime(dataframe_time['Timestamp']) + pd.Timedelta(hours=8)
        dataframe_time['Timestamp'] = dataframe_time['Timestamp'].astype(int) // 10 ** 9
        dataframe_mouse['Timestamp'] = pd.to_datetime(dataframe_mouse['Timestamp']) + pd.Timedelta(hours=8)
        dataframe_mouse['Timestamp'] = dataframe_mouse['Timestamp'].astype(int) // 10 ** 9
        dataframe_HR['LocalTimestamp'] = dataframe_HR['LocalTimestamp'].astype(int)

        start_time = dataframe_time.loc[dataframe_time['Event'] == 'Game Start', 'Timestamp']
        
        try:
            if not start_time.empty:
                start_time = start_time.iloc[0]
        except AttributeError:
            print('No Game Start recorded')

        # calculate base heartrate
        base_heartrate = dataframe_HR[(dataframe_HR['LocalTimestamp'] >= dataframe_HR['LocalTimestamp'][0]) &
                                        (dataframe_HR['LocalTimestamp'] < start_time)]['HR'].mean()

        # NOTE: 10 s intervals (modify for interval duration)
        interval = 10

        dataframe_HR['Interval'] = ((dataframe_HR['LocalTimestamp'] - start_time) // interval).astype(int)
        dataframe_HR = dataframe_HR.groupby('Interval')['HR'].mean().reset_index()
        dataframe_mouse['Interval'] = ((dataframe_mouse['Timestamp'] - start_time) // interval).astype(int)
        dataframe_mouse = dataframe_mouse.groupby('Interval')[['APM', 'Erratic Score']].mean().reset_index()

        merged_dataframe = pd.merge(dataframe_HR, dataframe_mouse, on=['Interval'])
        merged_dataframe = merged_dataframe[merged_dataframe['Interval'] >= 0]
        merged_dataframe['Base HR'] = base_heartrate

        # # NOTE: key event = 1, else -1
        key_events = dataframe_time.loc[dataframe_time['Event'] == 'Key Event', 'Timestamp']
        print(key_events)
        key_event_intervals = ((key_events - start_time) // interval).astype(int)
        print(key_event_intervals)
        merged_dataframe['EventLabel'] = -1
        for interval in key_event_intervals:
            merged_dataframe.loc[merged_dataframe['Interval'] == interval, 'EventLabel'] = 1

        # # NOTE: label applied to entire dataframe (1 = skilled, -1 = unskilled player)
        # merged_dataframe['label'] = 1

        return merged_dataframe

# NOTE: temporary for this semester
HR_file = 'test1/2025-02-19_10-35-34-762016_HR.csv'
mouse_file = 'test1/tracking_data.csv'
time_file = 'test1/timestamp_data.csv'
df = LoadData(HR_file, mouse_file, time_file).dataframe
print(df)

# plt.title('Heart Rate Vs Time')
# plt.plot(df['Interval'], df['HR'], label='Heart Rate')
# plt.xlabel('Time (10s intervals)')
# plt.ylabel('Heart Rate')
# plt.legend()
# plt.savefig('HR_sample.jpg')
# plt.show()

# plt.title('EDA Vs Time')
# plt.plot(df['Interval'], df['EA'], label='EDA')
# plt.xlabel('Time (10s intervals)')
# plt.ylabel('EDA')
# plt.legend()
# plt.savefig('EDA_sample.jpg')
# plt.show()