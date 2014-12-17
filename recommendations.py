__author__ = 'Royston'
# #NOTE : copied verbatim from the paper : Predictive Collective Intelligence by Toby Segaran.
# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}
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
    data = dict();
    with open('T:/data/datasets/movieLens/ml-100k/u1.base') as inf:
        for line in inf:
            words = line.split();
            words.pop(); #Discard the last word
            rating_number = int(words.pop());
            movie = words.pop();
            user_name = words.pop();
            if user_name in data:
                data[user_name][movie] = rating_number;
            else:
                data[user_name] = dict();
                data[user_name][movie] = rating_number;
    return data


allRatings = import_data()
print(sim_pearson(allRatings, '1', '2'));


import operator;


def get_top_similar_users(userNo):
    similarities = dict();
    for user in allRatings.keys():
        if user == userNo:
            continue;
        print(user);
        similarities[user] =  sim_pearson(allRatings, userNo, user);
    sorted_x = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x)
    return sorted_x;

# example usage. Build these most similar users to find a weighted average rank for every movie.
# -> More similar the user, the more weightage for the movies the user has watched to the final recommendation
sortedx = get_top_similar_users('1');
# Find the pearson distances from this user to every other user



