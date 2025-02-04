import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import SpaceTokenizer
import nltk
import pyLDAvis
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import defaultdict
# 토픽 모델링
# nltk의 불용어 리스트 다운로드
# nltk.download('punkt')
# nltk.download('stopwords')

class TopicModeling:
    def __init__(self, csv_file, num_topics=5):
        self.df = pd.read_csv(csv_file)
        self.num_topics = num_topics
        self.texts = []
        self.dictionary = None
        self.corpus = None
        self.lda_model = None
        self.space_tokenizer = SpaceTokenizer()
        
    def preprocess_texts(self):
            for text in self.df['text']:
                tokens = self.space_tokenizer.tokenize(text)
                filtered_tokens = [word for word in tokens if word.isalpha()]
                self.texts.append(filtered_tokens)

    # 단어 사전 생성 / 문서-단어 행렬 생성
    def create_dictionary_and_corpus(self):
        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]

    # LDA 모델 훈련
    def train_lda_model(self):
        self.lda_model = LdaModel(self.corpus, num_topics=self.num_topics, id2word=self.dictionary, passes=15)
        #결과 출력
        for idx, topic in self.lda_model.print_topics(-1):
            print(f"Topic {idx}: {topic}")

    # 토픽별 한글 단어 추출
    def extract_korean_words(self):
        korean_words_dict = {}
        for i in range(self.num_topics):
            topic_words = self.lda_model.show_topic(i, topn=30)
            korean_words = [word for word, prob in topic_words if re.match(r'^[가-힣]+$', word)]
            korean_words_dict[i] = korean_words
            print(f"Topic {i}: {', '.join(korean_words)}")
        return korean_words_dict



   
    # 한글 단어만 추출하여 워드클라우드 생성   
    def create_korean_wordcloud(self):
        for i in range(self.num_topics):
            plt.figure(figsize=(10, 5))
            plt.title(f'Topic {i+1}')
            # 각 주제의 단어와 중요도 추출 / 상위 30개 단어 추출
            words = self.lda_model.show_topic(i, topn=30)
            word_freq = defaultdict(float)
            # 한글 단어만 필터링하여 빈도수 저장
            for word, prob in words:
                if re.match(r'^[가-힣]+$', word):
                    word_freq[word] += prob
            
            wordcloud = WordCloud(width=800, height=400, background_color='black', font_path=r'C:/Windows/Fonts/malgun.ttf').generate_from_frequencies(word_freq)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.show()

    
    # LDA 모델 시각화
    def visualize_lda_model(self):
        vis = pyLDAvis.gensim_models.prepare(self.lda_model, self.corpus, self.dictionary)
        pyLDAvis.display(vis)
        
        
    def run(self):
        self.preprocess_texts()
        self.create_dictionary_and_corpus()
        self.train_lda_model()
        self.extract_korean_words()
        self.create_korean_wordcloud()
        self.visualize_lda_model()





