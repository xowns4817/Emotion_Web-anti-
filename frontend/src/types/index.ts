export interface SurveyQuestion {
  id: number;
  question: string;
  type: 'EMOJI_SELECT' | 'SLIDER' | 'SINGLE_SELECT' | 'MULTI_SELECT' | 'FREE_TEXT';
  options?: Array<{ emoji?: string; label: string; value: string } | string>;
  min?: number;
  max?: number;
  required?: boolean;
}

export interface SurveyAnswers {
  [key: string]: string | number | string[];
}

export interface EmotionResult {
  primaryEmotion: string;
  emotionScore: number;
  emotionDetail: Record<string, number>;
  recommendedMood: string;
}

export interface ContentItem {
  contentType: 'QUOTE' | 'VIDEO' | 'IMAGE';
  title: string;
  contentBody: string;
  source: string;
  thumbnailUrl?: string;
  relevanceScore: number;
}

export interface RecommendationResult {
  sessionId: string;
  status: string;
  emotion: EmotionResult | null;
  contents: ContentItem[];
}

export interface SurveySubmitResponse {
  sessionId: string;
  status: string;
}

export interface StatusResponse {
  sessionId: string;
  status: string;
}

export const EMOTION_COLORS: Record<string, string> = {
  '기쁨': '#FFD700',
  '슬픔': '#4682B4',
  '불안': '#9370DB',
  '분노': '#DC143C',
  '평온': '#3CB371',
  '피로': '#808080',
  '외로움': '#6A5ACD',
};

export const EMOTION_EMOJIS: Record<string, string> = {
  '기쁨': '😊',
  '슬픔': '😢',
  '불안': '😰',
  '분노': '😡',
  '평온': '😌',
  '피로': '😩',
  '외로움': '🥺',
};
