package com.nissan.api.service;

import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class LeitorCsvService {
    public List<String[]> lerDadosDeVendas(String caminhoDoArquivo) {
        List<String[]> registros = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(caminhoDoArquivo))) {
            String linha;
            
            // se for cabeçalho, vai pular a primeira linha
            br.readLine(); 
            
            // vai ler o arquivo linha por linha 
            while ((linha = br.readLine()) != null) {
                // Quebra a linha toda vez que encontrar uma vírgula
                String[] dadosDaLinha = linha.split(",");
                registros.add(dadosDaLinha);
            }
            
            System.out.println("CSV lido com sucesso! Total de linhas: " + registros.size());
            
        } catch (IOException e) {
            System.out.println("Erro ao tentar ler o arquivo: " + e.getMessage());
        }
        
        return registros;
    }
}
    
    

