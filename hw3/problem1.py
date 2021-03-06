import math
import numpy as np
import os
from time import gmtime, strftime


#-------------------------------------------------------------------------
'''
    Problem 1: User-based  recommender systems
    In this problem, you will implement a version of the recommender system using user-based method.
    You could test the correctness of your code by typing `nosetests test1.py` in the terminal.
'''

#--------------------------
def cosine_similarity(RA, RB):
    '''
        compute the cosine similarity between user A and user B.
        The similarity values between users are measured by observing all the items which have been rated by BOTH users.
        If an item is only rated by one user, the item will not be involved in the similarity computation.
        You need to first remove all the items that are not rated by both users from RA and RB.
        If the two users don't share any item in their ratings, return 0. as the similarity.
        Then the cosine similarity is < RA, RB> / (|RA|* |RB|).
        Here <RA, RB> denotes the dot product of the two vectors (see here https://en.wikipedia.org/wiki/Dot_product).
        |RA| denotes the L-2 norm of the vector RA (see here for example: http://mathworld.wolfram.com/L2-Norm.html).
        For more details, see here https://en.wikipedia.org/wiki/Cosine_similarity.
        Input:
            RA: the ratings of user A, a float python vector of length m (the number of movies).
                If the rating is unknown, the number is 0. For example the vector can be like [0., 0., 2.0, 3.0, 0., 5.0]
            RB: the ratings of user B, a float python vector
                If the rating is unknown, the number is 0. For example the vector can be like [0., 0., 2.0, 3.0, 0., 5.0]
        Output:
            S: the cosine similarity between users A and B, a float scalar value between -1 and 1.
        Hint: you could use math.sqrt() to compute the square root of a number
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    dotpro = 0.
    An = 0.
    Bn = 0.
    for i in range(len(RA)):
        if (RA[i]!=0. and RB[i]!=0.):
            dotpro += RA[i] * RB[i]
            An += RA[i]**2
            Bn += RB[i]**2
    d  = (math.sqrt(An) * math.sqrt(Bn))
    if d==0:
        return 0
    S = float(dotpro / d)
    #########################################
    return S


#--------------------------
def find_users(R, i):
    '''
        find the all users who have rated the i-th movie.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If a rating is unknown, the number is 0.
            i: the index of the i-th movie, an integer python scalar (Note: the index starts from 0)
        Output:
            idx: the indices of the users, a python list of integer values
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    idx = []
    for u in range(len(R[i])):
        if R[i][u]!=0.:
            idx.append(u)
    #########################################
    return idx

#--------------------------
def user_similarity(R, j, idx):
    '''
        compute the cosine similarity between a collection of users in idx list and the j-th user.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If a rating is unknown, the number is 0.
            j: the index of the j-th user, an integer python scalar (Note: the index starts from 0)
            idx: a list of user indices, a python list of integer values
        Output:
            sim: the similarity between any user in idx list and user j, a python list of float values. It has the same length as idx.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    sim = []
    for i in range(len(idx)):
        sim.append(cosine_similarity(R[:,j], R[:,idx[i]]))
    #########################################
    return sim


#--------------------------
def user_based_prediction(R, i_movie, j_user, K=5):
    '''
        Compute a prediction of the rating of the j-th user on the i-th movie using user-based approach.
        First we take all the users who have rated the i-th movie, and compute their similarities to the target user j.
        If there is no user who has rated the i-th movie, predict 3.0 as the default rating.
        From these users, we pick top K similar users.
        If there are less than K users who has rated the i-th movie, use all these users.
        We weight the user's ratings on i-th movie by the similarity between that user and the target user.
        Finally, we rescale the prediction by the sum of similarities to get a reasonable value for the predicted rating.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0.
            i_movie: the index of the i-th movie, an integer python scalar
            j_user: the index of the j-th user, an integer python scalar
            K: the number of similar users to compute the weighted average rating.
        Output:
            p: the predicted rating of user j on movie i, a float scalar value between 1. and 5.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    user_ind = find_users(R, i_movie)
    if len(user_ind)==0:
        return 3.0
    user_sim = user_similarity(R, j_user, user_ind)
    '''for i in range(len(user_sim)):
        for k in range( len(user_sim) - 1, i, -1):
            if ( user_sim[k] > user_sim[k - 1] ):
                swap( user_sim, k, k - 1 )
                swap1(user_ind, k, k-1)
    cand = K if len(user_ind)>K else len(user_ind)

    total = 0.
    weight = 0.
    for i in range(cand):
        total += user_sim[i] * R[i_movie, user_ind[i]]
        weight += user_sim[i]'''

    cand = K if len(user_ind)>K else len(user_ind)
    total = 0.
    weight = 0.
    sim_cand = []
    user_cand = []
    for i in range(cand):
        cur_max = 0
        cur_ind = 0
        for j in range(len(user_sim)):
            if user_sim[j]> cur_max and j not in user_cand:
                cur_max = user_sim[j]
                cur_ind = j
        sim_cand.append(cur_max)
        user_cand.append(cur_ind)
    for i in range(cand):
        total += sim_cand[i] * R[i_movie, user_ind[user_cand[i]]]
        weight += sim_cand[i]
    p = total / weight
    #########################################
    return p


#--------------------------
def compute_RMSE(ratings_pred, ratings_real):
    '''
        Compute the root of mean square error of the rating prediction.
        Input:
            ratings_pred: predicted ratings, a float python list
            ratings_real: real ratings, a float python list
        Output:
            RMSE: the root of mean squared error of the predicted rating, a float scalar.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    r = 0.
    total = 0.
    for i in range(len(ratings_real)):
        r += (ratings_pred[i] - ratings_real[i]) ** 2
        total += 1
    RMSE = math.sqrt(r/total)
    #########################################
    return RMSE



#--------------------------
def load_rating_matrix(filename = 'movielens_train.csv'):
    '''
        Load the rating matrix from a CSV file.  In the CSV file, each line represents (user id, movie id, rating).
        Note the ids start from 1 in this dataset.
        Input:
            filename: the file name of a CSV file, a string
        Output:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    r = np.genfromtxt(os.path.dirname(os.path.abspath(__file__))+'/'+filename, delimiter=',', dtype=float)
    ulen = int(np.amax(r[:, 0]))
    mlen = int(np.amax(r[:, 1]))
    R = np.zeros(shape = (mlen, ulen))
    for i in range(len(r)):
        uid = int(r[i, 0])
        mid = int(r[i, 1])
        R[mid-1, uid-1] = r[i, 2]
    #########################################
    return R


#--------------------------
def load_test_data(filename = 'movielens_test.csv'):
    '''
        Load the test data from a CSV file.  In the CSV file, each line represents (user id, movie id, rating).
        Note the ids in the CSV file start from 1. But the indices in u_ids and m_ids start from 0.
        Input:
            filename: the file name of a CSV file, a string
        Output:
            m_ids: the list of movie ids, an integer python list of length n. Here n is the number of lines in the test file. (Note indice should start from 0)
            u_ids: the list of user ids, an integer python list of length n.
            ratings: the list of ratings, a float python list of length n.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    R = np.genfromtxt(os.path.dirname(os.path.abspath(__file__))+'/'+filename, delimiter=',', dtype=float)
    m_ids = R[:, 1].tolist()
    u_ids = R[:, 0].tolist()
    ratings = R[:, 2].tolist()
    m_ids = [int(i-1) for i in m_ids]
    u_ids = [int(i-1) for i in u_ids]
    #########################################
    return m_ids, u_ids, ratings


#--------------------------
def movielens_user_based(train_file='movielens_train.csv', test_file ='movielens_test.csv', K = 5):
    '''
        Compute movie ratings in movielens dataset. Based upon the training ratings, predict all values in test pairs (movie-user pair).
        In the training file, each line represents (user id, movie id, rating).
        Note the ids start from 1 in this dataset.
        Input:
            train_file: the train file of the dataset, a string.
            test_file: the test file of the dataset, a string.
            K: the number of similar users to compute the weighted average rating.
        Output:
            RMSE: the root of mean squared error of the predicted rating, a float scalar.
    Note: this function may take 1-5 minutes to run.
    '''

    # load training set
    R = load_rating_matrix(train_file)

    # load test set
    m_ids, u_ids,ratings_real = load_test_data(test_file)
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    # predict on test set
    ratings_pred = []
    for i,j in zip(m_ids, u_ids):# get one pair (movie, user) from the two lists
        p = user_based_prediction(R,i,j,K) # predict the rating of j-th user's rating on i-th movie
        ratings_pred.append(p)
    #print(count)
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    # compute RMSE
    RMSE = compute_RMSE(ratings_pred,ratings_real)
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return  RMSE

def swap( A, i, j ):
    '''
        Swap the i-th element and j-th element in list A.
        Inputs:
            A:  a list, such as  [2,6,1,4]
            i:  an index integer for list A, such as  3
            j:  an index integer for list A, such as  0
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp

def swap1( A, i, j ):
    '''
        Swap the i-th element and j-th element in list A.
        Inputs:
            A:  a list, such as  [2,6,1,4]
            i:  an index integer for list A, such as  3
            j:  an index integer for list A, such as  0
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp
