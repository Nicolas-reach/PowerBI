package com.nissan.api.controller;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.nissan.api.service.GeminiService;
import com.nissan.api.service.LeitorCsvService;

@RestController
@RequestMapping("/api")
public class RelatorioController {

    private final LeitorCsvService leitor;
    private final GeminiService ia;

    // O Spring Boot injeta os serviços automaticamente aqui
    public RelatorioController(LeitorCsvService leitor, GeminiService ia) {
        this.leitor = leitor;
        this.ia = ia;
    }

    // Essa anotação cria a URL que o Power BI vai acessar
    @GetMapping("/relatorio")
    public String gerarRelatorio() {
        System.out.println("Recebendo requisição para gerar relatório...");
        
        // 1. Lê o CSV oficial com o caminho completo (use barras normais /)
        String caminhoArquivo = "C:/Users/user/OneDrive/Área de Trabalho/Projetos/vendas_tratadas.csv";
        List<String[]> dados = leitor.lerDadosDeVendas(caminhoArquivo);
        
        // 2. Monta o texto enviando TODAS as colunas para a IA (Modelo, Região, Receita, etc)
        StringBuilder textoParaIA = new StringBuilder();
        for (String[] linha : dados) {
            // O String.join junta todas as informações da linha separadas por vírgula
            textoParaIA.append(String.join(", ", linha)).append("; \n");
        }
        
        // 3. Pede para a IA e devolve como resposta da página web
        return ia.pedirRelatorio(textoParaIA.toString());
    }
}