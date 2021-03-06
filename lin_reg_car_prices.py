import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#local filepath strings

w10_csv = r"C:\Users\ayush\OneDrive\Desktop\ML Intro\car_prices.csv" 
lin_csv = '/home/ayush/Py_projects/ML Intro/car_price.csv'

r_bound = 0.3
df = pd.read_csv(lin_csv)
#print(df.columns)
#print(df.shape)



params = np.empty([23,1])

params_test = np.empty([9,1])


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


	df['milex'] = df['milex'].fillna(df['milex'].mean())

	#implemented enginex for numeric engine cc
	df['enginex'] = df['engine'].str.replace(' CC', '').astype(float)
	df['enginex'] = df['enginex'].fillna(df.enginex.mean())


	#implement max_power as powerx 

	df['powerx'] = df['max_power'].str.replace(' bhp', '')
	#print(df[['max_power','powerx']][:].head())
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

	#print('at : '+str(countat)+ ',   @ :'+str(countatrate) + ' TOTAL : '+str(countat+ countatrate))


	df['torquex'] = np.nan
	

	counttor = 0
	torqs = []
	countbad = 0


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

		

		if "~" in torq:
			avg_rpm = (return_dash_avg(torq.split('@')[1].split('~')))
			torq = torq.split('@')[0]+'@'+str(avg_rpm)+'rpm'
			

		if "rpm" not in torq:
			if(torq == 'nan'):
				pass
				if '@' in torq:
					torq+='rpm'
			else:
				pass
		if "@" in torq:
				tor_str = torq.split('@')[0]
				torqs.append(torq)
				#print(torq)
				counttor+=1
		else:
			if torq == 'nan':
				countbad+=1
				torqs.append('nan')

			else:
				torqs.append(torq)
				countbad+=1
				

	df['torquex'] = torqs
	nms = []
	rpms = []

	df['nmx'] = np.nan
	df['rpmx'] = np.nan

	countx=0

	for i in range(len(df.torquex)):
		torq = str(df['torquex'][i])
		t = torq.split('@')
		nm = t[0]
		nmx =''


		for j in range(len(nm)):
			if nm[j].isalpha() or nm[j] == '(':
				break
			else:
				nmx+=nm[j]

		
		if nmx == '':
			nms.append(0)
		else:
			nms.append(float(nmx))


		if '@' in torq:
			rpm = t[1]
			rpmx = ''
			for k in range(len(rpm)):
				if rpm[k].isalpha() or rpm[k] == '(':
					break
				else:
					rpmx+=rpm[k]

			if rpmx == '':
				rpms.append(0)
			else:
				rpms.append(float(rpmx))

		
		else:
			rpms.append(0)


	df['nmx'] = nms
	df['rpmx'] = rpms

	df['max_powerx'] = np.nan
	max_powx = []
	for i in range(len(df.powerx)):
		if(df['powerx'][i] != ''):
			max_powx.append(float(df['powerx'][i]))
		else:
			max_powx.append(0)

	df['max_powerx'] = max_powx


	#replace nan's in seats with mean

	df['seats'].fillna((df['seats'].median()), inplace=True)



	#print(df[:][['torque','nmx','rpmx']].tail(20))
	


	#print(counttor)
	#print(countbad)

	#After processing 96.85% of torque variables are formatted for use (7872/8128)

	#print(df.torque.value_counts())


def r_with_price(n):
	prc = df['selling_price']

	coeffs = (np.corrcoef(x=n.T, y=prc.T))
	return coeffs[1][0]

def get_x_array(arr):
	list_col = []
	for column in arr.columns:
		r_w_pr = r_with_price(df[column])
		if(abs(r_w_pr) > r_bound ):
			list_col.append(column)

	return df[:][list_col]

def elim_model():
	np.set_printoptions(suppress=True) # otherwise prints ndarray in scientific notation, set False for that
	#print(df.columns)

	#df['powerx'] = pd.to_numeric(df["powerx"], downcast="float")
	x0 = pd.DataFrame.to_numpy(df.loc[:, df.columns != 'selling_price'])
	
	#print(x0[0])
	
	x = pd.DataFrame.to_numpy(df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]])

	t = df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]

	elim_t = get_x_array(t)

	x = pd.DataFrame.to_numpy(elim_t)

	y = pd.DataFrame.to_numpy(df.loc[:, ['selling_price']])

	#pre-append X with 1xN array of ones
	one_n = np.ones(len(x))
	x = np.c_[one_n, x]

	#finding theta
	xt = np.transpose(x)
	xt_x = np.matmul(xt, x)

	xt_x_inv = np.linalg.inv(xt_x) #ERROR coming HERE!

	inv_prod = np.matmul(xt_x_inv, xt)

	theta = np.matmul(inv_prod, y)

	params_test[:] = theta 
	

	#print(theta)

	#print(theta.shape)

	#df_t = pd.DataFrame.to_numpy(t)


	print(predict(pd.DataFrame.to_numpy(t)[1]))			##IMPORTANT TESTING #1
	#print('Actual:', df[['selling_price']][:].head() )

	print(rms_error(elim_t))

	pred_test(elim_t)

def model():
	np.set_printoptions(suppress=True) # otherwise prints ndarray in scientific notation, set False for that
	#print(df.columns)

	#df['powerx'] = pd.to_numeric(df["powerx"], downcast="float")
	x0 = pd.DataFrame.to_numpy(df.loc[:, df.columns != 'selling_price'])
	
	#print(x0[0])
	
	x = pd.DataFrame.to_numpy(df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]])

	t = df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]

	get_x_array(t)

	y = pd.DataFrame.to_numpy(df.loc[:, ['selling_price']])

	#pre-append X with 1xN array of ones
	one_n = np.ones(len(x))
	x = np.c_[one_n, x]

	#finding theta
	xt = np.transpose(x)
	xt_x = np.matmul(xt, x)

	xt_x_inv = np.linalg.inv(xt_x) #ERROR coming HERE!

	inv_prod = np.matmul(xt_x_inv, xt)

	theta = np.matmul(inv_prod, y)

	params[:] = theta 

	#print(theta)

	#print(theta.shape)

	#df_t = pd.DataFrame.to_numpy(t)


	predict(pd.DataFrame.to_numpy(t)[1])			##IMPORTANT TESTING #1
	#print('Actual:', df[['selling_price']][:].head() )


def predict(arr):
	
	price = 0.0

	arr = np.insert(arr, 0, 1., axis=0)
	for a, b in zip(arr, params_test): #!!!!REPLACE WITH PARAMS IF NOT USING ELIM!

		#print(str(a)+ ' *  coeff: '+ str(b)+' = \t'+str(a*b)+'\t'+str(price)+'\n')
		price = price + (a*b)

	return price
	#print(df['selling_price'][1])




def pred_test(arr):
	t = df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]

	t = arr

	#print(df.selling_price.value_counts())
	count = 0;

	for i in range(len(t)):
		act = df.selling_price[i]
		price = predict(pd.DataFrame.to_numpy(t)[i])
		print('Actual : ', str(act), '\t','Predicted :', str(price), '\tOffset: ', str(float((price - act)/act)*100),'%' )


		
def find_corr():
	t = df.loc[:, ['selling_price','year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]

	col_names = t.columns

	# for y-x correlation

	pr = df.loc[:, ['selling_price']].to_numpy()
	n = t.to_numpy()
	i=0;
	for column in n.T:
		coeffs = (np.corrcoef(x=column, y=pr.T))
		print('r for ', col_names[i], ' and selling_price : ', float(coeffs[1][0]))
		i+=1

	i=0
	j=0
	#for x-x correlation
	for column in n.T:
		j=0
		for c2 in n.T:
		
				coeffs = (np.corrcoef(x=column, y=c2))
				r_val = coeffs[1][0]
				if(abs(r_val) > 0.6 and abs(r_val)!=1):
					print(col_names[i], ' : ', col_names[j], '\t', float(coeffs[1][0]))
				j+=1

		i+=1		


	#using min max scaling
	pass

def rms_error(arr): #returns value of root mean square error
	t = df.loc[:, ['year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]

	t = arr

	sum = 0
	count = 0;

	for i in range(len(t)):
		act = df.selling_price[i]
		price = predict(pd.DataFrame.to_numpy(t)[i])
		count+=1
		try:
			sum += (float(act)-float(price))**2
		except:
			print(str(act), ' : ', str(price))

	rmse = ((sum)**(0.5))/count
		
	return rmse

	pass

def test_plot():
	t = df.loc[:, ['selling_price','year', 'km_driven', 
       'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]
	
	t.plot(x='enginex', y='selling_price', style = 'o')
	plt.show()

	t.plot(x='milex', y='selling_price', style = 'o')
	plt.show()




	

process()


#model() ##MODEL METHOD, WITHOUT ELIMINATING BAD VARS

elim_model()

#find_corr()
#test_plot()


#pred_test()


def test():
	t = df.loc[:, ['year', 'km_driven', 
       	'seats', 'petrol', 'diesel', 'cng', 'lpg', 'indiv', 'dealer', 'trustmd',
       	'manual', 'auto', 'owner1', 'owner2', 'owner3', 'owner4', 'tdcar',
       	'milex', 'enginex', 'nmx', 'rpmx','max_powerx' ]]
	


	dataTypeSeries = t.dtypes   	
	print('Data type of each column of Dataframe :')
	print(dataTypeSeries)





#test()




