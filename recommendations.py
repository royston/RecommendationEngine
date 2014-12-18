__author__ = 'Royston'
# Data from http://grouplens.org/datasets/movielens/
from math import sqrt
# Returns the Pearson correlation coefficient for p1 and p2
# Would ideally use a well tested library for things like this. But copying the function vertabim from the book for now
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1
    # Find the number of elements
    n = len(si)
    # if they are no ratings in common, return 0
    if n == 0: return 0
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r


def import_data():
    data = dict()
    with open('T:/data/datasets/movieLens/ml-100k/u1.base') as inf:
        for line in inf:
            words = line.split()
            words.pop() #Discard the last word
            rating_number = int(words.pop())
            movie = words.pop()
            user_name = words.pop()
            if not user_name in data:
                data[user_name] = dict()
            data[user_name][movie] = rating_number
    return data


allRatings = import_data()


import operator
from operator import itemgetter

from collections import OrderedDict

def get_top_similar_users(userNo, n=20):
    similarities = dict()
    for user in allRatings.keys():
        if user == userNo:
            continue
        similarities[user] = sim_pearson(allRatings, userNo, user)
    return OrderedDict(sorted(similarities.items(), key=itemgetter(1), reverse=True))

# example usage. Build these most similar users to find a weighted average rank for every movie.
# -> More similar the user, the more weightage for the movies the user has watched to the final recommendation
def recommend(user):
    # Weighted average of the ranking that the most similar users
    users_movies = allRatings[user].keys()
    movie_to_total_similarity = dict()
    movie_to_weighted_rating = dict()
    top_similar_users = get_top_similar_users(user, 15)
    print(top_similar_users)
    for sim_user in top_similar_users.keys():
        similarity = top_similar_users[sim_user];
        for movie in allRatings[sim_user].keys():
            # Skip movies the user has already watched
            if movie in users_movies:
                continue
            if not movie in movie_to_total_similarity:
                movie_to_total_similarity[movie] = 0
            movie_to_total_similarity[movie] = movie_to_total_similarity[movie] + similarity

            if not movie in movie_to_weighted_rating:
                movie_to_weighted_rating[movie] = 0
            movie_to_weighted_rating[movie] = movie_to_weighted_rating[movie] + (allRatings[sim_user][movie] * similarity)
            if movie == '1622':
                print(movie, sim_user, allRatings[sim_user][movie], similarity)
    movie_recommendations = dict();
    for movie in movie_to_total_similarity:
        if movie_to_total_similarity[movie] == 0:
            continue
        movie_recommendations[movie] = movie_to_weighted_rating[movie] / movie_to_total_similarity[movie];
        #if movie_recommendations[movie] > 5:
        #    print(movie, movie_to_weighted_rating[movie],  movie_to_total_similarity[movie], movie_recommendations[movie])
    return OrderedDict(sorted(movie_recommendations.items(), key=itemgetter(1), reverse=True))

print(recommend('1'))



# Find the pearson distances from this user to every other user



