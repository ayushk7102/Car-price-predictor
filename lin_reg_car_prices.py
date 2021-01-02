import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#local filepath strings

w10_csv = r"C:\Users\ayush\OneDrive\Desktop\ML Intro\car_prices.csv" 
lin_csv = '/home/ayush/Py_projects/ML Intro/car_price.csv'

df = pd.read_csv(w10_csv)
#print(df.columns)
#print(df.shape)



def return_dash_avg(ls):
	sec = str(ls[-1])
	sec_str =""
	for i in range(0, len(sec)):
		if(sec[i].isdigit()):
			sec_str+=sec[i]
		else:
			break
	sec_f = float(sec_str)
	fir = str(ls[-2])

	f_str = ""
	for i in range(len(fir)-1, -1, -1):
		if(fir[i].isdigit()):
			f_str+=fir[i]
		else:
			break
	f_str = ''.join(reversed(f_str))
	
	if(f_str == ''):
		f_flt =0
	else:
		f_flt = float(f_str)

		return (f_flt+sec_f)/2.0


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
	#x = df['torque'].str.split('@')
	#x = df['torque'].str.split('at')

	countat= 0 
	countatrate = 0
	for i in range(len(df.torque)):
		iss = str(df['torque'][i])
		if "at" in iss:
			countat+=1
		elif "@" in iss:
			countatrate+=1
		else:
			#print(iss+ " "+str("at" in iss) )
			pass

	print('at : '+str(countat)+ ',   @ :'+str(countatrate) + ' TOTAL : '+str(countat+ countatrate))
	print(len(df.torque))


	df['torquex'] = np.nan
	df['torq'] = np.nan
	df['rpmx'] = np.nan
	counttor = 0

	for i in range(len(df.torquex)):
		torqx=""
		avg = 0
		Nm_val = 0
		rpm = 0

		torq = str(df['torque'][i])
		if "," in torq:
			torq = torq.replace(',','')

		if " at " in torq:
			torq = torq.replace(' at ','@')

		if "(kgm@ rpm)" in torq:
			#print(torq)
			torq = torq[0:torq.index("(kgm@ rpm)")]
			Nm_val = float(torq.split('@')[0])*9.81

			torq = str(round(Nm_val,3)) + torq[torq.index('@'):]


		elif "Nm" in torq:
			Nm_val = torq.split('Nm')[0]

		if "/" in torq:
			torq=torq.replace('/','@')

		if "-" in torq: 
			avg = return_dash_avg(torq.split('-'))
			torq = torq.split('@')[0] +'@' + str(avg)+ 'rpm'

		elif "-" not in torq :

			pass 

		if "rpm" not in torq:
			if(torq == 'nan'):
				pass
				if '@' in torq:
					torq+='rpm'
			else:
				pass
		if "@" in torq:
				tor_str = torq.split('@')[0]
				
				print(torq)
				counttor+=1

	print(counttor)

	#After processing 96.85% of torque variables are formatted for use (7872/8128)

	#print(df.torque.value_counts())
	
	
process()


print(df.columns)

