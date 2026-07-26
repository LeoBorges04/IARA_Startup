import os
import sys

# Adiciona o diretório do backend ao sys.path para import de módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rag_service import ingest_document, ingest_exercise_catalog, ingest_concept_base
from database import check_connection

EXERCISES_DATA = """## Ler e exibir um número
Categoria: Entrada e Saída
Ontologia: Problemas de Conversão
Dificuldade: Fácil
Descrição: Receber um valor numérico do usuário e exibir o mesmo valor na tela.
Conceitos envolvidos:
- Entrada de dados
- Variáveis
- Saída de dados
Palavras-chave: ler número, exibir número, entrada e saída
Pode aparecer como: Crie um programa que leia um inteiro e o mostre.

## Ler e exibir um nome
Categoria: Entrada e Saída
Ontologia: Problemas de Conversão
Dificuldade: Fácil
Descrição: Solicitar que o usuário digite seu nome e exibir uma mensagem de saudação.
Conceitos envolvidos:
- Strings
- Entrada de dados
- Saída de dados
Palavras-chave: ler nome, string, saudação
Pode aparecer como: Peça o nome do usuário e diga olá.

## Ler idade e exibir mensagem
Categoria: Entrada e Saída
Ontologia: Problemas de Classificação
Dificuldade: Fácil
Descrição: Receber a idade de uma pessoa e exibir quantos anos ela possui.
Conceitos envolvidos:
- Variáveis inteiras
- Entrada de dados
- Saída de dados
Palavras-chave: idade, pessoa, ler idade

## Ler dois números
Categoria: Entrada e Saída
Ontologia: Problemas de Conversão
Dificuldade: Fácil
Descrição: Receber dois números do usuário e exibi-los.
Conceitos envolvidos:
- Variáveis
- Entrada de dados
- Saída de dados

## Ler três números
Categoria: Entrada e Saída
Ontologia: Problemas de Conversão
Dificuldade: Fácil
Descrição: Receber três números e exibi-los em sequência.
Conceitos envolvidos:
- Variáveis
- Entrada de dados

## Média aritmética de notas
Categoria: Operações Matemáticas
Ontologia: Problemas de Acumulação
Dificuldade: Fácil
Descrição: Receber N notas ou 5 notas de um aluno, somar e calcular a média aritmética.
Conceitos envolvidos:
- Vetores
- Laço de repetição for
- Operadores aritméticos
- Saída de dados
Palavras-chave: média de notas, calcular média, vetor de notas, laço for
Pode aparecer como: Como fazer um programa para calcular a média de 5 notas?

## Maior entre dois números
Categoria: Comparações
Ontologia: Problemas de Comparação
Dificuldade: Fácil
Descrição: Receber dois números e identificar qual deles é o maior.
Conceitos envolvidos:
- Comparação entre valores
- Operadores relacionais
- Estrutura condicional if/else
Palavras-chave: maior número, comparar dois valores, maior valor
Pode aparecer como: Descubra qual número é maior entre A e B.

## Menor entre dois números
Categoria: Comparações
Ontologia: Problemas de Comparação
Dificuldade: Fácil
Descrição: Receber dois números e determinar o menor valor.
Conceitos envolvidos:
- Comparação entre valores
- Operadores relacionais
- if/else

## Par ou ímpar
Categoria: Operador Módulo
Ontologia: Problemas de Classificação
Dificuldade: Fácil
Descrição: Receber um número inteiro e verificar se ele é par ou ímpar usando o operador de resto (módulo).
Conceitos envolvidos:
- Operador Módulo
- Estrutura condicional if/else
Palavras-chave: par ou ímpar, resto da divisão, módulo %

## Aprovação do aluno
Categoria: Estruturas Condicionais
Ontologia: Problemas de Classificação
Dificuldade: Fácil
Descrição: Verificar se a média final do aluno é maior ou igual a 7 para aprovação, entre 5 e 6.9 para exame ou menor que 5 para reprovação.
Conceitos envolvidos:
- Condicionais encadeadas if/else if
- Operadores lógicos
- Comparação de médias
Palavras-chave: aprovação, reprovação, exame, média final

## Classificação do IMC
Categoria: Estruturas Condicionais
Ontologia: Problemas de Classificação
Dificuldade: Médio
Descrição: Calcular o IMC (peso / altura²) e classificar o resultado em faixas (Abaixo do peso, Normal, Sobrepeso, Obeso).
Conceitos envolvidos:
- Operadores aritméticos
- Condicionais encadeadas if/else if
- Comparação de intervalos

## Calculadora Simples com Switch
Categoria: Switch
Ontologia: Problemas de Conversão
Dificuldade: Fácil
Descrição: Receber dois números e um caractere de operação (+, -, *, /) e realizar o cálculo com switch case.
Conceitos envolvidos:
- Estrutura de escolha switch
- Operadores aritméticos
- Entrada de caracteres

## Somatório até zero
Categoria: While
Ontologia: Problemas de Acumulação
Dificuldade: Fácil
Descrição: Ler números continuamente até que o usuário digite zero e exibir a soma acumulada dos valores.
Conceitos envolvidos:
- Laço de repetição enquanto (while)
- Variável acumuladora
- Condição de parada

## Contagem de 1 a N
Categoria: For
Ontologia: Problemas de Repetição e Sequências
Dificuldade: Fácil
Descrição: Receber um valor limite N e exibir todos os números inteiros de 1 até N.
Conceitos envolvidos:
- Laço de repetição for
- Variável contadora
- Saída formatada

## Fatorial de um número
Categoria: Algoritmos Clássicos
Ontologia: Problemas de Acumulação
Dificuldade: Médio
Descrição: Calcular o fatorial de um número inteiro positivo N (N! = N * (N-1) * ... * 1).
Conceitos envolvidos:
- Laço de repetição for
- Multiplicação acumulada
- Casos base

## Sequência de Fibonacci
Categoria: Algoritmos Clássicos
Ontologia: Problemas de Repetição e Sequências
Dificuldade: Médio
Descrição: Gerar os N primeiros termos da sequência de Fibonacci (0, 1, 1, 2, 3, 5, 8...).
Conceitos envolvidos:
- Laço de repetição for
- Troca de variáveis / atualização de termos
- Vetores ou variáveis auxiliares

## Leitura e Impressão de Vetor
Categoria: Vetores
Ontologia: Problemas de Busca
Dificuldade: Fácil
Descrição: Ler N números inteiros para um vetor e em seguida imprimir todos os elementos armazenados.
Conceitos envolvidos:
- Declaração de vetor
- Laço de repetição for
- Acesso por índice

## Maior elemento do Vetor
Categoria: Vetores
Ontologia: Problemas de Busca
Dificuldade: Médio
Descrição: Percorrer um vetor numérico e encontrar o maior valor armazenado e seu índice.
Conceitos envolvidos:
- Vetores
- Laço de repetição for
- Lógica do maior elemento (comparação no loop)

## Leitura de Matriz 3x3
Categoria: Matrizes
Ontologia: Problemas de Busca
Dificuldade: Médio
Descrição: Preencher uma matriz de 3 linhas e 3 colunas e exibir a soma de todos os elementos da diagonal principal.
Conceitos envolvidos:
- Declaração de matriz bidimensional
- Laços aninhados (for duplo)
- Diagonal principal (índice i == j)

## Palíndromo em Strings
Categoria: Strings
Ontologia: Problemas de Validação
Dificuldade: Médio
Descrição: Verificar se uma palavra digitada é um palíndromo (lida igual de trás para frente, como 'arara').
Conceitos envolvidos:
- Manipulação de Strings
- Laço de repetição invertido
- Comparação de caracteres

## Ordenação Bubble Sort
Categoria: Ordenação
Ontologia: Problemas de Busca
Dificuldade: Médio
Descrição: Ordenar os elementos de um vetor em ordem crescente utilizando o algoritmo Bubble Sort.
Conceitos envolvidos:
- Vetores
- Laços aninhados (for duplo)
- Troca de elementos com variável temporária

## Busca Binária
Categoria: Busca
Ontologia: Problemas de Busca
Dificuldade: Avançado
Descrição: Realizar a busca de um elemento em um vetor previamente ordenado usando a divisão ao meio.
Conceitos envolvidos:
- Vetores ordenados
- Ponteiros de início, fim e meio
- Laço de repetição while
"""

CONCEPTS_DATA = """## Entrada e Saída de Dados

Linguagem: C++
Categoria: Entrada e Saída
Subcategoria: entrada e saida de dados
Título: Entrada e Saída de Dados - cin e cout

Descrição:
Em C++, a biblioteca iostream fornece a função cin para leitura de dados via teclado e a função cout para escrita/exibição na tela.

Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int valor;
    cout << "Digite um valor: ";
    cin >> valor;
    cout << "Valor digitado: " << valor << endl;
    return 0;
}
```

Observações:
* cin utiliza o operador >> para capturar entrada.
* cout utiliza o operador << para exibir dados.

## Declaração e Manipulação de Vetores

Linguagem: C++
Categoria: Vetores
Subcategoria: vetores
Título: Declaração e Manipulação de Vetores

Descrição:
Vetores (arrays) são estruturas de dados contíguas que armazenam múltiplos elementos do mesmo tipo acessíveis por um índice de 0 a N-1.

Código:
```cpp
// Declaração de vetor de tamanho fixo
tipo nomeVetor[tamanho];

// Exemplo de leitura com laço for:
for (int i = 0; i < tamanho; i++) {
    cin >> nomeVetor[i];
}
```

Observações:
* Os índices começam em 0 e vão até tamanho - 1.
* A iteração sobre um vetor é comumente realizada com o laço for.

## Laço de Repetição For

Linguagem: C++
Categoria: Estruturas de Repetição
Subcategoria: for
Título: Laço de Repetição - for

Descrição:
O laço for é utilizado para executar um bloco de código um número determinado de vezes. Possui inicialização, condição e incremento.

Código:
```cpp
for (int i = 0; i < limite; i++) {
    // Bloco de código a ser repetido
}
```

Observações:
* O contador é inicializado antes do loop.
* A condição é testada a cada iteração antes de executar o bloco.

## Operadores Aritméticos e Cálculos

Linguagem: C++
Categoria: Operadores
Subcategoria: operadores aritmeticos
Título: Operadores Aritméticos

Descrição:
Os operadores aritméticos fundamentais (+, -, *, /, %) permitem realizar somas, subtrações, multiplicações, divisões e cálculo de resto (módulo).

Código:
```cpp
int soma = a + b;
float media = soma / 5.0;
int resto = numero % 2;
```

Observações:
* Para divisão exata em ponto flutuante, utilize números com ponto decimal (ex: 5.0).
* O operador % retorna o resto inteiro da divisão.

## Estrutura Condicional - if e else

Linguagem: C++
Categoria: Estruturas Condicionais
Subcategoria: if
Título: Estrutura Condicional - if e else

Descrição:
A estrutura if avalia uma expressão booleana (verdadeiro ou falso). Se for verdadeira, executa o bloco do if; caso contrário, executa o bloco do else.

Código:
```cpp
if (condicao) {
    // Executado se a condição for verdadeira
} else {
    // Executado se a condição for falsa
}
```

Observações:
* Utilize operadores relacionais (==, !=, >, <, >=, <=) para formar a condição.

## Operador Módulo - Par ou Ímpar

Linguagem: C++
Categoria: Operador Módulo
Subcategoria: modulo %
Título: Operador Módulo - Resto da Divisão

Descrição:
O operador módulo (%) calcula o resto de uma divisão inteira. É amplamente utilizado para testar paridade ou múltiplos.

Código:
```cpp
if (numero % 2 == 0) {
    // O número é PAR
} else {
    // O número é ÍMPAR
}
```

Observações:
* Se numero % 2 == 0, o número é divisível por 2 (PAR).
"""

def main():
    print("=== INICIANDO GERAÇÃO E CARGA DAS BASES RAG (250 EXERCÍCIOS / CONCEITOS) ===")
    check_connection()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_ex_dir = os.path.join(base_dir, "data", "exercise_catalog")
    data_concept_dir = os.path.join(base_dir, "data", "concept_base")

    os.makedirs(data_ex_dir, exist_ok=True)
    os.makedirs(data_concept_dir, exist_ok=True)

    # Ingestão de todos os arquivos do Catálogo de Exercícios (Base 1)
    print("\n⏳ Ingerindo Base 1 (Catálogo de Exercícios)...")
    total_ex_docs = 0
    if os.path.exists(data_ex_dir):
        for fname in sorted(os.listdir(data_ex_dir)):
            if fname.endswith(".md"):
                fpath = os.path.join(data_ex_dir, fname)
                count = ingest_exercise_catalog(fname, file_path=fpath)
                total_ex_docs += count
                print(f"  -> {fname}: {count} exercícios ingeridos.")
    print(f"✅ Total Base 1 (Catálogo de Exercícios): {total_ex_docs} documentos no MongoDB Atlas.")

    # Ingestão de todos os arquivos da Base Conceitual (Base 2)
    print("\n⏳ Ingerindo Base 2 (Base Conceitual de Sintaxe)...")
    total_concept_docs = 0
    if os.path.exists(data_concept_dir):
        for fname in sorted(os.listdir(data_concept_dir)):
            if fname.endswith(".md"):
                fpath = os.path.join(data_concept_dir, fname)
                count = ingest_concept_base(fname, file_path=fpath)
                total_concept_docs += count
                print(f"  -> {fname}: {count} conceitos/templates ingeridos.")
    print(f"✅ Total Base 2 (Base Conceitual): {total_concept_docs} documentos no MongoDB Atlas.")

    print(f"\n🎉 CARGA COMPLETA CONCLUÍDA! Total geral no acervo RAG: {total_ex_docs + total_concept_docs} documentos.")

if __name__ == "__main__":
    main()
