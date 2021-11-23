from bs4 import BeautifulSoup as bs
import requests
from openpyxl import Workbook

data_product = []
for page_count in range(1, 4):
    url = requests.get(
        f"https://shop.molotok.kg/product-category/elektrotovary/page/{page_count}/"
    )  # Запрос к сайту
    html = url.content  # Получение html сайта
    soup = bs(html, "html.parser")  # Создаем суп
    url_tovar = soup.find_all(name="div", class_="image")
    url_list = []
    for urls in url_tovar:
        url_list.append(urls.find(name="a"))
    url_list_2 = []
    for content in url_list:
        url_list_2.append(content.get("href"))
    for html_tovar in url_list_2:
        html_parse = requests.get(html_tovar)
        html_source = html_parse.content
        soup_2 = bs(html_source, "html.parser")

        product_title = soup_2.find(name="h2", class_="content_title").getText()
        data_product.append(product_title)

        product_description = soup_2.find(name="div", class_="text_page")
        data_product.append(product_description.find(name="p").getText())

        product_img_url = soup_2.find("img")["src"]
        data_product.append(product_img_url)



        try:
            product_price = soup_2.find(name='span', class_='woocommerce-Price-amount').getText()
            data_product.append(product_price)
            try:
                filename = product_img_url.split('/')[-1]
                dp = requests.get(product_img_url)
                open(filename, 'wb').write(dp.content)
                print('Загружен файл: ' + filename)
            except requests.exceptions.MissingSchema:
                continue
        except AttributeError:
            data_product.append('none')
            continue



def chunks(nums_list: list, chunk_size: int) -> list:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    return [nums_list[i : i + chunk_size] for i in range(0, len(nums_list), chunk_size)]


wb = Workbook()
ws = wb.active

for item in chunks(data_product, chunk_size = 4):
    ws.append(item)
wb.save("Электротовары.xlsx")