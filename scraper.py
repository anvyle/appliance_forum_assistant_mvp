import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_threads(base_url, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    threads = []

    for page in range(1, num_pages + 1):
        url = f"{base_url.rstrip('/')}/page/{page}/"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Failed to load {url}")
            continue

        soup = BeautifulSoup(res.text, "lxml")

        for item in soup.select('li[data-controller="forums.front.forum.topicRow"]'):
            title_tag = item.select_one('.ipsDataItem_title a')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            relative_link = title_tag.get('href')
            if not isinstance(relative_link, str):
                continue

            link = urljoin(base_url, relative_link)

            thread_res = requests.get(link, headers=headers)
            if thread_res.status_code != 200:
                print(f"Failed to load thread: {link}")
                continue

            thread_soup = BeautifulSoup(thread_res.text, "lxml")
            all_post_text = []

            for post in thread_soup.select('article.cPost'):
                author_tag = post.select_one('.cAuthorPane_author')
                time_tag = post.select_one('time')
                content_tag = post.select_one('div[data-role="commentContent"]')

                author = author_tag.get_text(strip=True) if author_tag else "Unknown"
                time = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else "Unknown"

                if content_tag:
                    for quote in content_tag.select("blockquote"):
                        quote.decompose()
                    content = content_tag.get_text(separator="\n", strip=True)
                else:
                    content = "No content"

                post_string = f"{author} at {time}:\n{content}"
                all_post_text.append(post_string)

            full_thread_text = "\n\n".join(all_post_text)

            threads.append({
                "title": title,
                "url": link,
                "content": full_thread_text
            })

    return threads
