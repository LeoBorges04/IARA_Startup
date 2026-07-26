## Entrada e Saída de Dados

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
