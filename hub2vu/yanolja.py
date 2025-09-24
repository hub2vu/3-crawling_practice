
!pip install selenium
!pip install bs4
!pip install pandas
!pip install openpyxl
!pip install webdriver-manager



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Yanolja 리뷰 페이지로 이동
url = 'https://www.yanolja.com/reviews/domestic/10041505'
driver.get(url)

# 페이지 로딩을 위해 대기
time.sleep(3)

# 스크롤 설정: 페이지 하단까지 스크롤을 내리기
scroll_count = 10  # 스크롤 횟수 설정
for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # 스크롤 이후 대기




from bs4 import BeautifulSoup

# 웹페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')




# 리뷰 텍스트 추출
################################
tree=soup.select_one('.css-53gpk2') or soup
reviews_class = tree.select('.content-text.css-vjs6b8')
################################
reviews = []
# 각 리뷰 텍스트 정리 후 추가
for review in reviews_class:
     cleaned_text = review.get_text(strip=True).replace('\r', '').replace('\n', '')
     reviews.append(cleaned_text)
reviews






# 별점 추출
ratings = []

# ⭐ 별 아이콘 묶음 컨테이너들 선택
rating_containers = tree.select('.css-rz7kwu')   # 각 리뷰의 별 5개 영역

for container in rating_containers:
    # 컨테이너 내부에서만 '채워진 별' 세기
    # 많은 사이트에서 빈 별은 fill="none", 찬 별은 path에 fill="currentColor"가 들어갑니다.
    # filled_paths = container.select('svg path[fill="currentColor"]')
    # rating = len(filled_paths) if filled_paths is not None else 0
    stars = container.select("svg path")
    rating = 0
    for path in stars:
        if path.get("fill") == "currentColor" and path.get("fill-rule") is None:
            rating += 1
    ratings.append(rating)

print(ratings, " ... 총개수:", len(ratings))









import pandas as pd

# 별점과 리뷰를 결합하여 리스트 생성
data = list(zip(ratings, reviews))

# DataFrame으로 변환
df_reviews = pd.DataFrame(data, columns=['Rating', 'Review'])
df_reviews






# 평균 별점 계산
average_rating = df_reviews['Rating'].mean()
print("평균 별점:", average_rating)




from collections import Counter
import re

# 불용어 리스트 (한국어)
korean_stopwords = set(['이', '그', '저', '것', '들', '다', '을', '를', '에', '의', '가', '이', '는', '해', '한', '하', '하고', '에서', '에게', '과', '와', '너무', '잘', '또','좀', '호텔', '아주', '진짜', '정말'])

# 모든 리뷰를 하나의 문자열로 결합
all_reviews_text = " ".join(reviews)

# 단어 추출 (특수문자 제거)
words = re.findall(r'[가-힣]+', all_reviews_text)

# 불용어 제거
filtered_words = [w for w in words if w not in korean_stopwords]

# 단어 빈도 계산
word_counts = Counter(filtered_words)

# 자주 등장하는 상위 15개 단어 추출
common_words = word_counts.most_common(15)

print(common_words)




# 분석 결과 요약
summary_df = pd.DataFrame({
    'Average Rating': [average_rating],
    'Common Words': [', '.join([f"{word}({count})" for word, count in common_words])]
})

# 최종 DataFrame 결합
final_df = pd.concat([df_reviews, summary_df], ignore_index=True)
final_df



# Excel 파일로 저장
######## your code here ########
final_df.to_excel('yanolja.xlsx',index=False)




# 드라이버 종료
driver.quit()
