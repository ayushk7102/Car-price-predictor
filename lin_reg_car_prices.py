import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/home/ayush/Py_projects/ML Intro/car_price.csv')

print(df.columns)



def process():

	fuel_num = {
	  "Diesel": 0,
	  "Petrol": 1,
	  "LPG": 2,
	  "CNG": 3
	} 

	list_fuel = []
	for i in range (len(df.fuel)):
		old = (df['fuel'][i])
		list_fuel.append(fuel_num[old])
	
	df['fuelx'] = list_fuel

	seller_num = {
	  "Individual": 0,
	  "Dealer": 1,
	  "Trustmark Dealer": 2
	} 

	list_seller = []
	for i in range (len(df.seller_type)):
		old = (df['seller_type'][i])
		list_seller.append(seller_num[old])

	
	df['sellerx'] = list_seller

	trans_num = {
	  "Manual": 0,
	  "Automatic": 1
	  }

	list_trans = []

	for i in range(len(df.transmission)):
	  	old = df['transmission'][i]
	  	list_trans.append(trans_num[old])

	df['transx'] = list_trans


	owner_num = {
	  "First Owner": 1,
	  "Second Owner": 2,
	  "Third Owner": 3,
	  "Fourth & Above Owner": 4,
	  "Test Drive Car": 5
	} 

	list_owner = []

	for i in range(len(df.owner)):
	  	old = df['owner'][i]
	  	list_owner.append(owner_num[old])

	df['ownerx'] = list_owner

	print(df.sellerx.unique())

process()

print(df.max_power.unique())