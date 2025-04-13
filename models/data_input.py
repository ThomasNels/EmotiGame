# load data in from parsed EmotiBit CSV files, mouse/keyboard tracking, and timestamp file
# used by Data Notebooks and Models

import pandas as pd

class LoadData():
    def __init__(self, file_HR, file_mouse, skilled_player=False, hours=7):
        self.file_HR = file_HR
        self.file_mouse = file_mouse
        self.skilled_player = skilled_player
        self.hours = hours
        self.dataframe = self.create_dataframe()

    # used the webpage below for help with pandas and creating the final dataframe (merging)
    # https://www.geeksforgeeks.org/python-pandas-merging-joining-and-concatenating/ 
    def create_dataframe(self):
        # desired columns
        columns_HR = ['LocalTimestamp', 'HR']
        columns_mouse = ['Timestamp', 'APM', 'Importance', 'Game Time']

        # create dataframe
        dataframe_HR = pd.read_csv(self.file_HR, usecols=columns_HR)
        dataframe_mouse = pd.read_csv(self.file_mouse, usecols=columns_mouse)
        dataframe_mouse['Timestamp'] = pd.to_datetime(dataframe_mouse['Timestamp']) + pd.Timedelta(hours=self.hours)
        dataframe_mouse['Timestamp'] = dataframe_mouse['Timestamp'].astype(int) // 10 ** 9
        dataframe_HR['LocalTimestamp'] = dataframe_HR['LocalTimestamp'].astype(int)

        # record game start time
        start_time = dataframe_mouse.loc[dataframe_mouse['Game Time'] == 'start', 'Timestamp']

        try:
            if not start_time.empty:
                start_time = start_time.iloc[0]
        except AttributeError:
            print('No Game Start recorded')

        # record game end time
        end_time = dataframe_mouse.loc[dataframe_mouse['Game Time'] == 'end', 'Timestamp']
        try:
            if not end_time.empty:
                end_time = end_time.iloc[0]
        except AttributeError:
            print('No Game End recorded')

        # calculate base heartrate
        base_heartrate = dataframe_HR[(dataframe_HR['LocalTimestamp'] >= dataframe_HR['LocalTimestamp'][0]) &
                                        (dataframe_HR['LocalTimestamp'] < start_time)]['HR'].mean()

        # 10 s intervals
        interval = 10

        # clip dataframe to end_time interval + 1
        dataframe_HR = dataframe_HR[dataframe_HR['LocalTimestamp'] <= end_time + interval]
        dataframe_mouse = dataframe_mouse[dataframe_mouse['Timestamp'] <= end_time + interval]

        # Sync intervals between dataframes to merge into one
        dataframe_HR['Interval'] = ((dataframe_HR['LocalTimestamp'] - start_time) // interval).astype(int)
        dataframe_HR = dataframe_HR.groupby('Interval')['HR'].mean().reset_index()

        dataframe_mouse = dataframe_mouse.drop(['Game Time', 'Timestamp'], axis=1)
        dataframe_mouse = dataframe_mouse.dropna()
        dataframe_mouse['Interval'] = range(len(dataframe_mouse))

        # merge into one dataframe
        merged_dataframe = pd.merge(dataframe_HR, dataframe_mouse, on=['Interval'])
        merged_dataframe = merged_dataframe[merged_dataframe['Interval'] >= 0]
        merged_dataframe['Base HR'] = base_heartrate

        # label events and drop Game Time and Timestamp
        event_map = {'low': 0, 'med': 1, 'high': 2}
        merged_dataframe['Importance'] = merged_dataframe['Importance'].map(event_map)

        # NOTE: label applied to entire dataframe (1 = skilled, -1 = unskilled player)
        if self.skilled_player == True:
            merged_dataframe['Label'] = 1
        else:
            merged_dataframe['Label'] = 0

        return merged_dataframe