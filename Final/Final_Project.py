"""
Program/File: Final_Project.py
Name: Zachary Moccio
Date: 12/18/2022
Description: Final Project
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""
import csv
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk

data = pd.read_csv('C:/Users/Zachary Moccio/Python/Final/crash_info.csv')
data.sort_index()
index = data.set_index("UNIQUE KEY", inplace=True)
csv_file = open('C:/Users/Zachary Moccio/Python/Final/crash_info.csv', "r")
lines = csv_file.readlines()
data_headers = lines[0]
lines.pop(0)

st.title("Vehicle Collisions in NYC, Since 2015")
st.text("This page is designed to serve as a resourceful tool for anyone seeking to educate \n"
        "themselves on the underlying themes and/or patterns behind vehicle collisions. \n"
        "This specific sample dataset is recorded from collisions in NYC since 2015. Please \n"
        "use the provided tools below to observe the dataset as you wish to. The complete \n"
        "dataset can be found at the bottom of this page.")

st.write("Visuals - Noted Themes from Dataset:")

df_map = data.drop(["DATE", "TIME", "ZIP CODE", "LOCATION", "ON STREET NAME", "CROSS STREET NAME",
                    "OFF STREET NAME", "PERSONS INJURED", "PERSONS KILLED", "PEDESTRIANS INJURED",
                    "PEDESTRIANS KILLED", "CYCLISTS INJURED", "CYCLISTS KILLED", "MOTORISTS INJURED",
                    "MOTORISTS KILLED", "VEHICLE 1 TYPE", "VEHICLE 2 TYPE", "VEHICLE 3 TYPE", "VEHICLE 4 TYPE",
                    "VEHICLE 5 TYPE", "VEHICLE 1 FACTOR", "VEHICLE 2 FACTOR", "VEHICLE 3 FACTOR", "VEHICLE 4 FACTOR",
                    "VEHICLE 5 FACTOR"], inplace=False, axis=1)
df0 = df_map.loc[(df_map["LATITUDE"] > 0) & (df_map["LONGITUDE"] < 0)]

borough_list = []
hours = []
for line in lines:
    line = line.rstrip('\n').strip()
    # remove \n from each line
    fields = line.split(',')
    borough = fields[3]
    if borough != '':
        borough_list.append(borough)
    time = fields[2]
    times = time[0:2]
    times2 = times.replace(":", "")
    times2 = int(times2)
    hours.append(times2)
unique_bors = []
for i in borough_list:
    if i not in unique_bors:
        unique_bors.append(i)

select_bor = st.selectbox("Please select the borough you'd like to observe on the map: ", unique_bors)


def map():
    df_bor = df0.loc[df0["BOROUGH"] == select_bor]
    st.title(f"Collisions in {select_bor}")
    view_state = pdk.ViewState(latitude=df_bor["LATITUDE"].mean(),
                               longitude=df_bor["LONGITUDE"].mean(),
                               zoom=10,
                               pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=df_bor,
                       get_position='[LONGITUDE, LATITUDE]',
                       get_radius=100,
                       get_color=[169, 0, 100],
                       pickable=True
                       )
    layer2 = pdk.Layer('ScatterplotLayer',
                       data=df_bor,
                       get_position='[LONGITUDE, LATITUDE]',
                       get_radius=30,
                       get_color=[255, 255, 255],
                       pickable=True
                       )
    map = pdk.Deck(map_style='mapbox://styles/mapbox/outdoors-v11',
                   initial_view_state=view_state,
                   layers=[layer1, layer2])
    st.pydeck_chart(map)


map()


def early(hours):
    list = hours
    morning = [h for h in list if h <= 8]
    return morning


def midday(hours):
    list = hours
    afternoon = [h for h in list if 8 < h <= 16]
    return afternoon


def late(hours):
    list = hours
    night = [h for h in list if h >= 16]
    return night


def compare_hours_pie(hours):
    list = hours
    mass_total = 0
    for h in hours:
        mass_total += 1
    morning = early(list)
    morning_unique = []
    morn_count = 0
    morn_total = 0
    for h in morning:
        morn_count += 1
        if h not in morning_unique:
            morning_unique.append(h)
    for t in morning_unique:
        morn_total += 1
    afternoon = midday(list)
    afternoon_unique = []
    aft_count = 0
    aft_total = 0
    for h in afternoon:
        aft_count += 1
        if h not in afternoon_unique:
            afternoon_unique.append(h)
    for t in afternoon_unique:
        aft_total += 1
    night = late(list)
    night_unique = []
    night_count = 0
    night_total = 0
    for h in night:
        night_count += 1
        if h not in night_unique:
            night_unique.append(h)
    for t in night_unique:
        night_total += 1
    morning_unique.sort()
    afternoon_unique.sort()
    night_unique.sort()
    morn_perc = morn_count / mass_total
    aft_perc = aft_count / mass_total
    night_perc = night_count / mass_total
    timeframe = ['Early (0-8)', 'Mid-Day (8-16)', 'Late (16-24)']
    time_of_day = [morn_perc, aft_perc, night_perc]
    plt.pie(time_of_day, labels=timeframe, autopct='%.1f%%')
    plt.title("Collision Timeframes (24-hour)")
    print(f"Early Percentage: {morn_perc * 100}%\n"
          f"Mid-Day Percentage: {aft_perc * 100}%\n"
          f"Late Percentage: {night_perc * 100}%")


def brooke_time_compare():
    brook_total = []
    for line in lines:
        line = line.rstrip('\n').strip()
        # remove \n from each line
        fields = line.split(',')
        town = fields[3]
        morn_h = fields[2][:2]
        if ":" in morn_h:
            morn_h = morn_h.replace(":", "")
        morn_h = int(morn_h)
        if town == "BROOKLYN":
            brook_total.append(morn_h)
    return brook_total


def brook_time_hist(function):
    total_list = function
    # Set up the bins using plt.hist(bins = [])
    plt.hist(total_list, bins=[0, 8, 16, 24], color='grey')
    # Each range exists between the two consecutive numbers in bins list
    # Set labels for x-axis using plt.xticks([])
    plt.xticks([0, 8, 16, 24])
    # xticks does not need to match bins
    # Add title, labels, and show
    plt.title("Collision Times in Brooklyn")
    plt.xlabel('24-Hour Time Period')
    plt.ylabel('Quantity of Collisions in Time Period')
    plt.show()


from PIL import Image

pie = Image.open("C:/Users/Zachary Moccio/Python/Final/hours.png")
st.image(pie, width=600)


def collision_graph(town_list):
    unique_boroughs = []
    total_boroughs = 0
    for i in town_list:
        if i not in unique_boroughs:
            total_boroughs += 1
            unique_boroughs.append(i)
    q_total = 0
    k_total = 0
    x_total = 0
    si_total = 0
    m_total = 0
    for i in town_list:
        if i == unique_boroughs[0]:
            q_total += 1
        elif i == unique_boroughs[1]:
            k_total += 1
        elif i == unique_boroughs[2]:
            x_total += 1
        elif i == unique_boroughs[3]:
            si_total += 1
        else:
            m_total += 1
    num_boroughs = [q_total, k_total, x_total, si_total, m_total]
    array = np.arange(len(unique_boroughs))
    plt.xticks(array, unique_boroughs)
    plt.bar(array, num_boroughs, width=0.25, color="red")
    plt.xlabel("Boroughs")
    plt.ylabel("Number of Collsions")
    plt.title("Number of Vehicle Collisions per Borough")


from PIL import Image

bar = Image.open("C:/Users/Zachary Moccio/Python/Final/vehicles_per_borough.png")
st.image(bar, width=600)

from PIL import Image

hist = Image.open("C:/Users/Zachary Moccio/Python/Final/hist.png")
st.image(hist, width=600)

st.sidebar.write("\n")
st.sidebar.write("1. Looking for a specific detail about the collisions?")
st.sidebar.write("\n")
with open('C:/Users/Zachary Moccio/Python/Final/crash_info.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for column in csv_reader:
        headers = column
        break
select_header = st.sidebar.selectbox("Please select the vehicle detail you'd like to observe: ", headers[1:])
st.text("#1.")
st.write("Your selected target data with Unique Key:")
header = data.loc[:, [select_header]]
st.write(header)

st.sidebar.write("\n")
st.sidebar.write("2. Looking for a certain incident?")
st.sidebar.write("\n")
keys = []
for line in lines:
    line = line.rstrip('\n').strip()
    # remove \n from each line
    if line != '':
        fields = line.split(',')
        key = fields[0]
        key = int(key)
        if key not in keys:
            keys.append(key)
keys.sort()
incident = st.sidebar.select_slider("Please choose the unique key for the incident you'd like to observe: ", keys)
st.text("#2.")
st.write("Your selected target data with Unique Key:")
un_key = data.loc[incident, :]
st.write(un_key)

st.sidebar.write("\n")
st.sidebar.write("3. Looking for incidents with consequential injuries?")
st.sidebar.write("\n")
inj_types_list = ['PERSONS INJURED', 'PEDESTRIANS INJURED', 'CYCLISTS INJURED', 'MOTORISTS INJURED']
inj_type = st.sidebar.multiselect("Please select the injury types you'd like to observe:", inj_types_list)
st.text("#3.")
st.write("Your designated injury-incidents (select in sidebar):")
for i in inj_type:
    injuries = data.loc[(data[i] > 0), ["DATE", "TIME", i]]
    lengths = len(injuries)
    quant = int(lengths)
    st.write(injuries)
    st.write(f"There are {quant} injuries recorded of this type.")

st.write("\n")
st.text("#4.")
st.write("Complete dataset on the vehicle collisions: ")
st.sidebar.write("\n")
st.sidebar.write("4. Looking to sort the data?")
st.sidebar.write("\n")
sorted_data = st.sidebar.selectbox("Please select the header you'd like to sort by: ", headers[1:])
st.write(data.sort_values(sorted_data))
