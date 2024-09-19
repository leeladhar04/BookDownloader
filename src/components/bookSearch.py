from bs4 import BeautifulSoup 
import requests
# soup = BeautifulSoup("<p>Some<b>bad<i>HTML")

bookname=str(input("Book Name"))
bookname= bookname.replace(" ","+")
# https://annas-archive.org/search?q=john+c+hull
print(bookname)

url=f"https://annas-archive.org/search?q={bookname}"

response = requests.get(url)

if response.status_code==200:
    soup = BeautifulSoup(response.content, 'html.parser')
    book_link = soup.find('a', class_="js-vim-focus custom-a flex items-center relative left-[-10px] w-[calc(100%+20px)] px-2.5 outline-offset-[-2px] outline-2 rounded-[3px] hover:bg-black/6.7 focus:outline")
    href = book_link['href']
    BASE_SITE = "https://annas-archive.org"
    download_url=f"{BASE_SITE}{href}"

    book_name = book_link.find('div', class_="line-clamp-[2] leading-[1.2] text-[10px] lg:text-xs text-gray-500").text.strip()
    book_links= soup.find_all('a', class_="js-vim-focus custom-a flex items-center relative left-[-10px] w-[calc(100%+20px)] px-2.5 outline-offset-[-2px] outline-2 rounded-[3px] hover:bg-black/6.7 focus:outline")

    for books in book_links:
        print(books['href'])
        
    print(f"Book href: {href}")
    print(f"Book name: {book_name}")

    # Download the book
    download_response = requests.get(download_url)
    if download_response.status_code == 200:
        download_soup=BeautifulSoup(download_response.content,"html.parser")

        slow_download_links = download_soup.find_all('a', href=lambda x: x and '/slow_download/' in x)

        # Extract the href attribute for each link
        for link in slow_download_links:
            print(f"{BASE_SITE}{link['href']}")
    else:
        print("Failed to download book")

    # https://annas-archive.org/md5/f6427f93f0dc159c39b28b0d351ca6fa
else:
    print("Error occured")

# soup = BeautifulSoup(contents, 'html.parser')

# Find the <a> tag and extract the href
# book_link = soup.find('a', class_="js-vim-focus custom-a flex items-center relative left-[-10px] w-[calc(100%+20px)] px-2.5 outline-offset-[-2px] outline-2 rounded-[3px] hover:bg-black/6.7 focus:outline")
# href = book_link['href']

# # Find the name of the book (inside <div> with specific class)
# book_name = book_link.find('div', class_="line-clamp-[2] leading-[1.2] text-[10px] lg:text-xs text-gray-500").text.strip()

# print(f"Book href: {href}")
# print(f"Book name: {book_name}")


# url = 'https://example.com'

# # Make an HTTP request to the website
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Now you can extract specific elements, e.g., title or specific tags
#     # Example: Extract the title of the page
#     title = soup.title.string
#     print(f"Title of the page: {title}")
    
#     # Example: Find all the <a> tags (links) on the page
#     links = soup.find_all('a')
#     for link in links:
#         print(link.get('href'))