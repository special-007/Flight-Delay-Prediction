import MySQLdb;
import sys;
import numpy;
import math;
import re;

def find_size(a,n):
	d=numpy.percentile(a,25);
	e=numpy.percentile(a,75);
	s=float(n);
	w=s**(1./3);
	s=e-d;
	c=(2*s)/w;
	return c;


def find_size1(a,n):
	d=numpy.percentile(a,5);
	e=numpy.percentile(a,95);
	s=float(n);
	w=s** (1./3);
	s=e-d;
	c=(2*s)/w;
	return c;

def find_size2(a,n):
	d=numpy.percentile(a,1);
	e=numpy.percentile(a,99);
	s=float(n);
	w=s** (1./3);
	s=e-d;
	c=(2*s)/w;
	return c;

def diffro(a,b):
	a1=a[:2];
	a2=a[2:];
	b1=b[:2];
	b2=b[2:];
	c=abs(int(a1)-int(b1));
	d=abs(int(a2)-int(b2));
	if(int(a1)>int(b1) and int(a2)>int(b2)):
		return c*60+d;
	if(int(b1)>int(a1) and int(b2)>int(a2)):
		return c*60+d;
	return abs(c*60-d);


db=MySQLdb.connect("localhost","root","root","project");
cursor=db.cursor();

flight_no='"'+sys.argv[1]+'"';
day1=sys.argv[2];
month1=sys.argv[3];
year1=sys.argv[4];

month2=month1;
day2=day1;
if(len(month2.encode('utf-8'))==1):
	month2='0'+month1;
if(len(day2.encode('utf-8'))==1):
	day2='0'+day1;

date1=year1+month2+day2;

sql="SELECT ORIGIN_AIRPORT_ID,CRS_DEP_TIME FROM dataset WHERE MONTH='%s' AND DAY_OF_MONTH='%s' AND FL_NUM='%s'" % (month1,day1,flight_no);

airport_id="";
time="";
try:
	cursor.execute(sql);
	result=cursor.fetchall();
	for row in result:
		airport_id=row[0];
		time=row[1];
except:
	print sys.exc_info();

airport_id=repr(airport_id);
time=repr(time);

time=time[1:-1];

f=open("stationmapping.txt","r");
a=list();
b=list();
for i in range(94):
	num=f.readline().strip().split(' ');
	a.append(num[0]);
	b.append(num[1]);
wban1="";
r=0;
airport_id=airport_id[1:-1];
for g in a:
	if(g==airport_id):
		wban1=b[r];
		break;
	r=r+1;
sql="SELECT Time,SkyCondition,Visibility,WindSpeed,WindDirection,StationPressure from weatherdata where WBAN='%s' AND DATE='%s'" % (wban1,date1);
time=time[1:-1];
try:
	cursor.execute(sql);
	result=cursor.fetchall();
	cursor.close();
	skycond="";
	visibil="";
	windspeed="";
	winddir="";
	staionpre="";
	min=60;
	for row in result:
		#print row[0];
		#print time;
		if(diffro(row[0],time)<=min):
			skycond=row[1];
			visibil=row[2];
			windspeed=row[3];
			winddir=row[4];
			staionpre=row[5];
			min=diffro(row[0],time);
	print (skycond,visibil,windspeed,winddir,staionpre);
	sql1="SELECT SkyCondition,Visibility,WindSpeed,WindDirection,StationPressure from dataset";
	try:
		cursor=db.cursor();
		cursor.execute(sql1);
		result1=cursor.fetchall();
		cursor.close();
		visib=list();
		windsp=list();
		winddr=list();
		press=list();
		for row1 in result1:
			'''if(re.match("OVC",repr(row1[0]))):
				ovc+=1;
			elif(re.match("SCT",repr(row1[0]))):
				sct+=1;
			elif(re.match("BKN",repr(row1[0]))):
				bkn+=1;
			elif(re.match("VV",repr(row1[0]))):
				vv+=1;
			elif(re.match("FEW",repr(row1[0]))):
				few+=1;
			else:
				clr+=1;'''


			der=repr(row1[1]);

			if(der!="'M'" and der!='None'):
				der=der[1:-1];
				visib.append(float(der));

			der=repr(row1[2]);

			if(der!="'M'" and der!="'  '" and der!='None'):
				der=der[1:-1];
				windsp.append(int(der));

			der=repr(row1[3]);
			if(der!="'M'" and der!="'VR '" and der!='None'):
				der=der[1:-1];
				winddr.append(int(der));

			der=repr(row1[4]);
			if(der!="'M'" and der!='None'):
				der=der[1:-1];
				press.append(float(der));
			

		visib.sort();
		windsp.sort();
		winddr.sort();
		press.sort();
		a1=find_size1(visib,len(visib));
		a2=find_size(windsp,len(windsp));
		a3=find_size(winddr,len(winddr));
		a4=find_size2(press,len(press));
		lower_visib=list();
		upper_visib=list();
		lower_windsp=list();
		upper_windsp=list();
		lower_winddr=list();
		upper_winddr=list();
		lower_press=list();
		upper_press=list();

		temp=visib[0];
		while(temp<visib[len(visib)-1]):
			lower_visib.append(temp);
			upper_visib.append(temp+a1);
			temp=temp+a1;

		if(temp-a1<visib[len(visib)-1]):
			lower_visib.append(temp);
			upper_visib.append(visib[len(visib)-1]);



		temp=windsp[0];
		while(temp<windsp[len(windsp)-1]):
			lower_windsp.append(temp);
			upper_windsp.append(temp+a1);
			temp=temp+a2;

		if(temp-a2<windsp[len(windsp)-1]):
			lower_windsp.append(temp);
			upper_windsp.append(windsp[len(windsp)-1]);



		temp=winddr[0];
		while(temp<winddr[len(winddr)-1]):
			lower_winddr.append(temp);
			upper_winddr.append(temp+a3);
			temp=temp+a3;

		if(temp-a3<winddr[len(winddr)-1]):
			lower_winddr.append(temp);
			upper_winddr.append(winddr[len(winddr)-1]);



		temp=press[0];
		while(temp<press[len(press)-1]):
			lower_press.append(temp);
			upper_press.append(temp+a1);
			temp=temp+a4;

		if(temp-a4<press[len(press)-1]):
			lower_press.append(temp);
			upper_press.append(press[len(press)-1]);
        


		skycond1="";
		if(re.match("OVC",skycond)):
			skycond1="OVC";
		elif(re.match("SCT",skycond)):
			skycond1="SCT";
		elif(re.match("BKN",skycond)):
			skycond1="BKN";
		elif(re.match("VV",skycond)):
			skycond1="VV";
		elif(re.match("FEW",skycond)):
			skycond1="FEW";
		else:
			skycond1="CLR";

		lower_visib1=0;
		upper_visib1=0;
		med_visibl="";

		if(visibil=="'M'" or visibil=='M'):
			med_visibl="'M'";

		elif(visibil=='None' or visibil==''):
			med_visibl='None';

		else:
			for i in range(len(lower_visib)):
				visibil=repr(visibil);
				visibil=visibil[1:-1];
				if(float(visibil)>=lower_visib[i] and float(visibil)<upper_visib[i]):
					lower_visib1=lower_visib[i];
					upper_visib1=upper_visib[i];
					break;
		lower_windsp1=0;
		upper_windsp1=0;
		med_windsp="";
		if(windspeed=="'M'" or windspeed=='M'):
			med_windsp="'M'";
		elif(windspeed=="'  '"):
			med_windsp='None';
		elif(windspeed=='None' or windspeed==''):
			med_windsp='None';
		else:
			for i in range(len(lower_windsp)):
				windspeed=repr(windspeed);
				windspeed=windspeed[1:-1];
				if(int(windspeed)>=lower_windsp[i] and int(windspeed)<upper_windsp[i]):
					lower_windsp1=lower_windsp[i];
					upper_windsp1=upper_windsp[i];
					break;
		lower_winddr1=0;
		upper_winddr1=0;
		med_winddr="";
		if(winddir=="'M'" or winddir=='M'):
			med_winddr="'M'";
		elif(winddir=="'VR '" or winddir=='VR '):
			med_winddr="'VR '";
		elif(winddir=='None' or winddir==''):
			med_winddr='None';
		else:
			for i in range(len(lower_winddr)):
				winddir=repr(winddir);
				winddir=winddir[1:-1];
				#print winddir;
				if(int(winddir)>=lower_winddr[i] and int(winddir)<upper_winddr[i]):
					lower_winddr1=lower_winddr[i];
					upper_winddr1=upper_winddr[i];
					break;

		lower_press1=0;
		upper_press1=0;
		med_press="";


		if(staionpre=="'M'" or staionpre=='M'):
			med_press="'M'";
		elif(staionpre=='None' or staionpre==''):
			med_press='None';
		else:
			for i in range(len(lower_press)):
				staionpre=repr(staionpre);
				staionpre=staionpre[1:-1];
				if(float(staionpre)>=lower_press[i] and float(staionpre)<upper_press[i]):
					lower_press1=lower_press[i];
					upper_press1=upper_press[i];
					break;

		#Starting of bayesian
		sql2="SELECT DEP_DELAY,SkyCondition,Visibility,WindSpeed,WindDirection,StationPressure from dataset";

		delay1=0;
		delay2=0;
		delay3=0;
		delay4=0;
		delay5=0;

		count=[0]*70;
		rows=0;
		try:
			cursor=db.cursor();
			cursor.execute(sql2);
			result2=cursor.fetchall();
			#print result2;
			result3=list(result2);
			result3.pop(0);
			for row in result3:
				rows+=1;
				wet=repr(row[0]);
				wet=wet[1:-1];
				if(wet=='' or float(wet)==0.00):
					#print "12";
					delay1+=1;
					qwa=repr(row[1]);
					qwa=qwa[1:-1];
					#print re.match(skycond1,"FEW034 FEW164");
					if(re.match(skycond1,qwa)):
						count[0]+=1;
					if(repr(row[2])=="'M'" or repr(row[2])=='M'):
						count[1]+=1;
					elif(repr(row[2])=='None' or repr(row[2])==''):
						count[2]+=1;
					else:
						dwq=repr(row[2]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_visib1 and float(dwq)<upper_visib1):
							count[3]+=1;
					if(repr(row[3])=="'M'" or repr(row[3])=='M'):
						count[4]+=1;
					elif(repr(row[3])=="'  '"):
						count[5]+=1;
					elif(repr(row[3])=='None' or repr(row[3])==''):
						count[5]+=1;
					else:
						dwq=repr(row[3]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_windsp1 and int(dwq)<upper_windsp1):
							count[6]+=1;

					if(repr(row[4])=="'M'" or repr(row[4])=='M'):
						count[7]+=1;
					elif(repr(row[4])=="'VR '" or repr(row[4])=='VR '):
						count[8]+=1;
					elif(repr(row[4])=='None' or repr(row[4])==''):
						count[9]+=1;
					else:
						dwq=repr(row[4]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_winddr1 and int(dwq)<upper_winddr1):
							count[10]+=1;

					if(repr(row[5])=="'M'" or repr(row[5])=='M'):
						count[11]+=1;
					elif(repr(row[5])=='None' or repr(row[5])==''):
						count[12]+=1;
					else:
						dwq=repr(row[5]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_press1 and float(dwq)<upper_press1):
							count[13]+=1;


				elif(float(wet)>0.00 and float(wet)<=6.75):
					delay2+=1;
					qwa=repr(row[1]);
					qwa=qwa[1:-1];
					if(re.match(skycond1,qwa)):
						count[14]+=1;
					if(repr(row[2])=="'M'" or repr(row[2])=='M'):
						count[15]+=1;
					elif(repr(row[2])=='None' or repr(row[2])==''):
						count[16]+=1;
					else:
						dwq=repr(row[2]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_visib1 and float(dwq)<upper_visib1):
							count[17]+=1;

					if(repr(row[3])=="'M'" or repr(row[3])=='M'):
						count[18]+=1;
					elif(repr(row[3])=="'  '"):
						count[19]+=1;
					elif(repr(row[3])=='None' or repr(row[3])==''):
						count[19]+=1;
					else:
						dwq=repr(row[3]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_windsp1 and int(dwq)<upper_windsp1):
							count[20]+=1;

					if(repr(row[4])=="'M'" or repr(row[4])=='M'):
						count[21]+=1;
					elif(repr(row[4])=="'VR '" or repr(row[4])=='VR '):
						count[22]+=1;
					elif(repr(row[4])=='None' or repr(row[4])==''):
						count[23]+=1;
					else:
						dwq=repr(row[4]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_winddr1 and int(dwq)<upper_winddr1):
							count[24]+=1;

					if(repr(row[5])=="'M'" or repr(row[5])=='M'):
						count[25]+=1;
					elif(repr(row[5])=='None' or repr(row[5])==''):
						count[26]+=1;
					else:
						dwq=repr(row[5]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_press1 and float(dwq)<upper_press1):
							count[27]+=1;


				elif(float(wet)>6.75 and float(wet)<=19.00):
					delay3+=1;
					qwa=repr(row[1]);
					qwa=qwa[1:-1];
					if(re.match(skycond1,qwa)):
						count[28]+=1;
					if(repr(row[2])=="'M'" or repr(row[2])=='M'):
						count[29]+=1;
					elif(repr(row[2])=='None' or repr(row[2])==''):
						count[30]+=1;
					else:
						dwq=repr(row[2]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_visib1 and float(dwq)<upper_visib1):
							count[31]+=1;

					if(repr(row[3])=="'M'" or repr(row[3])=='M'):
						count[32]+=1;
					elif(repr(row[3])=="'  '"):
						count[33]+=1;
					elif(repr(row[3])=='None' or repr(row[3])==''):
						count[33]+=1;
					else:
						dwq=repr(row[3]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_windsp1 and int(dwq)<upper_windsp1):
							count[34]+=1;

					if(repr(row[4])=="'M'" or repr(row[4])=='M'):
						count[35]+=1;
					elif(repr(row[4])=="'VR '" or repr(row[4])=='VR '):
						count[36]+=1;
					elif(repr(row[4])=='None' or repr(row[4])==''):
						count[37]+=1;
					else:
						dwq=repr(row[4]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_winddr1 and int(dwq)<upper_winddr1):
							count[38]+=1;

					if(repr(row[5])=="'M'" or repr(row[5])=='M'):
						count[39]+=1;
					elif(repr(row[5])=='None' or repr(row[5])==''):
						count[40]+=1;
					else:
						dwq=repr(row[5]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_press1 and float(dwq)<upper_press1):
							count[41]+=1;


				elif(float(wet)>19.00 and float(wet)<=47.50):
					delay4+=1;
					qwa=repr(row[1]);
					qwa=qwa[1:-1];
					if(re.match(skycond1,qwa)):
						count[42]+=1;
					if(repr(row[2])=="'M'" or repr(row[2])=='M'):
						count[43]+=1;
					elif(repr(row[2])=='None' or repr(row[2])==''):
						count[44]+=1;
					else:
						dwq=repr(row[2]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_visib1 and float(dwq)<upper_visib1):
							count[45]+=1;

					if(repr(row[3])=="'M'" or repr(row[3])=='M'):
						count[46]+=1;
					elif(repr(row[3])=="'  '"):
						count[47]+=1;
					elif(repr(row[3])=='None' or  repr(row[3])==''):
						count[47]+=1;
					else:
						dwq=repr(row[3]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_windsp1 and int(dwq)<upper_windsp1):
							count[48]+=1;

					if(repr(row[4])=="'M'" or repr(row[4])=='M'):
						count[49]+=1;
					elif(repr(row[4])=="'VR '" or repr(row[4])=='VR '):
						count[50]+=1;
					elif(repr(row[4])=='None' or repr(row[4])==''):
						count[51]+=1;
					else:
						dwq=repr(row[4]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_winddr1 and int(dwq)<upper_winddr1):
							count[52]+=1;

					if(repr(row[5])=="'M'" or repr(row[5])=='M'):
						count[53]+=1;
					elif(repr(row[5])=='None' or repr(row[5])==''):
						count[54]+=1;
					else:
						dwq=repr(row[5]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_press1 and float(dwq)<upper_press1):
							count[55]+=1;



				else:
					delay5+=1;
					qwa=repr(row[1]);
					qwa=qwa[1:-1];
					if(re.match(skycond1,qwa)):
						count[56]+=1;
					if(repr(row[2])=="'M'" or repr(row[2])=='M'):
						count[57]+=1;
					elif(repr(row[2])=='None' or repr(row[2])==''):
						count[58]+=1;
					else:
						dwq=repr(row[2]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_visib1 and float(dwq)<upper_visib1):
							count[59]+=1;

					if(repr(row[3])=="'M'" or repr(row[3])=='M'):
						count[60]+=1;
					elif(repr(row[3])=="'  '"):
						count[61]+=1;
					elif(repr(row[3])=='None' or repr(row[3])==''):
						count[61]+=1;
					else:
						dwq=repr(row[3]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_windsp1 and int(dwq)<upper_windsp1):
							count[62]+=1;

					if(repr(row[4])=="'M'" or repr(row[4])=='M'):
						count[63]+=1;
					elif(repr(row[4])=="'VR '" or repr(row[4])=='VR '):
						count[64]+=1;
					elif(repr(row[4])=='None' or repr(row[4])==''):
						count[65]+=1;
					else:
						dwq=repr(row[4]);
						dwq=dwq[1:-1];
						if(int(dwq)>=lower_winddr1 and int(dwq)<upper_winddr1):
							count[66]+=1;

					if(repr(row[5])=="'M'" or repr(row[5])=='M'):
						count[67]+=1;
					elif(repr(row[5])=='None' or repr(row[5])==''):
						count[68]+=1;
					else:
						dwq=repr(row[5]);
						dwq=dwq[1:-1];
						if(float(dwq)>=lower_press1 and float(dwq)<upper_press1):
							count[69]+=1;

			pofdelay1=float(delay1)/float(rows);
			pofdelay2=float(delay2)/float(rows-delay1);
			pofdelay3=float(delay3)/float(rows-delay1);
			pofdelay4=float(delay4)/float(rows-delay1);
			pofdelay5=float(delay5)/float(rows-delay1);

			pofskyanddelay=[0]*5;
			pofvisibanddelay=[0]*5;
			pofwindspanddelay=[0]*5;
			pofwinddranddelay=[0]*5;
			pofwindpranddelay=[0]*5;

			pofskyanddelay[0]=float(count[0])/float(delay1);
			pofskyanddelay[1]=float(count[14])/float(delay2);
			pofskyanddelay[2]=float(count[28])/float(delay3);
			pofskyanddelay[3]=float(count[42])/float(delay4);
			pofskyanddelay[4]=float(count[56])/float(delay5);

			if(med_visibl=="'M'"):
				pofvisibanddelay[0]=float(count[1])/float(delay1);
				pofvisibanddelay[1]=float(count[15])/float(delay2);
				pofvisibanddelay[2]=float(count[29])/float(delay3);
				pofvisibanddelay[3]=float(count[43])/float(delay4);
				pofvisibanddelay[4]=float(count[57])/float(delay5);

			elif(med_visibl=='None'):
				pofvisibanddelay[0]=float(count[2])/float(delay1);
				pofvisibanddelay[1]=float(count[16])/float(delay2);
				pofvisibanddelay[2]=float(count[30])/float(delay3);
				pofvisibanddelay[3]=float(count[44])/float(delay4);
				pofvisibanddelay[4]=float(count[58])/float(delay5);

			else:
				pofvisibanddelay[0]=float(count[3])/float(delay1);
				pofvisibanddelay[1]=float(count[17])/float(delay2);
				pofvisibanddelay[2]=float(count[31])/float(delay3);
				pofvisibanddelay[3]=float(count[45])/float(delay4);
				pofvisibanddelay[4]=float(count[59])/float(delay5);

			if(med_windsp=="'M'"):
				pofwindspanddelay[0]=float(count[4])/float(delay1);
				pofwindspanddelay[1]=float(count[18])/float(delay2);
				pofwindspanddelay[2]=float(count[32])/float(delay3);
				pofwindspanddelay[3]=float(count[46])/float(delay4);
				pofwindspanddelay[4]=float(count[60])/float(delay5);								

			elif(med_windsp=="'  '" or med_windsp=='None'):
				pofwindspanddelay[0]=float(count[5])/float(delay1);
				pofwindspanddelay[1]=float(count[19])/float(delay2);
				pofwindspanddelay[2]=float(count[33])/float(delay3);
				pofwindspanddelay[3]=float(count[47])/float(delay4);
				pofwindspanddelay[4]=float(count[61])/float(delay5);

			else:
				pofwindspanddelay[0]=float(count[6])/float(delay1);
				pofwindspanddelay[1]=float(count[20])/float(delay2);
				pofwindspanddelay[2]=float(count[34])/float(delay3);
				pofwindspanddelay[3]=float(count[48])/float(delay4);
				pofwindspanddelay[4]=float(count[62])/float(delay5);

			if(med_winddr=="'M'"):
				pofwinddranddelay[0]=float(count[7])/float(delay1);
				pofwinddranddelay[1]=float(count[21])/float(delay2);
				pofwinddranddelay[2]=float(count[35])/float(delay3);
				pofwinddranddelay[3]=float(count[49])/float(delay4);
				pofwinddranddelay[4]=float(count[63])/float(delay5);

			elif(med_winddr=="'VR '"):
				pofwinddranddelay[0]=float(count[8])/float(delay1);
				pofwinddranddelay[1]=float(count[22])/float(delay2);
				pofwinddranddelay[2]=float(count[36])/float(delay3);
				pofwinddranddelay[3]=float(count[50])/float(delay4);
				pofwinddranddelay[4]=float(count[64])/float(delay5);

			elif(med_winddr=='None'):
				pofwinddranddelay[0]=float(count[9])/float(delay1);
				pofwinddranddelay[1]=float(count[23])/float(delay2);
				pofwinddranddelay[2]=float(count[37])/float(delay3);
				pofwinddranddelay[3]=float(count[51])/float(delay4);
				pofwinddranddelay[4]=float(count[65])/float(delay5);

			else:
				pofwinddranddelay[0]=float(count[10])/float(delay1);
				pofwinddranddelay[1]=float(count[24])/float(delay2);
				pofwinddranddelay[2]=float(count[38])/float(delay3);
				pofwinddranddelay[3]=float(count[42])/float(delay4);
				pofwinddranddelay[4]=float(count[66])/float(delay5);

			if(med_press=="'M'"):
				pofwindpranddelay[0]=float(count[11])/float(delay1);
				pofwindpranddelay[1]=float(count[25])/float(delay2);
				pofwindpranddelay[2]=float(count[39])/float(delay3);
				pofwindpranddelay[3]=float(count[53])/float(delay4);
				pofwindpranddelay[4]=float(count[67])/float(delay5);

			elif(med_press=='None'):
				pofwindpranddelay[0]=float(count[12])/float(delay1);
				pofwindpranddelay[1]=float(count[26])/float(delay2);
				pofwindpranddelay[2]=float(count[40])/float(delay3);
				pofwindpranddelay[3]=float(count[54])/float(delay4);
				pofwindpranddelay[4]=float(count[68])/float(delay5);

			else:
				pofwindpranddelay[0]=float(count[13])/float(delay1);
				pofwindpranddelay[1]=float(count[27])/float(delay2);
				pofwindpranddelay[2]=float(count[41])/float(delay3);
				pofwindpranddelay[3]=float(count[55])/float(delay4);
				pofwindpranddelay[4]=float(count[69])/float(delay5);				


			mylist=list();

			#mylist.append(pofdelay1*pofskyanddelay[0]*pofwindspanddelay[0]*pofwinddranddelay[0]*pofvisibanddelay[0]*pofwindpranddelay[0]);
			mylist.append(pofdelay2*pofskyanddelay[1]*pofwindspanddelay[1]*pofvisibanddelay[1]*pofwindpranddelay[1]);
			mylist.append(pofdelay3*pofskyanddelay[2]*pofwindspanddelay[2]*pofvisibanddelay[2]*pofwindpranddelay[2]);
			mylist.append(pofdelay4*pofskyanddelay[3]*pofwindspanddelay[3]*pofvisibanddelay[3]*pofwindpranddelay[3]);
			mylist.append(pofdelay5*pofskyanddelay[4]*pofwindspanddelay[4]*pofvisibanddelay[4]*pofwindpranddelay[4]);

			max_value=max(mylist);
			print mylist;
			my_index=mylist.index(max_value);

			print my_index;

			'''print (pofdelay1,pofdelay2,pofdelay3,pofdelay4,pofdelay5);
			print pofskyanddelay;
			print pofwindspanddelay;
			print pofwinddranddelay;
			print pofvisibanddelay;
			print pofwindpranddelay;'''

		except:
			print sys.exc_info();
			print "1";
	except:
		print sys.exc_info();
		print "2";
except:
	print sys.exc_info();
	print "3";
