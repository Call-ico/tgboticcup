import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_player_stats(nickname: str) -> Optional[Dict]:
    """
    Scrape player statistics from iccup.com DotA profile page.

    Args:
        nickname: The player's nickname/username on iccup.com

    Returns:
        Dictionary containing player statistics or None if player not found
    """
    url = f"https://iccup.com/dota/gamingprofile/{nickname}.html"

    try:
        # Log the scraping attempt
        logger.info(f"Scraping stats for player '{nickname}' from {url}")

        # Send the HTTP request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code != 200:
            logger.warning(f"Failed to retrieve page for {nickname}. Status code: {response.status_code}")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if profile exists
        if "Player not found" in response.text or "Profile not found" in response.text:
            logger.warning(f"Player '{nickname}' not found on iccup.com")
            return None

        # Extract player statistics
        stats = extract_player_stats(soup)

        if not stats:
            logger.warning(f"Could not extract stats for player '{nickname}'")
            return None

        logger.info(f"Successfully scraped stats for '{nickname}'")
        return stats

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when scraping stats for '{nickname}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error scraping stats for '{nickname}': {str(e)}")
        return None


def extract_player_stats(soup: BeautifulSoup) -> Dict:
    stats = {}

    try:
        # Получаем имя игрока
        username_element = soup.select_one('.profile-uname')
        if username_element:
            stats['Nickname'] = username_element.text.strip()

        # Парсим KDA сразу после ника
        kda_element = soup.select_one('.KPyTOCTb #k-num')
        if kda_element:
            stats['KDA'] = kda_element.text.strip()

        # Парсим PTS сразу после ника
        pts_element = soup.select_one('.i-pts')
        if pts_element:
            stats['PTS'] = pts_element.text.strip()

        # Извлекаем остальную статистику из таблиц
        stat_tables = soup.select('table.stata-body')

        for table in stat_tables:
            rows = table.select('tr')
            for row in rows:
                cells = row.select('td')
                if len(cells) >= 2:
                    key = cells[0].text.strip().replace(':', '')
                    if key in ["Ранк", "список игр"]:
                        continue
                    value_cell = cells[1]
                    div_d2 = value_cell.select_one('div.d2')
                    if div_d2 and div_d2.get('title'):
                        value = div_d2['title'].strip()
                    else:
                        value = value_cell.text.strip()
                    stats[key] = value

        # Парсим статус Online/Offline
        status_element = soup.select_one('.bnet-status')
        if status_element:
            status_text = status_element.get('title', 'Unknown').split(':')[-1].strip()
            stats['Status'] = status_text

        if not stats or len(stats) <= 1:
            logger.warning("Could not find any stats in the expected format")

        return stats

    except Exception as e:
        logger.error(f"Error extracting stats from HTML: {str(e)}")
        return {}



if __name__ == "__main__":
    # Пример использования
    nickname = "example_nickname"
    player_stats = get_player_stats(nickname)

    if player_stats:
        print("Player Statistics:")
        for key, value in player_stats.items():
            print(f"{key}: {value}")
    else:
        print(f"No statistics found for player '{nickname}'")
