import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv
import time

# --- Part 1: API 키 설정 및 클라이언트 초기화 ---
load_dotenv()
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("✅ OpenAI API 클라이언트 초기화 성공!")
except Exception as e:
    print(f"❌ API 키 설정 오류: {e}")
    exit()

# --- Part 2: 최종 데이터 정규화 함수 ---
def normalize_title_final(messy_title):
    """OpenAI API를 호출하여 노래 제목을 4가지 지정된 형태로 정규화합니다."""
    prompt = f"""
    You are a meticulous music metadata specialist AI. Your task is to process a given song title and return a JSON object with four specific fields: "original_title", "english_title", "japanese_title", and "korean_title".

    ## Field Descriptions:
    - "original_title": The title in its absolute original language of release.
    - "english_title": The official English title. If none exists, use the standard Romaji transliteration.
    - "japanese_title": The title written in Japanese characters. If the original is not Japanese, provide the common Japanese transliteration.
    - "korean_title": The official Korean title. If none exists, provide the standard Korean phonetic transliteration.
    - If a field is not applicable, use null.

    ## Examples:
    - Input: "Pretender"
      Output: {{"original_title": "Pretender", "english_title": "Pretender", "japanese_title": "プリテンダー", "korean_title": "프리텐더"}}
    - Input: "宿命"
      Output: {{"original_title": "宿命", "english_title": "Destiny", "japanese_title": "宿命", "korean_title": "숙명"}}

    ---
    ## Process this title:
    {messy_title}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ '{messy_title}' 처리 중 API 오류 발생: {e}")
        return None

# --- Part 3: 데이터 로딩 및 정규화 실행 ---
try:
    df = pd.read_csv('songs.csv')
    print(f"\n✅ 'songs.csv'에서 {len(df)}개의 데이터를 읽었습니다.")
except FileNotFoundError:
    print("❌ 'songs.csv' 파일을 찾을 수 없습니다.")
    exit()

print("\n⏳ 최종 데이터 정규화를 시작합니다...")
normalized_db = []
for title in df['messy_title']:
    print(f"  - '{title}' 정규화 중...")
    normalized_data = normalize_title_final(title)
    if normalized_data:
        normalized_db.append({'input_title': title, **normalized_data})
    time.sleep(1)

print("\n✅ 데이터 정규화 완료!")

# --- Part 4: 검색 기능 함수 ---
def search_song(query, db):
    """정규화된 DB에서 모든 언어로 노래를 검색합니다."""
    results = []
    query_lower = query.lower()
    for song_data in db:
        searchable_texts = [
            song_data.get('input_title'),
            song_data.get('original_title'),
            song_data.get('english_title'),
            song_data.get('japanese_title'),
            song_data.get('korean_title')
        ]
        for text in searchable_texts:
            if text and query_lower in text.lower():
                results.append(song_data)
                break
    return results

# --- Part 5: 사용자 검색 인터페이스 ---
print("\n🎶 통합 노래 검색 시스템 (전체보기: 'all', 종료: 'exit' 입력)")
while True:
    search_query = input("검색할 노래 제목을 입력하세요: ")
    
    if search_query.lower() == 'exit':
        print("프로그램을 종료합니다.")
        break
    
    # 'all' 명령어 추가: 전체 데이터 보기
    elif search_query.lower() == 'all':
        if not normalized_db:
            print("\n❌ 표시할 데이터가 없습니다.")
            continue
            
        print(f"\n--- 전체 정규화 데이터 ({len(normalized_db)}개) ---")
        for song in normalized_db:
            print(f"  - 원본 입력: {song['input_title']}")
            print(f"    - Original: {song['original_title']}")
            print(f"    - English: {song['english_title']}")
            print(f"    - Japanese: {song['japanese_title']}")
            print(f"    - Korean: {song['korean_title']}")
        print("---------------------------------")
        continue

    found_songs = search_song(search_query, normalized_db)
    
    if found_songs:
        print(f"\n✅ '{search_query}'에 대한 검색 결과:")
        for song in found_songs:
            print(f"  - 원본 입력: {song['input_title']}")
            print(f"    - Original: {song['original_title']}")
            print(f"    - English: {song['english_title']}")
            print(f"    - Japanese: {song['japanese_title']}")
            print(f"    - Korean: {song['korean_title']}")
    else:
        print(f"\n❌ '{search_query}'에 대한 검색 결과가 없습니다.")