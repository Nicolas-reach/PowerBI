package com.nissan.api.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class GeminiService {

    // Aqui o Spring Boot vai lá no application.properties e pega a sua chave automaticamente!
    @Value("${gemini.api.key}")
    private String apiKey;

    public String pedirRelatorio(String dadosDeVendas) {
        // URL oficial da API do Gemini 1.5 Flash (mais rápido e barato)
        String url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=" + apiKey;
        
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

       
        String prompt = "Atue como um analista de dados sênior da Nissan. Analise os seguintes dados de vendas e crie um resumo gerencial curto. Destaque os resultados de vendas por região e sugira duas estratégias práticas de melhoria baseadas nos números. Dados: " + dadosDeVendas;
        
        
        String requestBody = "{\"contents\":[{\"parts\":[{\"text\":\"" + prompt + "\"}]}]}";
        
        HttpEntity<String> request = new HttpEntity<>(requestBody, headers);
        
        try {
            // Fazendo o disparo pela internet e aguardando a resposta
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
            return response.getBody();
        } catch (Exception e) {
            return "Erro ao chamar IA do Google: " + e.getMessage();
        }
    }
}