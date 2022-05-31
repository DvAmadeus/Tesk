import numpy as np
import pandas as pd
import datetime
from statsmodels.formula.api import ols,glm


class BigData:
    def __init__(self):
        self.first = '2020-06-24'
        self.second = '2020-09-30'
        self.first1 = '2021-07-01'
        self.second1 = '2021-08-30'
        self.교통데이터 = pd.read_csv("교통데이터.csv",encoding='cp949')
        self.날씨데이터 = pd.read_csv("555.csv",encoding='cp949')
        self.지하철데이터 = pd.read_csv('2100.csv',encoding='cp949')
        self.교통데이터처리()
        self.날씨데이터처리()
        self.지하철()

      #  self.총데이터 = pd.concat([self.지하철데이터,self.날씨데이터],axis=1)
        target = self.교통데이터['평균교통량'].to_list()
        x_data = self.날씨데이터[["일강수량(mm)",'평균기온(°C)']].reset_index()  # 변수 여러개
        del x_data['일시']
        print(x_data)
        x_data = x_data.fillna(0)
        tq = self.지하철데이터
        print(self.지하철데이터)
        print(x_data)
        data = pd.concat([self.지하철데이터,x_data])
        data.columns = ["지하철","강수량",'기온']
        data = data.fillna(0)
        print(data)
        # for b0, 상수항 추가
        data.corr(method='pearson')
        data['지하철'].corr(data['기온'])
        print("상관관계",data['지하철'].corr(data['기온']))
        # OLS 검정
        multi_model = ols("지하철 ~기온",data=data)
        fitted_multi_model = multi_model.fit()
        print(fitted_multi_model.summary())

    def 교통데이터처리(self):
        self.교통데이터['일자'] = self.교통데이터['일자'].astype(str)
        self.교통데이터['일자'] = pd.to_datetime(self.교통데이터['일자'])
        self.교통데이터 = self.교통데이터[((self.교통데이터['지점번호'] == 'C-15') & (self.교통데이터['방향'] == '유입') & (self.교통데이터['일자'] >= self.first) & (self.교통데이터['일자'] <= self.second))]
        self.새로운데이터 = self.교통데이터
        self.새로운데이터['일자'] = pd.to_datetime(self.새로운데이터['일자']).apply(lambda x: x.date())


        self.li = []
        for i in self.새로운데이터['일자'].to_list():
            if i.weekday() == 5 or i.weekday() == 6:
                self.li.append(i.strftime("%Y-%m-%d"))
        self.교통데이터['일자'] = pd.to_datetime(self.교통데이터['일자'])

        for i in self.li:
            self.교통데이터 = self.교통데이터[self.교통데이터['일자'] != i]

        self.교통데이터 = self.교통데이터.sort_values(by='일자')
        self.교통데이터 = self.교통데이터.set_index("일자")
        self.교통데이터 = self.교통데이터.fillna(1300)
        self.교통데이터["평균교통량"] = self.교통데이터.mean(axis=1)
        print(self.교통데이터)
    def 날씨데이터처리(self):
        self.날씨데이터['일시'] = self.날씨데이터['일시'].astype(str)
        self.날씨데이터['일시'] = pd.to_datetime(self.날씨데이터['일시'])

        self.날씨데이터 = self.날씨데이터[(self.날씨데이터['일시'] >= self.first) & (self.날씨데이터['일시'] <= self.second) ]

        for i in self.li:
            self.날씨데이터 = self.날씨데이터[self.날씨데이터['일시'] != i]
        self.날씨데이터 = self.날씨데이터.fillna(0)
        self.날씨데이터 = self.날씨데이터.set_index("일시")
        print("날씨", self.날씨데이터)
        
    def 지하철(self):
        self.지하철데이터['날짜'] = self.지하철데이터['날짜'].astype(str)
        self.지하철데이터['날짜'] = pd.to_datetime(self.지하철데이터['날짜'])
        self.지하철데이터 = self.지하철데이터[(self.지하철데이터['날짜'] >= self.first) & (self.지하철데이터['날짜'] <= self.second) & ((self.지하철데이터['역명'] == '공덕') & (self.지하철데이터['호선명']=='6호선') )]
        for i in self.li:
            self.지하철데이터 = self.지하철데이터[self.지하철데이터['날짜'] != i]
        self.지하철데이터 = self.지하철데이터.fillna(0)
        self.지하철데이터 = self.지하철데이터.set_index("날짜").reset_index()
        self.지하철데이터 = self.지하철데이터['승차총승객수']
        print(self.지하철데이터)




