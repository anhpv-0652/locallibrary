from datetime import date

# Dành cho Model Genre
GENRE_NAME_MAX_LENGTH = 200
# Dành cho Model Book
BOOK_TITLE_MAX_LENGTH = 200
BOOK_SUMMARY_MAX_LENGTH = 1000
BOOK_ISBN_MAX_LENGTH = 13
# Dành cho Model Author
AUTHOR_NAME_MAX_LENGTH = 100
# Dành cho Model BookInstance
IMPRINT_MAX_LENGTH = 200
LOAN_STATUS_MAX_LENGTH = 1
LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
)
MAINTENANCE = 'm'
ON_LOAN = 'o'
AVAILABLE = 'a'
RESERVED = 'r'

BOOK_LIST_VIEW_PAGINATE = 10
DEFAULT_DATE_OF_DEATH = date(2020, 6, 11)
