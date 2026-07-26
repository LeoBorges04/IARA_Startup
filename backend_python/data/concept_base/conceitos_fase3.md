## Busca Binária em Vetores Ordenados

Linguagem: C++
Categoria: Busca
Subcategoria: busca binaria
Título: Busca Binária em Vetores Ordenados

Descrição:
A busca binária é um algoritmo eficiente de busca em vetores previamente ordenados. Ela compara a chave procurada com o elemento central do vetor, reduzindo o espaço de busca pela metade a cada passo.

Código:
```cpp
int buscaBinaria(int arr[], int tamanho, int chave) {
    int inicio = 0;
    int fim = tamanho - 1;
    while (inicio <= fim) {
        int meio = inicio + (fim - inicio) / 2;
        if (arr[meio] == chave) return meio; // Encontrado
        if (arr[meio] < chave) inicio = meio + 1;
        else fim = meio - 1;
    }
    return -1; // Não encontrado
}
```

Observações:
* O vetor DEVE estar previamente ordenado.
* Complexidade de tempo O(log N).

## Manipulação de Matrizes Bidimensionais

Linguagem: C++
Categoria: Matrizes
Subcategoria: matrizes
Título: Declaração e Leitura de Matrizes 2D

Descrição:
Matrizes são estruturas bidimensionais organizadas em linhas e colunas. O acesso aos elementos é feito por dois índices: `matriz[linha][coluna]`.

Código:
```cpp
// Declaração de matriz de N linhas e M colunas
int matriz[3][3];

// Leitura utilizando laços aninhados (for duplo)
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        cin >> matriz[i][j];
    }
}
```

Observações:
* O primeiro laço itera sobre as linhas (i).
* O segundo laço itera sobre as colunas (j).

## Manipulação de Strings

Linguagem: C++
Categoria: Strings
Subcategoria: strings
Título: Leitura e Comparação de Strings

Descrição:
Em C++, a classe std::string simplifica o armazenamento e manipulação de cadeias de caracteres.

Código:
```cpp
#include <string>
using namespace std;

string texto = "exemplo";
int tamanho = texto.length();

if (texto == "exemplo") {
    // Strings iguais
}
```

Observações:
* `texto.length()` retorna a quantidade de caracteres.
* Operadores `==` e `!=` funcionam diretamente para comparar strings.

## Declaração e Chamada de Funções

Linguagem: C++
Categoria: Funções
Subcategoria: funcoes
Título: Declaração e Chamada de Funções

Descrição:
Funções são blocos de código reaproveitáveis que realizam uma tarefa específica, podendo receber parâmetros e retornar um valor.

Código:
```cpp
// Declaração da função com retorno inteiro
int somar(int a, int b) {
    return a + b;
}

// Chamada no programa principal
int resultado = somar(5, 3);
```

Observações:
* `void` indica que a função não retorna nenhum valor.
* Os parâmetros passam dados para dentro da função.

## Algoritmo de Ordenação Bubble Sort

Linguagem: C++
Categoria: Ordenação
Subcategoria: bubble sort
Título: Algoritmo de Ordenação Bubble Sort

Descrição:
O Bubble Sort percorre o vetor várias vezes, comparando elementos adjacentes e trocando-os de posição se estiverem fora de ordem.

Código:
```cpp
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

Observações:
* Algoritmo simples de implementação.
* Complexidade de tempo O(N²).
