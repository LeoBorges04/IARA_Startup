# Catálogo de Exercícios - Áreas 1 e 2 (Comparação e Classificação)

## Maior entre dois números
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Condicionais e Testes Relacionais
- Conceitos: Estrutura Condicional, Operadores Relacionais, Entrada e Saída
- Descrição: Ler dois números inteiros e determinar qual é o maior deles.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a > b) {
        cout << a << endl;
    } else {
        cout << b << endl;
    }
    return 0;
}
```

## Menor entre dois números
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Condicionais e Testes Relacionais
- Conceitos: Estrutura Condicional, Operadores Relacionais
- Descrição: Ler dois números e exibir o menor valor informado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float x, y;
    cin >> x >> y;
    if (x < y) {
        cout << x << endl;
    } else {
        cout << y << endl;
    }
    return 0;
}
```

## Maior entre três números
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Condicionais Aninhadas
- Conceitos: Estrutura Condicional, Operadores Lógicos (AND)
- Descrição: Receber três números e determinar o maior deles usando condicionais.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n1, n2, n3;
    cin >> n1 >> n2 >> n3;
    if (n1 >= n2 && n1 >= n3) {
        cout << n1 << endl;
    } else if (n2 >= n1 && n2 >= n3) {
        cout << n2 << endl;
    } else {
        cout << n3 << endl;
    }
    return 0;
}
```

## Menor entre três números
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Condicionais Aninhadas
- Conceitos: Estrutura Condicional, Operadores Lógicos
- Descrição: Ler três números e encontrar o menor valor entre eles.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    int menor = a;
    if (b < menor) menor = b;
    if (c < menor) menor = c;
    cout << menor << endl;
    return 0;
}
```

## Maior e menor entre N valores
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Atualização de Maior/Menor em Laço
- Conceitos: Laço For, Condicional if, Atualização de Limites
- Descrição: Ler N números e encontrar o maior e o menor valor digitado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, valor;
    cin >> n >> valor;
    int maior = valor, menor = valor;
    for (int i = 1; i < n; i++) {
        cin >> valor;
        if (valor > maior) maior = valor;
        if (valor < menor) menor = valor;
    }
    cout << maior << " " << menor << endl;
    return 0;
}
```

## Verificar igualdade entre números
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Igualdade Relacional
- Conceitos: Operador de Igualdade (==), Condicional if-else
- Descrição: Verificar se dois números informados são iguais ou diferentes.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a == b) {
        cout << "Iguais" << endl;
    } else {
        cout << "Diferentes" << endl;
    }
    return 0;
}
```

## Verificar se número é positivo
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Sinais de Números
- Conceitos: Estrutura Condicional, Teste Maior que Zero
- Descrição: Verificar se um número lido é maior que zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float n;
    cin >> n;
    if (n > 0) cout << "Positivo" << endl;
    return 0;
}
```

## Verificar se número é negativo
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Sinais de Números
- Conceitos: Estrutura Condicional, Teste Menor que Zero
- Descrição: Verificar se um número lido é menor que zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float n;
    cin >> n;
    if (n < 0) cout << "Negativo" << endl;
    return 0;
}
```

## Verificar se número é nulo/zero
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Sinais de Números
- Conceitos: Teste de Zero (== 0)
- Descrição: Determinar se o número digitado é exatamente zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int num;
    cin >> num;
    if (num == 0) cout << "Zero" << endl;
    return 0;
}
```

## Verificar se número é par
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Paridade e Módulo
- Conceitos: Operador Módulo (%), Teste Paridade
- Descrição: Verificar se um número é divisível por 2 sem resto.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int num;
    cin >> num;
    if (num % 2 == 0) cout << "Par" << endl;
    return 0;
}
```

## Verificar se número é ímpar
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Paridade e Módulo
- Conceitos: Operador Módulo (%), Teste Ímpar
- Descrição: Verificar se o resto da divisão por 2 é diferente de zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int num;
    cin >> num;
    if (num % 2 != 0) cout << "Ímpar" << endl;
    return 0;
}
```

## Verificar divisibilidade por 3 e 5
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Divisibilidade Múltipla
- Conceitos: Operador Módulo, Operador Lógico AND (&&)
- Descrição: Determinar se um número é simultaneamente divisível por 3 e por 5.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    if (n % 3 == 0 && n % 5 == 0) cout << "Divisivel por 3 e 5" << endl;
    return 0;
}
```

## Comparar idades de duas pessoas
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Aplicação Prática de Comparação
- Conceitos: Leitura de dados, Comparação de inteiros
- Descrição: Ler os nomes e idades de duas pessoas e exibir o nome da pessoa mais velha.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string n1, n2;
    int i1, i2;
    cin >> n1 >> i1 >> n2 >> i2;
    if (i1 > i2) cout << n1 << endl;
    else cout << n2 << endl;
    return 0;
}
```

## Maior nota de uma turma
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação em Coleção
- Conceitos: Laço de repetição, Maior valor acumulado
- Descrição: Ler 10 notas e informar a maior nota obtida na turma.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float nota, maior = 0;
    for (int i = 0; i < 10; i++) {
        cin >> nota;
        if (nota > maior) maior = nota;
    }
    cout << maior << endl;
    return 0;
}
```

## Menor temperatura registrada
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação em Coleção
- Conceitos: Menor valor em laço
- Descrição: Ler as temperaturas de 7 dias da semana e informar a menor temperatura.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float temp, menor;
    cin >> menor;
    for (int i = 1; i < 7; i++) {
        cin >> temp;
        if (temp < menor) menor = temp;
    }
    cout << menor << endl;
    return 0;
}
```

## Comparar dois salários
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação Financeira
- Conceitos: Valores reais, Condicional if-else
- Descrição: Comparar os salários de dois funcionários e exibir a diferença entre eles.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double s1, s2;
    cin >> s1 >> s2;
    if (s1 > s2) cout << s1 - s2 << endl;
    else cout << s2 - s1 << endl;
    return 0;
}
```

## Trocar valores se A > B
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Troca Variáveis (Swap)
- Conceitos: Variável Auxiliar, Condicional
- Descrição: Garantir que a variável A armazene o menor valor e B o maior valor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a > b) {
        int temp = a;
        a = b;
        b = temp;
    }
    cout << a << " " << b << endl;
    return 0;
}
```

## Ordenar dois números em ordem crescente
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Ordenação Simples
- Conceitos: Teste Relacional, Impressão Ordenada
- Descrição: Ler dois números e exibi-los em ordem crescente.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a < b) cout << a << " " << b << endl;
    else cout << b << " " << a << endl;
    return 0;
}
```

## Ordenar dois números em ordem decrescente
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Ordenação Simples
- Conceitos: Teste Relacional, Impressão Decrescente
- Descrição: Ler dois números e exibi-los do maior para o menor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int x, y;
    cin >> x >> y;
    if (x > y) cout << x << " " << y << endl;
    else cout << y << " " << x << endl;
    return 0;
}
```

## Ordenar três números em ordem crescente
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Ordenação de 3 Elementos
- Conceitos: Trocas sucessivas de valores (Swap)
- Descrição: Receber três inteiros e exibi-los perfeitamente ordenados do menor para o maior.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    if (a > b) swap(a, b);
    if (b > c) swap(b, c);
    if (a > b) swap(a, b);
    cout << a << " " << b << " " << c << endl;
    return 0;
}
```

## Comparar comprimentos de duas strings
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação de Texto
- Conceitos: Método length(), Comparação de inteiros
- Descrição: Ler duas palavras e determinar qual delas tem mais caracteres.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string p1, p2;
    cin >> p1 >> p2;
    if (p1.length() > p2.length()) cout << p1 << endl;
    else cout << p2 << endl;
    return 0;
}
```

## Verificar se ano é bissexto
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Regras Calendário
- Conceitos: Operador Módulo, Expressões Lógicas Complexas
- Descrição: Verificar se um ano informado é bissexto (divisível por 400 ou por 4 e não por 100).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int ano;
    cin >> ano;
    if ((ano % 400 == 0) || (ano % 4 == 0 && ano % 100 != 0)) {
        cout << "Bissexto" << endl;
    } else {
        cout << "Nao Bissexto" << endl;
    }
    return 0;
}
```

## Verificar se número está dentro de um intervalo [A, B]
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Teste de Intervalo
- Conceitos: Operadores Relacionais, Operador Lógico AND
- Descrição: Determinar se o valor X pertence ao intervalo fechado [10, 50].
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int x;
    cin >> x;
    if (x >= 10 && x <= 50) cout << "Dentro do intervalo" << endl;
    else cout << "Fora do intervalo" << endl;
    return 0;
}
```

## Comparar duas datas (dia, mês, ano)
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação Cronológica
- Conceitos: Condicionais Aninhadas
- Descrição: Ler duas datas (dia, mês, ano) e indicar qual ocorreu primeiro.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int d1, m1, a1, d2, m2, a2;
    cin >> d1 >> m1 >> a1 >> d2 >> m2 >> a2;
    if (a1 < a2 || (a1 == a2 && m1 < m2) || (a1 == a2 && m1 == m2 && d1 < d2)) {
        cout << "Data 1 e mais antiga" << endl;
    } else {
        cout << "Data 2 e mais antiga" << endl;
    }
    return 0;
}
```

## Determinar o quadrante de um ponto (x, y)
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Geometria Analítica
- Conceitos: Testes de sinal em Coordenadas
- Descrição: Determinar em qual quadrante do plano cartesiano o ponto (X, Y) se encontra.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float x, y;
    cin >> x >> y;
    if (x > 0 && y > 0) cout << "Q1" << endl;
    else if (x < 0 && y > 0) cout << "Q2" << endl;
    else if (x < 0 && y < 0) cout << "Q3" << endl;
    else if (x > 0 && y < 0) cout << "Q4" << endl;
    return 0;
}
```

## Verificar se número é múltiplo de 10
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Múltiplos
- Conceitos: Operador Módulo (n % 10 == 0)
- Descrição: Verificar se o número informado é divisível por 10 sem resto.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    if (n % 10 == 0) cout << "Multiplo de 10" << endl;
    return 0;
}
```

## Maior elemento de um vetor
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação em Vetores
- Conceitos: Vetor, Laço For, Atualização de Maior
- Descrição: Percorrer um vetor de N números e encontrar seu maior elemento.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    int maior = v[0];
    for (int i = 1; i < n; i++) {
        if (v[i] > maior) maior = v[i];
    }
    cout << maior << endl;
    return 0;
}
```

## Menor elemento de um vetor
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Comparação em Vetores
- Conceitos: Vetor, Laço For, Atualização de Menor
- Descrição: Encontrar o menor elemento armazenado em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    int menor = v[0];
    for (int i = 1; i < n; i++) {
        if (v[i] < menor) menor = v[i];
    }
    cout << menor << endl;
    return 0;
}
```

## Posição do maior elemento de um vetor
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Busca de Índice
- Conceitos: Rastreamento de Índice em Vetor
- Descrição: Encontrar a posição (índice) onde se encontra o maior elemento do vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n], idxMaior = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        if (v[i] > v[idxMaior]) idxMaior = i;
    }
    cout << "Indice: " << idxMaior << endl;
    return 0;
}
```

## Posição do menor elemento de um vetor
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Busca de Índice
- Conceitos: Rastreamento de Índice em Vetor
- Descrição: Encontrar o índice da primeira ocorrência do menor elemento do vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n], idxMenor = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        if (v[i] < v[idxMenor]) idxMenor = i;
    }
    cout << "Indice: " << idxMenor << endl;
    return 0;
}
```

## Verificar se vetor está ordenado
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Verificação de Ordem
- Conceitos: Flag booleana, Teste em Pares de Elementos
- Descrição: Determinar se os elementos de um vetor estão dispostos em ordem crescente.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    bool ordenado = true;
    for (int i = 0; i < n - 1; i++) {
        if (v[i] > v[i + 1]) {
            ordenado = false;
            break;
        }
    }
    if (ordenado) cout << "Ordenado" << endl;
    else cout << "Nao Ordenado" << endl;
    return 0;
}
```

## Primalidade de um número inteiro
- Linguagem: C++
- Categoria: Comparação
- Subcategoria: Matemática e Divisores
- Conceitos: Laço de Repetição, Contador de Divisores, Condicional
- Descrição: Verificar se um número N é primo (possui apenas 2 divisores: 1 e ele mesmo).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, divisores = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (n % i == 0) divisores++;
    }
    if (divisores == 2) cout << "Primo" << endl;
    else cout << "Nao Primo" << endl;
    return 0;
}
```

## Classificação de idade (Criança, Jovem, Adulto, Idoso)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Faixas Etárias
- Conceitos: Condicionais em Cadeia (else-if)
- Descrição: Classificar uma pessoa com base na idade (0-12 Criança, 13-17 Jovem, 18-59 Adulto, 60+ Idoso).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int idade;
    cin >> idade;
    if (idade <= 12) cout << "Crianca" << endl;
    else if (idade <= 17) cout << "Jovem" << endl;
    else if (idade <= 59) cout << "Adulto" << endl;
    else cout << "Idoso" << endl;
    return 0;
}
```

## Classificação de notas (Conceitos A, B, C, D, F)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Mapeamento de Conceitos
- Conceitos: Estruturas Condicionais Cadeia
- Descrição: Converter nota numérica de 0 a 100 em conceito de A a F.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float nota;
    cin >> nota;
    if (nota >= 90) cout << "A" << endl;
    else if (nota >= 80) cout << "B" << endl;
    else if (nota >= 70) cout << "C" << endl;
    else if (nota >= 60) cout << "D" << endl;
    else cout << "F" << endl;
    return 0;
}
```

## Cálculo e classificação do IMC
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Indicadores de Saúde
- Conceitos: Operadores Aritméticos, Condicionais em Cadeia
- Descrição: Calcular o IMC (massa / altura^2) e classificar o resultado em faixas de peso.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float peso, altura;
    cin >> peso >> altura;
    float imc = peso / (altura * altura);
    if (imc < 18.5) cout << "Abaixo do peso" << endl;
    else if (imc < 25) cout << "Peso normal" << endl;
    else if (imc < 30) cout << "Sobrepeso" << endl;
    else cout << "Obesidade" << endl;
    return 0;
}
```

## Classificação de triângulos (Equilátero, Isósceles, Escaleno)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Geometria
- Conceitos: Condicionais Aninhadas, Operadores de Igualdade
- Descrição: Classificar um triângulo quanto aos seus lados (Equilátero, Isósceles ou Escaleno).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float a, b, c;
    cin >> a >> b >> c;
    if (a == b && b == c) cout << "Equilatero" << endl;
    else if (a == b || b == c || a == c) cout << "Isosceles" << endl;
    else cout << "Escaleno" << endl;
    return 0;
}
```

## Classificação de eleitor (Obrigatório, Facultativo, Não Eleitor)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Regras Jurídicas
- Conceitos: Operadores Lógicos OR e AND
- Descrição: Determinar a classe eleitoral conforme a idade (Menor de 16 Não Eleitor, 16-17 ou 70+ Facultativo, 18-69 Obrigatório).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int idade;
    cin >> idade;
    if (idade < 16) cout << "Nao Eleitor" << endl;
    else if (idade < 18 || idade >= 70) cout << "Facultativo" << endl;
    else cout << "Obrigatorio" << endl;
    return 0;
}
```

## Classificação de atletas por categoria de peso
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Esporte
- Conceitos: Tabela de decisão com else-if
- Descrição: Classificar luta por categoria de peso (Pena, Leve, Médio, Pesado).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float peso;
    cin >> peso;
    if (peso < 60) cout << "Pena" << endl;
    else if (peso < 75) cout << "Leve" << endl;
    else if (peso < 90) cout << "Medio" << endl;
    else cout << "Pesado" << endl;
    return 0;
}
```

## Classificação de produto por código de origem
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Mapeamento de Códigos
- Conceitos: Estrutura Switch-Case
- Descrição: Mapear o código de origem de um produto (1 Sul, 2 Norte, 3 Leste, 4 Oeste).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int codigo;
    cin >> codigo;
    switch (codigo) {
        case 1: cout << "Sul" << endl; break;
        case 2: cout << "Norte" << endl; break;
        case 3: cout << "Leste" << endl; break;
        case 4: cout << "Oeste" << endl; break;
        default: cout << "Importado" << endl; break;
    }
    return 0;
}
```

## Classificação de alíquota do Imposto de Renda
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Tabela Tributária
- Conceitos: Faixas salariais e porcentagens
- Descrição: Calcular a alíquota de imposto de renda com base no salário bruto.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float salario;
    cin >> salario;
    if (salario <= 2000) cout << "Isento" << endl;
    else if (salario <= 3500) cout << "7.5%" << endl;
    else if (salario <= 5000) cout << "15.0%" << endl;
    else cout << "22.5%" << endl;
    return 0;
}
```

## Classificação de veículos por número de eixos
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Pedágio
- Conceitos: Estrutura Switch-Case
- Descrição: Classificar o valor do pedágio pelo número de eixos do veículo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int eixos;
    cin >> eixos;
    if (eixos == 2) cout << "Passeio - R$ 5,00" << endl;
    else if (eixos == 3) cout << "Caminhao Leve - R$ 10,00" << endl;
    else cout << "Caminhao Pesado - R$ " << eixos * 5.0 << endl;
    return 0;
}
```

## Classificação de notas escolares (Aprovado, Exame, Reprovado)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Situação Acadêmica
- Conceitos: Operadores Relacionais, Condicionais em Cadeia
- Descrição: Determinar a situação final do aluno com base na média (>=7 Aprovado, 5 a 6.9 Exame, <5 Reprovado).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float media;
    cin >> media;
    if (media >= 7.0) cout << "Aprovado" << endl;
    else if (media >= 5.0) cout << "Exame" << endl;
    else cout << "Reprovado" << endl;
    return 0;
}
```

## Classificação de velocidade (Dentro do limite, Infração média, Infração grave)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Trânsito
- Conceitos: Porcentagem e Diferença de Limite
- Descrição: Classificar uma multa de trânsito dependendo do excesso sobre o limite permitido.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float vel, limite;
    cin >> vel >> limite;
    if (vel <= limite) cout << "Sem Infraction" << endl;
    else if (vel <= limite * 1.2) cout << "Infracao Media" << endl;
    else cout << "Infracao Grave" << endl;
    return 0;
}
```

## Classificação de ângulo (Agudo, Reto, Obtuso, Raso)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Geometria
- Conceitos: Testes de Igualdade e Intervalo
- Descrição: Classificar o tipo de um ângulo informado em graus (0-90 Agudo, 90 Reto, 90-180 Obtuso, 180 Raso).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int angulo;
    cin >> angulo;
    if (angulo < 90) cout << "Agudo" << endl;
    else if (angulo == 90) cout << "Reto" << endl;
    else if (angulo < 180) cout << "Obtuso" << endl;
    else if (angulo == 180) cout << "Raso" << endl;
    return 0;
}
```

## Classificação de temperatura corporal (Hipotermia, Normal, Febre, Febre Alta)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Medicina
- Conceitos: Faixas de valores reais (float)
- Descrição: Classificar a temperatura de um paciente.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float t;
    cin >> t;
    if (t < 35.5) cout << "Hipotermia" << endl;
    else if (t <= 37.2) cout << "Normal" << endl;
    else if (t <= 38.5) cout << "Febre" << endl;
    else cout << "Febre Alta" << endl;
    return 0;
}
```

## Classificação de cliente por pontuação de crédito
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Finanças
- Conceitos: Escores Numéricos
- Descrição: Classificar o risco financeiro de um cliente com base em seu Score de 0 a 1000.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int score;
    cin >> score;
    if (score < 300) cout << "Alto Risco" << endl;
    else if (score < 700) cout << "Risco Medio" << endl;
    else cout << "Baixo Risco" << endl;
    return 0;
}
```

## Classificação de solo por nível de pH
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Agronomia
- Conceitos: Teste de faixas de pH (Ácido, Neutro, Alcalino)
- Descrição: Determinar se a amostra de solo é Ácida (pH < 7), Neutra (pH == 7) ou Alcalina (pH > 7).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float ph;
    cin >> ph;
    if (ph < 7.0) cout << "Acido" << endl;
    else if (ph == 7.0) cout << "Neutro" << endl;
    else cout << "Alcalino" << endl;
    return 0;
}
```

## Classificação de sinal de trânsito (Pare, Atenção, Siga)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Automação
- Conceitos: Switch-case com caracteres
- Descrição: Mapear a cor da luz do semáforo ('R' Vermelho, 'Y' Amarelo, 'G' Verde).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    char cor;
    cin >> cor;
    switch (cor) {
        case 'R': cout << "Pare" << endl; break;
        case 'Y': cout << "Atencao" << endl; break;
        case 'G': cout << "Siga" << endl; break;
        default: cout << "Invalido" << endl; break;
    }
    return 0;
}
```

## Classificação de polígono por número de lados
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Geometria Plana
- Conceitos: Mapeamento Inteiro para Nome
- Descrição: Retornar o nome do polígono (3 Triângulo, 4 Quadrilátero, 5 Pentágono, 6 Hexágono).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int lados;
    cin >> lados;
    if (lados == 3) cout << "Triangulo" << endl;
    else if (lados == 4) cout << "Quadrilatero" << endl;
    else if (lados == 5) cout << "Pentagono" << endl;
    else if (lados == 6) cout << "Hexagono" << endl;
    else cout << "Poligono Generico" << endl;
    return 0;
}
```

## Classificação de risco de investimento por perfil
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Mercado Financeiro
- Conceitos: Perfil de Investidor (Conservador, Moderado, Arrojado)
- Descrição: Mapear a preferência de risco em perfil de investimento.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int opcao;
    cin >> opcao;
    if (opcao == 1) cout << "Conservador" << endl;
    else if (opcao == 2) cout << "Moderado" << endl;
    else if (opcao == 3) cout << "Arrojado" << endl;
    return 0;
}
```

## Classificação de nadadores por faixa etária
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Esporte Infantil
- Conceitos: Categorias de Natação (Infantil A, Infantil B, Juvenil, Adulto)
- Descrição: Determinar a categoria do nadador com base na sua idade.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int idade;
    cin >> idade;
    if (idade >= 5 && idade <= 7) cout << "Infantil A" << endl;
    else if (idade >= 8 && idade <= 10) cout << "Infantil B" << endl;
    else if (idade >= 11 && idade <= 17) cout << "Juvenil" << endl;
    else if (idade >= 18) cout << "Adulto" << endl;
    return 0;
}
```

## Classificação de horas de sono (Insuficiente, Ideal, Excessivo)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Saúde
- Conceitos: Intervalos Numéricos em Horas
- Descrição: Avaliar se a quantidade diária de horas dormidas é saudável (<7 Insuficiente, 7-9 Ideal, >9 Excessivo).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float horas;
    cin >> horas;
    if (horas < 7.0) cout << "Insuficiente" << endl;
    else if (horas <= 9.0) cout << "Ideal" << endl;
    else cout << "Excessivo" << endl;
    return 0;
}
```

## Classificação de qualidade do ar por índice de poluição
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Meio Ambiente
- Conceitos: Índice de Qualidade do Ar (IQA)
- Descrição: Classificar a qualidade do ar (Boa, Regular, Inadequada, Péssima).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int iqa;
    cin >> iqa;
    if (iqa <= 50) cout << "Boa" << endl;
    else if (iqa <= 100) cout << "Regular" << endl;
    else if (iqa <= 200) cout << "Inadequada" << endl;
    else cout << "Pessima" << endl;
    return 0;
}
```

## Classificação de empresas por faturamento (Micro, Pequena, Média, Grande)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Administração
- Conceitos: Porte Empresarial por Faturamento Anual
- Descrição: Classificar o porte da empresa com base em seu faturamento anual.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double faturamento;
    cin >> faturamento;
    if (faturamento <= 360000) cout << "Microempresa" << endl;
    else if (faturamento <= 4800000) cout << "Pequena Empresa" << endl;
    else if (faturamento <= 300000000) cout << "Media Empresa" << endl;
    else cout << "Grande Empresa" << endl;
    return 0;
}
```

## Classificação de matriz (Nula, Diagonal, Identidade, Genérica)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Álgebra Linear
- Conceitos: Análise de Propriedades de Matrizes
- Descrição: Verificar se uma matriz quadrada dada é Nula ou Identidade.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[2][2];
    for (int i=0; i<2; i++)
        for (int j=0; j<2; j++) cin >> m[i][j];
    
    if (m[0][0] == 1 && m[1][1] == 1 && m[0][1] == 0 && m[1][0] == 0) {
        cout << "Matriz Identidade" << endl;
    } else if (m[0][0] == 0 && m[1][1] == 0 && m[0][1] == 0 && m[1][0] == 0) {
        cout << "Matriz Nula" << endl;
    } else {
        cout << "Matriz Generica" << endl;
    }
    return 0;
}
```

## Classificação de triângulo retângulo por Teorema de Pitágoras
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Geometria
- Conceitos: Teorema de Pitágoras (a^2 = b^2 + c^2)
- Descrição: Determinar se o triângulo é Retângulo, Acutângulo ou Obtusângulo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float a, b, c;
    cin >> a >> b >> c;
    float a2 = a*a, b2 = b*b, c2 = c*c;
    if (a2 == b2 + c2) cout << "Retangulo" << endl;
    else if (a2 < b2 + c2) cout << "Acutangulo" << endl;
    else cout << "Obtusangulo" << endl;
    return 0;
}
```

## Classificação de caracter (Vogal, Consoante, Dígito, Símbolo)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Processamento de Caracteres
- Conceitos: Tabela ASCII e Funções isalpha/isdigit
- Descrição: Classificar um caractere digitado em Vogal, Consoante, Dígito ou Símbolo.
- Código:
```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char ch;
    cin >> ch;
    if (isdigit(ch)) cout << "Digito" << endl;
    else if (isalpha(ch)) {
        char lower = tolower(ch);
        if (lower=='a' || lower=='e' || lower=='i' || lower=='o' || lower=='u') cout << "Vogal" << endl;
        else cout << "Consoante" << endl;
    } else {
        cout << "Simbolo" << endl;
    }
    return 0;
}
```

## Classificação de conta bancária (Saldo Positivo, Saldo Zera, Em Overdraft)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Finanças
- Conceitos: Estado do Saldo
- Descrição: Classificar a situação financeira do cliente pelo saldo bancário.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double saldo;
    cin >> saldo;
    if (saldo > 0) cout << "Saldo Positivo" << endl;
    else if (saldo == 0) cout << "Saldo Zerado" << endl;
    else cout << "Em Overdraft" << endl;
    return 0;
}
```

## Classificação de frete por região e peso
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Logística
- Conceitos: Tabela bidimensional de decisão
- Descrição: Determinar a tarifa de entrega baseada no peso do pacote e estado de destino.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float peso;
    int regiao;
    cin >> peso >> regiao;
    if (regiao == 1) cout << peso * 10.0 << endl;
    else if (regiao == 2) cout << peso * 15.0 << endl;
    else cout << peso * 25.0 << endl;
    return 0;
}
```

## Classificação de desconto por volume de compra
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Vendas
- Conceitos: Desconto Progressivo por Unidades
- Descrição: Aplicar desconto de 5%, 10% ou 20% dependendo da quantidade de itens comprados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int qtd;
    float preco;
    cin >> qtd >> preco;
    float total = qtd * preco;
    if (qtd >= 50) total *= 0.80;
    else if (qtd >= 20) total *= 0.90;
    else if (qtd >= 10) total *= 0.95;
    cout << total << endl;
    return 0;
}
```

## Classificação de pressão arterial (Sistólica e Diastólica)
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Medicina
- Conceitos: Condicionais Compostas (AND/OR)
- Descrição: Classificar a pressão arterial em Normal, Pré-hipertensão ou Hipertensão.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int sis, dia;
    cin >> sis >> dia;
    if (sis < 120 && dia < 80) cout << "Normal" << endl;
    else if (sis <= 139 || dia <= 89) cout << "Pre-hipertensao" << endl;
    else cout << "Hipertensao" << endl;
    return 0;
}
```

## Classificação de terremoto por escala Richter
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Geofísica
- Conceitos: Magnitude na Escala Richter
- Descrição: Classificar o impacto de um sismo pela sua magnitude (Micro, Leve, Moderado, Forte, Grande).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float m;
    cin >> m;
    if (m < 3.0) cout << "Micro" << endl;
    else if (m < 5.0) cout << "Leve" << endl;
    else if (m < 7.0) cout << "Moderado" << endl;
    else cout << "Forte" << endl;
    return 0;
}
```

## Classificação de combustível por tipo e preço relativo
- Linguagem: C++
- Categoria: Classificação
- Subcategoria: Economia Doméstica
- Conceitos: Regra dos 70% Etanol x Gasolina
- Descrição: Determinar se é mais vantajoso abastecer com Etanol ou Gasolina.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float pEtanol, pGasolina;
    cin >> pEtanol >> pGasolina;
    if (pEtanol <= pGasolina * 0.70) cout << "Abasteca com Etanol" << endl;
    else cout << "Abasteca com Gasolina" << endl;
    return 0;
}
```
