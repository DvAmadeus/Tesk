import numpy as np
import pandas  as pd
import holidays
import datetime
import statsmodels.api as sm


class BigData:
    def __init__(self):
        self.first = '2020-07-01'
        self.second = '2020-08-30'
        self.first1 = '2021-07-01'
        self.second1 = '2021-08-30'
        self.교통데이터 = pd.read_csv("교통데이터.csv",encoding='cp949')
        self.날씨데이터 = pd.read_csv("555.csv",encoding='cp949')
        self.지하철데이터 = pd.read_csv('2100.csv',encoding='cp949')
        self.교통데이터처리()
        self.날씨데이터처리()

      #  self.총데이터 = pd.concat([self.지하철데이터,self.날씨데이터],axis=1)
        self.총데이터 = pd.concat([self.날씨데이터, self.교통데이터], axis=1)
        print(self.총데이터)
        X = self.총데이터['일강수량(mm)'].to_list()
        Y = self.총데이터['교통량'].to_list()
        results = sm.OLS(Y, sm.add_constant(X)).fit()
        print(results.summary())
        self.총데이터.corr(method="pearson")



    def 교통데이터처리(self):
        self.교통데이터['일자'] = self.교통데이터['일자'].astype(str)
        self.교통데이터['일자'] = pd.to_datetime(self.교통데이터['일자'])
        self.교통데이터 = self.교통데이터[((self.교통데이터['지점번호'] == 'C-14') & (self.교통데이터['방향'] == '유입') & (self.교통데이터['일자'] >= self.first) & (self.교통데이터['일자'] <= self.second)) | ((self.교통데이터['일자'] >= self.first1) & (self.교통데이터['일자'] <= self.second1))]
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
        self.교통데이터 = self.교통데이터.mean(axis=1)
        self.교통데이터 = self.교통데이터.to_frame().fillna(1300)

        self.교통데이터.columns = ['교통량']

    def 날씨데이터처리(self):
        self.날씨데이터['일시'] = self.날씨데이터['일시'].astype(str)
        self.날씨데이터['일시'] = pd.to_datetime(self.날씨데이터['일시'])
        self.날씨데이터 = self.날씨데이터[(self.날씨데이터['일시'] >= self.first) & (self.날씨데이터['일시'] <= self.second) | ((self.날씨데이터['일시'] >= self.first1) & (self.날씨데이터['일시'] <= self.second1))]
        for i in self.li:
            self.날씨데이터 = self.날씨데이터[self.날씨데이터['일시'] != i]
        self.날씨데이터 = self.날씨데이터.fillna(0)
        self.날씨데이터 = self.날씨데이터.set_index("일시")
        self.날씨데이터 = self.날씨데이터['일강수량(mm)']
    def 지하철(self):
        self.지하철데이터['날짜'] = self.지하철데이터['날짜'].astype(str)
        self.지하철데이터['날짜'] = pd.to_datetime(self.지하철데이터['날짜'])
        self.지하철데이터 = self.지하철데이터[(self.지하철데이터['날짜'] >= self.first) & (self.지하철데이터['날짜'] <= self.second) | ((self.지하철데이터['역명'] == '서울역') & (self.지하철데이터['호선명']=='1호선') & (self.지하철데이터['날짜'] >= self.first1) & (self.지하철데이터['날짜'] <= self.second1))]
        for i in self.li:
            self.지하철데이터 = self.지하철데이터[self.지하철데이터['날짜'] != i]
        self.지하철데이터 = self.지하철데이터.fillna(0)
        self.지하철데이터 = self.지하철데이터.set_index("날짜")
        self.지하철데이터 = self.지하철데이터['승차총승객수']




