directory=/www/wwwroot/crawler.news.gift.one/
fileArr=("cointime_krwiki.py" "kr_cointoday.py" "venturetimes_jpwiki.py" "cointime_jpwiki.py" "blockmedia.py" "btcnews.py" "cointelegraph.py" "coinchoice.py" "cointime.py" "jinse.py" "jp_coinpost.py" "jp_venturetimes.py" "kr_webdaily.py" "us_cryptonews.py" "jinniu.py")
for f in ${fileArr[@]};do
	echo $f >> $(date +%y%m%d).log
	python3 ${directory}$f
done
