import requests
import lxml.html

def lxml_page(html_text):
    tree = lxml.html.document_fromstring(html_text)
    text_original = tree.xpath("/html//text()")
    converted_list = []

    #removing unnecessary values in list
    for element in text_original:
        converted_list.append(element.strip())
    while '' in converted_list:
        converted_list.remove('')
    
    #removing "\n" in list
    symbols_removed = []
    for i in converted_list:
        symbols_removed.append(i.replace("\n", ""))

    #removing spaces in list
    spaces_removed = []
    for y in symbols_removed:
        spaces_removed.append(y.replace("   ", ""))
    print(spaces_removed)

def main():
    url = "https://urfu.ru/api/schedule/groups/lessons/985237/20211017/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html_text = requests.get(url, headers=headers).text
    lxml_page(html_text)

if __name__ == "__main__":
    main()

