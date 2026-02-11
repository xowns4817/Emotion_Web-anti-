package com.emotion.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Entity
@Table(name = "emotion_record")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EmotionRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "survey_response_id", nullable = false, unique = true)
    private SurveyResponse surveyResponse;

    @Column(name = "primary_emotion", nullable = false)
    private String primaryEmotion;

    @Column(name = "emotion_score", nullable = false)
    private Double emotionScore;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "emotion_detail", columnDefinition = "jsonb")
    private Map<String, Object> emotionDetail;

    @Column(name = "recommended_mood")
    private String recommendedMood;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @OneToMany(mappedBy = "emotionRecord", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ContentRecommendation> contentRecommendations;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}
