import GetOldTweets3 as got

# 최근 1년간(2018년 10월 15일~2019년 10월 14일) "자동차" 키워드가 들어간 Twitter Tweet을 1000개 가져오기
tweetCriteria = got.manager.TweetCriteria().setQuerySearch("자동차")\
    .setSince("2018-10-15")\
    .setUntil("2019-10-14")\
    .setMaxTweets(1000)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

# 찾을 문자 지정
s1 = "기아"
s2 = "현대"
s3 = "쉐보레"
s4 = "쌍용"

# 찾은 문자의 개수
c1 = 0
c2 = 0
c3 = 0
c4 = 0

# tweet.text의 타입 확인(문자열로 확인됨)
# print(type(tweets[0].text))

# tweets를 돌며 반복문 수행
for t in tweets:
    # 1000개의 트윗중 하나의 트윗의 문자열을 string에 저장
    string = t.text

    # count를 이용해서 문자열에 특정 문자가 몇개 있는지 찾아서 그 수만큼 더해서 저장.
    c1 += string.count(s1)
    c2 += string.count(s2)
    c3 += string.count(s3)
    c4 += string.count(s4)

# 각 문자가 1000개의 트윗중 몇번 들어있는지 출력
print("%s : %d회" % (s1, c1))
print("%s : %d회" % (s2, c2))
print("%s : %d회" % (s3, c3))
print("%s : %d회" % (s4, c4))
