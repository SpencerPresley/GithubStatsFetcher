import requests
from collections import defaultdict
from dotenv import load_dotenv
import os

load_dotenv()

# Instructions:
# 1) Generate a GitHub access token
# 2) Make a '.env' file
# 3) In .env do: GH_ACCESS_TOKEN={your access token here}
headers = {
    'Authorization': f'token {os.getenv("GH_ACCESS_TOKEN")}',
    'Accept': 'application/vnd.github.v3+json',
}

def fetch_repos(username):
    """Fetch repositories for a given user."""
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_languages(repo):
    """Fetch languages for a given repository."""
    languages_url = repo['languages_url']
    response = requests.get(languages_url, headers=headers)
    return response.json()

def calculate_language_stats(username):
    """Calculate language statistics across all repositories."""
    repos = fetch_repos(username=username)
    #print("check")
    #print(repos)
    lang_stats = defaultdict(int)
    
    for repo in repos:
        languages = fetch_languages(repo)
        for lang, bytes_of_code in languages.items():
            lang_stats[lang] += bytes_of_code
    
    total_bytes = sum(lang_stats.values())
    for lang, bytes_of_code in lang_stats.items():
        print(f"{lang}: {bytes_of_code / total_bytes:.2%}")
        
    lang_percentages = {lang: bytes_of_code / total_bytes for lang, bytes_of_code in lang_stats.items()}
    svg_img(lang_percentages)

def svg_img(lang_stats):
    """Generate an SVG image based on language stats."""
    max_width = 200  # Max width of the bar
    height_per_item = 20  # Height per language item
    svg_items = []
    
    svg_background = f'<rect width="100%" height="100%" fill="white"/>'
    svg_items.append(svg_background)
    
    y = 0
    for lang, percentage in lang_stats.items():
        width = max_width * percentage
        svg_item = f'<rect x="0" y="{y}" width="{width}" height="15" style="fill:blue;"/>' \
                   f'<text x="{width + 5}" y="{y + 10}" fill="black">{lang}: {percentage:.2%}</text>'
        svg_items.append(svg_item)
        y += height_per_item
    
    svg_height = len(lang_stats) * height_per_item
    svg_template = f'<svg width="{max_width + 300}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">' \
                   f'{" ".join(svg_items)}</svg>'
    
    with open("language_stats.svg", "w") as file:
        file.write(svg_template)
    print("SVG image generated.")
# Replace 'SpencerPresley' with your GitHub username
if __name__ == '__main__':
    calculate_language_stats('SpencerPresley')
    
