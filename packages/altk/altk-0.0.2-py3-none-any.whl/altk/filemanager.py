import math
import unicodedata
import codecs
import glob
import os
import operator
import datetime
from tqdm import tqdm


class FileManager(object):
    '''[summary]
    The FileManager object manages the read / write operations on the filesystem.
    '''

    # I/O directories
    _click_dir = 'clicks/'
    _consensus_dir = 'consensus/'
    _filename = ''
    _verbose = False

    # Initializer / Instance Attributes
    def __init__(self, filename, click_dir='clicks', consensus_dir='consensus', verbose=False):
        self._click_dir = click_dir + '/'
        self._consensus_dir = consensus_dir + '/'
        self._filename = filename
        self._verbose = verbose

        # create directories if needed
        if not os.path.exists(click_dir):
            os.makedirs(click_dir)
        if not os.path.exists(consensus_dir):
            os.makedirs(consensus_dir)

    def pprint(self, msg):
        '''Enhanced printing for ALTK.
        
        Arguments:
            msg {String} -- the message to be printed
        '''

        print('\n[altk]\t' + msg + '\t('+  datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + ')')


    # # # (1) Click Data Files
    def createClickFiles(self):
        '''A managing function that creates a text file for each image's click data.
        '''
        self.pprint(": Reading File :")
        # read in the click data and identify shifts in image reference.
        fragList, allClicks = self.readAnnotationFile(self._filename)
        fragments = self.findBreaks(allClicks)

        self.dumpStatistics(allClicks, fragments)

        self.pprint(": Writing Click Files :")
        for i in tqdm(range(len(fragments)-1)):
            f1 = fragments[i]
            f2 = fragments[i+1]
            self.writeClickFile(allClicks, int(f1[0]), f1[1], f2[1])


    def readAnnotationFile(self, filename):
        '''Reads the file containing annotation labels and their coordinates.
        
        Arguments:
            filename {String} -- the path of the filename to be opened
        
        Returns:
            fragList [List] -- a sorted list of image names
            clickData [List] -- a list of tuples that includes click data information, sorted by image name
        '''

        fragList = []
        clickData = []
        fall = []

        f = codecs.open(filename, encoding="utf-8", mode="r");
        for idx,l in tqdm(enumerate(f)):
            if idx == 0:
                continue
            v =  l.strip().split(",")

            if v[4] == '\\N' or v[5] == '\\N':
                continue

            fall.append(int(v[2]))
            clickData.append([int(v[1]), int(v[2]), int(v[4]), int(v[5]), v[6], v[3], v[9]])
        f.close()

        # sort the clicks by the image name
        clickData.sort(key=operator.itemgetter(1))
        fragList = sorted(list((set(fall))))

        return fragList, clickData

    @classmethod
    def findBreaks(self, clickData):
        '''Returns a list that identifies a change in image reference by row.
        
        Arguments:
            clickData {List} -- the pool of click data.
        
        Returns:
            breaks [List] -- a list of indices where changes in image reference occur
        '''

        fragment = []
        ff = clickData[0]
        fragment.append([ff[1],0])
        currentFragment = ff[1]
        for ii in range(len(clickData)):
            a = clickData[ii]
            if currentFragment != a[1]:
                fragment.append([a[1],ii])
                currentFragment = a[1]

        fragment.append([-1, len(clickData)])
        return fragment


    @classmethod
    def writeClickFile(self, clickData, imageIdentifier, iStart, iEnd):
        '''Writes click data for each data to file.
        
        Arguments:
            clickData {List} -- the pool of click data read from file.
            imageIdentifier {String} -- the identifier of the image.
            iStart {Number} -- the index of the click data to begin the reading procedure.
            iEnd {Number} -- the index of hte click data to end the reading procedure.
        '''

        filename = self._click_dir+"clicks_" + str(imageIdentifier) + ".txt"
        clicks = []
        for ic in range(iStart, iEnd):
            c = clickData[ic]
            clicks.append(c)

        f = codecs.open(filename, encoding="utf-8", mode="w");
        for c in clicks:
            f.write(str(c[0]) + "," + str(c[2]) + "," +str(c[3]) + "," + c[4] + "," + c[6] + "\n")
        f.close()


    @classmethod
    def calculateStatistics(self, allClicks, target, istart, iend):
        '''Calculates simple descriptive statistics about user contributions for each image.
        
        Arguments:
            allClicks {[type]} -- [description]
            target {[type]} -- [description]
            istart {bool} -- [description]
            iend {[type]} -- [description]
        
        Returns:
            [List] -- a List of Lists containing users and their clicks.
        '''


        clicks = []
        for ic in range(istart, iend):
            c = allClicks[ic]
            clicks.append(c)

        users = []
        for c in clicks:
            users.append(c[0])
        users = list(set(users))

        userClicks = []
        for u in users:
            clickCount = 0
            for c in clicks:
                if c[0] == u:
                    clickCount = clickCount + 1
                    session_id = int(c[5])
            userClicks.append([u, clickCount, session_id])

        userClicks.sort(key=operator.itemgetter(1), reverse=True)
        return [users, clicks, userClicks]

    @classmethod
    def dumpStatistics(self, allClicks, fragments):
        '''Writes calculated statistical information to file.
        
        Arguments:
            allClicks {[type]} -- the pool of click data read from file.
            fragments {[type]} -- [description]
        '''

        ff = open("statistics.txt", "w")
        for i in range(2, len(fragments)-1):
            f1 = fragments[i]
            f2 = fragments[i+1]
            users, clicks, userClicks = self.calculateStatistics(allClicks,  int(f1[0]), f1[1], f2[1])

            s = str(f1[1]) + "," + str(len(users)) + "," + str(len(clicks)) 
            for i in range(min(25, len(userClicks))):
                s = s + "," + str(userClicks[i][0]) + "," + str(userClicks[i][1]) + "," + str(userClicks[i][2])
            ff.write(s+ "\n")
        ff.close()


    # # # (2) Consensus Data Files

    def getClickFileList(self):
        '''Returns a list of click data files that have been created.
        
        Returns:
            List -- a list of filenames that hold click data for each file.
        '''

        return glob.glob(os.path.join( self._click_dir ,"*.txt"))

    def readClickFile(self,fname):

        fname = self._click_dir + fname +'.txt'

        # read the data into the arrays
        f = codecs.open(fname,encoding='utf-8',mode='r')
        uid = []
        x= []
        y = []
        c = []
        for l in f:
            v = l.strip().split(",")
            uid.append(int(v[0]))
            x.append(float(v[1]))
            y.append(float(v[2]))
            c.append(v[3])
        f.close()
        return(uid,x,y,c)

    def writeConsensusFile(self,outname, finalList):
        fname = self._consensus_dir +'consensus_' + outname + ".txt"
        ff = open(fname, 'wb')
        h = b"label\t x\t y\t consensus\t num clicks\t % conf \n"
        
        ff.write(h)
        nn = 1
        for f in finalList:

            # format the postional information for the character
            x = f[0]
            y = f[1]
            xchar = str(int(x * 10) / 10.0)
            ychar = str(int(y * 10) / 10.0)
            s = str(nn) + "\t"  + xchar + "\t" + ychar

            # find the unicode character that is the best fit and the others that were choosen
            characters = f[3]
            clabels = set(characters)
            d = dict.fromkeys(clabels,0)
            for c in characters:
                d[c] = d[c] + 1
                # convert from a dictionary back to a set of tuples
                dl = [(v,k) for k,v in d.items()]
                dls = sorted(dl,reverse=True)
                d0 = dls[0]

            # add the best choose consensus to the output string
            s = s + "\t" + d0[1] + "\t"


            # create the output string
            ss = ""
            for cc in dls:
                n = cc[0]
                c = cc[1]
                ss = ss + c + "("+str(n)+ ")"
            s = s + ss

            # add the number of clicks there were
            s = s + "\t" + str(len(characters)) + "\t" 

            # calculate and add the fraction of users with this top choice
            f = float(d0[0])   /float(len(characters))
            s = s + str(f)

            s = s+ "\n"
            ff.write(s.encode('utf-8'))
            nn = nn + 1


        ff.close()