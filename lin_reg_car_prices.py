import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/home/ayush/Py_projects/ML Intro/car_price.csv')

#print(df.columns)
#print(df.shape)


def process():	#pre-processing data 

#converting categorical variables into one hot encoding

	df['petrol'] = df['fuel'].replace({"Petrol": 1, "Diesel": 0 , "CNG" : 0, "LPG": 0})
	df['diesel'] = df['fuel'].replace({"Petrol": 0, "Diesel": 1 , "CNG" : 0, "LPG": 0})
	df['cng'] = df['fuel'].replace ({"Petrol": 0, "Diesel": 0 , "CNG" : 1, "LPG": 0})
	df['lpg'] = df['fuel'].replace ({"Petrol": 0, "Diesel": 0 , "CNG" : 0, "LPG": 1})
	

	#print(df.seller_type.value_counts())

	df['indiv'] = df['seller_type'].replace({"Individual": 1, "Dealer": 0, "Trustmark Dealer": 0})
	df['dealer'] = df['seller_type'].replace({"Individual": 0, "Dealer": 1, "Trustmark Dealer": 0})
	df['trustmd'] = df['seller_type'].replace({"Individual": 0, "Dealer": 0, "Trustmark Dealer": 1})



	df['manual'] = df['transmission'].replace({"Manual":1, "Automatic": 0})
	df['auto'] = df['transmission'].replace({"Manual":0, "Automatic": 1})
	

	#print(df.owner.value_counts())

	df['owner1'] = df['owner'].replace({'First Owner':1, 'Second Owner':0, 'Third Owner':0, 'Fourth & Above Owner':0,
 'Test Drive Car':0})
	df['owner2'] = df['owner'].replace({'First Owner':0, 'Second Owner':1, 'Third Owner':0, 'Fourth & Above Owner':0,
 'Test Drive Car':0})
	df['owner3'] = df['owner'].replace({'First Owner':0, 'Second Owner':0, 'Third Owner':1, 'Fourth & Above Owner':0,
 'Test Drive Car':0})
	df['owner4'] = df['owner'].replace({'First Owner':0, 'Second Owner':0, 'Third Owner':0, 'Fourth & Above Owner':1,
 'Test Drive Car':0})
	df['tdcar'] = df['owner'].replace({'First Owner':0, 'Second Owner':0, 'Third Owner':0, 'Fourth & Above Owner':0,
 'Test Drive Car':1})

	#implemented milex for numeric mileage
	df['mileage'] = df['mileage'].fillna(0)

	df['milex'] = df['mileage'].str.replace('kmpl', '')
	df['milex'] = df['milex'].str.replace('km/kg', '').astype(float)

	df['milex'] = df['milex'].astype(float)


	df['milex'] = df['milex'].fillna(0)

	#implemented enginex for numeric engine cc
	df['enginex'] = df['engine'].str.replace(' CC', '').astype(float)
	df['enginex'] = df['enginex'].fillna(0)


	#implement max_power as powerx 
	df['powerx'] = df['max_power'].str.replace(' bhp', '')
	df['powerx'] = df['powerx'].fillna(0)

	l = []

	for i in range (len(df.powerx)):
		try:
			m = df['powerx'][i]
			if m == '':
				l.append(float(0))
			else:
				l.append(float(df['powerx'][i]))

		except ValueError:
			print('Float conversion fail'+ '\''+df['powerx'][i]+'\'')


	#implement torquex, ignore nm Nm case, rpmx will store @rpm
	x = df['torque'].str.split('@')
	print(x)
	#print(df.torque.value_counts())
	
	




process()

