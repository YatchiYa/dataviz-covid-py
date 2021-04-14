import numpy as np
import matplotlib.pyplot as plt
import requests,datetime,os
import pandas as pd

def s_viz_3():	
	plt.style.use('ggplot') # ggplot formatting

	# COVID-19 Datasets
	github_url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/' # nyc data repository
	data_file_urls = ['boro.csv','totals/by-age.csv','totals/by-sex.csv','case-hosp-death.csv',
	                  'summary.csv','tests-by-zcta.csv'] # the .csv files to read where data exists
	
	age_nyc = pd.read_csv(github_url + data_file_urls[1])
	df = pd.DataFrame(age_nyc,columns=['AGE_GROUP','CASE_COUNT'])
	df = df.drop([11])
	ax = df.plot.bar(x='AGE_GROUP', rot=0)
	plt.savefig("img/new_york_case_covid_by_age.png")

	df = pd.DataFrame(age_nyc,columns=['AGE_GROUP','DEATH_COUNT'])
	df = df.drop([11])
	ax = df.plot.bar(x='AGE_GROUP', rot=0)
	plt.savefig("img/new_york_death_covid_by_age.png")

	df = pd.DataFrame(age_nyc,columns=['AGE_GROUP','CASE_COUNT', 'DEATH_COUNT'])
	df = df.drop([11])
	ax = df.plot.bar(x='AGE_GROUP', rot=0)
	plt.savefig("img/new_york_cas_and_death_covid_by_age.png")


	sexe_nyc = pd.read_csv(github_url + data_file_urls[2])
	df = pd.DataFrame(sexe_nyc,columns=['SEX_GROUP','CASE_COUNT'])
	df = df.drop([2])
	ax = df.plot.bar(x='SEX_GROUP', rot=0)
	plt.savefig("img/new_york_case_covid_by_sexe.png")

	df = pd.DataFrame(sexe_nyc,columns=['SEX_GROUP','DEATH_COUNT'])
	df = df.drop([2])
	ax = df.plot.bar(x='SEX_GROUP', rot=0)
	plt.savefig("img/new_york_death_covid_by_sexe.png")

	df = pd.DataFrame(sexe_nyc,columns=['SEX_GROUP','CASE_COUNT', 'DEATH_COUNT'])
	df = df.drop([2])
	ax = df.plot.bar(x='SEX_GROUP', rot=0)
	plt.savefig("img/new_york_cas_and_death_covid_by_sexe.png")

