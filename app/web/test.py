from flask import jsonify, request, render_template, flash
from app.view_models.book import BookCollection, BookViewModel
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.web import web

yushu_book = YuShuBook()
isbn = 9787229030933
yushu_book.search_by_isbn(isbn)
book = BookViewModel(yushu_book.first)
print(book)