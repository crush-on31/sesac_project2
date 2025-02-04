# app.py
import streamlit as st
import pandas as pd
import sys, os
# 상위 폴더에 있는거 import
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from naver_news_crawling import NewsCrawler
from topic_modeling import TopicModeling
import pyLDAvis
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import re




# 기사 가져오기 함수
def fetch_articles_and_save(sid, file_path):
    news_url = 'https://news.naver.com/section/template/SECTION_ARTICLE_LIST'
    crawler = NewsCrawler(news_url)
    articles = crawler.fetch_articles(sid)
    nouns_data = []
    
    if articles:  # 기사가 있으면
        for idx, article in enumerate(articles, start=1):
            print(f"\nArticle {idx}/{len(articles)}")
            content = crawler.fetch_article_content(article['link'])
            if content:
                body_preview = content['body']
                nouns = crawler.extract_nouns(body_preview)
                nouns_data.append({'text': nouns})
        
        df = pd.DataFrame(nouns_data)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print("성공")
    else:
        print("기사를 가져오는 데 실패했습니다.")

# 토픽 모델링 수행 함수
def perform_topic_modeling(uploaded_file, num_topics):
    topic_modeling = TopicModeling(uploaded_file, num_topics=num_topics)
    topic_modeling.run()
    return topic_modeling

# 주제별 단어 추출 및 시각화 함수
def display_topic_words_and_visualization(topic_modeling, num_topics):
    korean_words_dict = topic_modeling.extract_korean_words()

    for i, words in korean_words_dict.items():
        st.write(f"Topic {i+1}: {', '.join(words)}")

    vis = pyLDAvis.gensim_models.prepare(topic_modeling.lda_model, topic_modeling.corpus, topic_modeling.dictionary)
    st.write(pyLDAvis.display(vis))

    for i in range(num_topics):
        st.subheader(f'Topic {i + 1} Word Cloud')
        words = topic_modeling.lda_model.show_topic(i, topn=30)
        word_freq = {word: prob for word, prob in words if re.match(r'^[가-힣]+$', word)}
        wordcloud = WordCloud(width=800, height=400, background_color='black', font_path='C:/Windows/Fonts/malgun.ttf').generate_from_frequencies(word_freq)
        st.image(wordcloud.to_array(), use_container_width=True)






def render_page(change_page):
    # 페이지 렌더링 코드
    st.title("뉴스 페이지")
    # 세션 상태 초기화
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = 0

    # 탭 선택
    tab_titles = ["정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]
    data_titles = ["politics", "economy", "society", "life", "word", "IT"]
    tabs = st.tabs(tab_titles)

    # 각 탭 실행
    for i, tab in enumerate(tabs):
        with tab:
            st.session_state.selected_tab = i  # 현재 선택된 탭 저장
            st.write(f"{tab_titles[i]} 관련 데이터를 확인하세요.")

            file_path = f'C:/python_LLM/dashboard_project/data/articles_{data_titles[i]}.csv'

            if st.button("기사 가져오기", key=f"{i}_fetch"):
                fetch_articles_and_save(100 + i, file_path)

            uploaded_file = file_path
            num_topics = st.slider("분석할 토픽 수", min_value=2, max_value=10, value=5, key=f"{i}_num_topics")

            if st.button("분석하기", key=f"{i}_analyze"):
                topic_modeling = perform_topic_modeling(uploaded_file, num_topics)
                display_topic_words_and_visualization(topic_modeling, num_topics)