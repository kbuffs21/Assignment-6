import getopt, sys
import sys
import math


pollution = {'l' : 0.9,'h' : 0.1}
smoker = {'t' : 0.3, 'f' : 0.7}
cancer = {'t|ht' : 0.05,'t|hf' : 0.02, 't|lt' : 0.03, 't|lf' : 0.001 }
xray = {'t|t' : 0.9,'t|f' : 0.2}
dyspnoea = {'t|t' : 0.65,'t|f' :0.3}

def calc(pollution,smoker,cancer,xray,dyspnoea):
	cancer['t'] = cancer['t|ht']*pollution['h']*smoker['t'] + cancer['t|hf']*pollution['h']*smoker['f'] + cancer['t|lt']*pollution['l']*smoker['t'] + cancer['t|lf']*pollution['l']*smoker['f']
	cancer['f'] = 1 - cancer['t']
	dyspnoea['f|t'] = 1 - dyspnoea['t|t']
	dyspnoea['f|f'] = 1 - dyspnoea['t|f']
	xray['f|t'] = 1 - xray['t|t']
	xray['f|f'] = 1 - xray['t|f']

def parseArgs(a):
	chars = []
	for c in a:		
	   chars.append(c)
	i = 0
	while i < len(chars):
		if chars[i] == '~':
			temp = chars[i] + chars[i+1]
			chars.insert(i,temp)
			chars.pop(i+1)
			chars.pop(i+1)
		i = i + 1	
	return chars
	
def setPrior(a,b,pollution,smoker):
	if a == 'P':
		pollution['l'] = b
		pollution['h'] = (1-b)
	elif a == 'S':
		smoker['t'] = b
		smoker['f'] = (1-b)		

def calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea):
	calc(pollution,smoker,cancer,xray,dyspnoea)
	if a == 'D':
		a = 'd'
		b = '~d'
		t  = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		f  = calcMarginal(b,pollution,smoker,cancer,xray,dyspnoea)
		print 'prob(d=t) = {0}'.format(t)
		print 'prob(d=f) = {0}'.format(f)
		return 'Probability Distribution'
	elif a == 'X':
		a = 'x'
		b = '~x'
		t  = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		f  = calcMarginal(b,pollution,smoker,cancer,xray,dyspnoea)
		print 'prob(x=t) = {0}'.format(t)
		print 'prob(x=f) = {0}'.format(f)
		return 'Probability Distribution'
	elif a == 'C':
		a = 'c'
		b = '~c'
		t  = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		f  = calcMarginal(b,pollution,smoker,cancer,xray,dyspnoea)
		print 'prob(c=t) = {0}'.format(t)
		print 'prob(c=f) = {0}'.format(f)
		return 'Probability Distribution'
	elif a == 'P':
		a = 'p'
		b = '~p'
		t  = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		f  = calcMarginal(b,pollution,smoker,cancer,xray,dyspnoea)
		print 'prob(p=l) = {0}'.format(t)
		print 'prob(p=h) = {0}'.format(f)
		return 'Probability Distribution'
	elif a == 'S':
		a = 's'
		b = '~s'
		t  = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		f  = calcMarginal(b,pollution,smoker,cancer,xray,dyspnoea)
		print 'prob(s=t) = {0}'.format(t)
		print 'prob(s=f) = {0}'.format(f)
		return 'Probability Distribution'
	elif a == 'd':
		return (dyspnoea['t|t']*cancer['t'] + dyspnoea['t|f']*cancer['f'])
	elif a == '~d':
		return (dyspnoea['f|t']*cancer['t'] + dyspnoea['f|f']*cancer['f'])
	elif a == 'x':
		return (xray['t|t']*cancer['t'] + xray['t|f']*cancer['f'])
	elif a == '~x':
		return (xray['f|t']*cancer['t'] + xray['f|f']*cancer['f']) 		
	elif a == 'c':
		return cancer['t']
	elif a == '~c':
		return cancer['f']
	elif a == 's':
		return smoker['t']
	elif a == '~s':
		return smoker['f']
	elif a == 'p':
		return pollution['h']
	elif a == '~p':
		return pollution['l']
		
def calcConditional(a,b,pollution,smoker,cancer,xray,dyspnoea):
	a = parseArgs(a)
	b = parseArgs(b)
	n = calcJoint(a,pollution,smoker,cancer,xray,dyspnoea)
	x = calcJoint(b,pollution,smoker,cancer,xray,dyspnoea)
	if type(n) == str and type(b) == str:
		return n + ' / ' + b 
	else:
		inv = calcMarginal(b[0],pollution,smoker,cancer,xray,dyspnoea)
		return n * inv/x

def calcJoint(a,pollution,smoker,cancer,xray,dyspnoea):
	chars = []
	chars = parseArgs(a)
	product = 1
	temp = ''
	for a in chars:
		bollock = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
		if type(bollock) == str:
			temp = bollock
		else:
			product = product * bollock
	if temp != '':
		return temp
	else:
		return product 


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			setPrior(a[0], float(a[1:]),pollution,smoker)
		elif o in ("-m"):
			print "flag", o
			print "args", a
			ans = calcMarginal(a,pollution,smoker,cancer,xray,dyspnoea)
			print 'marginal prob of {0} = {1}'.format(a,ans)
		
		elif o in ("-g"):
			print "flag", o
			print "args", a
			p = a.find("|")
			ans = calcConditional(a[:p], a[p+1:],pollution,smoker,cancer,xray,dyspnoea)
			print 'condtional prob of {0} given {1} = {2}'.format(a[:p],a[p+1:],ans)
			
		elif o in ("-j"):
			print "flag", o
			print "args", a
			ans = calcJoint(a,pollution,smoker,cancer,xray,dyspnoea)
			print 'joint prob of {0} = {1}'.format(a,ans)
		else:
			assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()