import numpy as np
import pandas as pd
import time


def get_filters():
    
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter"""
    
    
    print("Hi,there! Welcome to this interactive data exploration dashboard!")
    print("Let's explore some US bikeshare data!")
    
    cities= ['Chicago','New York City','Washington']
    
    city= str(input("Which city do you want to explore its bikeshare data? Chicago, New York City, or Washington? ")).title()
    
    if city in cities:
        print("You chose to explore data about: {}".format(city))
    else:
        while city not in cities:
            print("You entered: '{}'\n Only Data about Chicago, New York City, and Washington available! Please Check Your Input and Try Again!".format(city))
            city= str(input("Which city do you want to explore its bikeshare data? Chicago, New York City, Washington: ")).title()
        print("You chose to explore data about: {}".format(city))
        
        
    months= ['All','January','February','March','April','May','June']

    month= str(input("Which month do you want to explore?(January ~ June) Enter the name of the month or enter (all) ")).title()
    
    if month in months:
        print("You applied these filters so far>>> City={}, Month={}".format(city,month))
    else:
        while month not in months:
            print("Only data about the first six months of the year is available! Please Try Again!")
            month= str(input("Which month do you want to explore?(January ~ June) Enter the name of the month or enter (all) ")).title()
        print("You applied these filters so far>>> City={}, Month={}".format(city,month))
      
    days= ['All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    day= str(input("Would you like to filter by a specific day of the week? Please enter the full day name (Saturday, Sunday, etc.) or enter (All) to include all the 7 days of the week  ")).title()
    
    if day in days:
        print(" You applied these filters>>> City={}, Month={}, Day={}".format(city,month,day))
    else:
        while day not in days:
            print("Invalid input!Please check your input and try again!")
            day= str(input("Would you like to filter by a specific day of the week? Please enter the full day name (Saturday, Sunday, etc.) or enter (All) to include all the 7 days of the week  ")).title()
        print(" You applied these filters>>> City={}, Month={}, Day={}".format(city,month,day))
   
    return city,month,day



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
    city= city.title()
    month= month.title()
    day= day.title()   
    
    if len(city.split())>1:
        city="_".join(city.split())
                   
    city_file= city.lower()+'.csv'
    df = pd.read_csv(city_file)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    
    if month != 'All':
        df = df[df['Month'] == month]
    if day != 'All':
        df= df[df['Day'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
      
    most_common_month= df['Month'].mode()[0]
    most_common_day= df['Day'].mode()[0]
    most_common_hour= df['Hour'].mode()[0]
    
    print("\nThe most common month: {} \n The most common day: {} \n The most common hour (24-hour format): {}\n".format(most_common_month,most_common_day,most_common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    most_common_start_station= df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_pair= pd.Series(df['Start Station']+'//'+df['End Station']).mode()[0]
    
    print("\nThe most common start station is: {}.".format(most_common_start_station))
    print("\nThe most common end station is: {}".format(most_common_end_station))
    print("\nThe most common start//end pair is:{}".format(most_common_pair))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_duration= df['Trip Duration'].sum()
    mean_duration= df['Trip Duration'].mean()
    
    print("\nThe total duration of travel time is: {}".format(total_duration))
    print("\nThe mean duration of travel time is: {}".format(mean_duration))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
   
    user_type_count= df['User Type'].value_counts()
    print("\nUser Type Information: \n{}".format(user_type_count))
    
    if 'Gender' in df.columns:
        gender_count= df['Gender'].value_counts()
        print("\nGender Count Information: \n{}".format(gender_count))
    else:
        print("\nNo Gender information is available in this dataset...\n")
        
    if 'Birth Year' in df.columns:
        oldest_user= int(df['Birth Year'].min())
        youngest_user= int(df['Birth Year'].max())
        common_year= int(df['Birth Year'].mode())
        print('\nThe oldest user was born in the year {}, \nwhile the youngest user was born in the year {}, \nand the most common year of birth is {}.'.format(oldest_user,youngest_user,common_year))
    else:
        print('\nNo Year of Birth information is available in this dataset...\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def main():
    """This is the main function that excutes the script
        Also, it will ask the user whether they want to display 5 rows of raw data and then the next 5 rows until it reaches the maximum index of the specified data...
        In addition, this function contains the restart prompt as well"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data= input('Would you like to display 5 rows of raw data from the dataset you chose? Enter yes or no.').lower()
        i=0
        print("The maximum index is: {}".format(df['Start Time'].idxmax()))
        while raw_data == 'yes'and i+5<=df['Start Time'].idxmax():
            i= i+5
            print(df.iloc[range(i)])
            raw_data= input('Would you like to display the next 5 rows of raw data from the dataset you chose? Enter yes or no.\n').lower()
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
    main()
