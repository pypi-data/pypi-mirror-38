import math
import unicodedata
import codecs
import glob
import os
from tqdm import tqdm

from altk.filemanager import FileManager

class Aggregator(object):
    '''[summary]
    The Aggregator handles the aggregation process that happens to all Ancient Lives data.
    '''
    _file_manager = None

    _version = 1
    _verbose = False

    # agglomeration threshold = pixel distance when you include the point in an exisitng seed
    _athreshold = 9
    _athreshold2 = _athreshold*_athreshold
    _lenThreshold = 5
    _userThreshold = 3 # minimum number of users to be viable
    _mergerDistance = 13

    # Initializer / Instance Attributes
    def __init__(   self, 
                    filename='markers.txt',
                    click_dir='clicks', 
                    consensus_dir='consensus', 
                    distanceThreshold=9,
                    lengthThreshold=5,
                    userThreshold=3,
                    mergerDistance=13,
                    version=1,
                    verbose=False):
        self._version = version
        self._verbose = verbose
        self._athreshold = distanceThreshold
        self._lenThreshold = lengthThreshold
        self._userThreshold = userThreshold
        self._mergerDistance = mergerDistance

        # instantiate a file manager
        self._file_manager = FileManager(filename=filename, click_dir=click_dir, consensus_dir=consensus_dir, verbose=verbose)


    def _aggregate(self):

        # retrieve the list of click data files
        flist = self._file_manager.getClickFileList()

        self._file_manager.pprint(': Aggregating Click Data :')
        for ii in tqdm(range(2,len(flist))):
            f1 = flist[ii]
            v = f1.split("/")
            nn = v[1]
            froot = nn.split(".")[0]
            #print "processing file ",ii, " name = ",froot
            r = self.processFile(froot)

    def run(self):
        # 1. create click files with the file manager
        self._file_manager.createClickFiles()

        # 2. perform the aggregation procedure
        self._aggregate()
    

    def createUserList(self,x,uid):
        # make a sublist of the cilcks for each of the users and the associated number of counts
        uset = list(set(uid))
        ucount = len(uset)

        userClickList= []
        userClickCount = []
        if(ucount > 100):
            return(userClickList, userClickCount, 0)

        for i in range(ucount):
            ut = uset[i]
            hh = []
            for idx,j in enumerate(range(len(uid))):
                uc = uid[j]
                if ut == uc:
                    hh.append(j)
            userClickList.append(hh)
            userClickCount.append(len(hh))
        return(userClickList, userClickCount, ucount)


    def createSeeds(self,x,y,c,olist,userClickList):
        # set up the seed points using the elements in the first list
        seeds = []
        i = 0
        listSection = olist[i][1]  # this is confusing, but it takes the list id of the longest list
        pointList = userClickList[listSection]
        for j in range(len(pointList)):
            k = pointList[j]
            xx = x[k]
            yy = y[k]
            cc = c[k]
            seeds.append( [xx,yy, [[xx,yy]], [cc]])
        return [seeds,pointList]


    def aggregateSeeds(self,x,y,c,olist,seeds,userClickList,pointList):
        # go through the rest of the lists
        #for i in range(1,2):
        for i in range(1, len(olist)):
            listSection = olist[i][1]  # index of the list we are examining
            lenSection= olist[i][0]

            if lenSection >= self._lenThreshold:
                pointList = userClickList[listSection]
                for j in range(len(pointList)):
                    k = pointList[j]
                    xx = x[k]
                    yy = y[k]
                    cc = c[k]
                    dmin = 10000000
                    imin = -1

                    for m in range(len(seeds)):
                        xt = seeds[m][0]
                        yt = seeds[m][1]
                        dx = xx-xt
                        dy = yy-yt
                        d2 = dx*dx + dy*dy
                        if d2 < dmin:
                            imin = m
                            dmin = d2
                    if (dmin < self._athreshold2):
                        seeds[imin][2].append([xx,yy])
                        seeds[imin][3].append(cc)
                        plist = seeds[imin][2]
                        xc = 0
                        yc = 0
                        for p in range(len(plist)):
                            xc = xc + plist[p][0]
                            yc = yc + plist[p][1]
                        xc = float(xc) / len(plist)
                        yc = float(yc) / len(plist)
                        seeds[imin][0] = xc
                        seeds[imin][1] = yc
                    else:
                        seeds.append( [xx,yy, [[xx,yy]], [cc]])
        return seeds


    def formConsensus(self,seeds):
        # eliminate the elements below the minimum number of user
        consensusList = []
        for i in range(len(seeds)):
            nn = len(seeds[i][2])
            if nn >= self._userThreshold:
                consensusList.append(seeds[i])
        return consensusList


    def dumpConsensus(self,fnameOut, consensusList):
        if fnameOut != "":
            ff = open(fnameOut,"w")
            for i in range(len(consensusList)):
                xx = consensusList[i][0]
                yy = consensusList[i][1]
                nn = len(consensusList[i][2])
                a = str(xx) + ", " + str(yy)+ ", " + str(nn)
                ff.write(a+"\n")
            ff.close()

    def mergeConsensus(self,consensusList, mergerDistance):
        # create a final list to merger close by locations
        mergerList = []
        for c in consensusList:
            mergerList.append([0, c[0], c[1], c[2], c[3]])

        # find pairs of cells to merger together
        mergerPairs = []
        for i in range(len(mergerList)-1):
            xc = mergerList[i][1]
            yc = mergerList[i][2]
            
            dmin = 10000000
            imin = -1
            for j in range(i+1, len(mergerList)):
                xt = mergerList[j][1]
                yt = mergerList[j][2]            
                dx = xc-xt
                dy = yc-yt
                d2 = dx*dx + dy*dy
                if (d2 < dmin):
                    imin = j
                    dmin = d2
            if dmin < mergerDistance * mergerDistance:
                mergerPairs.append([i, imin])

        return [mergerPairs, mergerList]



    def mergePairs(self,mergerPairs,mergerList):
        for m in mergerPairs:
            istart = m[0]
            iend = m[1]
            m1 = mergerList[istart]
            m2 = mergerList[iend]
            
            mergerList[iend][3] = list(m2[3]) + list(m1[3])
            mergerList[iend][4] = list(m2[4]) + list(m2[4])
            mergerList[istart][0] = -1
            
            plist = mergerList[iend][3]
            xc = 0
            yc = 0
            for p in range(len(plist)):
                xc = xc + plist[p][0]
                yc = yc + plist[p][1]
            xc = float(xc) / len(plist)
            yc = float(yc) / len(plist)
            mergerList[iend][1] = xc
            mergerList[iend][2] = yc


        finalList = []
        for m in mergerList:
            if m[0] != -1:
                finalList.append(m[1:5])


        return finalList



    def processFile(self, froot):

        [uid,x,y,c] = self._file_manager.readClickFile(froot)
        [userClickList, userClickCount, ucount] = self.createUserList(x,uid)
        if ucount < self._userThreshold:
            return

        # do a sort on the sizes of users
        ilist = list(i for i in range(ucount))
        tlist = zip(userClickCount, ilist)
        olist = sorted(tlist,reverse=True)

        [seeds,pointList] = self.createSeeds(x,y,c,olist,userClickList)
        seeds = self.aggregateSeeds(x,y,c,olist,seeds,userClickList,pointList)
        consensusList = self.formConsensus(seeds)

        # merger close pairs together to trim the consensus list
        [mergerPairs, mergerList] = self.mergeConsensus(consensusList, self._mergerDistance)
        finalList = self.mergePairs(mergerPairs,mergerList)
        finalList = sorted(finalList)

        # dump the preliminary and final consensus results
        #jj = self.dumpConsensus(fsimple, consensusList)
        #jj = self.dumpConsensus(ffinal, finalList)
        jj = self._file_manager.writeConsensusFile(froot, finalList)

