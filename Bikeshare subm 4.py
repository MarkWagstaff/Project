import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')


    while True:
      city = input("\nWhich city would you like to view? New York City, Chicago or Washington?\n").lower()
      if city not in ('New York City', 'Chicago', 'Washington'):
        print("Check your input and try again.")
        continue
      else:
        break

    while True:
      month = input("\nWhich month would you like to view? January, February, March, April, May, June or type 'all'.\n").lower()
      if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
        print("Check your input and try again.")
        continue
      else:
        break


    while True:
      day = input("\nWhich day of the week would you like to view? Please enter: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all'.\n").lower()
      if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'):
        print("Check your input and try again.")
        continue
      else:
        break

    return city, month, day

def display_raw_data(df):
    """Displays raw data statistics five rows at a time."""
    i = 0
    raw = input("\nWould you like to view the next five rows of raw data related to your selections? Enter yes or no.\n").lower()
    pd.set_option('display.max_columns',200)

    while True:
      if raw == 'no':
        break      
      elif raw == 'yes':
        print(df[i:i+5])
        i += 5
      repeat = input("\nWould you like to view more rows? Enter yes or no.\n").lower()
      if repeat == 'no':
        break
      else:
        raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()
        
    print('-'*40)


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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def round_decimal(decimal, decimal_places=1):
    """Rounds a decimal to the specified number of decimal places."""
    return round(decimal, decimal_places)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month, "Month(s)")

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', popular_day, "Minute(s)")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour, "Hour(s)")

    print("\nThis took %s seconds." % round_decimal(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)

    Combination_Station = df.groupby(['Start Station', 'End Station']).size().nlargest(1).index[0]
    print('\nMost Commonly used combination of start station and end station trip:', Combination_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', round_decimal(Total_Travel_Time/86400), " Days")

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', round_decimal(Mean_Travel_Time/60), " Minutes")

    print("\nThis took %s seconds." % round_decimal(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo data available for this month.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart == 'no':
          print("Have a great day")
          break
        elif restart == 'yes':
          continue
        else:
          print("Your input is invalid. Please enter only 'yes' or 'no'")

if __name__ == "__main__":
	main()