# imports
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# get soup from url
def get_soup(url):
    '''
    Get soup from url using BeautifulSoup

    arguments:
    url (str): url of page to parse

    returns:
    soup
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Parse fighter details including name, win, loss, and draw stats
def parse_fighter_stats(soup):
    '''
    Parse fighter details including name, win, loss, and draw stats from soup.

    arguments:
    soup (html): output of get_soup()

    returns:
    fighter_details (dict): Dictionary of fighter's name and record (wins, losses, draws)
    '''
    fighter_details = {}

    # Parse fighter's name
    fighter_name = soup.find('span', class_='b-content__title-highlight')
    if fighter_name:
        fighter_details['Name'] = fighter_name.text.strip()

    # Parse fighter's win, loss, draw stats
    stats_section = soup.find('ul', class_='b-list__box-list')
    if stats_section:
        stats = stats_section.find_all('li')
        for stat in stats:
            stat_text = stat.text.strip()
            if 'wins' in stat_text.lower():
                fighter_details['Wins'] = stat_text.split(":")[1].strip()
            elif 'losses' in stat_text.lower():
                fighter_details['Losses'] = stat_text.split(":")[1].strip()
            elif 'draws' in stat_text.lower():
                fighter_details['Draws'] = stat_text.split(":")[1].strip()

    return fighter_details

# Parse and organize fighter stats from soup
def parse_and_organize_fighter_stats(soup, fighter_url):
    '''
    Parse fighter stats and organize them into a DataFrame for better analysis.

    arguments:
    soup (html): output of get_soup()
    fighter_url (str): URL of the fighter's profile

    returns:
    fighter_stats_df (DataFrame): DataFrame containing fighter name and stats (wins, losses, draws)
    '''
    fighter_details = parse_fighter_stats(soup)
    
    # Add the fighter's URL to the stats
    fighter_details['URL'] = fighter_url
    
    # Convert the dictionary into a DataFrame
    fighter_stats_df = pd.DataFrame([fighter_details])
    
    return fighter_stats_df

# Generate list of fighter URLs for scraping
def generate_fighter_urls():
    '''
    Generate a list of URLs for each fighter in the UFC roster.

    arguments:
    None

    returns:
    list_of_fighter_urls (list): List of URLs for fighters' profiles
    '''
    list_of_fighter_urls = []
    base_url = 'http://ufcstats.com/statistics/fighters?char='

    # Loop through alphabet from 'a' to 'z' to scrape fighters' details
    for character in string.ascii_lowercase:
        fighter_url = f'{base_url}{character}&page=all'
        list_of_fighter_urls.append(fighter_url)
    
    return list_of_fighter_urls

# Scrape fighter details for a list of URLs
def scrape_fighter_details(fighter_urls):
    '''
    Scrape fighter details for all URLs in the provided list.

    arguments:
    fighter_urls (list): List of fighter profile URLs

    returns:
    all_fighter_details (DataFrame): DataFrame with fighter details such as name, wins, losses, and draws
    '''
    all_fighter_details = pd.DataFrame()
    
    for url in fighter_urls:
        soup = get_soup(url)  # Get the soup for each fighter URL
        fighter_stats_df = parse_and_organize_fighter_stats(soup, url)  # Parse and organize the stats
        all_fighter_details = pd.concat([all_fighter_details, fighter_stats_df], ignore_index=True)
    
    return all_fighter_details
