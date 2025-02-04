# style.py
def apply_custom_styles():
    return  """
    <style>
    .stButton button {
        background-color: #0d8cfb;  /* 버튼 배경 색상 변경 */
        color: white;  /* 텍스트 색상 */
        font-size: 16px;  /* 텍스트 크기 */
        border-radius: 25px;  /* 버튼 모서리 둥글게 */
        padding: 8px 10px;  /* 버튼 안의 여백 */
        border: 1px solid white;  /* 버튼 테두리 색상 (원하는 색상으로 변경) */
    }
    .stButton button:hover,active {
        background-color: #0b6f34;  /* 버튼에 마우스를 올렸을 때 배경 색상 */
        color: white;  /* 텍스트 색상 */
        border: 1px solid white;  /* 버튼 테두리 색상 (원하는 색상으로 변경) */

    }
    .stButton button:active {
        color: white; /* 클릭 시 글씨 색 */
        border: 1px solid white;  /* 클릭 시 테두리 색 */
        background-color: #0b6f34; /* 클릭 시 배경색 */
    }
    </style>
    """
# tab 스타일 삽입
def apply_tab_styles():
    return  """
    <style>
    /* 사이드바 배경색 */
    .css-1d391kg {
        background-color: #0b6f34 !important; /* 사이드바 배경색 */
    }

    /* 탭 활성화 시 (선택된 탭) 색상 */
    .css-1avcm0n > div[role="tablist"] > div[aria-selected="true"] {
        color: white !important;         /* 활성화된 탭 글씨 색상 */
        background-color: #0b6f34 !important; /* 활성화된 탭 배경색 */
        border: 1px solid #0b6f34 !important; /* 활성화된 탭 테두리 색 */
        border-radius: 5px;             /* 탭 모서리 둥글게 */
    }

    /* 비활성화된 탭 색상 */
    .css-1avcm0n > div[role="tablist"] > div[aria-selected="false"] {
        color: #333333 !important;      /* 비활성화된 탭 글씨 색상 */
        background-color: #f0f0f0 !important; /* 비활성화된 탭 배경색 */
        border: 1px solid #cccccc !important; /* 비활성화된 탭 테두리 색 */
        border-radius: 5px;             /* 탭 모서리 둥글게 */
    }
    </style>
    """