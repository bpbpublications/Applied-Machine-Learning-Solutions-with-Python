from typing import List
import uuid
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Scrapper:
    def __init__(self, url: str) -> None:
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), 
                                        options=options)
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def change_page(self, menu_item_xpath: str) -> None:
        sel_el = self.driver.find_element_by_xpath(menu_item_xpath)
        sel_el.click()
    
    def get_soup(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def expand(self) -> bool:
        try:
            expand = self.driver.find_element_by_xpath("/html/body/div[1]/div/button")
            expand.click()
            return True
        except Exception as err:
            print(err)
            return False

    def get_headline(self, headline_soup: BeautifulSoup) -> str: 
        return headline_soup.find('span', attrs={"itemprop": "headline"}).string
    
    def get_article(self, article_soup: BeautifulSoup) -> str: 
        return article_soup.find('div', attrs={"itemprop": "articleBody"}).string
    
    def get_all_headlines(self, soup: BeautifulSoup) -> bs4.element.ResultSet:
        return soup.find_all('div', class_=["news-card-title news-right-box"])
    
    def get_all_articles(self, soup: BeautifulSoup) -> bs4.element.ResultSet: 
        return soup.find_all('div', class_=["news-card-content news-right-box"])
    
    def get_data_from_page(self, category: str) -> dict:
        soup = self.get_soup()
        headlines, articles = self.get_all_headlines(soup), self.get_all_articles(soup)
        
        resp = [
            { 
                "category": category,
                "summary": self.get_headline(hsoup),
                "article": self.get_article(asoup)
            } 
                for hsoup, asoup in zip(headlines, articles)
        ]
        return resp
    
    def get_categories(self, soup: BeautifulSoup) -> List[str]:
        try:
            categories = [   c.text.strip() for c in 
                soup.find('ul', class_=["category-list"]).find_all('a')
            ]
            return categories[1:] # excluding All News
        except Exception as err:
            return []

    def build_summarization_dataset(self) -> List[dict]:
        soup = self.get_soup()
        summary_dataset = []
        if self.expand():
            for c in self.get_categories(soup):
                category_xpath = f"//li[text()='{c}']"
                self.driver.find_element_by_xpath(category_xpath).click()
                resp = self.get_data_from_page(c)
                summary_dataset.extend(resp)
                if not self.expand(): break
        return summary_dataset

    def get_full_text(self): pass
    def load_more(self): 
        try:
            self.driver.find_element_by_id("load_more_btn").click()
        except NoSuchElementException:
            print("[ INFO ] No more load more!")
            return

if __name__ == "__main__":
    url = "https://inshorts.com/en/read"
    crawler = Scrapper(url)
    sd = crawler.build_summarization_dataset()
    df = pd.DataFrame(sd)
    name = str(uuid.uuid4())
    df.to_csv(f"scrapped_inshorts_{name}.csv", index=False)
    crawler.driver.quit()

