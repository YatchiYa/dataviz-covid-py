
from g_viz import *
from modules import *

def viz_1():
    print("visual 1 ...")
    df = pd.read_csv("data/covid_19_data.csv")

    df.rename(columns={'ObservationDate': 'date', 
                         'Province/State':'state',
                         'SNo':'N',
                         'Country/Region': 'country',
                         'Confirmed': 'confirmed',
                         'Deaths':'deaths',
                         'Recovered':'recovered'
                        }, inplace=True)

    # Active Case = confirmed - deaths - recovered
    df['active'] = df['confirmed'] - df['deaths'] - df['recovered']

    top = df[df['date'] == df['date'].max()]
    top_casualities = top.groupby(by = 'country')['confirmed'].sum().sort_values(ascending = False).head(20).reset_index()

    plt.figure(figsize= (15,10))
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xlabel("Total cases",fontsize = 30)
    plt.ylabel('Country',fontsize = 30)
    plt.title("Top 20 countries having most confirmed cases" , fontsize = 30)
    ax = sns.barplot(x = top_casualities.confirmed, y = top_casualities.country)
    for i, (value, name) in enumerate(zip(top_casualities.confirmed,top_casualities.country)):
        ax.text(value, i-.05, f'{value:,.0f}',  size=10, ha='left',  va='center')
    ax.set(xlabel='Total cases', ylabel='Country')
    plt.savefig('img/top20_confirmed.png')



    top_actives = top.groupby(by = 'country')['active'].sum().sort_values(ascending = False).head(20).reset_index()
    plt.figure(figsize= (15,10))
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xlabel("Total cases",fontsize = 30)
    plt.ylabel('Country',fontsize = 30)
    plt.title("Top 20 countries having most active cases" , fontsize = 30)
    ax = sns.barplot(x = top_actives.active, y = top_actives.country)
    for i, (value, name) in enumerate(zip(top_actives.active, top_actives.country)):
        ax.text(value, i-.05, f'{value:,.0f}',  size=10, ha='left',  va='center')
    ax.set(xlabel='Total cases', ylabel='Country')
    plt.savefig('img/top20_active.png')


    top_deaths = top.groupby(by = 'country')['deaths'].sum().sort_values(ascending = False).head(20).reset_index()
    plt.figure(figsize= (15,10))
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xlabel("Total cases",fontsize = 30)
    plt.ylabel('Country',fontsize = 30)
    plt.title("Top 20 countries having most deaths" , fontsize = 30)
    ax = sns.barplot(x = top_deaths.deaths, y = top_deaths.country)
    for i, (value, name) in enumerate(zip(top_deaths.deaths,top_deaths.country)):
        ax.text(value, i-.05, f'{value:,.0f}',  size=10, ha='left',  va='center')
    ax.set(xlabel='Total cases', ylabel='Country')
    plt.savefig('img/top20_deaths.png')




    rate = top.groupby(by = 'country')['recovered','confirmed','deaths'].sum().reset_index()
    rate['recovery percentage'] =  round(((rate['recovered']) / (rate['confirmed'])) * 100 , 2)
    rate['death percentage'] =  round(((rate['deaths']) / (rate['confirmed'])) * 100 , 2)

    mortality = rate.groupby(by = 'country')['death percentage'].sum().sort_values(ascending = False).head(20).reset_index()
    plt.figure(figsize= (15,10))
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xlabel("Total cases",fontsize = 30)
    plt.ylabel('Country',fontsize = 30)
    plt.title("Top 20 countries having most mortality rate" , fontsize = 30)
    ax = sns.barplot(x = mortality['death percentage'], y = mortality.country)
    for i, (value, name) in enumerate(zip(mortality['death percentage'], mortality.country)):
        ax.text(value, i-.05, f'{value:,.0f}',  size=10, ha='left',  va='center')
    ax.set(xlabel='Mortality Rate in percentage', ylabel='Country')
    plt.savefig('img/top20_most_mortalité_rate.png')


    recovery = rate.groupby(by = 'country')['recovery percentage'].sum().sort_values(ascending = False).head(20).reset_index()
    plt.figure(figsize= (15,10))
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xlabel("Total cases",fontsize = 30)
    plt.ylabel('Country',fontsize = 30)
    plt.title("Top 20 countries having most recovery rate" , fontsize = 30)
    ax = sns.barplot(x = recovery['recovery percentage'], y = recovery.country)
    for i, (value, name) in enumerate(zip(recovery['recovery percentage'], recovery.country)):
        ax.text(value, i-.05, f'{value:,.0f}',  size=10, ha='left',  va='center')
    ax.set(xlabel='Recovery Rate in percentage', ylabel='Country')
    plt.savefig('img/top20_most_recover_rate.png')

    countries = top.groupby(by = 'country')['confirmed'].sum().sort_values(ascending = False)

    f = open("top_covid_confirmed_cases.txt", "w")
    f.write(" \n ------------------ \n covid_confirmed cases \n ")
    f.write(str(countries.head(20)))
    f.close()


    conf = top.groupby(by = 'country')['confirmed'].sum().sort_values(ascending = False)
    acct = top.groupby(by = 'country')['active'].sum().sort_values(ascending = False)
    dea = top.groupby(by = 'country')['deaths'].sum().sort_values(ascending = False)
    rec = top.groupby(by = 'country')['recovered'].sum().sort_values(ascending = False)


    f = open("france_covid.txt", "w")
    f.write(" \n ------------------ \n france covid_confirmed cases : ")
    f.write(str(conf["France"]))

    f.write(" \n ------------------ \n france covid_active cases : ")
    f.write(str(acct["France"]))

    f.write(" \n ------------------ \n france covid_recoverd cases : ")
    f.write(str(rec["France"]))

    f.write(" \n ------------------ \n france covid_deaths cases : ")
    f.write(str(dea["France"]))
    f.close()



    f = open("germany_covid.txt", "w")
    f.write(" \n ------------------ \n Germany covid_confirmed cases : ")
    f.write(str(conf["Germany"]))

    f.write(" \n ------------------ \n Germany covid_active cases : ")
    f.write(str(acct["Germany"]))

    f.write(" \n ------------------ \n Germany covid_recoverd cases : ")
    f.write(str(rec["Germany"]))

    f.write(" \n ------------------ \n Germany covid_deaths cases : ")
    f.write(str(dea["Germany"]))
    f.close()


    f = open("greece_covid.txt", "w")
    f.write(" \n ------------------ \n Greece covid_confirmed cases : ")
    f.write(str(conf["Greece"]))

    f.write(" \n ------------------ \n Greece covid_active cases : ")
    f.write(str(acct["Greece"]))

    f.write(" \n ------------------ \n Greece covid_recoverd cases : ")
    f.write(str(rec["Greece"]))

    f.write(" \n ------------------ \n Greece covid_deaths cases : ")
    f.write(str(dea["Greece"]))
    f.close()


    plus_touche = rate.groupby(by = 'country')['confirmed'].sum().sort_values(ascending = False).head(1).reset_index()

    f = open("pays_le_plus_touche.txt", "w")
    f.write(" \n ------------------ \n cases : ")
    f.write(str(plus_touche))
    f.close()


    moins_touche = rate.groupby(by = 'country')['confirmed'].sum().sort_values(ascending = False).tail(1).reset_index()

    f = open("pays_le_moins_touche.txt", "w")
    f.write(" \n ------------------ \n cases : ")
    f.write(str(moins_touche))
    f.close()


