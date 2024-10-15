import requests
from bs4 import BeautifulSoup

url = "https://duckboard.net/author/shahriaarrr"

def fetchBlogPosts():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('article')
    blogPosts = []
    for post in posts[:5]:
        title = post.find('h2').text.strip()
        link = post.find('a')['href'].strip()
        blogPosts.append(f"- 🔥 [{title}]({link})")
    
    print(f"Fetched blog posts: {blogPosts}")  # Debug print
    return blogPosts

def updateREADME(blogPosts):
    with open("README.md", "r") as readmeFile:
        content = readmeFile.readlines()

    with open("README.md", "w") as readmeFile:
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
