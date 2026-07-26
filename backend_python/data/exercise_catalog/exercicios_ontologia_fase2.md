# Catálogo de Exercícios - Áreas 3 e 4 (Acumulação e Contagem)

## Soma de N números digitados
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Somatório Simples
- Conceitos: Laço de Repetição, Variável Acumuladora (soma += valor)
- Descrição: Ler N números e calcular a soma total de todos os valores informados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    float val, soma = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        soma += val;
    }
    cout << soma << endl;
    return 0;
}
```

## Média aritmética de N notas
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Médias
- Conceitos: Somatório Acumulado, Divisão por Contagem
- Descrição: Calcular a média aritmética de N notas fornecidas pelo usuário.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    float nota, soma = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> nota;
        soma += nota;
    }
    cout << soma / n << endl;
    return 0;
}
```

## Média ponderada de 3 provas
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Médias Ponderadas
- Conceitos: Multiplicação por Peso, Somatório Ponderado
- Descrição: Receber 3 notas com pesos 2, 3 e 5 e calcular a média ponderada final.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float n1, n2, n3;
    cin >> n1 >> n2 >> n3;
    float media = (n1 * 2 + n2 * 3 + n3 * 5) / 10.0;
    cout << media << endl;
    return 0;
}
```

## Fatorial de um número N
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Produtório
- Conceitos: Variável Produtória (fat *= i), Laço For
- Descrição: Calcular o fatorial N! (produto de todos os inteiros de 1 a N).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    long long fat = 1;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        fat *= i;
    }
    cout << fat << endl;
    return 0;
}
```

## Somatório da série 1 a N
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Séries Numéricas
- Conceitos: Somatório de Inteiros Consecutivos
- Descrição: Calcular a soma S = 1 + 2 + 3 + ... + N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, s = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) s += i;
    cout << s << endl;
    return 0;
}
```

## Produto de N números informados
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Produtório
- Conceitos: Variável Acumuladora de Multiplicação (prod *= val)
- Descrição: Ler N números e calcular o produto total de todos os elementos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    double val, prod = 1.0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        prod *= val;
    }
    cout << prod << endl;
    return 0;
}
```

## Cálculo de Juros Simples acumulo
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Finanças
- Conceitos: Fórmula J = P * i * t, Montante Acumulado M = P + J
- Descrição: Calcular o montante final acumulado sob juros simples após T meses.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double p, i;
    int t;
    cin >> p >> i >> t;
    double juros = p * (i / 100.0) * t;
    cout << p + juros << endl;
    return 0;
}
```

## Cálculo de Juros Compostos ao longo de N meses
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Finanças
- Conceitos: Acumulação de Juros Mês a Mês (Montante *= (1 + i))
- Descrição: Simular a evolução do montante mês a mês com juros compostos acumulados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double m, i;
    int n;
    cin >> m >> i >> n;
    for (int mes = 1; mes <= n; mes++) {
        m *= (1.0 + i / 100.0);
    }
    cout << m << endl;
    return 0;
}
```

## Acumulação de vendas diárias de uma loja
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Controle Financeiro
- Conceitos: Acumulador com Condição de Parada (Flag 0 ou -1)
- Descrição: Somar todas as vendas do dia até que seja digitado o valor 0.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float venda, total = 0;
    while (cin >> venda && venda != 0) {
        total += venda;
    }
    cout << total << endl;
    return 0;
}
```

## Soma dos números pares de 1 a 100
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Filtragem e Acumulação
- Conceitos: Incremento de 2 em 2 ou Teste de Módulo no Laço
- Descrição: Somar todos os números pares no intervalo de 1 a 100.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int soma = 0;
    for (int i = 2; i <= 100; i += 2) {
        soma += i;
    }
    cout << soma << endl;
    return 0;
}
```

## Soma dos números ímpares de 1 a N
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Filtragem e Acumulação
- Conceitos: Teste de Ímpar e Somatório
- Descrição: Calcular o somatório dos números ímpares entre 1 e N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, soma = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (i % 2 != 0) soma += i;
    }
    cout << soma << endl;
    return 0;
}
```

## Somatório de fração (1/1 + 1/2 + 1/3 + ... + 1/N)
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Séries Harmônicas
- Conceitos: Acumulação Float com Cast (1.0 / i)
- Descrição: Calcular o valor da série H = 1/1 + 1/2 + ... + 1/N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    double h = 0.0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        h += 1.0 / i;
    }
    cout << h << endl;
    return 0;
}
```

## Somatório de fração alternada (1/1 - 1/2 + 1/3 - 1/4 + ...)
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Séries Alternadas
- Conceitos: Alternância de Sinal via Paridade do Índice
- Descrição: Calcular o somatório da série com sinais alternados até o N-ésimo termo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    double s = 0.0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (i % 2 != 0) s += 1.0 / i;
        else s -= 1.0 / i;
    }
    cout << s << endl;
    return 0;
}
```

## Cálculo de potência via multiplicações sucessivas
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Potenciação
- Conceitos: Multiplicação acumulada da Base por Expoente vezes
- Descrição: Calcular Base^Expoente sem utilizar a função pow().
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int base, exp;
    long long res = 1;
    cin >> base >> exp;
    for (int i = 0; i < exp; i++) res *= base;
    cout << res << endl;
    return 0;
}
```

## Acumulação de salário bruto com horas extras
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Folha de Pagamento
- Conceitos: Cálculo de Adicional de Horas Extras
- Descrição: Somar o salário base com as horas extras multiplicadas pela tarifa de 1.5x.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float salBase, valorHora;
    int hExtras;
    cin >> salBase >> valorHora >> hExtras;
    float total = salBase + (hExtras * valorHora * 1.5);
    cout << total << endl;
    return 0;
}
```

## Acumulação de pontos em programa de fidelidade
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Regras de Negócio
- Conceitos: Conversão de Valor de Compra para Pontos Acumulados
- Descrição: Acumular 1 ponto para cada R$ 10,00 gastos em compras.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float compra;
    int pontosTotal = 0;
    while (cin >> compra && compra > 0) {
        pontosTotal += (int)(compra / 10.0);
    }
    cout << pontosTotal << endl;
    return 0;
}
```

## Soma dos elementos de um vetor
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Vetores
- Conceitos: Iteração sobre Vetor, Acumulador em Laço
- Descrição: Somar todos os elementos contidos em um vetor de tamanho N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n], soma = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        soma += v[i];
    }
    cout << soma << endl;
    return 0;
}
```

## Média dos elementos de um vetor
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Vetores
- Conceitos: Somatório de Vetor e Divisão pelo Tamanho
- Descrição: Calcular a média dos valores armazenados em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    float v[n], soma = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        soma += v[i];
    }
    cout << soma / n << endl;
    return 0;
}
```

## Soma das linhas de uma matriz
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Matrizes
- Conceitos: Laços Encadeados (Linha/Coluna), Reinicialização do Acumulador da Linha
- Descrição: Calcular e exibir a soma dos elementos de cada linha de uma matriz L x C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        int somaLinha = 0;
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            somaLinha += m[i][j];
        }
        cout << "Linha " << i << ": " << somaLinha << endl;
    }
    return 0;
}
```

## Soma das colunas de uma matriz
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Matrizes
- Conceitos: Inversão de Laços de Percurso em Matriz
- Descrição: Calcular a soma de cada coluna de uma matriz L x C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++)
        for (int j = 0; j < c; j++) cin >> m[i][j];
        
    for (int j = 0; j < c; j++) {
        int somaCol = 0;
        for (int i = 0; i < l; i++) somaCol += m[i][j];
        cout << "Coluna " << j << ": " << somaCol << endl;
    }
    return 0;
}
```

## Soma dos elementos da diagonal principal de me uma matriz
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Matriz Quadrada
- Conceitos: Condição i == j em Matriz Quadrada
- Descrição: Somar apenas os elementos onde o índice da linha é igual ao da coluna (m[i][i]).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, somaDiag = 0;
    cin >> n;
    int m[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> m[i][j];
            if (i == j) somaDiag += m[i][j];
        }
    }
    cout << somaDiag << endl;
    return 0;
}
```

## Soma dos elementos da diagonal secundária de uma matriz
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Matriz Quadrada
- Conceitos: Condição i + j == N - 1 em Matriz Quadrada
- Descrição: Somar os elementos localizados na diagonal secundária de uma matriz N x N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, somaSec = 0;
    cin >> n;
    int m[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> m[i][j];
            if (i + j == n - 1) somaSec += m[i][j];
        }
    }
    cout << somaSec << endl;
    return 0;
}
```

## Acumulação de massa residual em decaimento radioativo
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Física/Química
- Conceitos: Divisão sucessiva por 2 em laço while
- Descrição: Determinar o tempo necessário para que a massa caia abaixo de 0.5g (meia-vida de 50s).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float massa;
    int tempo = 0;
    cin >> massa;
    while (massa >= 0.5) {
        massa /= 2.0;
        tempo += 50;
    }
    cout << tempo << " segundos" << endl;
    return 0;
}
```

## Acumulação de troco em moedas
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Algoritmo Guloso
- Conceitos: Subtrações sucessivas ou Divisão Inteira por Valores de Moeda
- Descrição: Decompor o valor do troco em moedas de 100, 50, 25, 10, 5 e 1 centavo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int centavos;
    cin >> centavos;
    int m100 = centavos / 100; centavos %= 100;
    int m50 = centavos / 50;   centavos %= 50;
    int m25 = centavos / 25;   centavos %= 25;
    int m10 = centavos / 10;   centavos %= 10;
    int m5  = centavos / 5;    centavos %= 5;
    int m1  = centavos;
    cout << m100 << " de 1 real, " << m50 << " de 50, " << m25 << " de 25, " << m10 << " de 10, " << m5 << " de 5, " << m1 << " de 1" << endl;
    return 0;
}
```

## Produto escalar de dois vetores
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Álgebra Vetorial
- Conceitos: Somatório de Produtos Elemento a Elemento (soma += u[i] * v[i])
- Descrição: Calcular o produto escalar entre dois vetores U e V de dimensão N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    float u[n], v[n], dot = 0;
    for (int i = 0; i < n; i++) cin >> u[i];
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = 0; i < n; i++) dot += u[i] * v[i];
    cout << dot << endl;
    return 0;
}
```

## Soma de dois vetores elemento a elemento
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Álgebra Vetorial
- Conceitos: Vetor Resultante R[i] = A[i] + B[i]
- Descrição: Somar dois vetores A e B e armazenar o resultado em um vetor C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int a[n], b[n], c[n];
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < n; i++) cin >> b[i];
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
        cout << c[i] << " ";
    }
    cout << endl;
    return 0;
}
```

## Acumulação de consumo de combustível em uma viagem
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Física Aplicada
- Conceitos: Somatório de Distâncias / Consumo Médio
- Descrição: Somar os trechos de uma viagem e calcular o consumo total de combustível.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int trechos;
    float dist, consumoKmL, distTotal = 0;
    cin >> trechos >> consumoKmL;
    for (int i = 0; i < trechos; i++) {
        cin >> dist;
        distTotal += dist;
    }
    cout << distTotal / consumoKmL << " Litros" << endl;
    return 0;
}
```

## Soma dos dígitos de um número inteiro
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Manipulação Numérica
- Conceitos: Operador Módulo % 10 e Divisão Inteira / 10 em Laço While
- Descrição: Extrair e somar todos os dígitos de um número inteiro positivo N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, somaDigitos = 0;
    cin >> n;
    while (n > 0) {
        somaDigitos += (n % 10);
        n /= 10;
    }
    cout << somaDigitos << endl;
    return 0;
}
```

## Somatório de quadrados (1^2 + 2^2 + 3^2 + ... + N^2)
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Séries Numéricas
- Conceitos: Acumulação do Quadrado do Índice
- Descrição: Calcular a soma dos quadrados dos primeiros N inteiros positivos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, somaQuadrados = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        somaQuadrados += (i * i);
    }
    cout << somaQuadrados << endl;
    return 0;
}
```

## Média harmônica de N valores
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Estatística
- Conceitos: Somatório dos Inversos (1 / val)
- Descrição: Calcular a média harmônica de N valores positivos (N / sum(1/x)).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    double val, somaInversos = 0.0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        somaInversos += (1.0 / val);
    }
    cout << n / somaInversos << endl;
    return 0;
}
```

## Média geométrica de N valores
- Linguagem: C++
- Categoria: Acumulação
- Subcategoria: Estatística
- Conceitos: Produtório Acumulado e Raiz N-ésima (pow(prod, 1.0/N))
- Descrição: Calcular a média geométrica de N números reais positivos.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int n;
    double val, prod = 1.0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        prod *= val;
    }
    cout << pow(prod, 1.0 / n) << endl;
    return 0;
}
```

## Contagem de números pares digitados
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Contadores Condicionais
- Conceitos: Variável Contadora (qtd++), Operador Módulo % 2
- Descrição: Ler N números e contar quantos deles são pares.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, num, pares = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> num;
        if (num % 2 == 0) pares++;
    }
    cout << pares << endl;
    return 0;
}
```

## Contagem de números ímpares digitados
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Contadores Condicionais
- Conceitos: Incremento de Contador (impares++)
- Descrição: Ler N números e contar a quantidade de números ímpares informados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, num, impares = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> num;
        if (num % 2 != 0) impares++;
    }
    cout << impares << endl;
    return 0;
}
```

## Contagem de números positivos e negativos
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Múltiplos Contadores
- Conceitos: Dois Contadores Independentes (pos++, neg++)
- Descrição: Ler N números e contar separadamente quantos são positivos e quantos são negativos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, val, pos = 0, neg = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        if (val > 0) pos++;
        else if (val < 0) neg++;
    }
    cout << "Positivos: " << pos << " | Negativos: " << neg << endl;
    return 0;
}
```

## Contagem de alunos aprovados e reprovados
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Estatística Acadêmica
- Conceitos: Teste de Média Mínima, Incremento em Estrutura Condicional
- Descrição: Ler as notas de N alunos e contar a quantidade de aprovados (nota >= 7.0) e reprovados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, aprovados = 0, reprovados = 0;
    float nota;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> nota;
        if (nota >= 7.0) aprovados++;
        else reprovados++;
    }
    cout << "Aprovados: " << aprovados << " | Reprovados: " << reprovados << endl;
    return 0;
}
```

## Contagem de pessoas maiores de idade
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Pesquisa Demográfica
- Conceitos: Teste de Idade >= 18, Contador
- Descrição: Ler as idades de 10 pessoas e contar quantas têm 18 anos ou mais.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int idade, maiores = 0;
    for (int i = 0; i < 10; i++) {
        cin >> idade;
        if (idade >= 18) maiores++;
    }
    cout << maiores << endl;
    return 0;
}
```

## Contagem de múltiplos de 3 em um intervalo
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Divisibilidade em Laço
- Conceitos: Laço For no Intervalo [A, B], Teste de Módulo 3
- Descrição: Contar quantos números inteiros no intervalo de 1 a 100 são divisíveis por 3.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int mult3 = 0;
    for (int i = 1; i <= 100; i++) {
        if (i % 3 == 0) mult3++;
    }
    cout << mult3 << endl;
    return 0;
}
```

## Contagem de múltiplos de 5 e 7 simultaneamente
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Múltipla Divisibilidade
- Conceitos: Condicional com Operador Lógico AND (&&)
- Descrição: Contar quantos números em um intervalo são divisíveis por 5 e 7 ao mesmo tempo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, mults = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (i % 5 == 0 && i % 7 == 0) mults++;
    }
    cout << mults << endl;
    return 0;
}
```

## Contagem de letras 'a' em um texto
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Processamento de Strings
- Conceitos: Iteração sobre String (char c : str), Comparação de Caracteres
- Descrição: Contar a frequência da letra 'a' (ou 'A') em uma palavra ou texto informado.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string texto;
    cin >> texto;
    int contaA = 0;
    for (char c : texto) {
        if (tolower(c) == 'a') contaA++;
    }
    cout << contaA << endl;
    return 0;
}
```

## Contagem de vogais em uma frase
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Processamento de Strings
- Conceitos: Teste de Pertencimento a Conjunto de Vogais
- Descrição: Contar quantas vogais (a, e, i, o, u) existem em uma frase.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string frase;
    getline(cin, frase);
    int vogais = 0;
    for (char c : frase) {
        char ch = tolower(c);
        if (ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u') vogais++;
    }
    cout << vogais << endl;
    return 0;
}
```

## Contagem de consoantes em um texto
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Processamento de Strings
- Conceitos: isalpha() e negação de vogais
- Descrição: Contar a quantidade de consoantes presentes em um texto.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string str;
    cin >> str;
    int consoantes = 0;
    for (char c : str) {
        if (isalpha(c)) {
            char ch = tolower(c);
            if (!(ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u')) consoantes++;
        }
    }
    cout << consoantes << endl;
    return 0;
}
```

## Contagem de valores acima da média da turma
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Análise em Dois Passos
- Conceitos: 1º Passos: Calcular Média | 2º Passo: Contar Maiores que a Média em Vetor
- Descrição: Armazenar notas em vetor, calcular a média e contar quantos alunos tiraram nota acima da média.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    float notas[n], soma = 0;
    for (int i = 0; i < n; i++) {
        cin >> notas[i];
        soma += notas[i];
    }
    float media = soma / n;
    int acima = 0;
    for (int i = 0; i < n; i++) {
        if (notas[i] > media) acima++;
    }
    cout << acima << endl;
    return 0;
}
```

## Contagem de elementos pares em um vetor
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Vetores
- Conceitos: Percurso de Vetor, Teste de Paridade no Vetor
- Descrição: Contar a quantidade de elementos pares armazenados em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, pares = 0;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        if (v[i] % 2 == 0) pares++;
    }
    cout << pares << endl;
    return 0;
}
```

## Contagem de números primos em um intervalo
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Laços Encadeados
- Conceitos: Laço Externo para Intervalo, Laço Interno para Teste de Primalidade
- Descrição: Contar a quantidade de números primos existentes entre 1 e N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, totalPrimos = 0;
    cin >> n;
    for (int num = 2; num <= n; num++) {
        int divs = 0;
        for (int i = 1; i <= num; i++) {
            if (num % i == 0) divs++;
        }
        if (divs == 2) totalPrimos++;
    }
    cout << totalPrimos << endl;
    return 0;
}
```

## Contagem de divisores de um número N
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Matemática
- Conceitos: Teste de Módulo (N % i == 0) e Incremento de Contador
- Descrição: Determinar quantos divisores inteiros positivos um número N possui.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, contDivs = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (n % i == 0) contDivs++;
    }
    cout << contDivs << endl;
    return 0;
}
```

## Contagem de ocorrências de um determinado valor em um vetor
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Vetores
- Conceitos: Comparação de Busca (v[i] == alvo) e Contador
- Descrição: Contar quantas vezes um determinado número X aparece dentro de um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, alvo, cont = 0;
    cin >> n >> alvo;
    int v[n];
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        if (v[i] == alvo) cont++;
    }
    cout << cont << endl;
    return 0;
}
```

## Contagem de elementos nulos (zeros) em uma matriz
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Matrizes
- Conceitos: Percurso Bidimensional (Matriz), Teste m[i][j] == 0
- Descrição: Contar quantos elementos iguais a zero existem em uma matriz L x C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, zeros = 0;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] == 0) zeros++;
        }
    }
    cout << zeros << endl;
    return 0;
}
```

## Contagem de elementos negativos em uma matriz
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Matrizes
- Conceitos: Percurso Bidimensional, Teste m[i][j] < 0
- Descrição: Contar a quantidade de números negativos presentes em uma matriz.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, negs = 0;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] < 0) negs++;
        }
    }
    cout << negs << endl;
    return 0;
}
```

## Contagem de dias com temperatura acima de 30°C
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Meteorologia
- Conceitos: Teste de Limite Real (temp > 30.0) e Contador
- Descrição: Ler as temperaturas de um mês (30 dias) e contar quantos dias foram quentes (> 30°C).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float temp;
    int diasQuentes = 0;
    for (int i = 0; i < 30; i++) {
        cin >> temp;
        if (temp > 30.0) diasQuentes++;
    }
    cout << diasQuentes << endl;
    return 0;
}
```

## Contagem de produtos em estoque com quantidade crítica
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Controle de Estoque
- Conceitos: Comparação de Quantidade com Nível Mínimo
- Descrição: Contar quantos itens do estoque estão abaixo do limite mínimo de 5 unidades.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, qtd, criticos = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> qtd;
        if (qtd < 5) criticos++;
    }
    cout << criticos << endl;
    return 0;
}
```

## Contagem de inteiros divisíveis por 4
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Divisibilidade
- Conceitos: Teste de Módulo 4
- Descrição: Contar a quantidade de números divisíveis por 4 em uma lista de N inteiros.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, val, div4 = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        if (val % 4 == 0) div4++;
    }
    cout << div4 << endl;
    return 0;
}
```

## Contagem de palpites corretos em jogo de sorteio
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Jogos e Loterias
- Conceitos: Comparação de Vetor de Palpites com Vetor do Sorteio
- Descrição: Comparar os 6 números apostados pelo usuário com os 6 números sorteados e contar os acertos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int aposta[6], sorteio[6], acertos = 0;
    for (int i = 0; i < 6; i++) cin >> aposta[i];
    for (int i = 0; i < 6; i++) cin >> sorteio[i];
    
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (aposta[i] == sorteio[j]) acertos++;
        }
    }
    cout << acertos << endl;
    return 0;
}
```

## Contagem de votos em eleição de 3 candidatos
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Apuração
- Conceitos: Múltiplos Contadores ou Vetor de Contagem com Switch
- Descrição: Contar os votos de uma eleição com 3 candidatos (1, 2, 3) e votos brancos/nulos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int voto, c1 = 0, c2 = 0, c3 = 0, nulos = 0;
    while (cin >> voto && voto != 0) {
        if (voto == 1) c1++;
        else if (voto == 2) c2++;
        else if (voto == 3) c3++;
        else nulos++;
    }
    cout << "C1: " << c1 << " | C2: " << c2 << " | C3: " << c3 << " | Nulos: " << nulos << endl;
    return 0;
}
```

## Contagem de trocas realizadas em uma ordenação Bubble Sort
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Algoritmos de Ordenação
- Conceitos: Incremento de Contador dentro da Troca (Swap) no Bubble Sort
- Descrição: Medir a eficiência do Bubble Sort contando o número total de trocas efetuadas.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, trocas = 0;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (v[j] > v[j + 1]) {
                swap(v[j], v[j + 1]);
                trocas++;
            }
        }
    }
    cout << trocas << endl;
    return 0;
}
```

## Contagem de digitos em um número inteiro
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Matemática
- Conceitos: Divisão sucessiva por 10 e Contador
- Descrição: Contar a quantidade de dígitos de um número inteiro positivo N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, digitos = 0;
    cin >> n;
    if (n == 0) digitos = 1;
    else {
        while (n > 0) {
            n /= 10;
            digitos++;
        }
    }
    cout << digitos << endl;
    return 0;
}
```

## Contagem de palavras em uma string
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Processamento de Texto
- Conceitos: Leitura de String viastringstream ou Contagem de Espaços
- Descrição: Determinar quantas palavras existem em uma frase.
- Código:
```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    string frase, palavra;
    getline(cin, frase);
    stringstream ss(frase);
    int palavras = 0;
    while (ss >> palavra) palavras++;
    cout << palavras << endl;
    return 0;
}
```

## Contagem de espaços em branco em um texto
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Processamento de Texto
- Conceitos: Comparação char c == ' '
- Descrição: Contar quantos caracteres de espaço em branco foram digitados na frase.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string frase;
    getline(cin, frase);
    int espacos = 0;
    for (char c : frase) {
        if (c == ' ') espacos++;
    }
    cout << espacos << endl;
    return 0;
}
```

## Contagem de elementos maiores que X em uma matriz
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Matrizes
- Conceitos: Percurso Bidimensional e Teste m[i][j] > X
- Descrição: Contar quantos elementos em uma matriz L x C são maiores que um limite X.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, x, cont = 0;
    cin >> l >> c >> x;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] > x) cont++;
        }
    }
    cout << cont << endl;
    return 0;
}
```

## Contagem de linhas totalmente nulas em uma matriz
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Álgebra Linear
- Conceitos: Flag de Linha Nula e Contador de Linhas Nulas
- Descrição: Contar quantas linhas de uma matriz são formadas exclusivamente por zeros.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, linhasNulas = 0;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        bool nula = true;
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] != 0) nula = false;
        }
        if (nula) linhasNulas++;
    }
    cout << linhasNulas << endl;
    return 0;
}
```

## Contagem de alunos com frequência acima de 75%
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Registro Escolar
- Conceitos: Cálculo da Porcentagem de Presenças e Contador
- Descrição: Contar quantos alunos obtiveram frequência suficiente (>= 75% das aulas).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int totalAulas, n, presencas, freqOk = 0;
    cin >> totalAulas >> n;
    for (int i = 0; i < n; i++) {
        cin >> presencas;
        if ((float)presencas / totalAulas >= 0.75) freqOk++;
    }
    cout << freqOk << endl;
    return 0;
}
```

## Contagem de transações bancárias do tipo depósito
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Extrato Bancário
- Conceitos: Teste do Sinal do Valor (valor > 0 indica Depósito)
- Descrição: Ler um histórico de N lançamentos e contar quantos foram depósitos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, depositos = 0;
    float val;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        if (val > 0) depositos++;
    }
    cout << depositos << endl;
    return 0;
}
```

## Contagem de números primos em um vetor
- Linguagem: C++
- Categoria: Contagem
- Subcategoria: Vetores e Primalidade
- Conceitos: Teste de Primalidade para cada elemento do Vetor
- Descrição: Ler um vetor de inteiros e contar quantos de seus elementos são números primos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, qtdPrimos = 0;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        int divs = 0;
        for (int k = 1; k <= v[i]; k++) {
            if (v[i] % k == 0) divs++;
        }
        if (divs == 2) qtdPrimos++;
    }
    cout << qtdPrimos << endl;
    return 0;
}
```
