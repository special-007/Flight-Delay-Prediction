import math;
import numpy;
a=list();
f=open('stationmapping.txt');
n=0;
for i in range(2):
	num=f.readline().strip().split(' ');
	if(""==num):
		break;
	n=n+1;
	for g in num:
		print g;
	a.append(int(num));
a.sort();
print a;
d=numpy.percentile(a,25);
e=numpy.percentile(a,75);
s=e-d;
c=(2*s)/math.pow(float(n),1/3);
print c;
