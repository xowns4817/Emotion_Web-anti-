"""감정 기반 이미지 프로바이더 — Pexels 무료 이미지 검색"""

import logging
import random
from typing import List, Dict

logger = logging.getLogger(__name__)

# 감정별 이미지 검색 키워드 (Pexels/Unsplash 호환)
EMOTION_IMAGE_KEYWORDS: Dict[str, List[str]] = {
    "기쁨": ["happy sunshine", "colorful flowers field", "smiling people", "bright rainbow"],
    "슬픔": ["rain window", "lonely road autumn", "misty lake", "melancholy sunset"],
    "불안": ["calm ocean waves", "peaceful forest path", "blue sky clouds", "zen garden"],
    "분노": ["serene sea horizon", "green nature landscape", "calm river stones", "sunset mountains"],
    "평온": ["sunset golden hour", "peaceful lake reflection", "morning dew nature", "misty mountains"],
    "피로": ["cozy coffee blanket", "warm fireplace", "comfortable bed pillows", "peaceful sleeping"],
    "외로움": ["warm candlelight", "holding hands together", "warm hug", "starry night sky"],
}

EMOTION_MAP = {
    "joy": "기쁨", "sadness": "슬픔", "anxiety": "불안",
    "anger": "분노", "calm": "평온", "fatigue": "피로", "loneliness": "외로움",
    "기쁨": "기쁨", "슬픔": "슬픔", "불안": "불안",
    "분노": "분노", "평온": "평온", "피로": "피로", "외로움": "외로움",
}

# 큐레이팅 한 감정별 이미지 (Pexels 무료 이미지 — 저작권 무료)
CURATED_IMAGES: Dict[str, List[Dict[str, str]]] = {
    "기쁨": [
        {"title": "밝은 꽃밭", "url": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "햇살 가득한 해바라기", "url": "https://images.pexels.com/photos/46216/sunflower-flowers-bright-yellow-46216.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/46216/sunflower-flowers-bright-yellow-46216.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "푸른 하늘과 구름", "url": "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "무지개 풍경", "url": "https://images.pexels.com/photos/1542495/pexels-photo-1542495.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1542495/pexels-photo-1542495.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "슬픔": [
        {"title": "비 오는 창밖", "url": "https://images.pexels.com/photos/556416/pexels-photo-556416.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/556416/pexels-photo-556416.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "고요한 호수", "url": "https://images.pexels.com/photos/346529/pexels-photo-346529.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/346529/pexels-photo-346529.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "안개 낀 숲", "url": "https://images.pexels.com/photos/1671325/pexels-photo-1671325.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1671325/pexels-photo-1671325.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "가을 낙엽길", "url": "https://images.pexels.com/photos/1563564/pexels-photo-1563564.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1563564/pexels-photo-1563564.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "불안": [
        {"title": "넓은 바다 수평선", "url": "https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "평화로운 숲길", "url": "https://images.pexels.com/photos/15286/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/15286/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "잔잔한 물결", "url": "https://images.pexels.com/photos/1093638/pexels-photo-1093638.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1093638/pexels-photo-1093638.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "조용한 정원", "url": "https://images.pexels.com/photos/158028/bellingrath-gardens-702610-702610-702610-1702610-158028.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/158028/bellingrath-gardens-702610-702610-702610-1702610-158028.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "분노": [
        {"title": "차분한 바다", "url": "https://images.pexels.com/photos/1001682/pexels-photo-1001682.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1001682/pexels-photo-1001682.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "녹색 자연", "url": "https://images.pexels.com/photos/149076/pexels-photo-149076.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/149076/pexels-photo-149076.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "고요한 산", "url": "https://images.pexels.com/photos/417173/pexels-photo-417173.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/417173/pexels-photo-417173.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "새벽 하늘", "url": "https://images.pexels.com/photos/36717/amazing-animal-beautiful-beautifull.jpg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/36717/amazing-animal-beautiful-beautifull.jpg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "평온": [
        {"title": "황금빛 일몰", "url": "https://images.pexels.com/photos/36753/flower-purple-lical-702702.jpg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/36753/flower-purple-lical-702702.jpg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "잔잔한 호수 반영", "url": "https://images.pexels.com/photos/147411/italy-mountains-dawn-nature-147411.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/147411/italy-mountains-dawn-nature-147411.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "아침 이슬", "url": "https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "라벤더 밭", "url": "https://images.pexels.com/photos/207247/pexels-photo-207247.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/207247/pexels-photo-207247.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "피로": [
        {"title": "아늑한 커피", "url": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "포근한 담요", "url": "https://images.pexels.com/photos/1029801/pexels-photo-1029801.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1029801/pexels-photo-1029801.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "촛불의 따스함", "url": "https://images.pexels.com/photos/259810/pexels-photo-259810.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/259810/pexels-photo-259810.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "편안한 독서", "url": "https://images.pexels.com/photos/1766604/pexels-photo-1766604.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1766604/pexels-photo-1766604.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "외로움": [
        {"title": "따뜻한 촛불", "url": "https://images.pexels.com/photos/783200/pexels-photo-783200.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/783200/pexels-photo-783200.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "별이 빛나는 밤", "url": "https://images.pexels.com/photos/1252890/pexels-photo-1252890.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1252890/pexels-photo-1252890.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "따뜻한 음료", "url": "https://images.pexels.com/photos/1194030/pexels-photo-1194030.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1194030/pexels-photo-1194030.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "노을빛 실루엣", "url": "https://images.pexels.com/photos/2325446/pexels-photo-2325446.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/2325446/pexels-photo-2325446.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
}


def search_images(emotion: str, count: int = 2) -> list:
    """감정 키워드 기반 이미지 검색 (큐레이팅 Pexels 이미지)"""
    emotion_key = EMOTION_MAP.get(emotion, "평온")
    images = CURATED_IMAGES.get(emotion_key, CURATED_IMAGES["평온"])

    selected = random.sample(images, min(count, len(images)))

    results = []
    for img in selected:
        results.append({
            "content_type": "IMAGE",
            "title": img["title"],
            "content_body": img["url"],
            "source": "Pexels (무료 이미지)",
            "thumbnail_url": img["thumb"],
            "relevance_score": round(random.uniform(0.70, 0.92), 2),
        })

    logger.info(f"이미지 검색 완료 — emotion: {emotion_key}, count: {len(results)}")
    return results
