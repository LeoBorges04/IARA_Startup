## Entrada e Saída em Java com Scanner

Linguagem: Java
Categoria: Entrada e Saída
Subcategoria: scanner java
Título: Entrada de Dados em Java com Scanner

Descrição:
Em Java, a classe java.util.Scanner é utilizada para ler dados de diferentes tipos (int, double, String) do teclado via System.in.

Código:
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite um valor: ");
        int valor = scanner.nextInt();
        System.out.println("Valor digitado: " + valor);
        scanner.close();
    }
}
```

Observações:
* `scanner.nextInt()` lê inteiros, `scanner.nextDouble()` lê números decimais.
* Sempre lembre de fechar o scanner ao final com `scanner.close()`.

## Listas Dinâmicas em Java com ArrayList

Linguagem: Java
Categoria: Estruturas de Dados
Subcategoria: arraylist
Título: Manipulação de ArrayList em Java

Descrição:
A classe ArrayList em Java permite criar vetores dinâmicos cujo tamanho pode crescer ou diminuir em tempo de execução.

Código:
```java
import java.util.ArrayList;

ArrayList<String> lista = new ArrayList<>();
lista.add("Item 1"); // Adiciona elemento
lista.add("Item 2");
String item = lista.get(0); // Acessa por índice
int tamanho = lista.size(); // Retorna o tamanho
```

Observações:
* `lista.add()` insere no final da lista.
* `lista.size()` retorna a quantidade de elementos armazenados.

## Entrada e Saída em C ANSI (printf e scanf)

Linguagem: C
Categoria: Entrada e Saída
Subcategoria: printf scanf
Título: Entrada e Saída em C com printf e scanf

Descrição:
Na linguagem C pura, a biblioteca stdio.h disponibiliza a função printf para exibição de texto formatado e scanf para leitura com especificadores de formato.

Código:
```c
#include <stdio.h>

int main() {
    int idade;
    printf("Digite sua idade: ");
    scanf("%d", &idade);
    printf("Idade informada: %d anos\n", idade);
    return 0;
}
```

Observações:
* `%d` especifica número inteiro, `%f` número flutuante, `%c` caractere.
* `scanf` exige o operador `&` para passar o endereço de memória da variável.

## Ponteiros e Passagem por Referência em C

Linguagem: C
Categoria: Ponteiros
Subcategoria: ponteiros
Título: Ponteiros e Modificação de Variáveis em C

Descrição:
Ponteiros são variáveis que armazenam o endereço de memória de outra variável. Permitem modificar o valor original de variáveis através de funções.

Código:
```c
void dobrarValor(int *ptr) {
    *ptr = (*ptr) * 2; // Desreferencia e modifica o valor original
}

int main() {
    int x = 10;
    dobrarValor(&x); // Passa o endereço de x
    // x agora vale 20
    return 0;
}
```

Observações:
* `&` obtém o endereço de memória de uma variável.
* `*` acessa o valor contido no endereço apontado pelo ponteiro.
