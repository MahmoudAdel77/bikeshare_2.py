import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
Cities = ['chicago', 'new york city', 'washington']
Months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
Days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike-share data!')
    print()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? \n').lower()
        if city in Cities:
            break
        else:
            print("Sorry I can't understand you, try again!!")
    print('Great! you would like to see {} data. '.format(city))
    print()

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Which month ('January', 'February', 'March', 'April', 'May', 'June') would you filter by or would you see "
            "all? for all just say 'all' \n").lower()
        if month in Months:
            break
        else:
            print('Sorry you choose wrong month, try again!!')
        print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Which day ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday') would you see? "
            "for all just say 'all' ( \n").lower()
        if day in Days:
            break
        else:
            print('Sorry you choose wrong day, try again!!')
    print('-' * 40)
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

    # Load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    else:
        month = df['month']

    # Filter by month to create the new dataframe
    df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('What is the most common month? \n', Months[common_month])
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('What is the most common day of week? \n', common_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('What is the most common hour? \n', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print('What is the most used start station? \n', most_start_station)
    # display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print('What is the most used end station? \n', most_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('What is the most frequent trip? \n', most_frequent)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('What is the total travel time? \n', total_travel_time)
    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(), 2)
    print('What is the Mean of travel time? \n', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bike-share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts().to_frame()
    print('What is the counts of user types? \n', counts_user_types)

    print()

    # Display counts of gender
    try:
        counts_user_gender = df['Gender'].value_counts().to_frame()
        print('What is the counts of gender? \n', counts_user_gender)
    except KeyError:
        print('Sorry!! Gender is not available for this input.')

    print()

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_birth = int(df['Birth Year'].min())
        most_recent_year_birth = int(df['Birth Year'].max())
        most_common_year_birth = int(df['Birth Year'].mode()[0])
        print(
            'The earliest year of birth {}, the most recent year of birth {}, the most common year of birth {} '.format(
                earliest_year_birth, most_recent_year_birth, most_common_year_birth))
    except KeyError:
        print('Sorry!! Birth Year is not available for this input.')

    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def head_five_rows(city):
    """Displays Data on first five rows by City."""

    print('\nData on first five rows by city...\n')
    start_time = time.time()

    # Display first five rows.
    df = pd.read_csv(CITY_DATA[city])
    first_five_rows = df.head()
    print(first_five_rows)

    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        head_five_rows(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
