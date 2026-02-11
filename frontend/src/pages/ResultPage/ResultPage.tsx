import type { RecommendationResult, ContentItem } from '../../types';
import { EMOTION_COLORS, EMOTION_EMOJIS } from '../../types';
import { useState } from 'react';
import './ResultPage.css';

interface ResultPageProps {
    result: RecommendationResult;
    onRetry: () => void;
}

type TabType = 'QUOTE' | 'VIDEO' | 'IMAGE';

export default function ResultPage({ result, onRetry }: ResultPageProps) {
    const [activeTab, setActiveTab] = useState<TabType>('QUOTE');

    const emotion = result.emotion;
    const emotionColor = emotion ? EMOTION_COLORS[emotion.primaryEmotion] || '#8A5CF6' : '#8A5CF6';
    const emotionEmoji = emotion ? EMOTION_EMOJIS[emotion.primaryEmotion] || '😊' : '😊';

    const filteredContents = result.contents.filter(
        (c) => c.contentType === activeTab
    );

    const tabs: { key: TabType; label: string; icon: string }[] = [
        { key: 'QUOTE', label: '글귀', icon: '📝' },
        { key: 'VIDEO', label: '영상', icon: '🎬' },
        { key: 'IMAGE', label: '사진', icon: '🖼️' },
    ];

    return (
        <div className="result-page">
            {/* Emotion Card */}
            {emotion && (
                <div
                    className="emotion-card"
                    style={{ '--emotion-color': emotionColor } as React.CSSProperties}
                >
                    <div className="emotion-emoji">{emotionEmoji}</div>
                    <h2 className="emotion-type">{emotion.primaryEmotion}</h2>
                    <div className="emotion-score-bar">
                        <div
                            className="emotion-score-fill"
                            style={{ width: `${emotion.emotionScore * 100}%` }}
                        ></div>
                    </div>
                    <p className="emotion-score-text">
                        감정 강도: {Math.round(emotion.emotionScore * 100)}%
                    </p>
                    <p className="emotion-mood">💡 {emotion.recommendedMood}</p>

                    {/* Emotion Detail */}
                    <div className="emotion-detail">
                        {Object.entries(emotion.emotionDetail).map(([key, value]) => {
                            const emotionLabels: Record<string, string> = {
                                joy: '기쁨', sadness: '슬픔', anxiety: '불안',
                                anger: '분노', calm: '평온', fatigue: '피로', loneliness: '외로움',
                            };
                            return (
                                <div key={key} className="detail-item">
                                    <span className="detail-label">{emotionLabels[key] || key}</span>
                                    <div className="detail-bar">
                                        <div
                                            className="detail-fill"
                                            style={{ width: `${(value as number) * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="detail-value">{Math.round((value as number) * 100)}%</span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Content Tabs */}
            <div className="content-section">
                <h3 className="content-title">🎁 맞춤 콘텐츠 추천</h3>

                <div className="tab-bar">
                    {tabs.map((tab) => (
                        <button
                            key={tab.key}
                            className={`tab-btn ${activeTab === tab.key ? 'active' : ''}`}
                            onClick={() => setActiveTab(tab.key)}
                        >
                            <span>{tab.icon}</span> {tab.label}
                        </button>
                    ))}
                </div>

                <div className="content-grid">
                    {filteredContents.length === 0 ? (
                        <p className="no-content">해당 콘텐츠가 없습니다.</p>
                    ) : (
                        filteredContents.map((content, idx) => (
                            <ContentCard key={idx} content={content} />
                        ))
                    )}
                </div>
            </div>

            {/* Retry Button */}
            <button className="retry-btn" onClick={onRetry}>
                🔄 다시 설문하기
            </button>
        </div>
    );
}

function ContentCard({ content }: { content: ContentItem }) {
    return (
        <div className={`content-card ${content.contentType.toLowerCase()}`}>
            {content.thumbnailUrl && (
                <div className="card-thumbnail">
                    <img src={content.thumbnailUrl} alt={content.title} loading="lazy" />
                </div>
            )}
            <div className="card-body">
                <h4 className="card-title">{content.title}</h4>
                {content.contentType === 'QUOTE' ? (
                    <p className="card-quote">"{content.contentBody}"</p>
                ) : (
                    <a
                        className="card-link"
                        href={content.contentBody}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        {content.contentType === 'VIDEO' ? '영상 보기 →' : '이미지 보기 →'}
                    </a>
                )}
                <div className="card-footer">
                    <span className="card-source">{content.source}</span>
                    <span className="card-score">
                        적합도 {Math.round(content.relevanceScore * 100)}%
                    </span>
                </div>
            </div>
        </div>
    );
}
