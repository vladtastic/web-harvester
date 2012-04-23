import cPickle as pickle

#this file reads the pickled file 'User Features.p' produced by
#parser.py and converts it to 'User Features Orange.tab'
#for easy reading into orange. Be careful about feature vector
#formatting stored as the first line in the pickle file

### write data out as an orange readable file ###

with open('User Features.p','r') as featureFile:
    with open('User Features Orange.tab','w') as featureFileO:
        users=pickle.load(featureFile)
        featureVectorNames=pickle.load(featureFile)
        for feature in featureVectorNames:
            featureFileO.write(feature+'\t')
        featureFileO.write('\n')
        for feature in featureVectorNames:
            featureFileO.write('c'+'\t')
        featureFileO.write('\n')
        for feature in featureVectorNames:
            featureFileO.write('\t')
        featureFileO.write('\n')
        for user in users:
            featureVector=pickle.load(featureFile)
            for feature in featureVector:
                featureFileO.write(str(feature)+'\t')
            featureFileO.write('\n')

        
        
