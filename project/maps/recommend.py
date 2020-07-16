"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    "*** YOUR CODE HERE ***"
    return min(centroids,key = lambda x: distance(x, location))
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
#    "*** YOUR CODE HERE ***"
    
#    Idea code:
#    find_closest(restoA, [centroids]) => centroid$
#    find_closest(restoB, [centroids]) => centroid$
#    find_closest(restoC, [centroids]) => centroid&
#    => [[centroid$, restoA],[centroid$, restoB],[centroid&, restoC]]
#    =>[[restoA, restoB],[restoC]]
    
    
    pairs = []
    for i in restaurants:
        j = find_closest(restaurant_location(i), centroids)
        pair = [j, i]
        pairs.append(pair) 
        
    return group_by_first(pairs)

#    return group_by_first([[find_closest(restaurant_location(restaurant), centroids),restaurant] for restaurant in restaurants])
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    "*** YOUR CODE HERE ***"
    x = []
    y = []
    
    for restaurant in cluster:
        x.append(restaurant_location(restaurant)[0])
        y.append(restaurant_location(restaurant)[1])
       
    return [mean(x), mean(y)]

#    return [mean(restaurant_location(restaurant)[0]),mean(restaurant_location(restaurant)[1]) for restaurant in cluster]
    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        "*** YOUR CODE HERE ***"
        clusters = group_by_centroid(restaurants, centroids)
        centroids = [find_centroid(cluster) for cluster in clusters ]
        
        
        # END Question 6
        n += 1
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # BEGIN Question 7
    Sxx = sum([(i - mean(xs))**2 for i in xs])
    Syy = sum([(j - mean(ys))**2 for j in ys])
    Sxy = sum([(xs[n] - mean(xs))*(ys[n] - mean(ys)) for n in range(len(xs))])
    
    b = Sxy/Sxx
    a = mean(ys)-b*mean(xs)
    r_squared = Sxy**2/(Sxx*Syy)
    # REPLACE THIS LINE WITH YOUR SOLUTION
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    "*** YOUR CODE HERE ***"
#    feature_fn_max = 0
#    for i in feature_fns:
#        k = find_predictor(user, restaurants, i)[1]
#        if k > feature_fn_max:
#            feature_fn_max = k
#    
#    return find_predictor(user, restaurants, feature_fn_max)

    predictor_list = [find_predictor(user, reviewed, feature_fn) for feature_fn in feature_fns]
    predictor_max, r_squared = max(predictor_list, key = lambda x: x[1])
    return predictor_max
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    "*** YOUR CODE HERE ***"
    
##     methode 2
#    all_dict = {}
#    for restaurant in restaurants:
#        if restaurant in reviewed:
#            all_dict[restaurant_name(restaurant)] = user_rating(user, restaurant_name(restaurant))
#        else:
#            all_dict[restaurant_name(restaurant)] = predictor(restaurant)
#            
#    return all_dict
    
##    methode 1
    rating_reviewed = [[restaurant_name(restaurant), user_rating(user, restaurant_name(restaurant))] for restaurant in reviewed]
    
    rating_predicted = [[restaurant_name(restaurant), predictor(restaurant)] for restaurant in restaurants if restaurant not in reviewed]

    return dict(rating_reviewed + rating_predicted)
#     END Question 9


#def user_rating(user, restaurant_name):
#    """Return the rating given for restaurant_name by user."""
#    reviewed_by_user = user_reviews(user) => return dict
#    user_review = reviewed_by_user[restaurant_name] => return one review
#    return review_rating(user_review) => return one number
################################################    
## Users
#
#def make_user(name, reviews):
#    """Return a user data abstraction."""
#    return [name, {review_restaurant_name(r): r for r in reviews}]
#
#def user_name(user):
#    """Return the name of the user, which is a string."""
#    return user[0]
#
#def user_reviews(user):
#    """Return a dictionary from restaurant names to reviews by the user."""
#    return user[1]
#####################################################
#    # Reviews
#
#def make_review(restaurant_name, rating):
#    """Return a review data abstraction."""
#    return [restaurant_name, rating]
#
#def review_restaurant_name(review):
#    """Return the restaurant name of the review, which is a string."""
#    return review[0]
#
#def review_rating(review):
#    """Return the number of stars given by the review, which is a
#    floating point number between 1 and 5."""
#    return review[1]
########################################################
    
#user = make_user('Mr. Mean Rating Minus One', [make_review('A', 3),make_review('B', 4),make_review('C', 1), ])
#cluster = [make_restaurant('A', [1, 2], [], 4, [make_review('A', 4),make_review('A', 4)]), make_restaurant('B', [4, 2], [], 3, [make_review('B', 5)]),make_restaurant('C', [-2, 6], [], 4, [make_review('C', 2)]),make_restaurant('D', [4, 4], [], 3.5, [make_review('D', 2.5),make_review('D', 3.5),]),]
#restaurants = {restaurant_name(r): r for r in cluster}
#to_rate = cluster[2:]
#fns = [restaurant_price, lambda r: mean(restaurant_ratings(r))]
#ratings = rate_all(user, to_rate, fns)

def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** YOUR CODE HERE ***"
    
    return [restaurant for restaurant in restaurants if query in restaurant_categories(restaurant)]
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [lambda r: mean(restaurant_ratings(r)),
            restaurant_price,
            lambda r: len(restaurant_ratings(r)),
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)