# LLM을 활용한 노래 제목 정규화 및 검색 시스템

이 프로젝트는 다양한 언어로 된 노래 제목을 OpenAI API를 통해 정규화하고, 통합 검색 기능을 제공하는 시스템입니다.

## 주요 기능
- OpenAI GPT-4o를 이용한 노래 제목 정규화
- 다국어 통합 검색
- 'all' 명령어로 전체 데이터 조회

## 설치 및 실행 방법
1.  필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
2.  `.env` 파일을 생성하고 본인의 OpenAI API 키를 입력합니다.
    ```
    OPENAI_API_KEY="sk-..."
    ```
3.  `songs.csv` 파일에 정규화할 노래 제목을 `messy_title` 헤더 아래에 추가합니다.

4.  아래 명령어로 프로그램을 실행합니다.
    ```bash
    python main.py
    ```