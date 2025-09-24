import requests
from bs4 import BeautifulSoup
url = "https://www.aladin.co.kr/shop/wbrowse.aspx?CID=1&BrowseTarget=List"
response = requests.get(url)  # 요청 보내기
html = response.text  # 응답 받은 HTML 문서
soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoup으로 파싱

root = soup.select_one(".browse-right") or soup  # 혹시 없으면 페이지 전체에서

# 1) 모든 책 제목 링크 수집 (각 항목의 '고유 식별자' 역할)
title_links = root.select("a.bo3")
data = []
for a in title_links:
    title = a.get_text(strip=True)
    link = a["href"] if a.has_attr("href") else None
    # 2) 제목 a태그에서 가까운 항목 컨테이너로 올라가기
    box = a.find_parent("div", class_="ss_book_box") \
       or a.find_parent("div", class_="ss_book_list") \
       or a.find_parent("li") \
       or a.parent
    # 3) 컨테이너 기준으로 세부 정보 추출 (구조 변동 대비해서 여유 선택자)
    # 가격: 알라딘은 보통 .ss_p2 또는 .price 류로 표시
    price_el = (box.select_one(".ss_p2")
                or box.select_one(".price")
                or box.find("span", class_="ss_p2"))
    price = price_el.get_text(" ", strip=True) if price_el else None
    # 평점: 별점 숫자/텍스트
    star_el = (box.select_one(".star_score")
               or box.select_one(".ss_book_list .star_score")
               or box.find(class_="star_score"))
    star = star_el.get_text(" ", strip=True) if star_el else None
    data.append([title,link,price,star])
import pandas as pd
df = pd.DataFrame(data, columns=['title', 'link', 'price', 'star'])
df
# pandas를 사용해 엑셀로 저장
df.to_excel('aladin1.xlsx',index=False)