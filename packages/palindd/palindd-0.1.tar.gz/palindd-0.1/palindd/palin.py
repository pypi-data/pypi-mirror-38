class palin:
	def __init__(self,string):
		self.string=string

		
		s=self.string
		a=[]
		for i in s:
			a.append(i)
		b=[]
		for i in range(len(a)-1,-1,-1):
			b.append(a[i])
		if(a==b):
			print('True')
		else:
			print('False')

# if __name__=='__main__':
# 	obj=palin('kaif')
# 	obj.check()