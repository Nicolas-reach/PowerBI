package com.nissan.api;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.nissan.api.service.LeitorCsvService;

@SpringBootApplication
public class ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiApplication.class, args);
	}

	@Bean
	CommandLineRunner testarLeitura(LeitorCsvService leitor) {
		return args -> {
			System.out.println("Iniciando teste de leitura...");
			// Aqui colocamos o nome do arquivo que acabamos de criar
			leitor.lerDadosDeVendas("vendas_teste.csv");
		};
	}
}
