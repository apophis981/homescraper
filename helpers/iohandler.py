import argparse
import datetime

def get_input(input_args):
    """
    Gathers command line input and return parsed input arguements

    Parameters: List of input args
    Returns parsed args
    """
    parser = argparse.ArgumentParser(description='Get user search specifics')

    # Mandatory arguements
    parser.add_argument('distance', type=int,
        help='Max number of miles away from desired location')
    parser.add_argument('geo', type=float, nargs=2,
        help='Lattitude then longitude ex: geo 37.557516 -122.287266')
    parser.add_argument('pricemin', type=int,
        help='minimum price for listing')
    parser.add_argument('pricemax', type=int,
        help='maximum price for listing')

    # Optional arguements
    parser.add_argument('--date',
                        type=lambda s: datetime.datetime.strptime(s, '%m/%d/%Y'),
                        help='Date separated by "/" ex: 10/21/2019')
    parser.add_argument('--bedrooms', type=int, metavar='#',
                        help='Minimum number of bedrooms')
    parser.add_argument('--sqft', type=int, metavar='###',
                        help='Minimum square footage')
    parser.add_argument('--cats', help='Add if you want cats allowed',
                        action='store_true')
    parser.add_argument('--dogs', help='Add if you want dogs allowed',
                        action='store_true')
    parser.add_argument('--wd', help='Add if you want washer and dryer',
                        action='store_true')


    args = parser.parse_args(input_args)
    return args
