package com.nissan.api;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import java.util.List;

import com.nissan.api.service.GeminiService;
import com.nissan.api.service.LeitorCsvService;

@SpringBootApplication
public class ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiApplication.class, args);
	}

	@Bean
	CommandLineRunner testarIntegracao(LeitorCsvService leitor, GeminiService ia) {
		return args -> {
			System.out.println("1. Lendo os dados do CSV falso...");
			List<String[]> dados = leitor.lerDadosDeVendas("vendas_teste.csv");
			
			// Montando uma frase simples com os dados para a IA entender
			StringBuilder textoParaIA = new StringBuilder();
			for (String[] linha : dados) {
				textoParaIA.append("Modelo: ").append(linha[1])
						   .append(" - Valor: R$").append(linha[2]).append("; ");
			}
			
			System.out.println("2. Enviando para o Google Gemini... (Aguarde alguns segundos)");
			String resposta = ia.pedirRelatorio(textoParaIA.toString());
			
			System.out.println("\n========= RELATÓRIO DA IA =========");
			System.out.println(resposta);
			System.out.println("===================================\n");
		};
	}
}
