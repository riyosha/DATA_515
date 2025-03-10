class ScraperError(Exception):
    """Custom exception for scraper errors."""
    pass


def validate_letterboxd_user(username):
    """Validates if a Letterboxd user exists."""
    profile_url = f'https://letterboxd.com/{username}/'
    response = requests.get(profile_url, timeout=10)
    
    if response.status_code != 200:
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")
    
    if (
        error_h1 and "Letterboxd" in error_h1.text and
        error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text and
        error_body
    ):
        return False
    return True


def letterboxd_user_reviews_scraper(username):
    """Scrapes reviews of a given Letterboxd user and stores them in a CSV file."""
    profile_url = f'https://letterboxd.com/{username}/films/reviews/'
    response = requests.get(profile_url, timeout=10)
    
    if response.status_code != 200:
        raise ScraperError(f"Failed to get user profile from {profile_url}. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    page_links = soup.find_all("li", class_="paginate-page")
    last_page = max((int(link.text) for link in page_links if link.text.isdigit()), default=1)
    
    reviews = []
    
    for i in range(1, last_page + 1):
        page_url = f"{profile_url}page/{i}/"
        page_response = requests.get(page_url, timeout=10)

        if page_response.status_code != 200:
            continue
        
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        
        for element in page_soup.find_all("div", class_="film-detail-content"):
            movie_tag = element.find("h2", class_="headline-2 prettify").find("a")
            year_tag = element.find("small", class_="metadata").find("a")
            rating_tag = element.find("span", class_="rating")
            date_tag = element.find("span", class_="date")
            review_tag = element.find("div", class_="js-review-body")
            
            reviews.append([
                movie_tag.text.strip() if movie_tag else None,
                f"https://letterboxd.com{movie_tag['href']}" if movie_tag else None,
                year_tag.text.strip() if year_tag else None,
                rating_tag.text.strip() if rating_tag else None,
                date_tag.text.replace("Watched", "").strip() if date_tag else None,
                review_tag.get_text(strip=True) if review_tag else None
            ])
    
    with open(f'{username}_reviews.csv', mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Movie Name", "Movie URL", "Year", "Rating", "Watched Date", "Review"])
        writer.writerows(reviews)


def letterboxd_user_stats_scraper(username):
    """Scrapes Letterboxd user statistics and stores them in a CSV file."""
    stats_url = f'https://letterboxd.com/{username}/stats'
    response = requests.get(stats_url, timeout=10)
    
    if response.status_code != 200:
        raise ScraperError(f"Couldn't find stats for {username}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    error_h1 = soup.find("h1")
    error_strong = soup.find("strong")
    error_body = soup.find("body", class_="error message-dark")
    
    if (
        error_h1 and "Letterboxd" in error_h1.text and
        error_strong and "Sorry, we can’t find the page you’ve requested." in error_strong.text and
        error_body
    ):
        raise ScraperError(f"No stats available for {username}")
    
    stats = soup.find_all("h4", class_="yir-member-statistic statistic")
    if len(stats) < 6:
        raise ScraperError(f"Insufficient stats data for {username}")
    
    extracted_stats = [stat.text.split()[0] for stat in stats[:6]]
    
    with open(f'{username}_stats.csv', mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Number of Years", "Total Hours Watched", "Number of Directors",
            "Number of Countries", "Longest Streak (days)", "Days with 2+ Films"
        ])
        writer.writerow(extracted_stats)

