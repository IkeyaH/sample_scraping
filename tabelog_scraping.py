from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import csv

options = Options()
driver = webdriver.Chrome(options=options)

# 渋谷・焼肉・飲み放題あり のページを開く
driver.get("https://tabelog.com/tokyo/A1303/A130301/rstLst/cond05-00-00/yakiniku/1/?LstReserve=0&LstSmoking=0&svd=20231118&svt=1900&svps=2&vac_net=0")
# 待機
sleep(5)
# データを取得するページ数ループ制限用
i = 0
RESTAURANT_INFO = []
HREF_LIST = []

while True:
  HREFS = driver.find_elements(By.CSS_SELECTOR, "a.list-rst__rst-name-target.cpy-rst-name")
  for HREF in HREFS:
    HREF_TITLE = HREF.get_attribute("href")
    HREF_LIST.append(HREF_TITLE)
  print("[INFO] HREF_LIST:", HREF_LIST)
  try:
    driver.find_element(By.XPATH, '//li[@class="c-pagination__item" and position()=last()]/a').click()
    i += 1
    if i == 5:
      break
  except:
    break

for EACH_LIST in HREF_LIST:
  driver.get(EACH_LIST)
  sleep(1)
  
  # タイトル
  title = driver.find_element(By.TAG_NAME, 'h1').text
  print("[INFO] title: ", title)
  
  # 評価
  try:
    rate = driver.find_element(By.CSS_SELECTOR, "span.rdheader-rating__score-val-dtl").text
  except:
    rate = str(0)
  print("[INFO] rate: ", rate)
  
  # 夜の予算 ※夜、昼でcssのセレクタが一緒なので、明確に取れるようにすべき
  try:
    night_budget = driver.find_element(By.CSS_SELECTOR, "span.c-rating-v3__val").text
  except:
    night_budget = ("undifind")
  print("[INFO] night_budget: ", night_budget)
  
  temp_array = [title, rate, night_budget]
  RESTAURANT_INFO.append(temp_array)
driver.quit()

RESTAURANT_INFO.sort(reverse=True, key=lambda x:x[1])

# 評価でソートし、csvに入れる
for EACH_RESTAURANT_INFO in RESTAURANT_INFO:
  with open('tmp.csv', 'a', newline="") as f:
    writer = csv.writer(f)
    # ※インデックス番号ではわかりにくい。ただの配列でなくrubyのハッシュのような機構を使うべきか。
    writer.writerow([EACH_RESTAURANT_INFO[0], EACH_RESTAURANT_INFO[1], EACH_RESTAURANT_INFO[2]])