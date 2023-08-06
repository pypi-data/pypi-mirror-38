import gc
import numpy_indexed as npi
import multiprocessing as mp
import logging
import pdb
import scipy.linalg as lng
from numpy.linalg import slogdet
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import *
import scipy
import MRATools as mt

from pathos.multiprocessing import ProcessPool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Node(object):


    def __init__(self, parent, ID, locs, notKnots, levelsFromLeaves,
                 J, r, critDepth, pipe=None):

        self.parent = parent
        self.children = []
        self.ID = ID
        self.res = len(ID)-1
        self.N = len(locs)
        self.locs = locs
        self.inds = {}
        self.critDepth = critDepth
        self.leaf=(not bool(levelsFromLeaves))
        
        if not self.leaf and len(notKnots)>max(r,J):
            if len(notKnots)>1e2:
                self.knots, self.kInds = self._getKnotsInds(r, notKnots, random=True)
            else:
                self.knots, self.kInds = self._getKnotsInds(r, notKnots)
        else: 
            self.knots = notKnots
            self.leaf=True
            try:
                self.kInds = np.arange(self.N)[np.flatnonzero(npi.contains(notKnots, self.locs))]
            except:
                pdb.set_trace()
        
        if not self.leaf and len(notKnots)>max(r,J):
            
            newNotKnots = notKnots[~npi.contains(self.knots, notKnots),:]
            # if there is fewer "spare" locations than splits, then make as many splits as there are locations
            minJ = min(J, len(newNotKnots)) 
            if self.N>1e2:
                splits = self._getSplits()
            else:
                splits = self._getJSplits(minJ, newNotKnots)
            #splits = self._getSplitsRobust(newNotKnots)


            
            if self.res==self.critDepth:
                pipes=[]; procs=[]



            pp = ProcessPool(nodes=4)
            
            chData = {'chID' : [], 'chLocs' : [], 'chNotKnots' : [] }
            NCh = len(splits)
            for j in range(NCh):
                chData['chID'] += [self.ID + str(j+1)]
                chLocs = locs[splits[j]]
                chData['chLocs'] += [chLocs]
                chData['chNotKnots'] += [chLocs[npi.contains(newNotKnots, chLocs)]]
                
            children = pp.map(Node, [self]*NCh, chData['chID'], chData['chLocs'], chData['chNotKnots'], [levelsFromLeaves-1]*NCh, [J]*NCh, [r]*NCh, [critDepth]*NCh)
            self.children = children
        

        
        

    def getLeaves(self):

        leaves = []
        if self.leaf:
            leaves.append(self)
        else:
            for ch in self.children:
                leaves.extend( ch.getLeaves() )

        return leaves

            


    
    def getOrderFromLeaves(self):

        leaves = self.getLeaves()

        
        def getLeafInds(leafID):
            path = list(leafID[(self.res+1):])[::-1]
            node = self
            inds = [np.arange(self.N)]
            
            while path:
                chId = node.children[int(path.pop())-1].ID
                inds.append( node.inds[chId] )
                node = node.children[int(chId[-1])-1]

            curInds = inds.pop()

            while inds:
                curInds = inds.pop()[curInds]

            return curInds

        leavesInds = [(leaf.ID, getLeafInds(leaf.ID)) for leaf in leaves]
        order = np.concatenate([tup[1] for tup in leavesInds])
        
        return order


            


    def getGrid(self):
        grid = self.knots
        for ch in self.children:
            chGrid = ch.getGrid()
            grid = np.vstack((grid, chGrid))
        return grid




            


    #@profile
    def _getKnotsInds(self, r, notKnots, random=False):

        if np.shape(self.locs)[1]==1:
            locs1d = self.locs.ravel()
            #knots = [np.percentile(locs1d, 100.0*i/(r+1), interpolation='nearest') for i in range(r+2)][1:-1]
            #knots = [np.percentile(notKnots1d, 100.0*i/(r+1), interpolation='nearest') for i in range(r+2)][1:-1]
            notKnots1d = notKnots.ravel()
            knots = [np.percentile(notKnots1d, 100.0*i/(r+1), interpolation='nearest') for i in range(r+2)][1:-1]
            kInds = np.arange(self.N)[np.flatnonzero(npi.contains(knots, locs1d))]
            

        else:
            if random and self.res>=0:
                inds = np.random.choice(np.arange(len(notKnots)), size=r, replace=False)
                knots = notKnots[inds]
            else:
                kmeans = KMeans(n_clusters=r, random_state=0).fit(notKnots)
                C = kmeans.cluster_centers_
                D = cdist(notKnots, C)
                knots = np.zeros((r, self.locs.shape[1]))
                for centr in range(r):
                    ind = np.argmin(D[:,centr])
                    knots[centr,:] = notKnots[ind]

            kInds = np.arange(self.N)[np.flatnonzero(npi.contains(knots, self.locs))]
        knots = self.locs[kInds] # this is to ensure that both kInds and knots are in the same order
        return knots, kInds
                                          

    
    
    

    #@profile
    def _getSplits(self):

        """
        If locations are 1D, splits into three segments with the same number of grid points.
        Otherwise splits into four segments, splitting in half along each axis.
        """

        if np.shape(self.locs)[1]==1:

            perc = np.percentile(self.locs, (33,66))
            
            locs_0 = np.where(self.locs[:,0]<perc[0])[0]
            locs_1 = np.where(np.logical_and(self.locs[:,0]>perc[0], self.locs[:,0]<perc[1]))[0]
            locs_2 = np.where(self.locs[:,0]>perc[1])[0]

            subdomains = [locs_0, locs_1, locs_2]

        else:
        
            means = np.mean(self.locs, axis=0)
        
            locs_00 = np.where(np.logical_and(self.locs[:,0]<=means[0], self.locs[:,1]<=means[1]))[0]
            locs_01 = np.where(np.logical_and(self.locs[:,0]<=means[0], self.locs[:,1]>means[1]))[0]
            locs_10 = np.where(np.logical_and(self.locs[:,0]>means[0], self.locs[:,1]<=means[1]))[0]
            locs_11 = np.where(np.logical_and(self.locs[:,0]>means[0], self.locs[:,1]>means[1]))[0]
            
            subdomains = [locs_00, locs_01, locs_10, locs_11]

        
        return subdomains






    def _getSplitsRobust(self, notKnots):

        """
        Works like _getSplits but accounts for the fact that there might be few grid points along
        a certain dimension. It first splits the points that are not the "middle" points (along x, y
        or both). Then it splits the "ties" into 4 parts. This is useful when we are dealing with, say
        a 3x3 grid and want to split it into four subregions. If we didn't use the robust method
        we might end up with one region that has 4 points, two regions with 2 points and one region with only
        a single point. 

        Useful only in 2D
        """
        med = np.median(notKnots, axis=0)

        all_ties = notKnots[np.where(np.logical_and(notKnots[:,0]==med[0], notKnots[:,1]==med[1]))]
        ties_inds = np.arange(self.N)[np.flatnonzero(npi.contains(all_ties, self.locs))]
        
        xy_ties = np.where(np.logical_and(notKnots[:,0]==med[0], notKnots[:,1]==med[1]))[0].ravel()
        x_ties = np.where(notKnots[:,0]==med[0])[0]
        y_ties = np.where(notKnots[:,1]==med[1])[0]
        
        pure_x_ties = np.setdiff1d(x_ties, xy_ties)
        pure_y_ties = np.setdiff1d(y_ties, xy_ties)
        array_xy_ties = np.array_split(xy_ties, 4)
                           
        locs_list = [np.array_split(xy_ties, 4), np.array_split(pure_x_ties, 4),  np.array_split(pure_y_ties, 4)[::-1]]
        locs = []
        for i in range(4):
            locs.append( np.hstack((locs_list[0][i], locs_list[1][i], locs_list[2][i])) )       
      
        locs[0] = np.setdiff1d(np.where(np.logical_and(self.locs[:,0] < med[0],  self.locs[:,1] < med[1]))[0], ties_inds)
        locs[1] = np.setdiff1d(np.where(np.logical_and(self.locs[:,0] < med[0],  self.locs[:,1] > med[1]))[0], ties_inds)
        locs[2] = np.setdiff1d(np.where(np.logical_and(self.locs[:,0] > med[0],  self.locs[:,1] < med[1]))[0], ties_inds)
        locs[3] = np.setdiff1d(np.where(np.logical_and(self.locs[:,0] > med[0],  self.locs[:,1] > med[1]))[0], ties_inds)       
            
        return locs


    

    def _getJSplits(self, J, notKnots):

        # if:
        #   * J=r+1, or if the number of knots is one less that the number
        #     of partitions,
        #   * we are in 1d,
        #   * there is enough grid points left,
        #   then we partition such that the knots are at the boundary;
        # else:
        #    do k-means etc.

        r = len(self.kInds)
        cond1 = J==r+1
        cond2 = self.locs.shape[1]==1
        cond3 = self.N>=(J+r)
        
        if cond1 and cond2 and cond3:
            subDomains = np.split(np.arange(self.N), self.kInds)
        else:
            subDomains = []

            # we need this to match the notKnots to their original indices
            allInds = np.arange(self.N)
            notKnotInds = np.arange(self.N)[np.flatnonzero(npi.contains(notKnots, self.locs))]

            #clustering
            nClusters = min(J, len(notKnots))
            kmeans = KMeans(n_clusters=nClusters, random_state=0).fit(notKnots)
            all_labels=kmeans.labels_

            #now assign knots from all previous resolutions to the nearby clusters
            centers = kmeans.cluster_centers_
            allKnotsInds = np.setdiff1d(np.arange(self.N), notKnotInds)
            allKnots = self.locs[ allKnotsInds, : ]
            D = cdist( allKnots, centers )
            knot_labels = np.argmin(D, axis=1)
            
            for j in range(J):
                indsInNotKnots = np.where(all_labels==j)[0]
                inds = notKnotInds[indsInNotKnots]
                # check if we should include a knot in this cluster
                
                kIndsInThisRegion = allKnotsInds[ np.where(knot_labels==j)[0] ]
                inds = np.hstack( (kIndsInThisRegion, inds) )
                inds = np.sort(inds)
                if len(inds):
                    subDomains.append(inds)

            if self.locs.shape[1]==1:
                subDomains = sorted(subDomains, key=lambda _arr: np.min(_arr))
                
        return subDomains   

