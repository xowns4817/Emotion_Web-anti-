EMOTION_ANALYSIS_PROMPT = """당신은 감정 분석 전문가입니다. 사용자의 설문 응답을 분석하여 감정 상태를 정밀하게 파악해주세요.

## 설문 응답 데이터
{survey_answers}

## 분석 지침
1. 주요 감정(primary_emotion)을 다음 중 하나로 판단하세요: 기쁨, 슬픔, 불안, 분노, 평온, 피로, 외로움
2. 감정 강도(emotion_score)를 0.0~1.0 사이로 측정하세요
3. 세부 감정(emotion_detail)을 딕셔너리 형태로 각 감정별 수치를 제공하세요
4. 추천 분위기(recommended_mood)를 한 마디로 표현하세요 (예: "위로와 공감", "활력 충전", "마음의 평화")

## 응답 형식 (반드시 JSON)
{{
    "primary_emotion": "감정명",
    "emotion_score": 0.0,
    "emotion_detail": {{
        "joy": 0.0,
        "sadness": 0.0,
        "anxiety": 0.0,
        "anger": 0.0,
        "calm": 0.0,
        "fatigue": 0.0,
        "loneliness": 0.0
    }},
    "recommended_mood": "추천 분위기"
}}
"""
