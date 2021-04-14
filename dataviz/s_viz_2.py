
from modules import *

def viz_2():
    print("visual 2 ...")
    df1 = pd.read_csv(URL_DATASET)
    list_countries = df1['Country'].unique().tolist()
    d_country_code = {} 
    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            country_code = country_data[0].alpha_3
            d_country_code.update({country: country_code})
        except:
            #print('could not add ISO 3 code for ->', country)
            d_country_code.update({country: ' '})

    for k, v in d_country_code.items():
        df1.loc[(df1.Country == k), 'iso_alpha'] = v

    fig = px.choropleth(data_frame = df1,
                        locations= "iso_alpha",
                        color= "Confirmed",  # value in column 'Confirmed' determines color
                        hover_name= "Country",
                        color_continuous_scale= 'RdYlGn',  #  color scale red, yellow green
                        animation_frame= "Date")

    fig.write_html("img/world_map_covid_confirmed.html")


    # ----------- Step 3 ------------
    fig = px.choropleth(data_frame = df1,
                        locations= "iso_alpha",
                        color= "Deaths",  # value in column 'Confirmed' determines color
                        hover_name= "Country",
                        color_continuous_scale= 'RdYlGn',  #  color scale red, yellow green
                        animation_frame= "Date")

    fig.write_html("img/world_map_covid_deaths.html")



