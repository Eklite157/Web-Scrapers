import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Enable different modes to increase efficiency
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--no-sandbox")

# Start browser and open webpage into classic novels section
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://openlibrary.org/search?subject=Accessible%20book')

#Function that extracts relevant information
def extract_books_on_page(driver):

    books_of_interest_on_page = []

    #Find all book items
    book_elements = driver.find_elements(By.CSS_SELECTOR, "li.searchResultItem")  

    for book in book_elements:
        
        #Find all books with available status
        status_elements = book.find_elements(By.CSS_SELECTOR, "a.cta-btn--available")
        status = None
        
        #Specify status 
        for element in status_elements:
            class_attr = element.get_attribute("class")
            if "read" in class_attr:
                status = "Read"
                break
            elif "borrow" in class_attr:
                status = "Borrow"
        

        if status:

            #Extract rating information
            rating_elements = book.find_elements(By.CSS_SELECTOR, "span[itemprop='ratingValue']")

            if rating_elements:
                rating_text = rating_elements[0].text.strip()

                rating_stars = float(rating_text.split(' ')[0])
                rating_count = int(rating_text.split('(')[1].split(' ')[0])

                #Filter books with valid rating
                if rating_stars >= 4 and rating_count >= 50:
                    #Extract book title
                    book_title = book.find_element(By.CSS_SELECTOR, 'h3.booktitle a').text.strip()
                    #Extract book author
                    book_author = book.find_element(By.CSS_SELECTOR, "span.bookauthor a").text.strip()
                    #Construct URL to enter each book for more information
                    book_link = book.find_element(By.CSS_SELECTOR, 'h3.booktitle a').get_attribute('href')

                    driver.get(book_link)


                    # Extract page count item
                    # If none exist, will return an empty list instead of raising an exception
                    page_count_elements = driver.find_elements(By.CSS_SELECTOR, "span[itemprop='numberOfPages']")

                    #Filter books that meet all criteria and attach the extracted information
                    if page_count_elements:
                        page_count_element=page_count_elements [0]
                        page_count = int(page_count_element.text)
                        
                        if page_count <= 800:
                            books_of_interest_on_page.append({
                                "Title": book_title,
                                "Author": book_author,
                                "Stars": rating_stars,
                                "Rating Count": rating_count,
                                "Status": status,
                                "Page Count": page_count
                            })
                
                    else:
                        books_of_interest_on_page.append({
                            "Title": book_title,
                            "Author": book_author,
                            "Stars": rating_stars,
                            "Rating Count": rating_count,
                            "Status": status,
                            "Page Count": "None"  # Indicate the absence of page count
                        })
                
                    driver.back()

    return books_of_interest_on_page

#Initialize an empty list of book data
all_books_of_interest = []

#Number is adustable
num_pages = 2

#Pagination
for page_num in range(1, num_pages + 1):

    print(f"Scraping page {page_num}...")
    page_url = f'https://openlibrary.org/search?subject=Accessible+book&page={page_num}'
    driver.get(page_url)

    #Add book information to list of book data
    books_on_page = extract_books_on_page(driver)
    all_books_of_interest.extend(books_on_page)

#Save to CSV file
df = pd.DataFrame(all_books_of_interest)
df.to_csv("books_of_interest.csv", index=False)
print(df)


driver.quit()
