import os
import cPickle as pickle
#scroll down to 'putting it all together' for main code
#make sure 'log_dir' is set to the log directory
#this file parses log files and converts them into user feature
#vectors which it dumps into a pickle file called 'User Features.p'

#####################################################################


### LineParser parses a line of a file that has to be passed in   ###
### It returns a parameter vector as follows                      ###

#  Collect Parameters: TimeStamp, UserId, Password, Url, TimeSpent, #
#  Clicks, CopyTextBinary, CopyText, SelectTextBinary, SelectText,  #
#  Scroll, Input, PageSave, Bookmark, Feedback. 15 in total.        #

class LineParser(object):
    def __init__(self,userName):
#at initialization parameters are set to be empty list
        self.parameters=[]
        self.userName=userName
    def parse_line(self,f1):
        self.parameters=[]
        line1=f1.readline()
        cursor=f1.tell()
#To make sure end of file is not reached
        if(line1!=''):
#collecting the entire set of raw parameters into one string 'line'
            if(line1.count(self.userName)==1):
                line=line1
            line1=f1.readline()
            while((line1.count(self.userName)==0) & (len(line1)>0)):
                line+=line1
                cursor=f1.tell()
                line1=f1.readline()
            f1.seek(cursor)
#collecting TimeStamp
            counter=line.find(',')
            TimeStamp=line[:counter]
            line=line[counter+1:]
#collecting UserId
            counter=line.find(',')
            UserId=line[:counter]
            line=line[counter+1:]
#collecting Password
            counter=line.find(',')
            Password=line[:counter]
            line=line[counter+1:]
#collecting Url
            counter=line.find(',')
            Url=line[:counter]
            line=line[counter+1:]
#collecting TimeSpent
            counter=line.find(',')
            TimeSpent=line[:counter]
            line=line[counter+1:]
#collecting Clicks
            counter=line.find(',')
            Clicks=line[:counter]
            line=line[counter+1:]
#collecting CopyTextBinary
            counter=line.find(',')
            CopyTextBinary=line[:counter]
            line=line[counter+1:]
#            if (TimeStamp=='2012.19.04.03.10.55'):
#                print 'lint is: ', line
#collecting Copy Text. The checks are to avoid commas within the copied text
            counter=line.find(',0,')
            counter2=line.find(',1,')
##            if (TimeStamp=='2012.19.04.03.10.55'):
##                print 'counter is: ', counter, ' and counter2 is: ', counter2
            if (counter<0):
                counter=counter2
            elif ((counter2>=0) and (counter2<counter)):
                counter=counter2
            CopyText=line[:counter]
            line=line[counter+1:]
#collecting SelectTextBinary
            counter=line.find(',')
            SelectTextBinary=line[:counter]
            line=line[counter+1:]
#collecting Feedback. Notice the direction of collection has reversed to avoid
#commas within selected text
            counter=line.rfind(',')
            Feedback=line[counter+1:]
            if(Feedback=='null\n'):
                Feedback='0'
            elif(Feedback=='0\n'):
                Feedback='-1'
            elif(Feedback=='1\n'):
                Feedback='1'                
            line=line[:counter]
#collecting Bookmark
            counter=line.rfind(',')
            Bookmark=line[counter+1:]
            line=line[:counter]
#collecting PageSave
            counter=line.rfind(',')
            PageSave=line[counter+1:]
            line=line[:counter]
#collecting Input
            counter=line.rfind(',')
            Input=line[counter+1:]
            line=line[:counter]
#collecting Scroll
            counter=line.rfind(',')
            Scroll=line[counter+1:]
            if (Scroll=='NaN'):
                Scroll='0'
            line=line[:counter]
#collecting SelectText
            SelectText=line
##            print TimeStamp
##            if (SelectTextBinary==''):
##                print "\nIt's SelectTextBinary!\n"
##                print 'CopyText is: ', CopyText
                
#Setting parameters
            self.parameters=[TimeStamp, UserId, Password, Url, int(TimeSpent), int(Clicks),
            int(CopyTextBinary), CopyText, int(SelectTextBinary), SelectText, int(Scroll), int(Input),
            int(PageSave), int(Bookmark), int(Feedback)]
        return self.parameters

### UserParser uses LineParser to parse through an entire user log file and ###
### return a feature vector for the user. The feature vector is defined as  ###

# featureVectorNames=['TotalUrls','TotalTime','AvgTimePerUrl','AvgClicksPerUrl', #
#                          'AvgCopyPerUrl','AvgSelectsperUrl','AvgScrollPerUrl',   #
#                          'AvgInputPerUrl','TotalPageSaves','TotalBookmarks',     #
#                          'PositiveFeedbackPerUrl','NegativeFeedbackPerUrl']      #


class UserParser(object):
    def __init__(self,log_dir):
        self.log_dir=log_dir
        self.featureVector=[]

    def get_log_dir(self):
        return self.log_dir

    def parse_user(self,userName):
        TotalUrls=0
        TotalTime=0
        TotalClicks=0
        TotalCopy=0
        TotalSelect=0
        TotalScroll=0
        TotalInput=0
        TotalPagesaves=0
        TotalBookmarks=0
        TotalPositiveFeedback=0;
        TotalNegativeFeedback=0;
        lp=LineParser(userName)
        with open(self.log_dir+'/'+userName+'.log','rb') as f1:
            parameters=lp.parse_line(f1)
            
# parameters looks like: #
# [TimeStamp, UserId, Password, Url, int(TimeSpent), int(Clicks),   #
# int(CopyTextBinary), CopyText, int(SelectTextBinary), SelectText, #
# int(Scroll), int(Input), int(PageSave), int(Bookmark),            #
# int(Feedback)]                                                    #

            while(len(parameters)!=0):
#Collecting values for feature vector
                TotalUrls+=1
                TotalTime+=parameters[4]
                TotalClicks+=parameters[5]
                TotalCopy+=parameters[6]
                TotalSelect+=parameters[8]
                TotalScroll+=parameters[10]
                TotalInput+=parameters[11]
                TotalPagesaves+=parameters[12]
                TotalBookmarks+=parameters[13]
                if(parameters[14]==1):
                    TotalPositiveFeedback+=1;
                elif(parameters[14]==-1):
                    TotalNegativeFeedback+=1;
                parameters=lp.parse_line(f1)
#Generating featureVector
        featureVector=[TotalUrls, TotalTime , float(TotalTime)/TotalUrls , float(TotalClicks)/TotalUrls ,
            float(TotalCopy)/TotalUrls , float(TotalSelect)/TotalUrls , float(TotalScroll)/TotalUrls ,
            float(TotalInput)/TotalUrls , float(TotalPagesaves)/TotalUrls , float(TotalBookmarks)/TotalUrls ,
            float(TotalPositiveFeedback)/TotalUrls , float(TotalNegativeFeedback)/TotalUrls]
        return featureVector

### user_name_parser is a function that parses the log_dir  ###
### for .log files and stores all such file names in a ,txt ###
### called 'User Name List'                                 ###

def user_name_parser(log_dir):
    dirList=os.listdir(log_dir)
    with open('User Name List.txt','w') as user_file:
        for f in dirList:
            file_name,ext= os.path.splitext(f)
            if(ext=='.log'):
                user_file.write(file_name+'\n')

### putting it all together ###
                
#parsing for user names
log_dir='D:/ACADS/CSE 6240/Project/Backend Stuff/Log files'
user_name_parser(log_dir)
#reading user name file into a list of users
users=[]
with open('User Name List.txt','r') as userFile: 
    userName=userFile.readline()
    while(userName!=''):
        userName=userName.split('\n')[0]
        users.append(userName)
        userName=userFile.readline()
featureVectorNames=['TotalUrls','TotalTime','AvgTimePerUrl','AvgClicksPerUrl', 
                          'AvgCopyPerUrl','AvgSelectsperUrl','AvgScrollPerUrl',   
                          'AvgInputPerUrl','TotalPageSaves','TotalBookmarks',     
                          'PositiveFeedbackPerUrl','NegativeFeedbackPerUrl']
#parsing each user log
up=UserParser(log_dir)
with open('User Features.p','w') as featureFile:
    pickle.dump(users,featureFile)
    pickle.dump(featureVectorNames,featureFile)
    for userName in users:
        featureVector=up.parse_user(userName)
        pickle.dump(featureVector,featureFile)

### The parser dumps the following into a pickle file: ###
### 1. A list of user names                            ### 
### 2. A list of feature names                         ###
### 3. Lists of feature vectors for all users          ###


            
            
    




























    
        
        
    
