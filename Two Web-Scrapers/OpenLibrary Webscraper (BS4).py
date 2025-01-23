import requests 

from bs4 import BeautifulSoup

import mysql.connector

import os

#Get database credentials from env variables
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")


#Make the MySQL connection
db_connection=mysql.connector.connect(
    host="localhost",
    user=db_user,
    password=db_password,
)

cursor=db_connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS BookDB;")

cursor.execute("USE BookDB;")

create_bookdb_query="""
CREATE TABLE IF NOT EXISTS books(
	id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    stars FLOAT,
    rating_count INT,
    availability VARCHAR(50)
);
"""

cursor.execute(create_bookdb_query)
db_connection.commit()


base_url="https://openlibrary.org/search?subject=Accessible+book&page={}"

# List to store book data
book_data = []


# Number of pages to scrape (number is adjustable)
num_pages = 2

#Pagination
for page_num in range(1, num_pages + 1):
    url = base_url.format(page_num)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #List of all book items
        books = soup.find_all('li', class_='searchResultItem')

        for book in books:
            
            #Extracting book title
            title_element=book.find('h3', class_='booktitle')

            if title_element and title_element.find('a').text:
                title = title_element.find('a').text

            else: 
                title='Unknown Title'

            #Extracting book author
            author_element = book.find('span', class_='bookauthor')

            if author_element and author_element.find('a'):
                author = author_element.find('a').text

            else: 
                author='Unknown Author'

            
            #Extracting star count and number of ratings
            rating_element = book.find('span', itemprop='ratingValue')
            if rating_element:
                rating_text = rating_element.text.strip()
                rating_stars = float(rating_text.split(' ')[0])
                rating_count = int(rating_text.split('(')[1].split(' ')[0])


            #Confirming book availability status
            valid_cta = book.find_all('a', class_='cta-btn--available')
            for cta in valid_cta:

                if 'cta-btn--read' in cta.get('class', []):
                    status = 'Read'
                    break 
                elif 'cta-btn--borrow' in cta.get('class', []):
                    status = 'Borrow'
                    break


            #Ensure that the books included have a star count and number of ratings
            if isinstance(rating_stars, float) and isinstance(rating_count, int):
                if status and rating_stars >= 4.0 and rating_count>=100:

                    #Execute SQL query to insert into MySQL database
                    cursor.execute("""
                        INSERT INTO books (title, author, stars, rating_count, availability)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title, author, rating_stars, rating_count, status))
                    
                    # Commit the transaction
                    db_connection.commit()

cursor.close()
db_connection.close()

print("Data successfully inserted!")
            