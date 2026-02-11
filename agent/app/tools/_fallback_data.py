"""Brave Search MCP 호출 실패 시 사용하는 폴백 데이터"""

FALLBACK_QUOTES = {
    "기쁨": [
        {"title": "행복은 습관이다", "body": "행복은 목적지가 아니라 여행 방식이다.", "author": "마거릿 리 런벡"},
        {"title": "감사의 힘", "body": "감사할 줄 아는 사람이 더 많은 것을 얻는다.", "author": "오프라 윈프리"},
        {"title": "기쁨의 발견", "body": "기쁨은 단순한 것들 속에 숨어 있다.", "author": "작자 미상"},
        {"title": "웃음의 가치", "body": "웃음은 영혼의 음악이다.", "author": "윌리엄 셰익스피어"},
        {"title": "긍정의 에너지", "body": "긍정적인 생각은 긍정적인 삶을 만든다.", "author": "노먼 빈센트 필"},
    ],
    "슬픔": [
        {"title": "비 온 뒤 무지개", "body": "비가 오지 않으면 무지개도 없다.", "author": "돌리 파튼"},
        {"title": "슬픔의 가치", "body": "슬픔을 느낄 수 있다는 것은 살아있다는 증거다.", "author": "작자 미상"},
        {"title": "위로의 말", "body": "힘든 시간은 지나가고 좋은 시간이 올 거예요.", "author": "작자 미상"},
        {"title": "상처와 치유", "body": "상처가 빛이 들어오는 곳이다.", "author": "루미"},
        {"title": "내일의 희망", "body": "오늘의 슬픔이 내일의 힘이 됩니다.", "author": "빅토르 위고"},
    ],
    "불안": [
        {"title": "걱정의 진실", "body": "걱정의 90%는 실제로 일어나지 않는다.", "author": "마크 트웨인"},
        {"title": "호흡의 힘", "body": "깊은 호흡을 하세요. 당신은 지금 이 순간 안전합니다.", "author": "틱낫한"},
        {"title": "천천히 괜찮아", "body": "불안은 미래에 대한 과도한 걱정일 뿐, 지금 이 순간에 집중하세요.", "author": "작자 미상"},
        {"title": "용기란", "body": "용기란 두려움이 없는 것이 아니라, 두려움보다 중요한 것이 있다고 판단하는 것이다.", "author": "앰브로스 레드문"},
        {"title": "지금 여기", "body": "과거는 이미 갔고, 미래는 아직 오지 않았다. 지금 이 순간만이 진짜다.", "author": "붓다"},
    ],
    "분노": [
        {"title": "감정의 주인", "body": "화가 날 때는 10까지 세어라. 매우 화가 나면 100까지 세어라.", "author": "토마스 제퍼슨"},
        {"title": "내려놓음", "body": "분노를 붙잡고 있는 것은 불타는 석탄을 쥐는 것과 같다.", "author": "붓다"},
        {"title": "평화의 선택", "body": "분노는 자신에게 독을 마시고 상대가 죽기를 바라는 것이다.", "author": "넬슨 만델라"},
        {"title": "용서의 힘", "body": "용서는 상대를 위한 것이 아니라, 자신을 자유롭게 하는 것이다.", "author": "루이스 스메데스"},
        {"title": "차가운 물", "body": "뜨거운 분노에는 차가운 이성의 물을 부어야 한다.", "author": "세네카"},
    ],
    "평온": [
        {"title": "고요한 마음", "body": "고요함 속에서 진정한 자신을 발견할 수 있습니다.", "author": "노자"},
        {"title": "바람처럼", "body": "바람처럼 자유롭게, 물처럼 유연하게 흘러가세요.", "author": "브루스 리"},
        {"title": "자연의 리듬", "body": "자연은 서두르지 않지만, 모든 것을 이루어낸다.", "author": "노자"},
        {"title": "내면의 평화", "body": "외부에서 평화를 찾지 마라, 내면에서 찾아라.", "author": "붓다"},
        {"title": "고요한 행복", "body": "가장 큰 행복은 마음이 평온할 때 온다.", "author": "달라이 라마"},
    ],
    "피로": [
        {"title": "쉬어가도 괜찮아", "body": "쉬는 것은 게으름이 아니라 재충전입니다.", "author": "작자 미상"},
        {"title": "자기 돌봄", "body": "자신을 돌보는 것은 이기적인 것이 아닙니다. 그것은 필수입니다.", "author": "오드리 로드"},
        {"title": "충분한 나", "body": "오늘 최선을 다했다면, 그것으로 충분합니다.", "author": "작자 미상"},
        {"title": "멈춤의 가치", "body": "가끔은 멈추어야 더 멀리 갈 수 있다.", "author": "작자 미상"},
        {"title": "에너지 충전", "body": "빈 컵으로는 다른 사람의 컵을 채울 수 없다. 먼저 자신을 채우세요.", "author": "작자 미상"},
    ],
    "외로움": [
        {"title": "혼자가 아닌 나", "body": "외로움은 혼자라는 뜻이 아니라, 누군가와 연결되고 싶다는 마음입니다.", "author": "작자 미상"},
        {"title": "소중한 나", "body": "당신은 사랑받을 자격이 있는 사람입니다.", "author": "작자 미상"},
        {"title": "고독의 선물", "body": "고독은 자신을 만나는 가장 깊은 방법이다.", "author": "폴 틸리히"},
        {"title": "별과 당신", "body": "밤하늘의 별도 하나하나 떨어져 있지만, 함께 빛나고 있잖아요.", "author": "작자 미상"},
        {"title": "연결된 세상", "body": "세상은 보이지 않는 실로 모두 연결되어 있다. 당신도 그 일부입니다.", "author": "작자 미상"},
    ],
}

FALLBACK_VIDEOS = {
    "기쁨": [
        {"title": "기분 좋아지는 음악 모음", "url": "https://www.youtube.com/results?search_query=기분좋은+음악", "thumbnail": None},
        {"title": "행복 에너지 충전 영상", "url": "https://www.youtube.com/results?search_query=행복한+영상", "thumbnail": None},
    ],
    "슬픔": [
        {"title": "마음 위로하는 피아노 음악", "url": "https://www.youtube.com/results?search_query=위로+피아노+음악", "thumbnail": None},
        {"title": "감성 힐링 영상", "url": "https://www.youtube.com/results?search_query=감성+힐링", "thumbnail": None},
    ],
    "불안": [
        {"title": "불안 해소 명상 가이드", "url": "https://www.youtube.com/results?search_query=불안해소+명상", "thumbnail": None},
        {"title": "자연 소리 ASMR", "url": "https://www.youtube.com/results?search_query=자연소리+ASMR", "thumbnail": None},
    ],
    "분노": [
        {"title": "분노 조절 명상", "url": "https://www.youtube.com/results?search_query=분노조절+명상", "thumbnail": None},
        {"title": "차분해지는 자연 영상", "url": "https://www.youtube.com/results?search_query=차분한+자연", "thumbnail": None},
    ],
    "평온": [
        {"title": "평화로운 일몰 타임랩스", "url": "https://www.youtube.com/results?search_query=일몰+타임랩스", "thumbnail": None},
        {"title": "잔잔한 재즈 모음", "url": "https://www.youtube.com/results?search_query=잔잔한+재즈", "thumbnail": None},
    ],
    "피로": [
        {"title": "숙면 백색 소음", "url": "https://www.youtube.com/results?search_query=백색소음+수면", "thumbnail": None},
        {"title": "스트레칭 루틴", "url": "https://www.youtube.com/results?search_query=스트레칭+루틴", "thumbnail": None},
    ],
    "외로움": [
        {"title": "따뜻한 에세이 읽어드립니다", "url": "https://www.youtube.com/results?search_query=위로+에세이", "thumbnail": None},
        {"title": "공감 힐링 영상", "url": "https://www.youtube.com/results?search_query=공감+힐링", "thumbnail": None},
    ],
}

FALLBACK_IMAGES = {
    "기쁨": [
        {"title": "밝은 꽃밭", "url": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/462118/pexels-photo-462118.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "햇살 가득한 해바라기", "url": "https://images.pexels.com/photos/46216/sunflower-flowers-bright-yellow-46216.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/46216/sunflower-flowers-bright-yellow-46216.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "푸른 하늘과 구름", "url": "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "슬픔": [
        {"title": "비 오는 창밖", "url": "https://images.pexels.com/photos/556416/pexels-photo-556416.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/556416/pexels-photo-556416.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "고요한 호수", "url": "https://images.pexels.com/photos/346529/pexels-photo-346529.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/346529/pexels-photo-346529.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "안개 낀 숲", "url": "https://images.pexels.com/photos/1671325/pexels-photo-1671325.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1671325/pexels-photo-1671325.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "불안": [
        {"title": "넓은 바다 수평선", "url": "https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1032650/pexels-photo-1032650.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "평화로운 숲길", "url": "https://images.pexels.com/photos/15286/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/15286/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "잔잔한 물결", "url": "https://images.pexels.com/photos/1093638/pexels-photo-1093638.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1093638/pexels-photo-1093638.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "분노": [
        {"title": "차분한 바다", "url": "https://images.pexels.com/photos/1001682/pexels-photo-1001682.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1001682/pexels-photo-1001682.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "녹색 자연", "url": "https://images.pexels.com/photos/149076/pexels-photo-149076.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/149076/pexels-photo-149076.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "고요한 산", "url": "https://images.pexels.com/photos/417173/pexels-photo-417173.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/417173/pexels-photo-417173.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "평온": [
        {"title": "잔잔한 호수 반영", "url": "https://images.pexels.com/photos/147411/italy-mountains-dawn-nature-147411.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/147411/italy-mountains-dawn-nature-147411.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "아침 이슬", "url": "https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "라벤더 밭", "url": "https://images.pexels.com/photos/207247/pexels-photo-207247.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/207247/pexels-photo-207247.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "피로": [
        {"title": "아늑한 커피", "url": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "포근한 담요", "url": "https://images.pexels.com/photos/1029801/pexels-photo-1029801.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1029801/pexels-photo-1029801.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "촛불의 따스함", "url": "https://images.pexels.com/photos/259810/pexels-photo-259810.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/259810/pexels-photo-259810.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
    "외로움": [
        {"title": "따뜻한 촛불", "url": "https://images.pexels.com/photos/783200/pexels-photo-783200.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/783200/pexels-photo-783200.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "별이 빛나는 밤", "url": "https://images.pexels.com/photos/1252890/pexels-photo-1252890.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1252890/pexels-photo-1252890.jpeg?auto=compress&cs=tinysrgb&w=300"},
        {"title": "따뜻한 음료", "url": "https://images.pexels.com/photos/1194030/pexels-photo-1194030.jpeg?auto=compress&cs=tinysrgb&w=600", "thumb": "https://images.pexels.com/photos/1194030/pexels-photo-1194030.jpeg?auto=compress&cs=tinysrgb&w=300"},
    ],
}
