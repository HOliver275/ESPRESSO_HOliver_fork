# os: https://docs.python.org/3/library/os.html
# math: https://docs.python.org/3/library/math.html#module-math
# random: https://docs.python.org/3/library/random.html
# shutil: https://docs.python.org/3/library/shutil.html
# numpy: https://numpy.readthedocs.io/en/latest/
import os, math, random, shutil, numpy

"""
Actually distributes the files.

param: files, a list of files to be distributed
param: places, the number of places where files are to be distributed
param: zipf, TODO work out what this parameter does
return: res, a list of lists of files to be distributed in each place
"""
def distribute(files,places,zipf):
   #print('In FileDistributor.distribute')
   #print('files follow: ')
   #print(files)
   #print('places: ' + str(places))
   #print('zipf: ' + str(zipf))
    # running sum
    total=0
    # if we are doing a zipf distribution
    if zipf==0:
        # get the average number of files per place and round it down to nearest int
        # and then multiply by number of places, so you have a result that is probably
        # less than the number of files to be distributed,
        # and you initialize the numbers list to that length
        numbers=[math.floor(len(files)/places)]*places
       #print('numbers = ' + str(numbers))
    else:
        # for each place where files are to be distributed, divide 1 by the array index times zipf
        # (where the denominator represents the word rank in the zipf equation)
        # such that you get a series of results with values in decreasing order
        # and you add each result to a running total
        for i in range(places):
            total +=1/((i+1)*zipf)
        # display the sum of all the denominators
        print (total)
        # reset the list of numbers to empty
        numbers=[]
        # now once again for each place where files are to be distributed,
        for i in range(places):
            # take the number of files to be distributed,
            # and divide it by each of the previous denominators times the sum of all the denominators,
            # rounded down to the nearest int
            # and append the result to the list of numbers
            numbers.append(math.floor(len(files)/(total*(i+1)*zipf)))
    # sum the list of numbers and display it
    print(sum(numbers))
    # whatever the difference is between the summed list of numbers,
    # and the actual number of files to distribute,
    # for each one,
    for i in range(len(files)-sum(numbers)):
        # get a random int that is less than the number of places
        j=math.floor(random.random()*places)
        # and get the list element at that random index, and add 1 to whatever value is at that index
        # so that there will be no orphaned files and all the files in the list will be distributed
        numbers[j]=numbers[j]+1
    
    # display the list of numbers
    print(numbers)
    # initialize another empty list
    # which will be a list of each lot of files to be distributed in each place
    res=[]
    # position ticker
    pos=0
    # now however many places there are
    for i in range(places):
        # get the next number in the list, and append a list with that many files from the initial list of all files
        # into the list of lots of files per place
        res.append(files[pos:pos+numbers[i]])
        # and move the position ticker to the next lot of files
        pos=pos+numbers[i]
    # return the list of lists of files to be distributed in each place
   #print('res follows: ')
   #print(res)
    return (res)

def distributenum(n,places,zipf):
    #a=1
    total=0
    if zipf==0:
        numbers=[math.floor(n/places)]*places
    else:
        for i in range(places):
            total +=1/((i+1)*zipf)
            #a/=((i+1)*zipf)
        print (total)
        numbers=[]
        for i in range(places):
            numbers.append(math.floor(n/(total*(i+1)*zipf)))
    print(sum(numbers))
    for i in range(n-sum(numbers)):
        j=math.floor(random.random()*places)
        numbers[j]=numbers[j]+1
    return (numbers)
    

def powerdistribute(files,places,p):
    #a=1
    total=0
    if p==0:
        numbers=[math.floor(len(files)/places)]*places
    else:
        for i in range(places):
            total +=1/((i+1)**p)
            #a/=((i+1)*zipf)
        print (total)
        numbers=[]
        for i in range(places):
            numbers.append(math.floor(len(files)/(total*((i+1)**p))))
    print(sum(numbers))
    for i in range(len(files)-sum(numbers)):
        j=math.floor(random.random()*places)
        numbers[j]=numbers[j]+1
    print(numbers)
    res=[]
    pos=0
    for i in range(places):
        res.append(files[pos:pos+numbers[i]])
        pos=pos+numbers[i]
    return (res)

def sort_local (datasource,targetdir, numberofservers, serverzipf,numberofpods,podzipf):
    shutil.rmtree(targetdir)
    os.mkdir(targetdir)
    print(directory)
    filelist=[]
    for filename in os.listdir(datasource):
        f = os.path.join(datasource, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filelist.append(filename)
    print(filelist)
    podlist=distribute(filelist,numberofpods,podzipf)
    random.shuffle(podlist)
    final=distribute(podlist,numberofservers,serverzipf)
    j=0
    for s in range(len(final)):
        servername = 'server'+str(s)
        serverpath = os.path.join(targetdir, servername)
        os.mkdir(serverpath)
        for p in range(len(final[s])):
            podname = servername+'pod'+str(p)
            podpath = os.path.join(serverpath, podname)
            os.mkdir(podpath)
            for f in final[s][p]:
                src = os.path.join(datasource,f)
                dst = os.path.join(podpath,f)
                j=j+1
                print(j)
                shutil.copy(src, dst)
        print("end server")

"""
Normally distributes files.

param: files, a list of files to distribute. Example value: [(rdflib.term.BNode('Ppod10'), ..., rdflib.term.BNode('Ppod29'))]
param: places, the number of places to distribute the files to. Example value: 1
param: disp, the standard deviation. Example value: 0
return: res, a list of lists of files to distribute in each place. Example value: [[(rdflib.term.BNode('Ppod10'), ..., rdflib.term.BNode('Ppod29'))]]
"""
def normaldistribute(files,places,disp):
    #print('Inside normaldistribute.')
    #print('input: files:')
    #print(files)
    #print('input: places: ' + str(places))
    #print('input: disp: ' + str(disp))
    # if the standard deviation is 0,
    # multiply the number of files per place (rounded down) by the number of places to get (a number less than or equal to) the length of the numbers list
    if disp==0:
        numbers=[math.floor(len(files)/places)]*places
    else: # if the standard deviation is not 0
        # get a float representing the mean files to distribute per place
        loc=float(len(files))/places
        # multiply the mean by the standard deviation
        scale=loc*disp
        # draw random samples from the normal distribution
        ran=numpy.random.normal(loc,scale,places)
        # running sum
        total=0
        # for each place where files are to be distributed
        for i in range(places):
            # switch negative numbers to positive 1 [TODO ?]
            if ran[i]<0:
                ran[i]=1
            # add to the running sum
            total += ran[i]
        
        # display the running sum
        print (total)
        # initialize an empty number list
        numbers=[]
        # for each place where files are to be distributed
        for i in range(places):
            # multiply the mean number of files per place by that place's
            # random number
            numbers.append(math.floor(ran[i]*len(files)/total))
    # on first pass this would just be the number of files?
    print(sum(numbers))
    # and for each block of files to distribute
    for i in range(len(files)-sum(numbers)):
        # you get a random float between 0 and 1.0, times the number of places (rounded down)
        j=math.floor(random.random()*places)
        # and this makes the distribution normal
        numbers[j]=numbers[j]+1
    # display the list of numbers
    print(numbers)
    # initialize a new empty list
    res=[]
    # place tracker
    pos=0
    # for every place
    for i in range(places):
        # append to a list the slice of files allocated for that place
        res.append(files[pos:pos+numbers[i]])
        # and move the position along
        pos=pos+numbers[i]
    # return the list of allocated files
    #print('res follows: ')
    #print(res)
    return (res)
    
"""
Pareto

param: files, the list of files to distribute
param: places, the number of places to which files are to be distributed
param: alpha, the shape parameter for the Pareto distribution
return: res, a list of files sampled from the input file list
"""
def paretopluck(files,places,alpha):
    # initialize an empty list
    res=[]
    # for each place to which files are to be distributed
    for i in range(places):
        # get the Pareto distribution, rounded down to the nearest int
        i=math.floor(random.paretovariate(alpha))
        # make sure the Pareto distribution is not greater than the number
        # of files to distribute
        if i>len(files):
            i=len(files)
        # append a random selection of that many files from the file list into the new list
        res.append(random.sample(files, i))
    # return the list of lists of newly sampled files - one list per place
    return(res)