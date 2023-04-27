from itemadapter import ItemAdapter
from quotesToScrapy.spiders.scroll import ScrollSpider
from .items import Quotes
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


class QuotestoscrapyPipeline:
    def __init__(self) -> None:
        self.create_conn()
        self.create_table()

    def create_conn(self):
        self.conn = mysql.connector.connect(
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASS"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"],
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes;""")
        self.curr.execute(
            """CREATE TABLE quotes (
            id INT NOT NULL AUTO_INCREMENT,
            phrase VARCHAR(1000) NULL,
            author VARCHAR(50) NULL,
            PRIMARY KEY (id));"""
        )

    def store_items(self, item: Quotes):
        self.curr.execute(
            """INSERT INTO quotes (phrase, author) VALUES (%s, %s);""",
            (item["phrase"][0], item["author"][0]),
        )
        self.conn.commit()

    def process_item(self, item: Quotes, spider: ScrollSpider):
        self.store_items(item)
        return item
