from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_book_details(book_name):
    book_name = book_name.replace(" ", "+")
    url = f"https://annas-archive.org/search?q={book_name}"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all book links and images
        all_book_links = soup.find_all('a', class_="js-vim-focus custom-a flex items-center relative left-[-10px] w-[calc(100%+20px)] px-2.5 outline-offset-[-2px] outline-2 rounded-[3px] hover:bg-black/6.7 focus:outline")
        images = soup.find_all('img')

        book_links = []
        for book_link in all_book_links:
            href = book_link['href']
            BASE_SITE = "https://annas-archive.org"
            download_url = f"{BASE_SITE}{href}"

            # Extract the name or other info from the link
            book_name = book_link.find('div', class_="line-clamp-[2] leading-[1.2] text-[10px] lg:text-xs text-gray-500").text.strip()
            
            book_links.append({
                'name': book_name,
                'url': download_url
            })

        # Limit images to the number of books
        image_links = [img.get('src') for img in images][:len(book_links)]

        return book_links, image_links
    return [], []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_links, image_links = fetch_book_details(book_name)

        # Pair each book with its corresponding image
        results = [{'book': book, 'image': image} for book, image in zip(book_links, image_links)]

        if results:
            return render_template('results.html', results=results)
        else:
            return "No results found or error occurred", 404

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0")
