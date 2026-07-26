// Exemplo Genérico de Estrutura de Dados: Lista Simplesmente Encadeada em C++
// Este é um modelo conceitual genérico para fins de estudo de sintaxe de ponteiros e structs.

#include <iostream>

struct No {
    int valor;
    No* proximo;
};

// Exemplo de inserção no início da lista
void inserirInicio(No*& cabeca, int novoValor) {
    No* novoNo = new No();
    novoNo->valor = novoValor;
    novoNo->proximo = cabeca;
    cabeca = novoNo;
}

// Exemplo de percurso na lista
void imprimirLista(No* cabeca) {
    No* atual = cabeca;
    while (atual != nullptr) {
        std::cout << atual->valor << " -> ";
        atual = atual->proximo;
    }
    std::cout << "NULL" << std::endl;
}
