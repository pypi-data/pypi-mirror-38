"""
This is the one and only Quilt Lang file.
"""
import warnings
import keyword
import importlib
import string
import pprint
import secrets
import textwrap
import subprocess
import os
import sys
import logging
import pkg_resources
import clipboard
import math
import statistics
import random
import datetime
import time
import calendar
import webbrowser
import urllib
import loremipsum
import colour
"""
Uncatagorised
"""
def userinput(prompttext=""):
 if sys.version_info>(3,0):
  return input(str(prompttext))
 return raw_input(str(prompttext))
def shellinput(initialtext='>> ',splitpart=' '):
 try:
  str(initialtext)
 except RuntimeError:
  raise RuntimeWarning("Cannot convert type "+str(type(initialtext))+"to str")
 shelluserinput=userinput(str(initialtext))
 if splitpart=='' or splitpart is None:
  return shelluserinput
 commands=[]
 for item in enumerate(shelluserinput.split(splitpart)):
  commands.append(item[1])
 return commands
def colourcode(startcolourcode,destinationtype,longhex=False):
 c=colour.Color(str(startcolourcode))
 if destinationtype.lower()=='hex':
  if longhex is True:
   return c.hex_l
  return c.hex
 elif destinationtype.lower()=='hsl':
  return c.hsl
 elif destinationtype.lower()=='rgb':
  return c.rgb
 elif destinationtype.lower()=='red':
  return c.red
 elif destinationtype.lower()=='blue':
  return c.blue
 elif destinationtype.lower()=='green':
  return c.green
 elif destinationtype.lower()=='hue':
  return c.hue
 elif destinationtype.lower()=='sat':
  return c.saturation
 elif destinationtype.lower()=='lum':
  return c.luminance
 raise RuntimeWarning("Destination colour code not specified correctly")
def changecolour(colourcode,action,amount=100):
 c=colour.Color(colourcode)
 if action=='red':
  c.red=amount/100
  return c
 elif action=='blue':
  c.blue=amount/100
  return c
 elif action=='green':
  c.green=amount/100
  return c
 elif action=='hue':
  c.hue=amount/100
  return c
 elif action=='sat':
  c.saturation=amount/100
  return c
 elif action=='lum':
  c.luminance=amount/100
  return c
def leadingzero(number,minlength):
 return str(number).zfill(int(minlength))
def absolutenum(number):
 return abs(number)
def splitstring(string,split_character=' ',part=None):
 if part is None:
  return str(string).split(split_character)
 return str(string).split(split_character)[part]
def sort(listtosort,key=None,reversesort=False):
 return sorted(listtosort,key=key,reverse=reversesort)
def pykeyword(operation='list',keywordtotest=None):
 if operation=='list':
  return str(keyword.kwlist)
 elif operation=='check':
  return keyword.iskeyword(str(keywordtotest))
def prettyprinter(listtoprint,stream=None,indent=1,width=80,depth=None):
 pprint.pprint(listtoprint,stream,indent,width,depth)
def genipsum(sentences=1):
 return loremipsum.get_sentences(sentences)
def bintobool(integer):
 if isinteger(integer)and integer<2 and integer>-1:
  if integer==0:
   return False
  elif integer==1:
   return True
def modulereload(modulename):
 importlib.reload(modulename)
def warnconfig(action='default'):
 if action=='default':
  warnings.filterwarnings('default')
 elif action=='error':
  warnings.filterwarnings('error')
 elif action=='ignore':
  warnings.filterwarnings('ignore')
 elif action=='always':
  warnings.filterwarnings('always')
 elif action=='module':
  warnings.filterwarnings('module')
 elif action=='once':
  warnings.filterwarnings('once')
def message_print(text,amount=1):
 for _ in range(amount):
  print(text)
def shapesides(inputtocheck,inputtype='shape'):
 inputtocheck=inputtocheck.lower()
 shapestosides={'triangle':3,'square':4,'pentagon':5,'hexagon':6,'heptagon':7,'octagon':8,'nonagon':9,'decagon':10,'hendecagon':11,'dodecagon':12,'triskaidecagon':13,'tetrakaidecagon':14,'pentadecagon':15,'hexakaidecagon':16,'heptadecagon':17,'octakaidecagon':18,'enneadecagon':19,'Icosagon':20,'triacontagon':30,'tetracontagon':40,'pentacontagon':50,'hexacontagon':60,'heptacontagon':70,'octacontagon':80,'enneacontagon':90,'hectagon':100,'chiliagon':1000,'myriagon':10000,'megagon':1000000,'googolgon':pow(10,100)}
 if inputtype=='shape':
  if inputtocheck in shapestosides:
   return shapestosides[inputtocheck]
  return "ngon"
def comparenum(value1,value2,comparison):
 if isnum(value1)and isnum(value2):
  comparison=comparison.lower()
  if comparison=='equals':
   return value1==value2
  elif comparison=='not equal':
   return value1!=value2
  elif comparison=='less than':
   return value1<value2
  elif comparison=='greater than':
   return value1>value2
  elif comparison=='more than':
   return value1>value2
  elif comparison=='less than or equal to':
   return value1<=value2
  elif comparison=='greater than or equal to':
   return value1>=value2
  elif comparison=='more than or equal to':
   return value1>=value2
def throwerror(errortext):
 raise RuntimeWarning("Forced Error: "+str(errortext))
def delay(seconds):
 time.sleep(seconds)
def wait_enter(times=1):
 for _ in range(times):
  userinput('')
def convertstring(value):
 return str(value)
def opposite(boolean):
 try:
  return not boolean
 except RuntimeError:
  raise RuntimeWarning('An Error Has Occurred: Nor A Bool Or Len Was Provided (0014)')
def isdecimal(value):
 return bool(isinstance(value,float))
def isstring(variable):
 return bool(isinstance(variable,str))
def istype(variable,typeexpected):
 return bool(isinstance(variable,typeexpected))
def isinteger(value):
 return bool(isinstance(value,int))
def isboolean(value):
 return isinstance(value,bool)
def happybirthday(person):
 print('Happy Birthday To You')
 time.sleep(2)
 print('Happy Birthday To You')
 time.sleep(2)
 print('Happy Birthday Dear '+str(person[0].upper())+str(person[1:]))
 time.sleep(2)
 print('Happy Birthday To You')
def difference(num1,num2):
 return abs(num1-num2)
def divisable(num1,num2):
 return bool(num1%num2==0)
def isempty(variable):
 return bool(variable=='')
def length(value):
 try:
  return len(convertstring(value))
 except OverflowError:
  raise RuntimeWarning('An Error Has Occured: The length of the object exceeds         the limit of {0}'.format(str((charlimit()))))
def cowsay(text='',align='centre'):
 align=align.lower()
 cowtext=str(text)
 topbar=' '
 bottombar=' '
 spacing=''
 for _ in range(len(text)+2):
  topbar=topbar+'_'
  bottombar=bottombar+'-'
 if align in["center","centre"]:
  for _ in range((int(len(topbar)/2))+1):
   spacing=spacing+' '
 elif align=='left':
  spacing=' '
 elif align=='right':
  for _ in range(len(text)+2):
   spacing=spacing+' '
 print(topbar)
 print('( '+cowtext+' )')
 print(bottombar)
 print(spacing+r'o   ^__^ ')
 print(spacing+r' o  (oO)\_______')
 print(spacing+r'    (__)\       )\/\ ')
 print(spacing+r'     U  ||----w | ')
 print(spacing+r'        ||     || ')
def getletter(variable,letternumber):
 return str(variable)[letternumber-1]
def onlist(listtocheck,item):
 return item in listtocheck
def jointext(firststring,secondstring):
 return str(firststring)+str(secondstring)
def about():
 print('You Are Using ROS Code')
 print('ROS Code Is licensed Under The Apache License 2.0')
 print('Type "ros.license()" To Read The license')
def pyname(ifmain=False):
 if ifmain is True:
  return __name__=="__main__"
 return __name__
def convertbinary(value,argument):
 if argument=='to':
  try:
   return bin(value)
  except RuntimeError:
   raise RuntimeWarning('Invalid Value (0016)')
 elif argument=='from':
  try:
   return format(value)
  except RuntimeError:
   raise RuntimeWarning('Invalid Value (0016)')
def reversetext(texttoreverse,ignoretype=False):
 if ignoretype is False:
  if isinteger(texttoreverse):
   return int(str(texttoreverse)[::-1])
  elif isdecimal(texttoreverse):
   return float(str(texttoreverse)[::-1])
  return str(texttoreverse)[::-1]
 return str(texttoreverse)[::-1]
def reverselist(listtoreverse):
 return listtoreverse.reverse()
def replacetext(string,texttofind,texttoreplace):
 return string.replace(texttofind,texttoreplace)
def evaluate(evaluation):
 return eval(str(evaluation))
def execute(execution):
 exec(str(execution))
def gettype(value):
 return type(value)
def pingtest(returntrue=False):
 if returntrue:
  return True
 print("Pong!")
def convertascii(value,command='to'):
 command=command.lower()
 if command=='to':
  try:
   return chr(value)
  except ValueError:
   raise RuntimeWarning('Invalid Symbol Value (0014)')
 elif command=='from':
  try:
   return ord(value)
  except ValueError:
   raise RuntimeWarning('Invalid Symbol (0015)')
 else:
  raise RuntimeWarning('An Error Has Occurred: Invalid Operation Entered (0008)')
def availchar(charactertype):
 if charactertype=='letters':
  return string.ascii_letters
 elif charactertype=='lowercase':
  return string.ascii_lowercase
 elif charactertype=='uppercase':
  return string.ascii_uppercase
 elif charactertype=='digits':
  return string.digits
 elif charactertype=='hexdigits':
  return string.hexdigits
 elif charactertype=='punctuation':
  return string.punctuation
 elif charactertype=='printable':
  return string.printable
 elif charactertype=='whitespace':
  return string.whitespace
 else:
  raise RuntimeWarning('An Error Has Occurred: Invalid Operation Entered (0008)')
def wordvalue(word):
 total=0
 for i in enumerate(word):
  total+=letternum(word[i])
 return total
def enum(arguments):
 return enumerate(arguments)
def textbetween(variable,firstnum=None,secondnum=None,locationoftext='regular'):
 if locationoftext=='regular':
  return variable[firstnum:secondnum]
 elif locationoftext=='toend':
  return variable[firstnum:]
 elif locationoftext=='tostart':
  return variable[:secondnum]
def letternum(letter):
 if len(letter)==1 and isstring(letter):
  letter=letter.lower
  alphaletters=availchar('lowercase')
  for i in range(len(alphaletters)):
   if getletter(letter,1)==getletter(alphaletters,i+1):
    return i+1
def spacelist(listtospace):
 output=''
 space=''
 output+=str(listtospace[0])
 space+=' '
 for listnum in range(1,len(listtospace)):
  output+=space
  output+=str(listtospace[listnum])
 return output
def numlistbetween(num1,num2,option='list',listoption='string'):
 if option=='list':
  if listoption=='string':
   output=''
   output+=str(num1)
   for currentnum in range(num1+1,num2+1):
    output+=','
    output+=str(currentnum)
  elif listoption=='list':
   output=[]
   for currentnum in range(num1,num2+1):
    output.append(str(currentnum))
   return output
 elif option=='count':
  return num2-num1
def textalign(text,maxlength,align='left'):
 spaces=''
 if align=='left':
  return text
 elif align=='centre' or align=='center':
  for _ in range(int((maxlength-len(text))/2)):
   spaces+=' '
 elif align=='right':
  for _ in range(maxlength-len(text)):
   spaces+=' '
 return spaces+text
def decintfix(decorint=0):
 if str(decorint)[-2:]=='.0':
  return int(decorint)
 return float(decorint)
"""
Maths
"""
def autosolve(equation):
 try:
  num1=int(equation.split(" ")[0])
 except ValueError:
  num1=float(equation.split(" ")[0])
 try:
  num2=int(equation.split(" ")[2])
 except ValueError:
  num2=float(equation.split(" ")[2])
 if equation.split(" ")[1]in["+","plus","add"]:
  return num1+num2
 elif equation.split(" ")[1]in["-","minus","subtract"]:
  return num1-num2
 elif equation.split(" ")[1]in["*","times","multiply"]:
  return num1*num2
 elif equation.split(" ")[1]in["/","divide","quotient"]:
  return num1/num2
 elif equation.split(" ")[1]in["%","remainder","rem"]:
  return num1%num2
def autohard(equation):
 try:
  num1=int(equation.split(" ")[1])
 except ValueError:
  num1=float(equation.split(" ")[1])
 if equation.split(" ")[0]=="log":
  return math.log(num1)
 elif equation.split(" ")[0]=="acos":
  return math.acos(num1)
 elif equation.split(" ")[0]=="asin":
  return math.asin(num1)
 elif equation.split(" ")[0]=="atan":
  return math.atan(num1)
 elif equation.split(" ")[0]=="cos":
  return math.cos(num1)
 elif equation.split(" ")[0]=="hypot":
  try:
   num2=int(equation.split(" ")[2])
  except ValueError:
   num2=float(equation.split(" ")[2])
  return math.hypot(num1,num2)
 elif equation.split(" ")[0]=="sin":
  return math.sin(num1)
 elif equation.split(" ")[0]=="tan":
  return math.tan(num1)
def equation(operation,firstnum,secondnum):
 if not isnum(firstnum)and isnum(secondnum):
  raise RuntimeWarning('An Error Has Occured: One Of The Values Specified Is Not A Number (0002)')
 if operation=='plus':
  return(firstnum+secondnum)
 elif operation=='minus':
  return(firstnum-secondnum)
 elif operation=='multiply':
  return(firstnum*secondnum)
 elif operation=='divide':
  if not secondnum==0:
   return(firstnum/secondnum)
 else:
  raise RuntimeWarning('An Error Has Occured: You Entered An Invalid Operation (0003)')
def scientific(number,operation,number2=None,logbase=10):
 if operation=='log':
  return math.log(number,logbase)
 elif operation=='acos':
  return math.acos(number)
 elif operation=='asin':
  return math.asin(number)
 elif operation=='atan':
  return math.atan(number)
 elif operation=='cos':
  return math.cos(number)
 elif operation=='hypot':
  return math.hypot(number,number2)
 elif operation=='sin':
  return math.sin(number)
 elif operation=='tan':
  return math.tan(number)
def fracsimplify(numerator,denominator):
 if numerator==denominator:
  return '1/1'
 elif numerator>denominator:
  limit=int(numerator/2)
 elif numerator<denominator:
  limit=int(denominator/2)
 for i in range(2,limit):
  checknum=limit-i
  if numerator%checknum==0 and denominator%checknum==0:
   numerator=numerator/checknum
   denominator=denominator/checknum
 return str(int(numerator))+'/'+str(int(denominator))
def circleconvert(amount,currentformat,newformat):
 currentformat=currentformat.lower()
 newformat=newformat.lower()
 if currentformat==newformat:
  return amount
 if currentformat=='radius':
  if newformat=='diameter':
   return amount*2
  elif newformat=='circumference':
   return amount*2*math.pi
 elif currentformat=='diameter':
  if newformat=='radius':
   return amount/2
  elif newformat=='circumference':
   return amount*math.pi
 elif currentformat=='circumference':
  if newformat=='radius':
   return amount/math.pi/2
  elif newformat=='diameter':
   return amount/math.pi
def amountdiv(number,minnum,maxnum):
 amount=0
 for i in range(minnum,maxnum+1):
  if number%i==0:
   amount+=1
 return amount
def constant(constanttype):
 constanttype=constanttype.lower()
 if constanttype=='pi':
  return math.pi
 elif constanttype=='e':
  return math.e
 elif constanttype=='tau':
  return math.tau
 elif constanttype=='inf':
  return math.inf
 elif constanttype=='nan':
  return math.nan
 elif constanttype in['phi','golden']:
  return(1+5**0.5)/2
def power(number,power):
 return math.pow(number,power)
def squareroot(number):
 return math.sqrt(number)
def factorial(n):
 if n==0:
  return 1
 return n*factorial(n-1)
def average(numbers,averagetype='mean'):
 averagetype=averagetype.lower()
 try:
  statistics.mean(numbers)
 except RuntimeError:
  raise RuntimeWarning('An Error Has Occured: List Not Specified (0018)')
 if averagetype=='mean':
  return statistics.mean(numbers)
 elif averagetype=='mode':
  return statistics.mode(numbers)
 elif averagetype=='median':
  return statistics.median(numbers)
 elif averagetype=='min':
  return min(numbers)
 elif averagetype=='max':
  return max(numbers)
 elif averagetype=='range':
  return max(numbers)-min(numbers)
 else:
  raise RuntimeWarning('An Error Has Occured: You Entered An Invalid Operation (0003)')
def numprop(value,propertyexpected):
 if propertyexpected=='triangular':
  x=(math.sqrt(8*value+1)-1)/2
  return bool(x-int(x)>0)
 elif propertyexpected=='square':
  return math.sqrt(value).is_integer()
 elif propertyexpected=='cube':
  x=value**(1/3)
  x=int(round(x))
  return bool(x**3==value)
 elif propertyexpected=='even':
  return value%2==0
 elif propertyexpected=='odd':
  return not value%2==0
 elif propertyexpected=='positive':
  return bool(value>0)
 elif propertyexpected=='negative':
  return bool(value<0)
 elif propertyexpected=='zero':
  return bool(value==0)
def posnegtoggle(number):
 if bool(number>0):
  return number-number*2
 elif bool(number<0):
  return number+abs(number)*2
 elif bool(number==0):
  return number
def isinfinite(variable):
 return bool(math.isfinite(variable))
def isfalse(variable):
 if variable in[0,0.0,False,[],{},math.nan,""]:
  return True
 return False
def less_or_equal(number):
 try:
  return math.floor(number)
 except RuntimeError:
  raise RuntimeWarning('An Error Has Occured: Number Not Provided (0016)')
def compare(value1,value2,comparison):
 if not isinstance(comparison,str):
  raise RuntimeWarning("ERROR: comparison argument must be a string.")
 if comparison=='is':
  return value1==value2
 elif comparison=='or':
  return value1 or value2
 elif comparison=='and':
  return value1 and value2
 raise RuntimeWarning("Invalid comparison operator specified.")
def factors(number):
 factors=[]
 for i in range(1,number+1):
  if number%i==0:
   factors.append(i)
 return factors
def eulercalc(faces,edges,verticies):
 return verticies+edges-faces
def randomnum(minimum=1,maximum=2):
 if isnum(minimum):
  if isnum(maximum):
   return random.randint(minimum,maximum)
  raise RuntimeWarning("Maximum number is not a number.")
 raise RuntimeWarning('Minimum number is not a number.')
def isfib(number):
 num1=1
 num2=1
 while True:
  if num2<number:
   tempnum=num2
   num2+=num1
   num1=tempnum
  elif num2==number:
   return True
  else:
   return False
def isprime(number):
 if number==1:
  return False
 for i in range(2,int(number**0.5)+1):
  if number%i==0:
   return False
 return True
def convertbase(number,base=10):
 integer=number
 if not integer:
  return '0'
 sign=1 if integer>0 else-1
 alphanum=string.digits+string.ascii_lowercase
 nums=alphanum[:base]
 res=''
 integer*=sign
 while integer:
  integer,mod=divmod(integer,base)
  res+=nums[mod]
 return('' if sign==1 else '-')+res[::-1]
def isnum(value):
 try:
  return bool(isinstance(value,(float,int)))
 except RuntimeError:
  return False
def quadrant(xcoord,ycoord):
 xneg=bool(xcoord<0)
 yneg=bool(ycoord<0)
 if xneg is True:
  if yneg is False:
   return 2
  return 3
 if yneg is False:
  return 1
 return 4
def flipcoords(xcoord,ycoord,axis):
 axis=axis.lower()
 if axis=='y':
  if xcoord>0:
   return str(xcoord-xcoord-xcoord)+', '+str(ycoord)
  elif xcoord<0:
   return str(xcoord+abs(xcoord)*2)+', '+str(ycoord)
  elif xcoord==0:
   return str(xcoord)+', '+str(ycoord)
  raise RuntimeWarning("The X coordinate is neither larger, smaller or the same as 0.")
 elif axis=='x':
  if ycoord>0:
   return str(xcoord)+', '+str(ycoord-ycoord-ycoord)
  elif ycoord<0:
   return str(ycoord+abs(ycoord)*2)+', '+str(xcoord)
  elif ycoord==0:
   return str(xcoord)+', '+str(ycoord)
  raise RuntimeWarning("The Y coordinate is neither larger, smaller or the same as 0.")
 raise RuntimeWarning("Invalid axis. Neither x nor y was specified.")
def lcm(num1,num2):
 if num1>num2:
  bigger=num1
 else:
  bigger=num2
 while True:
  if bigger%num1==0 and bigger%num2==0:
   return bigger
  bigger+=1
def hcf(num1,num2):
 if num1>num2:
  smaller=num2
 else:
  smaller=num1
 for i in range(1,smaller+1):
  if((num1%i==0)and(num2%i==0)):
   return i
def pythrule(first,second):
 return(first*second)/2
"""
Secure
"""
def randstring(length=1):
 charstouse=string.ascii_letters+string.digits+string.punctuation
 newpass=''
 for _ in range(length):
  newpass+=str(charstouse[random.randint(0,len(charstouse)-1)])
 return newpass
def tokhex(length=10,urlsafe=False):
 if urlsafe is True:
  return secrets.token_urlsafe(length)
 return secrets.token_hex(length)
"""
String
"""
def catwalk(text):
 return ' '.join(text.split())
def converttabs(text,spaces=4):
 return text.replace('\t',' '*spaces)
def shortentext(text,minlength,placeholder='...'):
 return textwrap.shorten(text,minlength,placeholder=str(placeholder))
def wraptext(text,maxlength):
 return textwrap.wrap(text,maxlength)
def unindent(text):
 return textwrap.dedent(text)
def paraspace(paragraphspaces=1):
 for _ in range(paragraphspaces):
  print('',end='\n')
def randomstr(valuelist):
 try:
  return random.choice(valuelist)
 except IndexError:
  raise RuntimeWarning('An Error Has Occured: List Not Specified (0018)')
def case(text,casing_format='sentence'):
 if casing_format=='uppercase':
  return str(text.upper())
 elif casing_format=='lowercase':
  return str(text.lower())
 elif casing_format=='sentence':
  return str(text[0].upper())+str(text[1:])
 elif casing_format=='caterpillar':
  return str(text.lower().replace(" ","_"))
 else:
  raise RuntimeWarning("Invalid text format specified")
"""
System
"""
def getplatform():
 return sys.platform
def shellcommand(command):
 subprocess.call(str(command))
def pipupdate():
 packages=[d for d in pkg_resources.working_set]
 subprocess.call('pip install --upgrade '+' '.join(packages))
def dirtool(operation,directory):
 operation=operation.lower()
 if operation=='exists':
  return bool(os.path.exists(directory))
 if operation=='create':
  if os.path.exists(directory):
   raise RuntimeWarning('An Error Has Occured: Directory Already Exists (0007)')
  else:
   os.makedirs(directory)
 elif operation=='delete':
  if os.path.exists(directory):
   os.rmdir(directory)
  else:
   raise RuntimeWarning('An Error Has Occured: Directory Doesn\'t Exist (0009)')
 else:
  raise RuntimeWarning('An Error Has Occured: Invalid Operation Entered (0008)')
def file(operation,path):
 operation=operation.lower()
 if operation=='exists':
  return bool(os.path.isfile(path))
 if operation=='read':
  if os.path.isfile(path):
   with open(path,'r')as f:
    return[line.strip()for line in f]
  raise RuntimeWarning('An Error Has Occured: File Not Found (0012)')
 elif operation=='delete':
  if os.path.isfile(path):
   os.remove(path)
  else:
   raise RuntimeWarning('An Error Has Occured: File Not Found (0012)')
 elif operation=='create':
  if not file('exists',path):
   open(path,'w').close()
  else:
   raise RuntimeWarning('An Error Has Occured: File Already Exists (0013)')
 elif operation=='clear':
  if os.path.isfile(path):
   open(path,'w').close()
  raise RuntimeWarning('An Error Has Occured: File Not Found (0012)')
 else:
  raise RuntimeWarning('An Error Has Occured: Invalid Operation Entered (0008)')
def exitexecution(arguments=0):
 sys.exit(arguments)
def charlimit():
 return sys.maxsize
def unilimit():
 return sys.maxunicode
def pyversion(part=None):
 if part is None:
  return sys.version_info
 return sys.version_info[part]
def pyexec():
 return sys.executable
def pycopyright():
 return sys.copyright
def loglevel(leveltype=None,isequal=False):
 leveltype=leveltype.lower()
 loglevels={"none":0,"debug":10,"info":20,"warning":30,"error":40,"critical":50}
 if leveltype is None and isequal is False:
  return logging.getEffectiveLevel()
 if leveltype is not None and isequal is True:
  if leveltype in loglevels.values():
   return leveltype==logging.getEffectiveLevel()
  elif leveltype in loglevels:
   return loglevels[leveltype]==logging.getEffectiveLevel()
  raise RuntimeWarning("Incorrect input provided. It should be none, debug, info, warning, error or critical")
 if leveltype in loglevels.values():
  logging.basicConfig(level=leveltype)
 elif leveltype in loglevels:
  logging.basicConfig(level=loglevels[leveltype])
 else:
  raise RuntimeWarning("Incorrect input provided. It should be none, debug, info, warning, error or critical")
def logfile(targetfile="ros.log"):
 try:
  str(targetfile)
 except RuntimeError:
  raise RuntimeWarning("Cannot convert type "+str(type(targetfile))+"to str")
 try:
  logging.basicConfig(filename=str(targetfile))
 except RuntimeError:
  raise RuntimeWarning("Invalid target file specified")
def clipaction(action='get',text=None):
 if action=='get':
  return clipboard.paste()
 elif action=='set':
  clipboard.copy(str(text))
 elif action=='append':
  clipboard.copy(str(clipboard.paste)+str(text))
 elif action=='preceed':
  clipboard.copy(str(text)+str(clipboard.paste))
 else:
  raise RuntimeWarning("Invalid clipboard action specified.")
def text(operation,path,argument):
 operation=operation.lower()
 if operation=='write':
  if os.path.isfile(path):
   fh=open(path,'w')
   fh.write(argument)
  else:
   raise RuntimeWarning('An Error Has Occured: File Not Found (0012)')
 elif operation=='append':
  if os.path.isfile(path):
   fh=open(path,'a')
   fh.write(argument)
  else:
   raise RuntimeWarning('An Error Has Occured: File Not Found (0012)')
"""
Time
"""
def dayofweek(day,month,year,formatresult=True):
 if formatresult is False:
  return calendar.weekday(year,month,day)+1
 days={0:'Monday',1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
 return days[calendar.weekday(year,month,day)]
def leapyear(year):
 return bool(calendar.isleap(year))
def closeyear(year):
 return int(year%4)
def converttime(time,currentformat,newformat):
 currentformat=currentformat.lower()
 newformat=newformat.lower()
 if currentformat==newformat:
  return time
 if currentformat=='seconds':
  if newformat=='milliseconds':
   return time*1000
  elif newformat=='minutes':
   return time/60
  elif newformat=='hours':
   return time/60/60
  elif newformat=='days':
   return time/60/60/24
  elif newformat=='weeks':
   return time/60/60/24/7
  elif newformat=='fortnights':
   return time/60/60/24/14
  elif newformat=='years':
   return time/60/60/24/365
  elif newformat=='decades':
   return time/60/60/24/365/10
  elif newformat=='centuaries':
   return time/60/60/24/365/100
  elif newformat=='millenniums':
   return time/60/60/24/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='minutes':
  if newformat=='milliseconds':
   return time*60*1000
  elif newformat=='seconds':
   return time*60
  elif newformat=='hours':
   return time/60
  elif newformat=='days':
   return time/60/24
  elif newformat=='weeks':
   return time/60/24/7
  elif newformat=='fortnights':
   return time/60/24/14
  elif newformat=='years':
   return time/60/24/365
  elif newformat=='decades':
   return time/60/24/365/10
  elif newformat=='centuaries':
   return time/60/24/365/100
  elif newformat=='millenniums':
   return time/60/24/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='hours':
  if newformat=='milliseconds':
   return time*60*60*1000
  elif newformat=='seconds':
   return time*60*60
  elif newformat=='minutes':
   return time/60
  elif newformat=='days':
   return time/24
  elif newformat=='weeks':
   return time/24/7
  elif newformat=='fortnights':
   return time/24/14
  elif newformat=='years':
   return time/24/7/365
  elif newformat=='decades':
   return time/24/365/10
  elif newformat=='centuaries':
   return time/24/365/100
  elif newformat=='millenniums':
   return time/24/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='days':
  if newformat=='milliseconds':
   return time*24*60*60*1000
  elif newformat=='seconds':
   return time*24*60*60
  elif newformat=='minutes':
   return time*24*60
  elif newformat=='hours':
   return time*24
  elif newformat=='weeks':
   return time/24/7
  elif newformat=='fortnights':
   return time/60/24/14
  elif newformat=='years':
   return time/60/24/7/365
  elif newformat=='decades':
   return time/7/365/10
  elif newformat=='centuaries':
   return time/7/365/100
  elif newformat=='millenniums':
   return time/7/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='weeks':
  if newformat=='milliseconds':
   return time*7*24*60*60*1000
  elif newformat=='seconds':
   return time*7*24*60*60
  elif newformat=='minutes':
   return time*7*24*60
  elif newformat=='hours':
   return time*7*24
  elif newformat=='fortnights':
   return time*7/14
  elif newformat=='years':
   return time*7/365
  elif newformat=='decades':
   return time*7/365/10
  elif newformat=='centuaries':
   return time*7/365/100
  elif newformat=='millenniums':
   return time*7/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='fortnights':
  if newformat=='milliseconds':
   return time*14*24*60*60*1000
  elif newformat=='seconds':
   return time*14*24*60*60
  elif newformat=='minutes':
   return time*14*24*60
  elif newformat=='hours':
   return time*14*24
  elif newformat=='weeks':
   return time*14
  elif newformat=='years':
   return time*14/365
  elif newformat=='decades':
   return time*14/365/10
  elif newformat=='centuaries':
   return time*14/365/100
  elif newformat=='millenniums':
   return time*14/365/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='years':
  if newformat=='milliseconds':
   return time*365*24*60*60*1000
  elif newformat=='seconds':
   return time*365*24*60*60
  elif newformat=='minutes':
   return time*365*24*60
  elif newformat=='hours':
   return time*365*24
  elif newformat=='days':
   return time*365
  elif newformat=='weeks':
   return time*365/7
  elif newformat=='fortnights':
   return time*365/14
  elif newformat=='decades':
   return time/10
  elif newformat=='centuaries':
   return time/100
  elif newformat=='millenniums':
   return time/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='decades':
  if newformat=='milliseconds':
   return time*10*365*24*60*60*1000
  elif newformat=='seconds':
   return time*10*365*24*60*60
  elif newformat=='minutes':
   return time*10*365*24*60
  elif newformat=='hours':
   return time*10*365*24
  elif newformat=='days':
   return time*10*365
  elif newformat=='weeks':
   return time*10*365/7
  elif newformat=='fortnights':
   return time*10*365/14
  elif newformat=='years':
   return time*10
  elif newformat=='centuaries':
   return time*10/100
  elif newformat=='millenniums':
   return time*10/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='centuaries':
  if newformat=='milliseconds':
   return time*100*365*24*60*60*1000
  elif newformat=='seconds':
   return time*100*365*24*60*60
  elif newformat=='minutes':
   return time*100*365*24*60
  elif newformat=='hours':
   return time*100*365*24
  elif newformat=='days':
   return time*100*365
  elif newformat=='weeks':
   return time*100*365/7
  elif newformat=='fortnights':
   return time*100*365/14
  elif newformat=='years':
   return time*100
  elif newformat=='decades':
   return time*100/10
  elif newformat=='millenniums':
   return time*100/1000
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 elif currentformat=='millenniums':
  if newformat=='milliseconds':
   return time*1000*365*24*60*60*1000
  elif newformat=='seconds':
   return time*1000*365*24*60*60
  elif newformat=='minutes':
   return time*1000*365*24*60
  elif newformat=='hours':
   return time*1000*365*24
  elif newformat=='days':
   return time*1000*365
  elif newformat=='weeks':
   return time*1000*365/7
  elif newformat=='fortnights':
   return time*1000*365/14
  elif newformat=='years':
   return time*1000
  elif newformat=='decades':
   return time*1000/10
  elif newformat=='centuaries':
   return time*1000/100
  else:
   raise RuntimeWarning("Incorrect new time format specified.")
 else:
  raise RuntimeWarning("Incorrect old time format specified.")
def minyear():
 return datetime.MINYEAR
def maxyear():
 return datetime.MAXYEAR
def timezone():
 return time.timezone
def timesince():
 return time.time()
def getdatetime(timedateformat='complete'):
 timedateformat=timedateformat.lower()
 if timedateformat=='day':
  return((str(datetime.datetime.now())).split(' ')[0]).split('-')[2]
 elif timedateformat=='month':
  return((str(datetime.datetime.now())).split(' ')[0]).split('-')[1]
 elif timedateformat=='year':
  return((str(datetime.datetime.now())).split(' ')[0]).split('-')[0]
 elif timedateformat=='hour':
  return(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
 elif timedateformat=='minute':
  return(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1]
 elif timedateformat=='second':
  return(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2]
 elif timedateformat=='millisecond':
  return(str(datetime.datetime.now())).split('.')[1]
 elif timedateformat=='yearmonthday':
  return(str(datetime.datetime.now())).split(' ')[0]
 elif timedateformat=='daymonthyear':
  return((str(datetime.datetime.now())).split(' ')[0]).split('-')[2]+'-'+((str(datetime.datetime.now())).split(' ')[0]).split('-')[1]+'-'+((str(datetime.datetime.now())).split(' ')[0]).split('-')[0]
 elif timedateformat=='hourminutesecond':
  return((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]
 elif timedateformat=='secondminutehour':
  return(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2]+':'+(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1]+':'+(((str(datetime.datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
 elif timedateformat=='complete':
  return str(datetime.datetime.now())
 elif timedateformat=='datetime':
  return(str(datetime.datetime.now())).split('.')[0]
 elif timedateformat=='timedate':
  return((str(datetime.datetime.now())).split('.')[0]).split(' ')[1]+' '+((str(datetime.datetime.now())).split('.')[0]).split(' ')[0]
 else:
  raise RuntimeWarning("Invalid time date format used.")
def timeit(command,round_result=True):
 t1=time.clock()
 exec(command)
 t2=time.clock()
 if round_result is True:
  return int(t2-t1)
 return t2-t1
"""
Web
"""
def mailto(to,cc,bcc,subject,body,autorun=True):
 mailurl='mailto:'+str(to)
 if cc is None and bcc is None and subject is None and body is None:
  if autorun is True:
   webbrowser.open_new_tab(str(mailurl))
  return str(mailurl)
 mailurl+='?'
 if cc is not None:
  mailurl+='cc='+str(cc)
  added=True
 added=False
 if bcc is not None:
  if added is True:
   mailurl+='&'
  mailurl+='bcc='+str(cc)
  added=True
 if subject is not None:
  if added is True:
   mailurl+='&'
  mailurl+='subject='+str(subject)
  added=True
 if body is not None:
  if added is True:
   mailurl+='&'
  mailurl+='body='+str(body)
  added=True
 if autorun is True:
  webbrowser.open_new_tab(str(mailurl))
 else:
  return mailurl
def openurl(url):
 try:
  webbrowser.open(url)
 except webbrowser.Error:
  raise RuntimeWarning('An Error Has Occured: Unable To Open URL (0017)')
def newwindow(url):
 try:
  webbrowser.open_new(url)
 except webbrowser.Error:
  raise RuntimeWarning('An Error Has Occured: Unable To Open URL (0017)')
def newtab(url):
 try:
  webbrowser.open_new_tab(url)
 except webbrowser.Error:
  raise RuntimeWarning('An Error Has Occured: Unable To Open URL (0017)')
def getbrowser():
 try:
  webbrowser.get(using=None)
 except RuntimeError:
  return None
def filedownload(source,destination):
 if not isempty(source):
  if not isempty(destination):
   try:
    urllib.request.urlretrieve(source,destination)
   except RuntimeError:
    raise RuntimeWarning('An Error Has Occured: File Download Error (0010)')
  else:
   raise RuntimeWarning('An Error Has Occured: Source Or Destination Invalid (0011)')
 else:
  raise RuntimeWarning('An Error Has Occured: Source Or Destination Invalid (0011)')
"""
Copyright
"""
def quiltlicense(raw=False):
 if raw is False:
  print('Quilt is licensed under the Apache License 2.0')
  print(u'\u2714'+' Permissions: Commercial use, Modification, Distribution, Patent use And Private use')
  print(u'\u274c'+' Limitations: Trademark use, Liability And Warranty')
  print(u'\u2139'+' Conditions: License and copyright notice And State changes')
  print('To View, The Full license, Go To https://rosurl.ga/ROS-Code-license')
 else:
  print('Quilt Is licensed Under The Apache License 2.0')
  print('Permissions: Commercial use, Modification, Distribution, Patent use And Private use')
  print('Limitations: Trademark use, Liability And Warranty')
  print('Conditions: License and copyright notice And State changes')
  print('To View, The Full license, Go To https://rosurl.ga/ROS-Code-license')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
