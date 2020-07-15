## Scraper website lotto.pl (my private project :)).

New version, because page lotto.pl is updated. Now usage API www.lotto.pl/api.

Script get three games results from one request:

* Lotto
* LottoPlus
* SuperSzansa


crontab for example:
```sh
0 13 * * * python3 /path/to/script/download_lotto.py [OPTIONS] >> ~/.logs/download_lotto.log
```

## Options for script

* --game - games kind (only Lotto is default)
* --size-result - count results on page
* --page - page number of result
* --db-file - path to DB exists file


Options not implemented yet:

* --id-draw select draw from System Lotto ID
* --date-draw select draw from Date

### Runing script

Get 30 records first

```sh
python3 download_lotto.py --db-file ~/file.db --page 1 --size-result 30
```

`--page 2` get previous 30 records, etc.

## Structure file database in lotto_draws.db3.sql

You must create database file from script SQL.

Tables like games type/name lowercase:
  * lotto
  * lottoplus
  * superszansa

Columns in all tables:
  * system_id => ID draw result (lotto.pl)
  * date => date draw
  * numbers - numbers not sorted
