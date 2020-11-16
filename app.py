import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

# Reading the world data from covid.ourworldindata.org
# The data is cumulative, so the total_cases for a day sums up the cases per day
df1 = pd.read_csv("https://covid.ourworldindata.org/data/ecdc/full_data.csv")
analysis = st.sidebar.selectbox("Analysis", ["Overview", "Fatalities", "Trend"])
if analysis == "Overview":
    o1 = st.selectbox("Dashboards", ["Global", "India"])
    if o1 == "Global":
        # Covid 19 Global Dashboard title formatting with markdown
        st.markdown(
            '''
            <link rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=Suez+One">
            <div style="font-family: 'Suez One';font-size:70px; background-color:white; color:black"><center>Covid-19 Global Dashboard</center></div>
            ''', unsafe_allow_html=True
        )
        st.header(" ")

        # Getting the unique dates present in the dataset
        dates = list(set(df1.date))
        # Sorting the dates to get the most recent date
        # If we use datetime to get the current day, at 12am there will be no data to show as the data for the day would not be updated yet
        dates.sort()
        dt_tday = dates[-1]
        # Getting the data for the most recent date
        td = df1[df1['date'] == dt_tday]
        # Resetting the index
        td = td.reset_index(drop=True)
        # This the text used for the hover data, anything to be added to it should be done here
        # Add a '<br>' after each name and data to move to the next line
        txt = ' Country: ' + td['location'].astype(str) + '<br>' + ' Cases: ' + td['total_cases'].astype(
            str) + '<br>' + ' Deaths: ' + td['total_deaths'].astype(str)
        # The country names are converted to lowercase for compatibility with the inbuilt location names in graph_object plotting
        td['location'] = td['location'].str.lower()
        # Saving the world data from the dataset
        world = td[td['location'] == 'world']
        # Removing the world data from the dataset
        td = td[td['location'] != 'world']
        # This is to plot the global map
        fig1 = go.Figure(data=go.Choropleth(
            locations=td['location'],
            locationmode='country names',
            z=td['total_cases'],  # Colour of the countries are based on this value
            colorbar_title="Total Cases",
            text=txt,  # Hoverdata
            colorbar={'len': 0.75, 'lenmode': 'fraction'},
            marker_line_color='black',
            marker_line_width=0.5))

        fig1.update_layout(
            title={  # This is to set the size and location of the title of the map
                'text': 'Global Covid Data',
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'Black', 'size': 30}},
            geo=dict(  # Removing the frame borders and giving the projection type
                showframe=False,
                showcoastlines=True,
            ),
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ))
        st.plotly_chart(fig1, config={'displayModeBar': False})
        # Printing out the statistics of the world for the most recent date
        st.header("World Statistics")
        c = world['total_cases'].iloc[0]
        d = world['total_deaths'].iloc[0]
        st.write("Confirmed Cases:", int(c))
        st.write("Confirmed Deaths:", int(d))
        st.write("Fatality Rate:", round((d / c) * 100, 2), '%')
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.header("Country-wise statistics")
        # Getting a list of all the unique contries present after removing 'World'
        countries = list(set(df1.location))
        countries.remove('World')
        countries.remove('International')
        countries.sort()
        countries.remove('India')
        countries.insert(0, 'India')
        # The dropdown for selecting the country
        option1 = st.selectbox("Country", countries)
        # Checking if there is a country selected and if there is, give its information
        if (len(option1) != 0):
            # This is to pull out the day and total cases for the selected country
            day_data = {}
            temp = df1[df1['location'] == option1]
            day_data[f'{option1} date'] = temp['date']
            day_data[f'{option1} cases'] = temp[['total_cases']].diff(axis=0).fillna(0).astype(int)
            day_data[f'{option1} deaths'] = temp[['total_deaths']].diff(axis=0).fillna(0).astype(int)
            # Plot used for the Univ.ai Covid dashboard question
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(211)
            ef = pd.DataFrame()
            ef['date'] = day_data[f'{option1} date'].astype('datetime64[ns]')
            ef['cases'] = day_data[f'{option1} cases']
            ax.bar(ef.date, ef.cases, color='#007acc', alpha=0.3)
            ax.plot(ef.date, ef.cases, marker='o', color='#007acc')
            # ax.text(0.01,1,f'{option1} daily case count',transform = ax.transAxes, fontsize = 23);
            ax.set_title(f'{option1} daily case count', fontsize=23)
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
            ax.tick_params(rotation=60)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax1 = fig.add_subplot(212)
            ef['deaths'] = day_data[f'{option1} deaths']
            ax1.bar(ef.date, ef.deaths, color='#007acc', alpha=0.3)
            ax1.plot(ef.date, ef.deaths, marker='o', color='#007acc')
            ax1.set_title(f'{option1} daily death count', fontsize=23)
            ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
            ax1.tick_params(rotation=60)
            ax1.spines['right'].set_visible(False)
            ax1.spines['top'].set_visible(False)
            fig.tight_layout()
            st.plotly_chart(fig, config={'displayModeBar': False})
            # Printing out information for the country for the most recent date
            c = td[td['location'] == option1.lower()]['total_cases'].iloc[0]
            d = td[td['location'] == option1.lower()]['total_deaths'].iloc[0]
            st.write("Confirmed Cases:", int(c))
            st.write("Confirmed Deaths:", int(d))
            st.write("Fatality Rate:", round((d / c) * 100, 2), '%')
        df = df1
        df = df[(df.location != 'World') & (df.location != 'International')]
        df['date'] = df['date'].astype('datetime64[ns]')
        st.header('Comparison of infection growth')
        st.write("")
        country_name_input = st.multiselect(
            'Country name',
            df.groupby('location').count().reset_index()['location'].tolist())
        # by country name
        if len(country_name_input) > 0:
            subset_data = df[df['location'].isin(country_name_input)]

            total_cases_graph = alt.Chart(subset_data).transform_filter(
                alt.datum.total_cases > 0
            ).mark_line().encode(
                x=alt.X('date:T', title='Date', timeUnit='yearmonthdate', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('total_cases:Q', title='Confirmed cases'),
                color='location',
                tooltip=['location', 'total_cases'],
            ).properties(
                width=750,
                height=300
            ).configure_axis(
                labelFontSize=10,
                titleFontSize=15
            )
            st.altair_chart(total_cases_graph)
    elif o1 == "India":
        # Repeating the same for India
        st.title('Covid Analysis for India')
        # Reading the data from covid19india.org
        data = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")
        # The data contains an unassigned state which is removed
        df = data[data['State'] != 'State Unassigned']
        # Removing unnecessary columns
        df = df[['Date', 'State', 'Confirmed', 'Recovered', 'Deceased']]
        # Renaming the columns since the hover data is based on the column names
        df.columns = ['Date', 'State', 'Confirmed Cases', 'Recovered', 'Deceased']
        # Getting a list of all dates
        dates = list(set(df.Date))
        dates.sort()
        # Getting a list of all States
        states = list(set(df.State))
        # Findingtodays date
        dt_tday = dates[-1]
        # Finding yesterdays date
        dt_yday = dates[-2]
        # Getting todays data for all states available
        dfc = df[df['Date'] == dt_tday]
        # This is done for compatibility of state names with the geojson
        dfc = dfc.replace("Andaman and Nicobar Islands", 'Andaman & Nicobar')
        # Saving the data for India
        India = dfc[dfc['State'] == 'India']
        # Removing India's data from the dataset
        dfc = dfc[dfc['State'] != 'India']
        # Link to the geojson
        gj = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        fig2 = px.choropleth(
            dfc,
            geojson=gj,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Confirmed Cases',
            color_continuous_scale="Blues",
            projection="mercator",
            hover_data=['State', 'Confirmed Cases', 'Deceased',
                        'Recovered'])  # The data is pulled out from the dataframe dfc in this case
        fig2.update_geos(fitbounds="locations", visible=False)
        fig2.update_layout(
            autosize=False,
            width=700,  # Here I am able to change the height and width of the graph unlike before
            height=700,
            title={
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'blue', 'size': 40}}
        )
        st.plotly_chart(fig2, config={'displayModeBar': False})
        # Printing out India's stats
        st.header("India Statistics")
        c = India['Confirmed Cases'].iloc[0]
        d = India['Deceased'].iloc[0]
        r = India['Recovered'].iloc[0]
        st.write("Confirmed Cases:", int(c))
        st.write("Confirmed Deaths:", int(d))
        st.write("Recovered:", int(r))
        st.write("Current Cases:", int(c - d - r))
        st.write("Fatality Rate:", round((d / c) * 100, 2), '%')
        st.write("Recovery Rate:", round((r / c) * 100, 2), '%')
        # Removing India from the list of states
        states = list(dfc.sort_values(by=['Confirmed Cases', 'Deceased'], ascending=[False, False]).State)
        option = st.selectbox("State", states)
        # Giving the information for each state similar to info for each country
        if (len(option) != 0):
            day_data = {}
            temp = df[df['State'] == option]
            day_data[f'{option} date'] = temp['Date']
            day_data[f'{option} cases'] = temp[['Confirmed Cases']].diff(axis=0).fillna(0).astype(int)
            day_data[f'{option} recovered'] = temp[['Recovered']].diff(axis=0).fillna(0).astype(int)
            day_data[f'{option} deaths'] = temp[['Deceased']].diff(axis=0).fillna(0).astype(int)
            fig = plt.figure(figsize=(8, 9))
            ax = fig.add_subplot(311)
            ef = pd.DataFrame()
            ef['date'] = day_data[f'{option} date'].astype('datetime64[ns]')
            ef['cases'] = day_data[f'{option} cases']
            ax.bar(ef.date, ef.cases, color='#007acc', alpha=0.3)
            ax.plot(ef.date, ef.cases, marker='o', color='#007acc')
            ax.set_title(f'{option} daily case count', fontsize=23);
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
            ax.tick_params(rotation=60)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax1 = fig.add_subplot(312)
            ef['deaths'] = day_data[f'{option} deaths']
            ax1.bar(ef.date, ef.deaths, color='#007acc', alpha=0.3)
            ax1.plot(ef.date, ef.deaths, marker='o', color='#007acc')
            ax1.set_title(f'{option} daily death count', fontsize=23)
            ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
            ax1.tick_params(rotation=60)
            ax1.spines['right'].set_visible(False)
            ax1.spines['top'].set_visible(False)
            ax2 = fig.add_subplot(313)
            ef['recovered'] = day_data[f'{option} recovered']
            ax2.bar(ef.date, ef.recovered, color='#007acc', alpha=0.3)
            ax2.plot(ef.date, ef.recovered, marker='o', color='#007acc')
            ax2.set_title(f'{option} daily recovery count', fontsize=23)
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
            ax2.tick_params(rotation=60)
            ax2.spines['right'].set_visible(False)
            ax2.spines['top'].set_visible(False)
            fig.tight_layout()
            st.plotly_chart(fig, config={'displayModeBar': False})
            dfc = dfc.replace("Andaman & Nicobar", 'Andaman and Nicobar Islands')
            c = dfc[dfc['State'] == option]['Confirmed Cases'].iloc[0]
            d = dfc[dfc['State'] == option]['Deceased'].iloc[0]
            r = dfc[dfc['State'] == option]['Recovered'].iloc[0]
            st.write("Confirmed Cases:", int(c))
            st.write("Confirmed Deaths:", int(d))
            st.write("Recovered:", int(r))
            st.write("Current Cases:", int(c - d - r))
            st.write("Fatality Rate:", round((d / c) * 100, 2), '%')
            st.write("Recovery Rate:", round((r / c) * 100, 2), '%')

elif analysis == "Fatalities":
    df2 = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

    # getting the latest date in the dataset
    dat = list(set(df2.date))
    dat.sort()
    dat = dat[-1]

    # gives the most recent data of every country
    df2_temp = df2.loc[df2['date'] == dat]
    df2_temp = df2_temp[(df2_temp.location != 'World') & (df2_temp.location != 'International')]
    req_data = df2_temp
    req_data['total_deaths'] = req_data['total_deaths'].fillna(0)
    req_data = req_data.set_index("location")

    # dropping rows with 0 cases
    for loca in req_data.index:
        if (req_data.total_cases[loca] < 1.0):
            req_data = req_data.drop([loca])

    # fatalities number
    desired = (req_data["total_deaths"].sort_values(ascending=True))

    # fatalities %
    desired2 = desired.copy()
    for i in desired.index:
        desired2[i] = (desired[i] / req_data.loc[i, "total_cases"]) * 100
    desired2 = (desired2.sort_values(ascending=True))
    f1 = st.selectbox("Fatalities", ["By number", "By rate"])
    if f1 == "By number":
        fig = plt.figure(figsize=(10, 15))
        ax = fig.gca()  # get current axes for figure
        desired[-20:].plot.barh(color='r', alpha=0.7)
        for p, c, ch in zip(range(desired[-20:].shape[0]), desired[-20:].index, desired[-20:].values):
            plt.annotate(str(round(ch)), xy=(ch + 1, p), va='center')
        ax.tick_params(axis="both", which='both',  # major and minor ticks
                       length=0)
        ax.tick_params(axis="x", labeltop=False, labelbottom=False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        st.write(fig)

    elif f1 == "By rate":
        fig = plt.figure(figsize=(10, 15))
        ax = fig.gca()  # get current axes for figure
        desired2[-20:].plot.barh(color='r', alpha=0.7)
        for p, c, ch in zip(range(desired2[-20:].shape[0]), desired2[-20:].index, desired2[-20:].values):
            plt.annotate(str(round(ch, 1)) + "%", xy=(ch + 0.1, p), va='center')
        ax.tick_params(axis="both", which='both',  # major and minor ticks
                       length=0)
        ax.tick_params(axis="x", labeltop=False, labelbottom=False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        st.write(fig)

elif analysis == "Trend":
    t1 = st.selectbox("Global cases trend", ["Past week", "Past month"])
    df = df1
    df = df[(df.location != 'World') & (df.location != 'International')]
    trend1 = (df.groupby("date").sum()["total_cases"] / float(1e6))
    if t1 == "Past week":
        fig = plt.figure(figsize=(16, 10))
        ax = fig.gca()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f M'))  # adding unit to y-axis values
        ax.set_xlabel("Date", fontsize=23)
        ax.set_ylabel("Global Cases", fontsize=23)
        ax.plot(trend1[-8:-1], "ro")
        ax.plot(trend1[-8:-1], alpha=0.2)
        st.write(fig)
    elif t1 == "Past month":
        fig = plt.figure(figsize=(16, 10))
        ax = fig.gca()
        ax.set_xticks([0, 4, 9, 14, 19, 24, 29])
        ax.set_xticklabels(
            [trend1.index[-31], trend1.index[-26], trend1.index[-21], trend1.index[-16], trend1.index[-11],
             trend1.index[-6], trend1.index[-2]])
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f M'))
        ax.plot(trend1[-31:-1], "ro")
        ax.plot(trend1[-31:-1], alpha=0.2)
        ax.set_xlabel("Date", fontsize=23)
        ax.set_ylabel("Global Cases", fontsize=23)
        st.write(fig)