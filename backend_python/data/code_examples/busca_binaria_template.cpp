// Exemplo Genérico de Algoritmo de Busca Binária Iterativa em C++
// Modelo genérico para estudo de lógica de ponteiros inicio, fim e meio.

#include <iostream>
#include <vector>

int buscaBinaria(const std::vector<int>& arr, int alvo) {
    int inicio = 0;
    int fim = arr.size() - 1;

    while (inicio <= fim) {
        int meio = inicio + (fim - inicio) / 2;

        if (arr[meio] == alvo) {
            return meio; // Encontrado
        }
        if (arr[meio] < alvo) {
            inicio = meio + 1; // Busca na metade direita
        } else {
            fim = meio - 1; // Busca na metade esquerda
        }
    }
    return -1; // Não encontrado
}
