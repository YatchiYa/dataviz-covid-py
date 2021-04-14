
from modules import *

#function to read the data
def read_data():
    # Import datasets as pandas dataframes
    raw_data_confirmed = pd.read_csv(confirmed_cases_data_url)
    raw_data_deaths = pd.read_csv(death_cases_data_url)
    raw_data_recovered = pd.read_csv(recovery_cases_data_url)
    return (raw_data_confirmed, raw_data_deaths, raw_data_recovered)

#function to write in files
def write_in_file(raw_data_confirmed, raw_data_deaths, raw_data_recovered):
    f = open("covid_head.txt", "w")
    f.write(" \n ------------------ \n raw_data_confirmed cases \n ")
    f.write(str(raw_data_confirmed.head()))
    f.write("\n")
    f.write(str(raw_data_confirmed.tail()))

    f.write(" \n\n\n\n ------------------ \n raw_data_deaths cases \n ")
    f.write(str(raw_data_deaths.head()))
    f.write("\n")
    f.write(str(raw_data_deaths.tail()))

    f.write(" \n\n\n\n ------------------ \n raw_data_recovered cases \n ")
    f.write(str(raw_data_recovered.head()))
    f.write("\n")
    f.write(str(raw_data_recovered.tail()))
    f.close()


# function to get the country data only
def get_country_data(raw_data_confirmed, raw_data_deaths, raw_data_recovered):
    confirmed_country = raw_data_confirmed.groupby(['Country/Region']).sum().drop(['Lat', 'Long'], axis=1)
    deaths_country = raw_data_deaths.groupby(['Country/Region']).sum().drop(['Lat', 'Long'], axis=1)
    recover_country = raw_data_recovered.groupby(['Country/Region']).sum().drop(['Lat', 'Long'], axis=1)
    return (confirmed_country, deaths_country, recover_country)

# transpose the data columns
def transpose(confirmed_country, deaths_country, recover_country):
    confirmed_country = confirmed_country.transpose()
    deaths_country = deaths_country.transpose()
    recover_country = recover_country.transpose()
    return (confirmed_country, deaths_country, recover_country)

# transform the date string to date Date
def tranform_date(confirmed_country, deaths_country, recover_country):
    # transform the object dates in date time
    # Set index as DateTimeIndex
    datetime_index = pd.DatetimeIndex(confirmed_country.index)
    confirmed_country.set_index(datetime_index, inplace=True)

    datetime_index2 = pd.DatetimeIndex(deaths_country.index)
    deaths_country.set_index(datetime_index2, inplace=True)

    datetime_index3 = pd.DatetimeIndex(recover_country.index)
    recover_country.set_index(datetime_index3, inplace=True)
    return (confirmed_country, deaths_country, recover_country)

# simple ploting data
def simple_plot(data, path, ylab, title):
    # Plot time series of several countries of interest
    fig = plt.figure()
    poi = ['China', 'US', 'Italy', 'France', 'Spain', 'Australia', 'Belgium']
    data[poi].plot(figsize=(20,10), linewidth=1, marker='.', colormap='brg', fontsize=10)
    plt.xlabel('Date', fontsize=10);
    plt.ylabel(ylab, fontsize=10);
    plt.title(title, fontsize=10);
    plt.savefig(path)

# get data above some value defined
def filter_data_plus_vlue(data, value, path, msg):
    # Loop over columns & set values < value to None
    for col in data.columns:
        data.loc[(data[col] <= value),col] = None

    # Check out tail
    #print(data.tail())
    # Drop columns that are all NaNs (i.e. countries that haven't yet reached value deaths)
    data.dropna(axis=1, how='all', inplace=True)
    data_drop = data.reset_index().drop(['index'], axis=1)

    for col in data_drop.columns:
        data_drop[col] = data_drop[col].shift(-data_drop[col].first_valid_index())
    # check out head
    #print(deaths_country_drop.head())
    ax = data_drop.plot(figsize=(20,10), linewidth=2, marker='.', fontsize=20)
    ax.legend(ncol=3, loc='upper right')
    plt.xlabel('Days', fontsize=20);
    plt.ylabel('Number of Reported Deaths', fontsize=20);
    plt.title(msg, fontsize=20);
    plt.savefig(path)

def filter_data_plus_vlue_log(data, value, path, msg):
    # Loop over columns & set values < value to None
    for col in data.columns:
        data.loc[(data[col] <= value),col] = None

    # Check out tail
    #print(data.tail())
    # Drop columns that are all NaNs (i.e. countries that haven't yet reached value deaths)
    data.dropna(axis=1, how='all', inplace=True)
    data_drop = data.reset_index().drop(['index'], axis=1)

    for col in data_drop.columns:
        data_drop[col] = data_drop[col].shift(-data_drop[col].first_valid_index())
    # check out head
    #print(deaths_country_drop.head())
    # Plot semi log time series 
    ax = data_drop.plot(figsize=(20,10), linewidth=2, marker='.', fontsize=20, logy=True)
    ax.legend(ncol=3, loc='upper right')
    plt.xlabel('Days', fontsize=20);
    plt.ylabel('Deaths Patients count', fontsize=20);
    plt.title(msg, fontsize=20);
    plt.savefig(path)


def exec():
    print("visual 0 ...")
    #execution
    raw_data_confirmed, raw_data_deaths, raw_data_recovered = read_data()
    write_in_file(raw_data_confirmed, raw_data_deaths, raw_data_recovered)
    confirmed_country, deaths_country, recover_country = get_country_data(raw_data_confirmed, raw_data_deaths, raw_data_recovered)
    # transpose the columns and rows
    confirmed_country, deaths_country, recover_country = transpose(confirmed_country, deaths_country, recover_country)
    confirmed_country, deaths_country, recover_country = tranform_date(confirmed_country, deaths_country, recover_country)


    # Plot time series of several countries of interest
    simple_plot(confirmed_country, "img/confirmed_country.png", 'Reported Confirmed cases count', 'Reported Confirmed Cases Time Series')
    simple_plot(confirmed_country, "img/confirmed_country_log.png", 'Reported Confirmed Cases Logarithmic count', 'Reported Confirmed Cases Logarithmic Time Series')
    simple_plot(deaths_country, "img/deaths_country.png", 'Number of Reported Deaths', 'Reported Deaths Time Series')
    simple_plot(deaths_country, "img/deaths_country_log.png", 'Reported deaths Cases Logarithmic count', 'Reported deaths Cases Logarithmic Time Series')

    #filter the data
    filter_data_plus_vlue(deaths_country, 20000, "img/deaths_country_at_least_20000_deaths.png", "Total reported coronavirus deaths for places with at least 2000 deaths")
    filter_data_plus_vlue(deaths_country, 100000, "img/deaths_country_at_least_100000_deaths.png", "Total reported coronavirus deaths for places with at least 100000 deaths")
    filter_data_plus_vlue(deaths_country, 200000, "img/deaths_country_at_least_200000_deaths.png", "Total reported coronavirus deaths for places with at least 200000 deaths")
    filter_data_plus_vlue_log(deaths_country, 100000, "img/deaths_country_at_least_100000_deaths_semi_log", "Total reported coronavirus deaths for places with at least 100000 deaths semi log")
    filter_data_plus_vlue_log(deaths_country, 200000, "img/deaths_country_at_least_200000_deaths_semi_log", "Total reported coronavirus deaths for places with at least 200000 deaths semi log")

    # recover country
    simple_plot(recover_country, "img/recover_country.png", 'Number of recover cases', 'Reported recover Time Series')


    poi = ['China', 'US', 'Italy', 'France', 'Spain', 'Australia', 'Belgium']
    recover_country[poi].plot(figsize=(20,10), linewidth=2, marker='.', colormap='brg', fontsize=20, logy=True)
    plt.xlabel('Date', fontsize=20);
    plt.ylabel('Reported recover Cases Logarithmic count', fontsize=20);
    plt.title('Reported recover Cases Logarithmic Time Series', fontsize=20);
    plt.savefig("img/recover_country_log.png")



    # Loop over columns & set values < 2000 to None
    for col in recover_country.columns:
        recover_country.loc[(recover_country[col] <= 200),col] = None

    # Check out tail
    #print(recover_country.tail())
    # Drop columns that are all NaNs (i.e. countries that haven't yet reached 200 deaths)
    recover_country.dropna(axis=1, how='all', inplace=True)
    recover_country_drop = recover_country.reset_index().drop(['index'], axis=1)

    for col in recover_country_drop.columns:
        recover_country_drop[col] = recover_country_drop[col].shift(-recover_country_drop[col].first_valid_index())
    # check out head
    #print(recover_country_drop.head())
    ax = recover_country_drop.plot(figsize=(20,10), linewidth=2, marker='.', fontsize=20)
    ax.legend(ncol=3, loc='upper right')
    plt.xlabel('Days', fontsize=20);
    plt.ylabel('Number of Reported recover', fontsize=20);
    plt.title('Total reported coronavirus recover for places with at least 200 recover', fontsize=20);
    plt.savefig("img/recover_country_at_least_200_recover.png")



    # Loop over columns & set values < 2000 to None
    for col in recover_country.columns:
        recover_country.loc[(recover_country[col] <= 500000),col] = None

    # Check out tail
    #print(recover_country.tail())
    # Drop columns that are all NaNs (i.e. countries that haven't yet reached 200 deaths)
    recover_country.dropna(axis=1, how='all', inplace=True)
    recover_country_drop = recover_country.reset_index().drop(['index'], axis=1)

    for col in recover_country_drop.columns:
        recover_country_drop[col] = recover_country_drop[col].shift(-recover_country_drop[col].first_valid_index())
    # check out head
    #print(recover_country_drop.head())
    ax = recover_country_drop.plot(figsize=(20,10), linewidth=2, marker='.', fontsize=20)
    ax.legend(ncol=3, loc='upper right')
    plt.xlabel('Days', fontsize=20);
    plt.ylabel('Number of Reported recover', fontsize=20);
    plt.title('Total reported coronavirus recover for places with at least 200 recover', fontsize=20);
    plt.savefig("img/recover_country_at_least_500000_recover.png")



    # Plot time series of several countries of interest

    # Loop over columns & set values < 100000 to None
    for col in deaths_country.columns:
        deaths_country.loc[(deaths_country[col] <= 10000),col] = None

    # Check out tail
    #print(deaths_country.tail())
    # Drop columns that are all NaNs (i.e. countries that haven't yet reached 100000 deaths)
    deaths_country.dropna(axis=1, how='all', inplace=True)
    deaths_country_drop = deaths_country.reset_index().drop(['index'], axis=1)

    for col in deaths_country_drop.columns:
        deaths_country_drop[col] = deaths_country_drop[col].shift(-deaths_country_drop[col].first_valid_index())

    deaths_long = deaths_country_drop.reset_index().melt(id_vars='index', value_name='Deaths').rename(columns={'index':'Day'})
    # altair plot 
    chart = alt.Chart(deaths_long).mark_line(strokeWidth=4, opacity=0.7).encode(
        x='Day',
        y='Deaths',
        color='Country/Region'
    ).properties(
        width=800,
        height=650
    )
    chart.save('img/altair_deaths.html')

