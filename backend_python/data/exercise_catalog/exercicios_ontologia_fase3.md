# Catálogo de Exercícios - Áreas 5 e 6 (Busca e Conversão)

## Busca sequencial/linear em um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Algoritmos de Busca
- Conceitos: Laço For, Comparação v[i] == alvo, Interrupção (break)
- Descrição: Buscar um valor X em um vetor e informar a posição da primeira ocorrência.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, alvo, pos = -1;
    cin >> n >> alvo;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    for (int i = 0; i < n; i++) {
        if (v[i] == alvo) {
            pos = i;
            break;
        }
    }
    cout << pos << endl;
    return 0;
}
```

## Busca binária em um vetor ordenado
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Algoritmos de Busca
- Conceitos: Divisão e Conquista, Ponteiros inicio/fim/meio
- Descrição: Realizar busca binária com complexidade O(log N) em um vetor previamente ordenado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, chave;
    cin >> n >> chave;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    int inicio = 0, fim = n - 1, pos = -1;
    while (inicio <= fim) {
        int meio = inicio + (fim - inicio) / 2;
        if (v[meio] == chave) {
            pos = meio;
            break;
        }
        if (v[meio] < chave) inicio = meio + 1;
        else fim = meio - 1;
    }
    cout << pos << endl;
    return 0;
}
```

## Encontrar o índice da primeira ocorrência de um número
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Busca de Índice
- Conceitos: Retorno Antecipado do Índice em Laço
- Descrição: Localizar a posição do primeiro elemento par em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n], idx = -1;
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = 0; i < n; i++) {
        if (v[i] % 2 == 0) {
            idx = i;
            break;
        }
    }
    cout << idx << endl;
    return 0;
}
```

## Encontrar o índice da última ocorrência de um número
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Busca Reversa
- Conceitos: Percurso do Fim para o Início do Vetor
- Descrição: Localizar o índice da última vez que o elemento X aparece no vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, alvo, pos = -1;
    cin >> n >> alvo;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = n - 1; i >= 0; i--) {
        if (v[i] == alvo) {
            pos = i;
            break;
        }
    }
    cout << pos << endl;
    return 0;
}
```

## Verificar se um elemento existe no vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Pertencimento
- Conceitos: Variável Booleana de Presença (found)
- Descrição: Determinar se o número X está presente no vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, x;
    cin >> n >> x;
    int v[n];
    bool achou = false;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        if (v[i] == x) achou = true;
    }
    if (achou) cout << "Encontrado" << endl;
    else cout << "Nao Encontrado" << endl;
    return 0;
}
```

## Encontrar o maior elemento de um vetor e seu índice
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Extremos em Coleção
- Conceitos: Rastreamento do Maior Valor e de sua Posição
- Descrição: Exibir o valor do maior número e o índice onde ele está armazenado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    int idxMaior = 0;
    for (int i = 1; i < n; i++) {
        if (v[i] > v[idxMaior]) idxMaior = i;
    }
    cout << "Maior: " << v[idxMaior] << " no indice " << idxMaior << endl;
    return 0;
}
```

## Encontrar o menor elemento de um vetor e seu índice
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Extremos em Coleção
- Conceitos: Rastreamento do Menor Valor e de sua Posição
- Descrição: Exibir o menor valor e o índice onde ele foi localizado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    int idxMenor = 0;
    for (int i = 1; i < n; i++) {
        if (v[i] < v[idxMenor]) idxMenor = i;
    }
    cout << "Menor: " << v[idxMenor] << " no indice " << idxMenor << endl;
    return 0;
}
```

## Busca do segundo maior elemento de um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Ranking e Posições
- Conceitos: Rastreamento de Maior1 e Maior2
- Descrição: Encontrar o segundo maior número único em um vetor de inteiros.
- Código:
```cpp
#include <iostream>
#include <climits>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    int m1 = INT_MIN, m2 = INT_MIN;
    for (int i = 0; i < n; i++) {
        if (v[i] > m1) {
            m2 = m1;
            m1 = v[i];
        } else if (v[i] > m2 && v[i] != m1) {
            m2 = v[i];
        }
    }
    cout << "Segundo Maior: " << m2 << endl;
    return 0;
}
```

## Encontrar elemento em uma matriz (linha e coluna)
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Busca Bidimensional
- Conceitos: Coordenadas (Linha, Coluna) em Matriz
- Descrição: Buscar o valor X em uma matriz e exibir sua linha e coluna.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, alvo;
    cin >> l >> c >> alvo;
    int m[l][c];
    int lin = -1, col = -1;
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] == alvo) {
                lin = i; col = j;
            }
        }
    }
    cout << "Linha: " << lin << " | Coluna: " << col << endl;
    return 0;
}
```

## Encontrar o maior elemento em cada linha de uma matriz
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Matrizes
- Conceitos: Maior por Linha em Matriz
- Descrição: Para cada linha de uma matriz, encontrar e imprimir o maior valor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        int maiorLin = -99999;
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            if (m[i][j] > maiorLin) maiorLin = m[i][j];
        }
        cout << "Maior da linha " << i << ": " << maiorLin << endl;
    }
    return 0;
}
```

## Encontrar o menor elemento em cada coluna de uma matriz
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Matrizes
- Conceitos: Menor por Coluna em Matriz
- Descrição: Para cada coluna de uma matriz, encontrar e imprimir o menor valor.
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
        int menorCol = 99999;
        for (int i = 0; i < l; i++) {
            if (m[i][j] < menorCol) menorCol = m[i][j];
        }
        cout << "Menor da coluna " << j << ": " << menorCol << endl;
    }
    return 0;
}
```

## Busca de um nome em uma lista de alunos (string array)
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Strings
- Conceitos: Comparação de Strings (names[i] == busca)
- Descrição: Buscar o nome de um aluno em um vetor de strings.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    string busca;
    cin >> n >> busca;
    string alunos[n];
    bool encontrado = false;
    for (int i = 0; i < n; i++) {
        cin >> alunos[i];
        if (alunos[i] == busca) encontrado = true;
    }
    if (encontrado) cout << "Aluno presente" << endl;
    else cout << "Aluno ausente" << endl;
    return 0;
}
```

## Busca de um produto pelo código de barras
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Registros e Structs
- Conceitos: Busca em Struct por Campo ID
- Descrição: Buscar a descrição e o preço de um produto dado o seu código de barras.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

struct Produto {
    int cod;
    string nome;
    float preco;
};

int main() {
    int n, codBusca;
    cin >> n >> codBusca;
    Produto prods[n];
    for (int i = 0; i < n; i++) cin >> prods[i].cod >> prods[i].nome >> prods[i].preco;
    
    for (int i = 0; i < n; i++) {
        if (prods[i].cod == codBusca) {
            cout << prods[i].nome << " R$ " << prods[i].preco << endl;
            break;
        }
    }
    return 0;
}
```

## Encontrar primeiro número negativo em um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Filtro e Busca
- Conceitos: Teste v[i] < 0 e Interrupção
- Descrição: Localizar e exibir o primeiro valor menor que zero presente no vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = 0; i < n; i++) {
        if (v[i] < 0) {
            cout << "Primeiro negativo: " << v[i] << " no indice " << i << endl;
            break;
        }
    }
    return 0;
}
```

## Busca de valor em matriz tridimensional
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Matrizes Multidimensionais
- Conceitos: Três Laços Encadeados (X, Y, Z)
- Descrição: Localizar as coordenadas (i, j, k) de um valor em um cubo tridimensional.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[2][2][2], alvo;
    cin >> alvo;
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            for (int k = 0; k < 2; k++) {
                cin >> m[i][j][k];
                if (m[i][j][k] == alvo) {
                    cout << "Achou em (" << i << "," << j << "," << k << ")" << endl;
                }
            }
    return 0;
}
```

## Encontrar elemento mais próximo de uma média
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Distância Absoluta
- Conceitos: Cálculo de Média, Menor Diferença Absoluta (fabs(v[i] - media))
- Descrição: Encontrar o elemento do vetor cujo valor é mais próximo da média aritmética dos dados.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int n;
    cin >> n;
    float v[n], soma = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        soma += v[i];
    }
    float media = soma / n;
    int idxProximo = 0;
    float menorDiff = fabs(v[0] - media);
    for (int i = 1; i < n; i++) {
        float diff = fabs(v[i] - media);
        if (diff < menorDiff) {
            menorDiff = diff;
            idxProximo = i;
        }
    }
    cout << "Mais proximo da media (" << media << "): " << v[idxProximo] << endl;
    return 0;
}
```

## Busca de caractere em uma string
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Processamento de Texto
- Conceitos: Método str.find(ch)
- Descrição: Localizar a posição da primeira ocorrência de um caractere em uma string.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string texto;
    char target;
    cin >> texto >> target;
    size_t pos = texto.find(target);
    if (pos != string::npos) cout << "Posicao: " << pos << endl;
    else cout << "Nao encontrado" << endl;
    return 0;
}
```

## Busca de subcadeia (substring) em um texto
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Processamento de Texto
- Conceitos: Método str.find(sub)
- Descrição: Determinar se uma palavra-chave (subcadeia) existe dentro de um texto longo.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string texto, sub;
    getline(cin, texto);
    cin >> sub;
    if (texto.find(sub) != string::npos) cout << "Subcadeia encontrada" << endl;
    else cout << "Subcadeia nao encontrada" << endl;
    return 0;
}
```

## Encontrar a palavra mais longa em uma frase
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Processamento de Texto
- Conceitos: sstringstream, Comparação de Tamanhos de Strings
- Descrição: Ler uma frase e encontrar qual palavra possui o maior número de letras.
- Código:
```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    string frase, palavra, maiorPalavra = "";
    getline(cin, frase);
    stringstream ss(frase);
    while (ss >> palavra) {
        if (palavra.length() > maiorPalavra.length()) maiorPalavra = palavra;
    }
    cout << maiorPalavra << endl;
    return 0;
}
```

## Encontrar a chave de menor valor em um vetor não ordenado
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Algoritmos de Seleção
- Conceitos: Inicialização com Primeiro Elemento e Percurso
- Descrição: Encontrar a menor chave inteira contida no vetor.
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

## Encontrar o valor mediano em um vetor ordenado
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Estatística
- Conceitos: Acesso pelo Índice do Meio em Vetor Ordenado
- Descrição: Acessar a mediana de um vetor previamente ordenado de tamanho N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    float v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    if (n % 2 != 0) cout << "Mediana: " << v[n / 2] << endl;
    else cout << "Mediana: " << (v[n / 2 - 1] + v[n / 2]) / 2.0 << endl;
    return 0;
}
```

## Busca por interpolação em vetor ordenado
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Busca Avançada
- Conceitos: Estimativa de Posição por Interpolação Linear
- Descrição: Realizar busca por interpolação em dados uniformemente distribuídos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, alvo;
    cin >> n >> alvo;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    int low = 0, high = n - 1, pos = -1;
    while (low <= high && alvo >= v[low] && alvo <= v[high]) {
        int mid = low + ((double)(high - low) / (v[high] - v[low])) * (alvo - v[low]);
        if (v[mid] == alvo) { pos = mid; break; }
        if (v[mid] < alvo) low = mid + 1;
        else high = mid - 1;
    }
    cout << pos << endl;
    return 0;
}
```

## Encontrar elemento duplicado em um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Verificação de Duplicatas
- Conceitos: Laços Encadeados de Comparação (i e j)
- Descrição: Encontrar o primeiro valor que aparece duplicado no vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n, dup = -1;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (v[i] == v[j]) {
                dup = v[i];
                break;
            }
        }
        if (dup != -1) break;
    }
    cout << dup << endl;
    return 0;
}
```

## Encontrar interseção entre dois vetores
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Teoria dos Conjuntos
- Conceitos: Comparação Cruzada entre Dois Vetores
- Descrição: Exibir os elementos que estão presentes simultaneamente no vetor A e no vetor B.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int a[n], b[n];
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < n; i++) cin >> b[i];
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (a[i] == b[j]) {
                cout << a[i] << " ";
                break;
            }
        }
    }
    cout << endl;
    return 0;
}
```

## Encontrar diferença entre dois vetores
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Teoria dos Conjuntos
- Conceitos: Elementos do Vetor A que NÃO pertencem ao Vetor B
- Descrição: Imprimir os elementos de A que não estão contidos no vetor B.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int a[n], b[n];
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < n; i++) cin >> b[i];
    
    for (int i = 0; i < n; i++) {
        bool presente = false;
        for (int j = 0; j < n; j++) {
            if (a[i] == b[j]) { presente = true; break; }
        }
        if (!presente) cout << a[i] << " ";
    }
    cout << endl;
    return 0;
}
```

## Busca de cliente por CPF em cadastro
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Cadastro
- Conceitos: Struct e Comparação de String de CPF
- Descrição: Procurar os dados do cliente através de seu CPF em uma lista de struct.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

struct Cliente {
    string cpf;
    string nome;
};

int main() {
    int n;
    string cpfBusca;
    cin >> n >> cpfBusca;
    Cliente cad[n];
    for (int i = 0; i < n; i++) cin >> cad[i].cpf >> cad[i].nome;
    
    for (int i = 0; i < n; i++) {
        if (cad[i].cpf == cpfBusca) {
            cout << "Cliente: " << cad[i].nome << endl;
            break;
        }
    }
    return 0;
}
```

## Busca do maior valor da diagonal principal
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Matrizes
- Conceitos: Percurso da Diagonal Principal m[i][i] e Maior
- Descrição: Encontrar o maior elemento localizado na diagonal principal de uma matriz N x N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> m[i][j];
        
    int maiorDiag = m[0][0];
    for (int i = 1; i < n; i++) {
        if (m[i][i] > maiorDiag) maiorDiag = m[i][i];
    }
    cout << maiorDiag << endl;
    return 0;
}
```

## Encontrar elemento Sela em uma matriz (menor da linha, maior da coluna)
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Matrizes Avançadas
- Conceitos: Elemento Sela (Mínimo da Linha e Máximo da Coluna)
- Descrição: Verificar se existe um Elemento Sela na matriz.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[3][3];
    for (int i=0; i<3; i++)
        for (int j=0; j<3; j++) cin >> m[i][j];
        
    for (int i = 0; i < 3; i++) {
        int minLin = m[i][0], colIdx = 0;
        for (int j = 1; j < 3; j++) {
            if (m[i][j] < minLin) { minLin = m[i][j]; colIdx = j; }
        }
        bool ehSela = true;
        for (int k = 0; k < 3; k++) {
            if (m[k][colIdx] > minLin) { ehSela = false; break; }
        }
        if (ehSela) { cout << "Sela: " << minLin << endl; break; }
    }
    return 0;
}
```

## Busca de arquivo por extensão em lista de nomes
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Manipulação de Arquivos/Strings
- Conceitos: Teste de Sufixo de String (.txt, .pdf, .cpp)
- Descrição: Imprimir apenas os nomes dos arquivos que terminam com ".cpp".
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    string arq;
    for (int i = 0; i < n; i++) {
        cin >> arq;
        if (arq.length() >= 4 && arq.substr(arq.length() - 4) == ".cpp") {
            cout << arq << endl;
        }
    }
    return 0;
}
```

## Encontrar primeiro número primo em um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Algoritmos Combinados
- Conceitos: Teste de Primalidade e Retorno Antecipado do Primeiro Elemento
- Descrição: Percorrer o vetor e exibir o primeiro valor que seja número primo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = 0; i < n; i++) {
        int divs = 0;
        for (int k = 1; k <= v[i]; k++) {
            if (v[i] % k == 0) divs++;
        }
        if (divs == 2) {
            cout << "Primeiro primo: " << v[i] << endl;
            break;
        }
    }
    return 0;
}
```

## Encontrar valor mais frequente (Moda) em um vetor
- Linguagem: C++
- Categoria: Busca
- Subcategoria: Estatística
- Conceitos: Contagem de Frequência e Maior Ocorrência (Moda)
- Descrição: Determinar o valor que aparece com maior frequência (Moda) em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    int moda = v[0], maxFreq = 0;
    for (int i = 0; i < n; i++) {
        int freq = 0;
        for (int j = 0; j < n; j++) {
            if (v[i] == v[j]) freq++;
        }
        if (freq > maxFreq) {
            maxFreq = freq;
            moda = v[i];
        }
    }
    cout << "Moda: " << moda << endl;
    return 0;
}
```

## Conversão de temperatura Celsius para Fahrenheit
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Fórmulas Físicas
- Conceitos: F = (C * 9/5) + 32
- Descrição: Converter valor em graus Celsius para Fahrenheit.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float c;
    cin >> c;
    float f = (c * 9.0 / 5.0) + 32.0;
    cout << f << endl;
    return 0;
}
```

## Conversão de temperatura Fahrenheit para Celsius
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Fórmulas Físicas
- Conceitos: C = (F - 32) * 5/9
- Descrição: Converter valor de Fahrenheit para Celsius.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float f;
    cin >> f;
    float c = (f - 32.0) * 5.0 / 9.0;
    cout << c << endl;
    return 0;
}
```

## Conversão de temperatura Celsius para Kelvin
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Fórmulas Físicas
- Conceitos: K = C + 273.15
- Descrição: Converter valor em Celsius para Kelvin.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float c;
    cin >> c;
    cout << c + 273.15 << endl;
    return 0;
}
```

## Conversão de moeda Real para Dólar
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Câmbio
- Conceitos: Divisão pela Taxa de Câmbio
- Descrição: Converter quantia em Reais para Dólares informando a cotação atual.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float reais, cotacaoDolar;
    cin >> reais >> cotacaoDolar;
    cout << reais / cotacaoDolar << endl;
    return 0;
}
```

## Conversão de moeda Dólar para Real
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Câmbio
- Conceitos: Multiplicação pela Taxa de Câmbio
- Descrição: Converter Dólares em Reais dada a cotação.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float dolares, cotacao;
    cin >> dolares >> cotacao;
    cout << dolares * cotacao << endl;
    return 0;
}
```

## Conversão de moeda Real para Euro
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Câmbio
- Conceitos: Reais / CotacaoEuro
- Descrição: Converter valor de Reais para Euro.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float reais, cotEuro;
    cin >> reais >> cotEuro;
    cout << reais / cotEuro << endl;
    return 0;
}
```

## Conversão de metros para centímetros e milímetros
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Sistema Métrico
- Conceitos: Multiplicação por 100 e 1000
- Descrição: Converter distância em metros para cm e mm.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float metros;
    cin >> metros;
    cout << metros * 100 << " cm | " << metros * 1000 << " mm" << endl;
    return 0;
}
```

## Conversão de quilômetros para milhas
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Sistema Imperial
- Conceitos: Fator 1 Km = 0.621371 Milhas
- Descrição: Converter distância em KM para Milhas terrestres.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float km;
    cin >> km;
    cout << km * 0.621371 << " milhas" << endl;
    return 0;
}
```

## Conversão de horas para minutos e segundos
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Unidades de Tempo
- Conceitos: Multiplicação por 60 e 3600
- Descrição: Converter quantidade inteira de horas em minutos e segundos totais.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int h;
    cin >> h;
    cout << h * 60 << " min | " << h * 3600 << " seg" << endl;
    return 0;
}
```

## Conversão de segundos totais para horas, minutos e segundos
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Unidades de Tempo
- Conceitos: Decomposição por Divisão e Módulo (3600 e 60)
- Descrição: Receber um tempo em segundos totais e formatá-lo em HH:MM:SS.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int totalSeg;
    cin >> totalSeg;
    int h = totalSeg / 3600;
    int m = (totalSeg % 3600) / 60;
    int s = totalSeg % 60;
    cout << h << "h " << m << "m " << s << "s" << endl;
    return 0;
}
```

## Conversão de número inteiro para binário
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Bases Numéricas
- Conceitos: Restos Sucessivos por 2 armazenados em Vetor ou Reversão
- Descrição: Converter número decimal para sua representação binária.
- Código:
```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> bin;
    if (n == 0) bin.push_back(0);
    while (n > 0) {
        bin.push_back(n % 2);
        n /= 2;
    }
    for (int i = bin.size() - 1; i >= 0; i--) cout << bin[i];
    cout << endl;
    return 0;
}
```

## Conversão de número binário para decimal
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Bases Numéricas
- Conceitos: Potências de 2 (Dígito * 2^i)
- Descrição: Converter string ou número binário para valor decimal inteiro.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int main() {
    string bin;
    cin >> bin;
    int dec = 0, tam = bin.length();
    for (int i = 0; i < tam; i++) {
        if (bin[tam - 1 - i] == '1') dec += pow(2, i);
    }
    cout << dec << endl;
    return 0;
}
```

## Conversão de decimal para hexadecimal
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Bases Numéricas
- Conceitos: Formatação em Stream hex
- Descrição: Converter inteiro decimal para formato Hexadecimal usando std::hex.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << hex << uppercase << n << endl;
    return 0;
}
```

## Conversão de ângulos de graus para radianos
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Trigonometria
- Conceitos: Rad = Graus * M_PI / 180.0
- Descrição: Converter ângulo em graus para radianos.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float graus;
    cin >> graus;
    float rad = graus * M_PI / 180.0;
    cout << rad << endl;
    return 0;
}
```

## Conversão de radianos para graus
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Trigonometria
- Conceitos: Graus = Rad * 180.0 / M_PI
- Descrição: Converter ângulo de radianos para graus sexagimais.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float rad;
    cin >> rad;
    float graus = rad * 180.0 / M_PI;
    cout << graus << endl;
    return 0;
}
```

## Conversão de velocidade de km/h para m/s
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Cinemática
- Conceitos: Divisão por 3.6
- Descrição: Converter velocidade de Km/h para metros por segundo (m/s).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float kmh;
    cin >> kmh;
    cout << kmh / 3.6 << " m/s" << endl;
    return 0;
}
```

## Conversão de m/s para km/h
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Cinemática
- Conceitos: Multiplicação por 3.6
- Descrição: Converter velocidade de m/s para Km/h.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float ms;
    cin >> ms;
    cout << ms * 3.6 << " km/h" << endl;
    return 0;
}
```

## Conversão de peso de quilos para libras
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Unidades de Massa
- Conceitos: 1 Kg = 2.20462 Libras
- Descrição: Converter massa em Quilogramas para Libras (lbs).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float kg;
    cin >> kg;
    cout << kg * 2.20462 << " lbs" << endl;
    return 0;
}
```

## Conversão de volume de litros para galões
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Unidades de Volume
- Conceitos: 1 Galão US = 3.78541 Litros
- Descrição: Converter volume de Litros para Galões americanos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float litros;
    cin >> litros;
    cout << litros / 3.78541 << " galoes" << endl;
    return 0;
}
```

## Conversão de texto para maiúsculas (toupper)
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Manipulação de Texto
- Conceitos: Iteração sobre String e aplicação de toupper(c)
- Descrição: Converter todos os caracteres de uma string para maiúsculas.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string str;
    cin >> str;
    for (char &c : str) c = toupper(c);
    cout << str << endl;
    return 0;
}
```

## Conversão de texto para minúsculas (tolower)
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Manipulação de Texto
- Conceitos: Aplicação de tolower(c)
- Descrição: Converter texto para letras minúsculas.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string str;
    cin >> str;
    for (char &c : str) c = tolower(c);
    cout << str << endl;
    return 0;
}
```

## Conversão de caractere numérico ('0'-'9') para inteiro (int)
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Tabela ASCII
- Conceitos: Subtração do Caractere '0' (ch - '0')
- Descrição: Converter um dígito do tipo char em seu valor inteiro correspondente.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    char ch;
    cin >> ch;
    int val = ch - '0';
    cout << "Valor inteiro: " << val << endl;
    return 0;
}
```

## Conversão de inteiro para caractere char
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Tabela ASCII
- Conceitos: Soma de '0' (val + '0') ou Cast (char)n
- Descrição: Converter um número de 0 a 9 para seu caractere '0'-'9'.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int num;
    cin >> num;
    char ch = num + '0';
    cout << "Caractere: " << ch << endl;
    return 0;
}
```

## Conversão de dias para anos, meses e dias
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Calendário
- Conceitos: Decomposição Inteira de Dias (365 e 30)
- Descrição: Converter N dias em anos, meses e dias restantes.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int dias;
    cin >> dias;
    int anos = dias / 365;
    int meses = (dias % 365) / 30;
    int diasRestantes = (dias % 365) % 30;
    cout << anos << " anos, " << meses << " meses e " << diasRestantes << " dias" << endl;
    return 0;
}
```

## Conversão de armazenamento (Bytes para KB, MB e GB)
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Computação
- Conceitos: Divisão Sucessiva por 1024.0
- Descrição: Converter um tamanho em Bytes para KiloBytes, MegaBytes e GigaBytes.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    double bytes;
    cin >> bytes;
    double kb = bytes / 1024.0;
    double mb = kb / 1024.0;
    double gb = mb / 1024.0;
    cout << kb << " KB | " << mb << " MB | " << gb << " GB" << endl;
    return 0;
}
```

## Conversão de coordenadas polares para cartesianas
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Trigonometria
- Conceitos: x = r * cos(theta), y = r * sin(theta)
- Descrição: Converter ponto polar (r, theta) em coordenadas cartesianas (x, y).
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float r, theta;
    cin >> r >> theta;
    float x = r * cos(theta);
    float y = r * sin(theta);
    cout << "X: " << x << " | Y: " << y << endl;
    return 0;
}
```

## Conversão de coordenadas cartesianas para polares
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Trigonometria
- Conceitos: r = sqrt(x^2 + y^2), theta = atan2(y, x)
- Descrição: Converter ponto cartesiano (x, y) em coordenadas polares (r, theta).
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float x, y;
    cin >> x >> y;
    float r = sqrt(x*x + y*y);
    float theta = atan2(y, x);
    cout << "r: " << r << " | theta: " << theta << " rad" << endl;
    return 0;
}
```

## Conversão de notas de 0-100 para conceito A-F
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Escala de Avaliação
- Conceitos: Mapeamento de Faixa para Caractere
- Descrição: Converter nota de 0 a 100 para a letra correspondente do conceito.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int nota;
    cin >> nota;
    char conceito;
    if (nota >= 90) conceito = 'A';
    else if (nota >= 80) conceito = 'B';
    else if (nota >= 70) conceito = 'C';
    else if (nota >= 60) conceito = 'D';
    else conceito = 'F';
    cout << conceito << endl;
    return 0;
}
```

## Conversão de código ASCII para caractere correspondente
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Tabela ASCII
- Conceitos: Cast explícito (char)codigo
- Descrição: Imprimir o caractere correspondente ao código inteiro ASCII informado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int code;
    cin >> code;
    cout << (char)code << endl;
    return 0;
}
```

## Conversão de valor líquido para bruto considerando impostos
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Finanças
- Conceitos: ValorBruto = ValorLiquido / (1 - Taxa)
- Descrição: Calcular o valor bruto necessário para se obter um determinado valor líquido.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float liq, imps;
    cin >> liq >> imps;
    float bruto = liq / (1.0 - imps / 100.0);
    cout << bruto << endl;
    return 0;
}
```

## Conversão de tempo de execução de milissegundos para segundos
- Linguagem: C++
- Categoria: Conversão
- Subcategoria: Desempenho
- Conceitos: Divisão Float por 1000.0
- Descrição: Converter tempo de execução medido em ms para segundos decimais.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    long ms;
    cin >> ms;
    cout << ms / 1000.0 << " s" << endl;
    return 0;
}
```
