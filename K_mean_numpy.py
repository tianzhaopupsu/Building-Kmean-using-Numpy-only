############We assume that we have multi-dimensional data in the file.
### The code needs two input: data is the input data, toler is the tolerance of the converging point
import numpy as np
import matplotlib.pyplot as plt
class Kmean:


  def __init__(self,data,toler,k):
    self.data=data
    self.toler=toler
    self.k=k
    return


  def K_cal(self):
######find max and min for each dimension in data for next initialization purpose
    max_min=np.empty((self.data.shape[1],2))
    for di in range(self.data.shape[1]):
      max_min[di,0]=np.min(self.data[:,di])
      max_min[di,1]=np.max(self.data[:,di])
    elbow=np.empty((self.k-1,2))
    for i in range(2,self.k+1):
      centroid=np.empty((i,self.data.shape[1]))
      for ri in range(i):
        for ci in range(self.data.shape[1]):
          centroid[ri,ci]=max_min[ci,0]+(max_min[ci,1]-max_min[ci,0])*(ri+1)/i
      m,n=centroid.shape
      newcent=centroid*100
      dif=np.mean(np.abs(newcent-centroid))


######converging section, algorithm tries to find the best centroids
      while dif>self.toler:
        dis_recorder=np.empty((self.data.shape[0],2))
        for ii in range(self.data.shape[0]):
            dis_recorder[ii,:]=self.min_dis(centroid,self.data[ii,:])
        for j in range(i):
          points = self.data[dis_recorder[:,0] == j]
          newcent[j,0]=np.mean(points[:,0])
          newcent[j,1]=np.mean(points[:,1])
        dif=np.mean(np.abs(newcent-centroid))
        centroid=newcent
      evalu=0
      for jj in range(i):
        xcol=self.data[dis_recorder[:,0] == jj]
        ycol=self.data[dis_recorder[:,1] == jj]
        if xcol.shape[0]>0:
          xval=np.sum((xcol)-centroid[jj,0])**2/xcol.shape[0]
        else:
          xval=0
        if ycol.shape[0]>0:
          yval=np.sum((ycol)-centroid[jj,1])**2/ycol.shape[0]
        else:
          yval=0
        evalu+=xval+yval
      elbow[i-2,0]=i
      elbow[i-2,1]=evalu/i
    return centroid, elbow


#####calculate euclidean distance and find the minimum distance among centers.
  def min_dis(self,centers,points):
    m,n=centers.shape
    dis=np.empty(m)
    for i in range(m):
      dis[i]=np.sqrt(np.sum((centers[i,:]-points)**2))
    mindex=np.argmin(dis)
    return (mindex,dis[mindex])


#####we generate 3 2D distributions with norm. randoms
### in princeple, the converged result should approach these three centers

center1=[5,7]
center2=[15,17]
center3=[9,27]
###make type1 distribution 100 points
testa=np.random.normal(loc=center1[0],scale=1,size=(100,1))
testb=np.random.normal(loc=center1[1],scale=1,size=(100,1))
type1=np.column_stack((testa,testb))
###make type2 distribution 100 points
testa=np.random.normal(loc=center2[0],scale=1,size=(100,1))
testb=np.random.normal(loc=center2[1],scale=1,size=(100,1))
type2=np.column_stack((testa,testb))
###make type3 distribution 100 points
testa=np.random.normal(loc=center3[0],scale=1,size=(100,1))
testb=np.random.normal(loc=center3[1],scale=1,size=(100,1))
type3=np.column_stack((testa,testb))
#####concatenate all three types and randomnize the sequence
data=np.concatenate((type1,type2,type3))



#### run code and plotting few things
ans=Kmean(data,0.0000001,3)
a,b=ans.K_cal()

####visualize the result, yellow dots are predicted centroids.
########As we all know that the performance might go local minimum rather than the global one
plt.scatter(type1[:,0], type1[:,1], c='red', label='Group 1')
plt.scatter(type2[:,0], type2[:,1], c='blue', label='Group 2')
plt.scatter(type3[:,0], type3[:,1], c='green', label='Group 3')
plt.scatter(a[:,0], a[:,1], c='yellow', label='Predicted')
plt.figure()
plt.plot(b[:,0],b[:,1],marker='o',linestyle='none')
plt.show()

