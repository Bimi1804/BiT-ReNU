
plant_txt = """
SalesStatistics <|-- DailyStatistics
SalesStatistics <|-- WeeklyStatistics
VehiclePurchase <|-- Leasing 
VehiclePurchase <|-- Financing
VehiclePurchase <|-- CashPurchase
Customer <|-- CorporateCustomer
Customer <|-- PrivateCustomer
Vehicle <|-- PassengerVehicle
Vehicle <|-- Truck
Vehicle <|-- Motorcycle
PassengerVehicle <|-- Convertible 
PassengerVehicle <|-- Sedan 
PassengerVehicle <|-- SuV 

WeeklyStatistics "1..*" *-- "0..*" DailyStatistics
SalesStatistics "1..*" *-- "0..*" VehiclePurchase 


Employee "1..*" -- "0..*" VehiclePurchase: advises
Customer "1..*" -- "1..*" VehiclePurchase: makes
VehiclePurchase "0..*" -- "1..*" Vehicle: sells"""








sql_statements = []

#-----------------------------------------------------
generalization = []
composition = []
plant_asc_lines = plant_txt.splitlines()
for line in plant_asc_lines:
	if "<|--" in line:
		generalization.append(line)
		plant_txt = plant_txt.replace(line,"")
	if "*--" in line:
		composition.append(line)
		plant_txt = plant_txt.replace(line,"")

for gen in generalization:
	arrow = gen.find("<|--")
	sql_statements.append(f"""INSERT OR IGNORE INTO generalization(super_class,sub_class) 
											VALUES ('{gen[:arrow]}','{gen[arrow+4:]}')""")


for line in composition:
	pointer = line.find('"')
	class_a = line[:pointer]
	line = line[pointer:]
	pointer = line.find("..")
	low_a = line[:pointer].replace('"',"")
	line = line[pointer+2:]
	pointer = line.find('"')
	up_a = line[:pointer].replace('"',"")
	line = line[pointer+1:]
	line = line[line.find('"')+1:]
	pointer = line.find("..")
	low_b = line[:pointer]
	line = line[pointer:]
	pointer = line.find('"')
	up_b = line[:pointer].replace("..","")
	line = line[pointer+1:]
	class_b = line
	sql_statements.append(f"""INSERT OR IGNORE INTO associations(asc_name,agg_kind,
							class_name_a,class_name_b,lower_a,lower_b,upper_a,upper_b) 
							VALUES ('is part of','composite','{class_a}','{class_b}','{low_a}','{up_a}','{low_b}','{up_b}')""")

plant_asc_lines = plant_txt.splitlines()
associations = []
for line in plant_asc_lines:
	if line != "" and line != "@enduml":
		associations.append(line)
for line in associations:
	pointer = line.find('"')
	class_a = line[:pointer]
	line = line[pointer:]
	pointer = line.find("..")
	lower_a = line[:pointer].replace('"',"")
	line = line[pointer+2:]
	pointer = line.find('"')
	upper_a = line[:pointer].replace('"',"")
	line = line[pointer+1:]
	line = line[line.find('"')+1:]
	pointer = line.find("..")
	lower_b = line[:pointer]
	line = line[pointer:]
	pointer = line.find('"')
	upper_b = line[:pointer].replace("..","")
	line = line[pointer+1:]
	pointer = line.find(":")
	class_b = line[:pointer]
	asc_name = line[pointer+1:]
	sql_statements.append(f"""INSERT OR IGNORE INTO associations
							(asc_type,asc_name,class_a,class_b,lower_a,upper_a,lower_b,upper_b) 
							VALUES ('none','{asc_name}','{class_a}','{class_b}','{lower_a}','{upper_a}','{lower_b}','{upper_b}')""")

for i in sql_statements:
	print(i)