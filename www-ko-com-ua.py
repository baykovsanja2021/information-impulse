# Импортируем необходимую документацию для текстового
# форматирования данных.  
import json
# Импортируем HTTP-библиотеку для Python.
import requests
# Импортируем библиотеку Python для извлечения данных из файлов HTML и XML.
from bs4 import BeautifulSoup


# Присваиваем имя переменной для адреса ссылки сайта.
seed="https://ko.com.ua/allarticles"


# Следующая функция извлекает необходимую информацию 
# из найденых обьектов.
def get_page_content(link):
    # Создаем и отправляем Request запрос на получение
    # экземпляра Response-объекта. 
    page = requests.get(link)
    # Извлекаем данные найденых обьектов из файлов HTML и XML.
    soup = BeautifulSoup(page.content, "html.parser")
    # Формируем словарь с структурой данных ивлекаемой информации.
    page_info = {
        "url": "link",  # ссылка на новость
        "title": "soup.h1.text",  # заголовок новости
        "img": "soup.find('div',class_='content artbody').img['src']",  # ссылка на изображение
        "body": "soup.find('p',class_='intro1').text",  # текст новости
        "author": "soup.find('span',class_='submitted').a.text",  # автор новости (если указывается)
        "date": "soup.find('span',class_='submitted').text.strip().split()[-4:]",  # дата публикации новости в формате DD-MM-YY
        "time": None  # время публикации новости в формате HH:MM
    }

    # Извлекаем необходимую информацию и выводим на экран.    
    url=link # Ссылка приходит на вход (уже выведена на экран).
    print(f"ссылка на статью: {url}")
    title=soup.h1.text # извлекаем заголовок.
    print(f"заголовок:{title}")
    img=soup.find('div',class_='content artbody').img['src'] # Ссылка на картинку.
    print(f'ссылка на картинку:{"https://ko.com.ua"+img}')
    body=soup.find('p',class_='intro1').text # Получаем краткое содержание текста.
    print(f"текст:{body}")
    author=soup.find('span',class_='submitted').a.text # Автор статьи.
    print(f"автор статьи:{author}")
    date=soup.find('span',class_='submitted').text.strip().split()[-4:] # Дата в формате:DD-MM-YY.
    print(f'дата:{" ".join(date)}') # при выводе на экран применяем метод для сборки строки с разделителем.
    return page_info # Возвращаем наши данные.


# Данная функция извлекает из сайта необходимые ссылки.
def get_links():
    # По HTTP-протоколу делаем запрос на получение
    # экземпляра Response-объекта.    
    r = requests.get(seed)
    # Извлекаем данные обьекта из файлов HTML и XML.
    soup = BeautifulSoup(r.content, "html.parser")
    # Создаем список для необходимых ссылок.    
    result=[]
    # С помощью цикла собираем интересующие обьекты. 
    for node in soup.find_all('div',class_='node'):   
        # Ищем элемент содержащий нужные ссылки и извлекаемую информацию.
        link=node.find("a")    
        # Добавляем в созданый список ссылку извлеченную из найденного
        # элемента применяем конкатенацию с адресом ссылки сайта.
        result.append("https://ko.com.ua"+link.get('href'))
        # Выводим на экран полученый результат.
        print("https://ko.com.ua"+link.get('href'))         
        # Возвращаем полученый результат. 
    return result  
 

# Эта функция для сохранения данных
def main():
    links = get_links() # Возьмем наши ссылки.
    top_news = [] # Cоздадим список в который будем добавлять данные.  
    for link in links: # С помощью цикла пройдемся по нашим ссылкам.
        print(f"Обрабатывается {link}") # Выводим на экран сообщение о начале обработки.
        info = get_page_content(link) # Собираем наши данные по каждой ссылке.
        top_news.append(info) # Здесь добавляем получаемые данные в список.
    
    with open("www-news-com.json", "wt") as f: # Открываем json файл.
         json.dump(top_news, f )# форматируем данные в json файл.
    print("Работа завершена") # Выводим на экран сообщение о завершении работы.

# Главнаю функция.
if __name__ == "__main__": # Если выполняется данное условие.
    main() # Выполняем главную функцию.