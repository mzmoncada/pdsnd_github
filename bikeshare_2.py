import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    
    #need loop to catch for errors
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Of the cities, Chicago, Washington, and New York City, which would you like to explore?\n')).lower()
            if not city:
                raise ValueError('\nThat is an empty string.')
            if city not in CITY_DATA:
                raise ValueError('\nThat city is not in our database. Please try again.')
            print('You have selected to analyze \'{}\'.'.format(city.title()))
            break
        except ValueError as e:
            print(e)
        

    # get user input for month (all, january, february, ... , june)
    month_potential = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    
   # month = str(input('For what month? Write \'all\' for all months.')).lower()
    while True:
        try:
            month = str(input('Of the first 6 months in the year, which would you like to filter by? Type \'all\' to view all months.\n')).lower()
            if not month:
                raise ValueError('\nThat is an empty string. Please try again.')
            if month not in month_potential:
                raise ValueError('\nThat is not an acceptable option. Please try again.')
            if month != 'all':
                print('You have selected to filter by \'{}\'.'.format(month.title()))
            break
        except ValueError as e:
            print(e)
    
  # get user input for day in integer format
    day_potential= ['All','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
  
    while True:
        try:
            day = str(input('What day of the week would you like to filter by? Type \'all\' to view all days.\n'))
            if not day:
                raise ValueError('\nThat is an empty value. Please try again.')
            if day.title() not in day_potential:
                raise ValueError('\nThat is not an acceptable input. Please try again.')
            if day.title() != 'All':
                print('You have selected to filter by \'{}\'.'.format(day))
            break
        except ValueError as e:
            print(e)

    # get user input for day of week (all, monday, tuesday, ... sunday)


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

     # load data file into a dataframe
    print(CITY_DATA[city])
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #print(df['month'])
    #print('months')

    # extract day of the week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #print(df['day_of_week'])
    print('The starting shape is {}'.format(df.shape))

    # extract hours
    df['start hour'] = pd.DatetimeIndex(df['Start Time']).hour
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        print('month index filter is {}'.format(month))
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        print('The new filtered month shape is {}'.format(df.shape))
        #print(df)

    # filter by day of week if applicable
    if day.title() != 'All':
        df = df[df['day_of_week']==day.title()]
        print('The new filtered day shape is {}'.format(df.shape))
        #print(df)
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #display the most common month; if the month is already filtered, this should be equivalent
    month_dict = {'1':'January',
                  '2':'February',
                  '3':'March',
                  '4':'April',
                  '5':'May',
                  '6': 'June'}
    popular_month = month_dict[str(df['month'].mode()[0])]
    print(popular_month)
    print('\nThe most common month in the selected data set is {}.'.format(popular_month))


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week in the selected data set is {}.'.format(popular_day))


    # display the most common start hour
    popular_start_hour = df['start hour'].mode()[0]
    print('\nThe most common start hour in the selected data set is {}.'.format(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station in the selected data set is {}.'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station in the selected data set is {}.'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_comb = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    most_frequent_comb_a = most_frequent_comb.iloc[0:1]
    print('\nThe most common combination of start and stop station in the selected data set is: \n\n{}.'.format(most_frequent_comb_a))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total travel time for this filtered data set is {} seconds. Wow, that\'s a lot!'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('\nThe mean travel time for this filtered data set is {} seconds.'.format(round(df['Trip Duration'].mean(),2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    print('\nHere is a breakdown of different user types: \n{}'.format(df['User Type'].value_counts()))

    # Display counts of gender
    try:
        different_genders = df['Gender'].value_counts()
        print('\nHere is a breakdown of different user genders: \n{}'.format(different_genders))
    except:
        print('\nThis data set lacks gender data.')
    

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('\nThe earliest birth in the data set was in {}.'.format(earliest_birth))
        print('\nThe most recent birth in the data set was {}.'.format(most_recent_birth))
        print('\nTHe most common birth year in the data set was {}.'.format(most_common_birth))
    except:
        print('\nThis data set lacks birth year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def view_raw_data(df):

    index1 = 0

    index2 = 5

    while True:

        raw_data = input('Would you like to see 5 rows of data?\nPlease write \'yes\' to continue or anything else to exit.\n').lower()

        if raw_data == 'yes':

            print(df.iloc[index1:index2])

            index1 += 5

            index2 += 5

        else:

            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
