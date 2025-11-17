import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

months = ['january', 'february', 'march', 'april', 'may', 'june']
valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Ask user to specify city, month, and day.
    """
    print("Hello! Let's explore some US bikeshare data!")
    print("you can choose chicago, new york city, or washington to get the data from")

    # city
    while True:
        city = input('choose a city\n').strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("invalid input (try: chicago, new york city, washington)")

    # month
    while True:
        month = input('choose a month from january until june or enter all to show all months\n').strip().lower()
        if month in months or month == 'all':
            break
        else:
            print("invalid input (try: january..june or all)")

    # day
    while True:
        day = input('choose a day or enter all to show all days\n').strip().lower()
        if day in valid_days or day == 'all':
            break
        else:
            print("invalid input (try: monday..sunday or all)")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for selected city and filter by month/day if needed.
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"file not found: {CITY_DATA[city]}")
        return pd.DataFrame()
    except Exception as e:
        print("error reading the file:", e)
        return pd.DataFrame()

    # convert to datetime and add helper columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month            # 1-12
    df['month_name'] = df['Start Time'].dt.month_name()
    df['day_name'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # filter month
    if month != 'all':
        m_idx = months.index(month) + 1  # january -> 1
        df = df[df['month'] == m_idx]

    # filter day
    if day != 'all':
        df = df[df['day_name'] == day]

    df = df.reset_index(drop=True)
    return df


def time_stats(df):
    """Display stats on most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df.empty:
        print("no data for these filters.")
    else:
        # most common month (use month_name inside filtered range)
        if 'month_name' in df.columns and not df['month_name'].empty:
            try:
                common_month = df['month_name'].value_counts().idxmax()
                print('Most common month:', common_month)
            except:
                print('Most common month: N/A')
        else:
            print('Most common month: N/A')

        # most common day of week
        if 'day_name' in df.columns and not df['day_name'].empty:
            try:
                common_day = df['day_name'].value_counts().idxmax()
                print('Most common day of week:', common_day.capitalize())
            except:
                print('Most common day of week: N/A')
        else:
            print('Most common day of week: N/A')

        # most common start hour
        if 'hour' in df.columns and not df['hour'].empty:
            try:
                common_hour = int(df['hour'].value_counts().idxmax())
                print('Most common start hour:', common_hour)
            except:
                print('Most common start hour: N/A')
        else:
            print('Most common start hour: N/A')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display stats on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print("no data for these filters.")
    else:
        # start station
        if 'Start Station' in df.columns and not df['Start Station'].empty:
            try:
                print('Most commonly used start station:', df['Start Station'].value_counts().idxmax())
            except:
                print('Most commonly used start station: N/A')
        else:
            print('Most commonly used start station: N/A')

        # end station
        if 'End Station' in df.columns and not df['End Station'].empty:
            try:
                print('Most commonly used end station:', df['End Station'].value_counts().idxmax())
            except:
                print('Most commonly used end station: N/A')
        else:
            print('Most commonly used end station: N/A')

        # combination
        if 'Start Station' in df.columns and 'End Station' in df.columns:
            try:
                combo = (df['Start Station'] + ' -> ' + df['End Station'])
                print('Most frequent trip:', combo.value_counts().idxmax())
            except:
                print('Most frequent trip: N/A')
        else:
            print('Most frequent trip: N/A')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display stats on total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print("no data for these filters.")
    else:
        if 'Trip Duration' in df.columns:
            total = df['Trip Duration'].sum()
            mean = df['Trip Duration'].mean()
            print('Total travel time (seconds):', int(total))
            print('Mean travel time (seconds):', round(mean, 2))
        else:
            print('Trip Duration column not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display stats on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print("no data for these filters.")
    else:
        # user types
        if 'User Type' in df.columns:
            print('User Type counts:')
            try:
                print(df['User Type'].value_counts(dropna=False).to_string())
            except:
                print('N/A')
        else:
            print('User Type info not available.')

        print()

        # gender
        if 'Gender' in df.columns:
            print('Gender counts:')
            try:
                print(df['Gender'].value_counts(dropna=False).to_string())
            except:
                print('N/A')
        else:
            print('Gender info not available.')

        print()

        # birth year
        if 'Birth Year' in df.columns and df['Birth Year'].notna().any():
            try:
                by = df['Birth Year'].dropna().astype(float)
                earliest = int(by.min())
                most_recent = int(by.max())
                most_common = int(by.value_counts().idxmax())
                print('Earliest year of birth:', earliest)
                print('Most recent year of birth:', most_recent)
                print('Most common year of birth:', most_common)
            except:
                print('Birth Year stats: N/A')
        else:
            print('Birth Year info not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """
    Show raw data 5 rows at a time upon user request.
    """
    if df.empty:
        return
    i = 0
    while True:
        ans = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()
        if ans.startswith('y'):
            end = i + 5
            if i >= len(df):
                print('No more data to display.')
                break
            print(df.iloc[i:end].to_string(index=False))
            i = end
            if i >= len(df):
                print('No more data to display.')
                break
        elif ans.startswith('n'):
            break
        else:
            print("please answer yes or no.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No rows match your filters.")
            print("Try different month/day or a different city.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            print("Goodbye ")
            break


if __name__ == "__main__":
    main()
