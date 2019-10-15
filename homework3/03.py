import GetOldTweets3 as got

# 최근 3년간(2016년 10월 15일~2019년 10월 14일) 문재인 대통령의 Twitter Tweet을 1000개 가져오기
tweetCriteria = got.manager.TweetCriteria().setUsername("moonriver365")\
    .setSince("2016-10-15")\
    .setUntil("2019-10-14")\
    .setMaxTweets(1000)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

s1 = "북한"
s2 = "위안부"
l1 = list()
l2 = list()
# tweet.text의 타입 확인(문자열로 확인됨)
# print(type(tweets[0].text))

# tweets1를 돌며 반복문 수행
for t in tweets:
    # 1000개의 트윗중 하나의 트윗의 문자열을 string에 저장
    string = t.text

    # 트윗 문자열에 북한 문자가 있다면 그 트윗 l1에 저장
    if s1 in string:
        l1.append(string)
    # 트윗 문자열에 위안부 문자가 있다면 그 트윗 l2에 저장
    if s2 in string:
        l2.append(string)

# 북한과 위안부 토픽에 관한 저장된 트윗 문자열 출력
print("북한 Topic")
print("----------------------------------------------------")
for i in range(len(l1)):
    print(l1[i])
print("----------------------------------------------------")
print("위안부 Topic")
print("----------------------------------------------------")
for i in range(len(l2)):
    print(l2[i])
print("----------------------------------------------------")
