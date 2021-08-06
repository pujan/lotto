## The Scraper website lotto.pl (my private project :)).

New version, because page lotto.pl is updated. Now usage the API https://www.lotto.pl/api.

A script get three games results from one request:

* Lotto
* LottoPlus
* SuperSzansa


crontab for example:
```sh
0 13 * * * python3 /path/to/script/download_lotto.py [OPTIONS] >> ~/.logs/download_lotto.log
```

## Options for the script

* --game - games kind (only Lotto is default)
* --size-result - count results on page
* --page - page number of result
* --db-file - path to DB exists file


Options not implemented yet:

* --id-draw select draw from System Lotto ID
* --date-draw select draw from Date

### Runing the script

Get the first 30 records

```sh
python3 download_lotto.py --db-file ~/file.db --page 1 --size-result 30
```

`--page 2` get the previous 30 records, etc.

## Database file structure in lotto_draws.db3.sql

You need to create a database from a SQL script.

Tables as games types/names (lowercase):
  * lotto
  * lottoplus
  * superszansa

Columns in all tables:
  * system_id => a ID draw result (https://www.lotto.pl)
  * date => a date draw
  * numbers - numbers not sorted
