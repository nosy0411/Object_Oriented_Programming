import GetOldTweets3 as got

# 최근 3년간(2016년 10월 15일~2019년 10월 14일) "성균관대" 키워드가 들어간 Twitter Tweet을 1000개 가져오기
tweetCriteria = got.manager.TweetCriteria().setQuerySearch("성균관대")\
    .setSince("2016-10-15")\
    .setUntil("2019-10-14")\
    .setMaxTweets(1000)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

s1 = "자연과학캠퍼스"
# tweet.text의 타입 확인(문자열로 확인됨)
# print(type(tweets[0].text))

# tweets를 돌며 반복문 수행
for t in tweets:
    # 1000개의 트윗중 하나의 트윗의 문자열을 string에 저장
    string = t.text

    # 트윗 문자열에 자연과학캠퍼스 문자가 있다면 그 트윗 출력
    if s1 in string:
        print(string)
        print("\n")
