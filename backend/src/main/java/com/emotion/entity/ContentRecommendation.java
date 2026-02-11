package com.emotion.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "content_recommendation")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContentRecommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "emotion_record_id", nullable = false)
    private EmotionRecord emotionRecord;

    @Column(name = "content_type", nullable = false)
    @Enumerated(EnumType.STRING)
    private ContentType contentType;

    @Column(name = "title", nullable = false)
    private String title;

    @Column(name = "content_body", columnDefinition = "text")
    private String contentBody;

    @Column(name = "source")
    private String source;

    @Column(name = "thumbnail_url")
    private String thumbnailUrl;

    @Column(name = "relevance_score")
    private Double relevanceScore;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    public enum ContentType {
        QUOTE, VIDEO, IMAGE
    }
}
