package com.emotion.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Table(name = "survey_response")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SurveyResponse {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "session_id", nullable = false, unique = true)
    private String sessionId;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "answers", columnDefinition = "jsonb")
    private Map<String, Object> answers;

    @Column(name = "status", nullable = false)
    @Enumerated(EnumType.STRING)
    private SurveyStatus status;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @OneToOne(mappedBy = "surveyResponse", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private EmotionRecord emotionRecord;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        if (this.status == null) {
            this.status = SurveyStatus.PENDING;
        }
    }

    public enum SurveyStatus {
        PENDING, ANALYZING, COMPLETED, FAILED
    }
}
