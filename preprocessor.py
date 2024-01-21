import re
import pandas as pd
import streamlit as st
def clean_message(message):
    # Remove non-printable characters using regex
    cleaned_message = re.sub(r'[^\x20-\x7E]', '', message)
    return cleaned_message
def preprocess(data):
    pattern = '.\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{1,2}]'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='[%d/%m/%y, %H:%M:%S]')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:

        entry = re.split('^(?:([^:]+))', message)

        if entry[1:]:  # username

            users.append(entry[1])
            #entry[2] = clean_message(entry[2])
            messages.append(entry[2])
        else:
            print('here')
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df['message'] = df['message'].str[1:]
    df['message'] = df['message'].str.strip()

    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['message'] = df['message'].astype(str)
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

