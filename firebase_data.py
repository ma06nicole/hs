# import firebase_admin
# import pandas as pd
# import time

# cred_object = firebase_admin.credentials.Certificate('cred_obj.json')
# default_app = firebase_admin.initialize_app(cred_object, {
# 	'databaseURL': "https://hatespeech-abd47-default-rtdb.firebaseio.com"
# 	})

# from firebase_admin import db

# ref = db.reference("/")

# while True:
# 	data = ref.get()
# 	print(data)
# 	df = pd.DataFrame.from_dict(data)
# 	df = df.transpose()
# 	# print(df)
# 	df2 = df["loc"].value_counts()
# 	print(df2)
# 	row_names = df2.index
# 	print(row_names)
# 	# df2 = df.groupby("loc").count()
# 	# print(df2)
# 	# print(df2.shape)
# 	# df3 = row_names.concat(df2)
# 	# print(df3)
# 	df3 = pd.DataFrame(df2 , index = row_names)
# 	df3.reset_index(inplace=True)
# 	df3 = df3.rename(columns = {'index':'State'})
# 	print(df3)
# 	time.sleep(30)