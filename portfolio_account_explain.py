
portfolio_account = [
                        {'전략1':
                                {
                                   '전략1로 선택한 금융상품1': [('날짜1','계좌에 있는 금융상품1을 통한 금액'),('날짜2','계좌에 있는 금융상품1을 통한 금액')],
                                   '전략1로 선택한 금융상품2': [('날짜1','계좌에 있는 금융상품2을 통한 금액'),('날짜2','계좌에 있는 금융상품2을 통한 금액')]
                                }
                        },
                        {'전략2':
                                {
                                    '전략2로 선택한 금융상품3': [('날짜1','계좌에 있는 금융상품3을 통한 금액'),('날짜2','계좌에 있는 금융상품3을 통한 금액')],
                                    '전략2로 선택한 금융상품4': [('날짜1','계좌에 있는 금융상품4을 통한 금액'),('날짜2','계좌에 있는 금융상품4을 통한 금액')]
                                }
                        },
                        {'전략3':
                                {
                                    '전략3로 선택한 금융상품5': [('날짜1','계좌에 있는 금융상품5을 통한 금액'),('날짜2','계좌에 있는 금융상품5을 통한 금액')],
                                    '전략3로 선택한 금융상품6': [('날짜1','계좌에 있는 금융상품6을 통한 금액'),('날짜2','계좌에 있는 금융상품6을 통한 금액')]
                                }
                        },
                        {
                                '포트폴리오 계좌추이':[('날짜1','계좌에 있는 포트폴리오 총 금액'),('날짜2','계좌에 있는 포트폴리오 총 금액')]
                        }
                    ]
  
print(portfolio_account[0]) # {'전략1': {'전략1로 선택한 금융상품1': [('날짜1', '계좌에 있는 금융상품1을 통한 금액'), ('날짜2', '계좌에 있는 금융상품1을 통한 금액')], '전략1로 선택한 금융상품2': [('날짜1', '계좌에 있는 금융상품2을 통한 금액'), ('날짜2', '계좌에 있는 금융상품2을 통한 금액')]}}
print(portfolio_account[0]['전략1']) # {'전략1로 선택한 금융상품1': [('날짜1', '계좌에 있는 금융상품1을 통한 금액'), ('날짜2', '계좌에 있는 금융상품1을 통한 금액')], '전략1로 선택한 금융상품2': [('날짜1', '계좌에 있는 금융상품2을 통한 금액'), ('날짜2', '계좌에 있는 금융상품2을 통한 금액')]}
print(portfolio_account[0]['전략1']['전략1로 선택한 금융상품1']) # [('날짜1', '계좌에 있는 금융상품1을 통한 금액'), ('날짜2', '계좌에 있는 금융상품1을 통한 금액')]
print(portfolio_account[0]['전략1']['전략1로 선택한 금융상품1'][0]) # ('날짜1', '계좌에 있는 금융상품1을 통한 금액')
print(portfolio_account[0]['전략1']['전략1로 선택한 금융상품1'][1]) # ('날짜2', '계좌에 있는 금융상품1을 통한 금액')
print(portfolio_account[1]) # {'전략2': {'전략2로 선택한 금융상품3': [('날짜1', '계좌에 있는 금융상품3을 통한 금액'), ('날짜2', '계좌에 있는 금융상품3을 통한 금액')], '전략2로 선택한 금융상품4': [('날짜1', '계좌에 있는 금융상품4을 통한 금액'), ('날짜2', '계좌에 있는 금융상품4을 통한 금액')]}}
print("---------------")
print(list(portfolio_account[0].keys())[0]) # 전략1
print(list(portfolio_account[1].keys())[0]) # 전략2
print(list(portfolio_account[2].keys())[0]) # 전략3