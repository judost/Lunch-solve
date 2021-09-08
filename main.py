import pandas as pd # 전처리를 위한
import matplotlib.pyplot as plt # 도표화를 위한
import seaborn as sns # 표에 색을 입히는
import warnings # 경고 무시
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning) # 경고 무시
plt.rc('font', family='Malgun Gothic') # 글꼴 설정
df = pd.read_csv('seoul.csv') # 파일 부르기
way = df['payment_method'].str.contains('카드')
way = df['payment_method'].str.contains('현금')
way = df['payment_method'].str.contains('제로페이')
df_card = df[way] # way(카드, 현금, 제로페이)에 있는 것 넣기
df_card_m = df_card[['exec_loc','exec_amount']] # way 중 loc, amount 선택
df_copy = df_card_m[['exec_loc']] # 복사해서 수정하기
df_copy = df_copy.apply(lambda x: x.str.strip('㈜')) # ㈜ 삭제
df_copy = df_copy.replace(r'\([^)]+\)','',regex=True) # 괄호 안의 내용 삭제
df_card_m[['exec_loc']] = df_copy # 수정한 내용 넣기 (업데이트)
df_card_m = df_card_m.loc[df_card_m['exec_loc'].notnull()] # 결측치 제거
df_card_m.reset_index(drop=True,inplace=True) # 데이터 인덱스 순서 재조정
most_visit = df_card_m['exec_loc'].value_counts() # 방문 횟수 세기
best_payment = df_card_m.groupby('exec_loc')['exec_amount'].agg(sum).astype('int64').nlargest(30) # (loc에 있는 amount의 중복된 값을 합친다. / 큰 순서 정렬)
colors = sns.color_palette('gist_rainbow',30) # 색 설정
plt.subplot(2,1,1) # 위쪽 화면의 반 위치
most_visit.head(30).plot.bar(x=best_payment, color = colors, align='edge', edgecolor='#F0F8FF',title='Best visit', figsize=(20,10)) # 30개 내용 표(막대그래프) 그리기 & 표 색 설정 & 막대 바깥 선 색 설정
plt.ylabel('방문 횟수', fontsize=10) # y축에 부연 설명 적기
plt.subplot(2,1,2) # 아래 화면의 반 위치
best_payment.plot.bar(color=colors, align='edge', edgecolor='#F0F8FF', title='Best payment', figsize=(20,10))
plt.xlabel('가게명', fontsize=10) # x축에 부연 설명 적기
plt.ylabel('금액 (단위 : 백만원)', fontsize=10)
plt.show() # 표 그리기