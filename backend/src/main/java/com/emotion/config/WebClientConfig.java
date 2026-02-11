package com.emotion.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.beans.factory.annotation.Value;

@Configuration
public class WebClientConfig {

    @Value("${agent.server.url}")
    private String agentServerUrl;

    @Bean
    public WebClient agentWebClient() {
        return WebClient.builder()
                .baseUrl(agentServerUrl)
                .build();
    }
}
