import MySQLdb;
import sys;

db = MySQLdb.connect("localhost","root","root","project" );
cursor=db.cursor();

f=open("stationmapping.txt","r");
a=list();
b=list();
for i in range(94):
	num=f.readline().strip().split(' ');
	a.append(num[0]);
	b.append(num[1]);

sql="SELECT YEAR,MONTH,DAY_OF_MONTH,ORIGIN_AIRPORT_ID,CRS_DEP_TIME FROM dataset";
try:
	cursor.execute(sql);
	result=cursor.fetchall();
	cursor.close();
	for row in result:
		airport_id=row[3];
		dayofmonth=row[2];
		month1=row[1];
		year1=row[0];
		time1=row[4];
		r=0;
		wban1=0;
		#print a;
		#print b;
		#print airport_id;
		month2=month1;
		dayofmonth2=dayofmonth;
		if(len(dayofmonth2.encode('utf-8'))==1):
			dayofmonth2='0'+dayofmonth;
		if(len(month2.encode('utf-8'))==1):
			month2='0'+month1;
		for f in a:
			if(f==airport_id):
				wban1=b[r];
				break;
			r=r+1;
		time1=time1[1:-1];
		date1=year1 + month2 + dayofmonth2  ;
		sql1="SELECT Time,SkyCondition,DryBulbCelsius,Visibility,WindSpeed,WindDirection,StationPressure FROM weatherdata WHERE WBAN='%s' AND Date='%s'" % (wban1,date1);
		try:
			cursor=db.cursor();
			cursor.execute(sql1);
			result1=cursor.fetchall();
			for row in result1:
				if(abs(int(row[0])-int(time1))<=100):
					#print row;
					skycond=row[1];
					drybulb=row[2];
					visib=row[3];
					windsp=row[4];
					winddir=row[5];
					stapres=row[6];


					time2='"'+time1+'"';
					print year1;
					print month1;
					print dayofmonth;
					print airport_id;
					print time2;

					sql3="SELECT * FROM dataset WHERE YEAR='%s' AND MONTH='%s' AND DAY_OF_MONTH='%s' AND ORIGIN_AIRPORT_ID='%s' AND CRS_DEP_TIME='%s'" % (year1,month1,dayofmonth,airport_id,time2);
					try:
						cursor=db.cursor();
						cursor.execute(sql3);
						result3=cursor.fetchall();
						print result3;
						'''for rq in result3:
							print rq;
							print "\n";'''
					except:
						print "dewfwe";

					sql2="UPDATE dataset set SkyCondition='%s',DryBulbCelsius='%s',Visibility='%s',WindSpeed='%s',WindDirection='%s',StationPressure='%s' WHERE YEAR='%s' AND MONTH='%s' AND DAY_OF_MONTH='%s' AND ORIGIN_AIRPORT_ID='%s' AND CRS_DEP_TIME='%s'" % (skycond,drybulb,visib,windsp,winddir,stapres,year1,month1,dayofmonth,airport_id,time2);
					try:
						cursor.execute(sql2);
						db.commit();
					except:
						db.rollback();
						print "Error\n";
					
		except:
			print sys.exc_info();
except:
	print sys.exc_info();
db.close();
