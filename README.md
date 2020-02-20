Scraper website lotto.pl (my private project :)). Only "lotto" draw results (sorted numbers).

crontab for example:
0 13 * * * python3 /path/to/script/download_lotto.py >> ~/.logs/download_lotto.log


Structure file database 'losowania.db':

Table:
  losowania (draw)

Columns:
  id_losowania => ID draw result (lotto.pl)
  data => date
  liczby => numbers

date of first record: 2017-05-25

TODO:
* download other games results (separate scripts and tables in database)
* translate to English structure DB
