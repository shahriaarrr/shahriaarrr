import re
import random
import requests
from bs4 import BeautifulSoup

url = "https://duckboard.net/author/shahriaarrr"

emojis = ["🔥", "🌟", "🚀", "💻", "📚", "🎉", "✨", "📝"]

def fetchBlogPosts():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Use the provided selector to find post containers
    posts = soup.select(".uael-post__thumbnail")
    blogPosts = []

    for post in posts[:5]:
        # Find the 'a' tag within each post container
        link_tag = post.find("a")
        if link_tag:
            title = link_tag.get("title", "").strip()
            link = link_tag.get("href", "").strip()
            if title and link:
                title = re.sub(r"[\u200b-\u200d\ufeff]", "", title)
                # Select a random emoji
                random_emoji = random.choice(emojis)
                blogPosts.append(f"- {random_emoji} [{title}]({link})")

    print(f"Fetched blog posts: {blogPosts}")  # Debug print
    return blogPosts

def updateREADME(blogPosts):
    with open("README.md", "r", encoding="utf8") as readmeFile:
        content = readmeFile.readlines()

    with open("README.md", "w", encoding="utf8") as readmeFile:
        insideBlogSection = False
        for line in content:
            if line.strip() == "<!-- BLOGPOSTS:START -->":
                insideBlogSection = True
                readmeFile.write(line)
                print("Updating blog posts in README...")  # Debug print
                for post in blogPosts:
                    readmeFile.write(f"{post}\n")
            elif line.strip() == "<!-- BLOGPOSTS:END -->":
                insideBlogSection = False
                readmeFile.write(line)
            elif not insideBlogSection:
                readmeFile.write(line)

if __name__ == "__main__":
    blogPosts = fetchBlogPosts()
    updateREADME(blogPosts)

