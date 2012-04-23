## k-means clustering of user-features ##
#this file reads in from 'User Features Orange.tab' and contains
#methods to deal with clusters

import Orange
import cPickle as pickle
import matplotlib.pyplot as plt
import math

### The Cluster class makes it easy to retrieve and store  ###
### clusters made by the different cluserting algorithms   ###


#class variables:
# 1. noClusters: counters no. of clustered stored in class
# 2. clusterDict: A dictionary of the type (clusterName,k)->cluster
# 3. scoreDict: A dictionary of the type clusterName->[list1,list2]
#    where list1: List of no. of centroids and List2: corresponding
#    scores

class Cluster(object):
    def __init__(self):
#initializes to all empty variables
        self.noClusters=0
        self.clusterDict={}
        self.scoreDict={}

#adds a cluster with the given arguments into both clusterDict and
#clusterScore
    def add_cluster(self,cluster,clusterName,k,score):
        if ((clusterName,k) in self.clusterDict):
            print clusterName,' cluster already exists with',str(k),' centroids\n'
        else:
            self.clusterDict[(clusterName,k)]=cluster
            if clusterName in self.scoreDict:
                self.scoreDict[clusterName][0].append(k)
                self.scoreDict[clusterName][1].append(score)
            else:self.scoreDict[clusterName]=[[k],[score]]
            self.noClusters+=1

#returns to clusterDict
    def all_clusters(self):
        return self.clusterDict

#returns the scoreDict
    def all_scores(self):
        return self.scoreDict

#returns the cluster for a specific clusterName and k(no. of centroids)
    def give_cluster(self,clusterName,k):
        if (clusterName,k) in self.clusterDict:
            return self.clusterDict[(clusterName,k)]
        else: print clusterName, " Hasn't been implemented for ",k," centroids\n"

#returns the lists of no. of centroids and correspoding scores for a
#specific clusterName
    def cluster_score(self,clusterName):
        if clusterName in self.scoreDict:
            return self.scoreDict[clusterName][0],self.scoreDict[clusterName][1]
        else: print clusterName, " Hasn't been implemented"

#returns all stored clusterNames
    def cluster_names(self):
        return scoreDict.keys()


#load usernames
with open('User Features.p','r') as featureFile:
    users=pickle.load(featureFile)

### kmeans ###

#create new cluster object
c=Cluster()

#load data into orange
data=Orange.data.Table('User Features Orange')

print "#### Running K-MEANS WITH DIVERSITY INITIALIZATION ####"

clusterName='kmeans_div'
#no. of centroids varies from 2 to half the no. of users
for k in range(2,int(len(users)/2)):
    km_diversity = Orange.clustering.kmeans.Clustering(data, centroids = k,
            initialization=Orange.clustering.kmeans.init_diversity)
    cluster=km_diversity.clusters
    score = Orange.clustering.kmeans.score_silhouette(km_diversity)
    c.add_cluster(cluster,clusterName,k,score)
print c.cluster_score(clusterName)
##print 'DIVERSITY INITIALIZATION ',c.give_cluster('kmeans_div',3)
plt.figure(1)
plt.plot(c.cluster_score(clusterName)[0],c.cluster_score(clusterName)[1])
plt.xlabel('No. of Clusters')
plt.ylabel('Silhouette Coefficient')
plt.title('K-MEANS WITH DIVERSITY INITIALIZATION')
plt.figure(2)

print "#### Running K-MEANS WITH HIERACHICAL INITIALIZATION ####"

#no. data points to user starts from half the users to all with steps of 3

for p in range(int(len(users)/2),len(users)+1,3):
    clusterName='kmeans_h_'+str(p)
    for k in range(2,int(len(users)/2)):
        km_diversity = Orange.clustering.kmeans.Clustering(data, centroids = k,
                initialization=Orange.clustering.kmeans.init_hclustering(n=8))
        cluster=km_diversity.clusters
        score = Orange.clustering.kmeans.score_silhouette(km_diversity)
        c.add_cluster(cluster,clusterName,k,score)
    print p,'Initializers:',c.cluster_score(clusterName)
    plt.plot(c.cluster_score(clusterName)[0],c.cluster_score(clusterName)[1])
    plt.text(c.cluster_score(clusterName)[0][1],c.cluster_score(clusterName)[1][1],'Initializers= '+str(p))
plt.xlabel('No. of Clusters')
plt.ylabel('Silhouette Coefficient')
plt.title('K-MEANS WITH HIERACHICAL INITIALIZATION')
##print 'HIERACHICAL INITIALIZATION\n'
##for p in range(int(len(users)/2),len(users)+1,3):
##    print p,'Initializers:',c.give_cluster('kmeans_h_'+str(p),3)



### Hiearchichal Clustering ###
print '#### Running HIEARCHICHAL CLUSTERING ####'
clusterName='h_clustering'
root = Orange.clustering.hierarchical.clustering(data,
    distance_constructor=Orange.distance.Euclidean,
    linkage=Orange.clustering.hierarchical.AVERAGE)

for k in range(2,int(len(users)/2)):
    cluster=Orange.clustering.hierarchical.top_cluster_membership(root, k)
    centers=[[0.]*len(data[0])]*k
    membership=[0]*k
#computing cluster centers
    for i in range(len(cluster)):
        membership[cluster[i]]+=1
        for j in range(len(data[i])):
            centers[cluster[i]][j]+=data[i][j]
    for i in range(k):
        for j in range(len(data[0])):
            centers[i][j]=centers[i][j]/membership[i]
#computing the rmse
    total_dist=0.0
    for i in range(len(cluster)):
        dist=0.0
        for j in range(len(data[i])):
            dist+=math.pow(data[i][j]-centers[cluster[i]][j],2)
        dist=math.sqrt(dist)
        total_dist+=dist
    avg_dist=total_dist/len(cluster)
    c.add_cluster(cluster,clusterName,k,avg_dist)
##print 'HIEARCHICHAL INITIALIZATION ',c.give_cluster(clusterName,3)
print c.cluster_score(clusterName)
print 
plt.figure(3)
plt.plot(c.cluster_score(clusterName)[0],c.cluster_score(clusterName)[1])
plt.xlabel('No. of Clusters')
plt.ylabel('RMSE')
plt.title('HIEARCHICHAL CLUSTERING')
plt.show()


