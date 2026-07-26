# Catálogo de Exercícios - Áreas 7 e 8 (Validação e Repetição com Matrizes)

## Validação de nota no intervalo [0, 10] com laço do-while
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Validação de Entrada
- Conceitos: Laço Do-While, Condição de Repetição (nota < 0 || nota > 10)
- Descrição: Garantir que a nota digitada pelo usuário esteja estritamente no intervalo [0, 10].
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float nota;
    do {
        cout << "Digite uma nota (0 a 10): ";
        cin >> nota;
    } while (nota < 0.0 || nota > 10.0);
    cout << "Nota valida: " << nota << endl;
    return 0;
}
```

## Validação de idade maior que zero
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Validação Numérica
- Conceitos: Laço While para Repetição até Entrada Válida
- Descrição: Solicitar a idade do usuário até que seja fornecido um número estritamente positivo (> 0).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int idade;
    cin >> idade;
    while (idade <= 0) {
        cout << "Idade invalida. Digite novamente: ";
        cin >> idade;
    }
    cout << "Idade aceita: " << idade << endl;
    return 0;
}
```

## Validação de senha numérica de 4 dígitos
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Segurança
- Conceitos: Teste de Intervalo de Senha (1000 a 9999)
- Descrição: Validar se a senha digitada possui exatamente 4 dígitos numéricos.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int senha;
    do {
        cin >> senha;
    } while (senha < 1000 || senha > 9999);
    cout << "Senha cadastrada com sucesso!" << endl;
    return 0;
}
```

## Validação de confirmação de senha (senha == confirmacao)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Segurança
- Conceitos: Igualdade de Strings em Laço de Confirmação
- Descrição: Repetir a solicitação de confirmação de senha até que coincida com a senha informada.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1, s2;
    cin >> s1;
    do {
        cout << "Confirme a senha: ";
        cin >> s2;
    } while (s1 != s2);
    cout << "Senhas conferem!" << endl;
    return 0;
}
```

## Validação de gênero ('M' ou 'F')
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Validação de Caracteres
- Conceitos: tolower/toupper e Teste de Opções Válidas em Do-While
- Descrição: Exigir que o usuário digite apenas 'M' ou 'F' (independente de maiúscula/minúscula).
- Código:
```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char g;
    do {
        cin >> g;
        g = toupper(g);
    } while (g != 'M' && g != 'F');
    cout << "Genero validado: " << g << endl;
    return 0;
}
```

## Validação de salário maior que o mínimo
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Regras de Negócio
- Conceitos: Teste Salário >= 1412.0 em Laço
- Descrição: Repetir a leitura do salário até que ele seja maior ou igual ao salário mínimo vigente.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float sal;
    do {
        cin >> sal;
    } while (sal < 1412.0);
    cout << "Salario aceito: " << sal << endl;
    return 0;
}
```

## Validação de estado civil ('S', 'C', 'V', 'D')
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Cadastro
- Conceitos: Pertencimento a Conjunto de Opções Válidas
- Descrição: Validar a entrada do estado civil ('S' Solteiro, 'C' Casado, 'V' Viúvo, 'D' Divorciado).
- Código:
```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char ec;
    do {
        cin >> ec;
        ec = toupper(ec);
    } while (ec != 'S' && ec != 'C' && ec != 'V' && ec != 'D');
    cout << "Estado civil validado" << endl;
    return 0;
}
```

## Validação de data válida (dia, mês e ano considerando bissexto)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Validação Complexa
- Conceitos: Teste de Limites de Dias por Mês e Regra do Ano Bissexto
- Descrição: Determinar se uma data formada por (dia, mês, ano) é calendariamente válida.
- Código:
```cpp
#include <iostream>
using namespace std;

bool ehBissexto(int ano) {
    return (ano % 400 == 0) || (ano % 4 == 0 && ano % 100 != 0);
}

int main() {
    int d, m, a;
    cin >> d >> m >> a;
    bool valida = true;
    if (a < 1 || m < 1 || m > 12 || d < 1) valida = false;
    else {
        int diasNoMes[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && ehBissexto(a)) diasNoMes[2] = 29;
        if (d > diasNoMes[m]) valida = false;
    }
    if (valida) cout << "Data Valida" << endl;
    else cout << "Data Invalida" << endl;
    return 0;
}
```

## Validação de triângulo (a < b + c e b < a + c e c < a + b)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Geometria
- Conceitos: Desigualdade Triangular
- Descrição: Verificar se três segmentos de reta podem formar um triângulo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float a, b, c;
    cin >> a >> b >> c;
    if (a < b + c && b < a + c && c < a + b) {
        cout << "Triangulo Valido" << endl;
    } else {
        cout << "Triangulo Invalido" << endl;
    }
    return 0;
}
```

## Validação de número positivo para cálculo de raiz quadrada
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Matemática
- Conceitos: Prevenção de Domínio Inválido (sqrt de negativo)
- Descrição: Impedir o cálculo da raiz quadrada se o número for negativo.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float x;
    cin >> x;
    if (x >= 0) {
        cout << sqrt(x) << endl;
    } else {
        cout << "Erro: Numero negativo" << endl;
    }
    return 0;
}
```

## Validação de denominador diferente de zero para divisão
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Prevenção de Erro de Execução (Division by Zero)
- Conceitos: Teste Denominador != 0 em Divisão
- Descrição: Validar se o divisor de uma operação de divisão é diferente de zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float a, b;
    cin >> a >> b;
    if (b != 0) {
        cout << a / b << endl;
    } else {
        cout << "Erro: Divisao por zero" << endl;
    }
    return 0;
}
```

## Validação de código de opção de menu (1 a 5)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Interface do Usuário
- Conceitos: Menu em Do-While com Validação de Opção
- Descrição: Exibir menu e repetir a leitura até que uma opção válida (1 a 5) seja informada.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int op;
    do {
        cout << "1-Somar 2-Subtrair 3-Sair: ";
        cin >> op;
    } while (op < 1 || op > 3);
    cout << "Opcao selecionada: " << op << endl;
    return 0;
}
```

## Validação de comprimento de string mínimo (ex: nome >= 3 chars)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Formulários
- Conceitos: Validação str.length() >= 3 em Laço
- Descrição: Exigir que o nome informado pelo usuário contenha pelo menos 3 caracteres.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nome;
    do {
        cin >> nome;
    } while (nome.length() < 3);
    cout << "Nome cadastrado: " << nome << endl;
    return 0;
}
```

## Validação de e-mail (presença de '@' e '.')
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Processamento de Texto
- Conceitos: Teste de Subcadeia em E-mail (find('@') e find('.'))
- Descrição: Verificar se a string de e-mail contém os caracteres obrigatórios '@' e '.'.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string email;
    cin >> email;
    if (email.find('@') != string::npos && email.find('.') != string::npos) {
        cout << "E-mail valido" << endl;
    } else {
        cout << "E-mail invalido" << endl;
    }
    return 0;
}
```

## Validação de formato de hora (0 <= hora <= 23, 0 <= min <= 59)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Relógio
- Conceitos: Teste de Limites para Horas e Minutos
- Descrição: Validar se os inteiros informados correspondem a uma hora válida (HH:MM).
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int h, m;
    cin >> h >> m;
    if (h >= 0 && h <= 23 && m >= 0 && m <= 59) {
        cout << "Horario Valido" << endl;
    } else {
        cout << "Horario Invalido" << endl;
    }
    return 0;
}
```

## Validação de digito verificador de conta bancária
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Algoritmos de Verificação
- Conceitos: Cálculo de Módulo 11 para Dígito Verificador
- Descrição: Calcular o dígito verificador da conta e comparar com o informado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int conta, dvInformado;
    cin >> conta >> dvInformado;
    int soma = 0, temp = conta, peso = 2;
    while (temp > 0) {
        soma += (temp % 10) * peso;
        temp /= 10;
        peso++;
    }
    int dvCalculado = 11 - (soma % 11);
    if (dvCalculado >= 10) dvCalculado = 0;
    
    if (dvCalculado == dvInformado) cout << "DV Valido" << endl;
    else cout << "DV Invalido" << endl;
    return 0;
}
```

## Validação de limite de tentativas de login (max 3 tentativas)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Controle de Acesso
- Conceitos: Contador de Tentativas em Laço com Flag de Bloqueio
- Descrição: Bloquear o acesso após 3 tentativas incorretas de senha.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string senhaCorreta = "1234", entrada;
    int tentativas = 0;
    bool acessoGarantido = false;
    
    while (tentativas < 3) {
        cin >> entrada;
        if (entrada == senhaCorreta) {
            acessoGarantido = true;
            break;
        }
        tentativas++;
        cout << "Senha incorreta. Tentativas restantes: " << 3 - tentativas << endl;
    }
    if (acessoGarantido) cout << "Acesso Liberado!" << endl;
    else cout << "Conta Bloqueada!" << endl;
    return 0;
}
```

## Validação de intervalo numérico com repetição até ser válido
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Repetição
- Conceitos: Validação Genérica de Faixa [MIN, MAX]
- Descrição: Repetir a leitura de um número inteiro até que ele esteja entre 1 e 100.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int val;
    cin >> val;
    while (val < 1 || val > 100) {
        cout << "Fora do intervalo [1, 100]. Tente novamente: ";
        cin >> val;
    }
    cout << "Valor aceito: " << val << endl;
    return 0;
}
```

## Validação de valor de saque múltiplo de 10
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Caixa Eletrônico
- Conceitos: Teste de Módulo (valor % 10 == 0)
- Descrição: Validar se o valor do saque em um caixa eletrônico é múltiplo de 10.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int valor;
    cin >> valor;
    if (valor > 0 && valor % 10 == 0) {
        cout << "Saque Aprovado" << endl;
    } else {
        cout << "Valor invalido. Notas de 10 disponiveis." << endl;
    }
    return 0;
}
```

## Validação de temperatura dentro de faixa física possível (-273 a 1000)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Física
- Conceitos: Zero Absoluto em Celsius (-273.15)
- Descrição: Validar se a temperatura informada não viola o zero absoluto da física.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float temp;
    cin >> temp;
    if (temp >= -273.15) cout << "Temperatura Valida" << endl;
    else cout << "Invalida: Abaixo do Zero Absoluto" << endl;
    return 0;
}
```

## Validação de caracteres alfabéticos em um nome
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Processamento de Texto
- Conceitos: isalpha() para cada caractere da string
- Descrição: Verificar se o nome contém apenas letras e espaços.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string nome;
    getline(cin, nome);
    bool valido = true;
    for (char c : nome) {
        if (!isalpha(c) && c != ' ') {
            valido = false;
            break;
        }
    }
    if (valido) cout << "Nome Valido" << endl;
    else cout << "Nome Invalido (caracteres especiais)" << endl;
    return 0;
}
```

## Validação de número primo positivo
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Matemática
- Conceitos: Validação Numérica + Teste de Primalidade
- Descrição: Exigir um número inteiro positivo e validar se ele é primo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    do {
        cin >> n;
    } while (n <= 1);
    
    int divs = 0;
    for (int i = 1; i <= n; i++) if (n % i == 0) divs++;
    if (divs == 2) cout << "Primo Valido" << endl;
    else cout << "Nao e primo" << endl;
    return 0;
}
```

## Validação de preço de produto maior que zero
- Linguagem: C++
- Categoria: Validação
- Subcategoria: E-commerce
- Conceitos: Teste de Preço > 0 em do-while
- Descrição: Impedir o cadastro de produtos com preço nulo ou negativo.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    float preco;
    do {
        cin >> preco;
    } while (preco <= 0);
    cout << "Preco validado: R$ " << preco << endl;
    return 0;
}
```

## Validação de quantidade de estoque não negativa
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Controle de Estoque
- Conceitos: Teste Qtd >= 0
- Descrição: Garantir que a quantidade em estoque digitada não seja menor que zero.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int qtd;
    do {
        cin >> qtd;
    } while (qtd < 0);
    cout << "Estoque registrado: " << qtd << endl;
    return 0;
}
```

## Validação de chave Pix (simulação de tipo CPF/Email/Telefone)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Pagamentos
- Conceitos: Análise do Formato da String da Chave
- Descrição: Identificar e validar o tipo de chave Pix cadastrada.
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string chave;
    cin >> chave;
    if (chave.find('@') != string::npos) cout << "Chave Email" << endl;
    else if (chave.length() == 11) cout << "Chave CPF/Telefone" << endl;
    else cout << "Chave Invalida" << endl;
    return 0;
}
```

## Validação de CPF (checagem simples de tamanho 11 dígitos)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Documentos
- Conceitos: Verificação de Comprimento e Apenas Dígitos
- Descrição: Verificar se o CPF informado possui exatamente 11 caracteres numéricos.
- Código:
```cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string cpf;
    cin >> cpf;
    bool apenasNum = true;
    for (char c : cpf) if (!isdigit(c)) apenasNum = false;
    
    if (cpf.length() == 11 && apenasNum) cout << "CPF no Formato Valido" << endl;
    else cout << "CPF Invalido" << endl;
    return 0;
}
```

## Validação de raio de círculo positivo
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Geometria
- Conceitos: Prevenção de Geometria Impossível
- Descrição: Exigir que o raio de um círculo seja um valor estritamente positivo para calcular sua área.
- Código:
```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float r;
    do {
        cin >> r;
    } while (r <= 0);
    cout << "Area: " << M_PI * r * r << endl;
    return 0;
}
```

## Validação de matriz quadrada (linhas == colunas)
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Álgebra Linear
- Conceitos: Teste de Igualdade entre Dimensões
- Descrição: Verificar se o número de linhas é igual ao número de colunas antes de operar com matriz quadrada.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    if (l == c) cout << "Matriz Quadrada Valida" << endl;
    else cout << "Matriz Nao Quadrada" << endl;
    return 0;
}
```

## Validação de dimensões para multiplicação de matrizes
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Álgebra Linear
- Conceitos: Teste Colunas de A == Linhas de B (cA == rB)
- Descrição: Validar se duas matrizes A(rA x cA) e B(rB x cB) podem ser multiplicadas.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int rA, cA, rB, cB;
    cin >> rA >> cA >> rB >> cB;
    if (cA == rB) cout << "Multiplicacao Possivel" << endl;
    else cout << "Dimensoes Incompativeis" << endl;
    return 0;
}
```

## Validação de resposta de sim/não ('S' ou 'N')
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Controle de Fluxo
- Conceitos: Validação em Do-While com toupper
- Descrição: Exigir resposta 'S' ou 'N' para continuar ou encerrar a execução.
- Código:
```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char resp;
    do {
        cout << "Deseja continuar? (S/N): ";
        cin >> resp;
        resp = toupper(resp);
    } while (resp != 'S' && resp != 'N');
    cout << "Resposta aceita: " << resp << endl;
    return 0;
}
```

## Validação de formato de data no padrão DD/MM/AAAA
- Linguagem: C++
- Categoria: Validação
- Subcategoria: Processamento de Texto
- Conceitos: Teste de Posição das Barras ('/') em String
- Descrição: Verificar se a string informada possui as barras na posição correta (índices 2 e 5).
- Código:
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string data;
    cin >> data;
    if (data.length() == 10 && data[2] == '/' && data[5] == '/') {
        cout << "Formato DD/MM/AAAA correto" << endl;
    } else {
        cout << "Formato invalido" << endl;
    }
    return 0;
}
```

## Impressão de tabuada de multiplicação de 1 a 10
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Laços Encadeados
- Conceitos: Dois Laços For Encadeados (Tabuada Completa)
- Descrição: Imprimir a tabuada completa do 1 ao 10 em formato de grade.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        for (int j = 1; j <= 10; j++) {
            cout << i << " x " << j << " = " << i * j << "\t";
        }
        cout << endl;
    }
    return 0;
}
```

## Gerar matriz identidade N x N
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Matrizes Especiais
- Conceitos: Condicional (i == j ? 1 : 0) em Laços Encadeados
- Descrição: Gerar e exibir a matriz identidade de ordem N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) m[i][j] = 1;
            else m[i][j] = 0;
            cout << m[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Matriz transposta de uma matriz M x N
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Operações com Matrizes
- Conceitos: Atribuição T[j][i] = M[i][j]
- Descrição: Calcular e exibir a matriz transposta N x M de uma matriz M x N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int m[l][c], t[c][l];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            t[j][i] = m[i][j];
        }
    }
    for (int j = 0; j < c; j++) {
        for (int i = 0; i < l; i++) cout << t[j][i] << " ";
        cout << endl;
    }
    return 0;
}
```

## Preenchimento de matriz com valores informados pelo usuário
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Leitura de Matrizes
- Conceitos: Laços For Encadeados com cin >> m[i][j]
- Descrição: Ler os dados para preencher uma matriz bidimensional L x C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
        }
    }
    return 0;
}
```

## Exibição de matriz em formato de grade
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Formatação de Saída
- Conceitos: Impressão de Tabulação (\t) e Quebra de Linha (endl)
- Descrição: Imprimir os valores da matriz perfeitamente alinhados em formato de tabela.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l = 3, c = 3;
    int m[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cout << m[i][j] << "\t";
        }
        cout << endl;
    }
    return 0;
}
```

## Soma de duas matrizes A e B de mesma dimensão
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Operações com Matrizes
- Conceitos: Soma Elemento a Elemento C[i][j] = A[i][j] + B[i][j]
- Descrição: Calcular a matriz resultante da soma de duas matrizes A e B de dimensão L x C.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int a[l][c], b[l][c], res[l][c];
    for (int i=0; i<l; i++) for (int j=0; j<c; j++) cin >> a[i][j];
    for (int i=0; i<l; i++) for (int j=0; j<c; j++) cin >> b[i][j];
    
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            res[i][j] = a[i][j] + b[i][j];
            cout << res[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Subtração de duas matrizes A e B
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Operações com Matrizes
- Conceitos: Subtração Elemento a Elemento C[i][j] = A[i][j] - B[i][j]
- Descrição: Calcular a diferença entre duas matrizes A e B de mesma dimensão.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c;
    cin >> l >> c;
    int a[l][c], b[l][c], res[l][c];
    for (int i=0; i<l; i++) for (int j=0; j<c; j++) cin >> a[i][j];
    for (int i=0; i<l; i++) for (int j=0; j<c; j++) cin >> b[i][j];
    
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            res[i][j] = a[i][j] - b[i][j];
            cout << res[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Multiplicação de matriz por um escalar
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Operações com Matrizes
- Conceitos: Multiplicação de Todos os Elementos por um Fator K
- Descrição: Multiplicar todos os elementos de uma matriz por um número K informado.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int l, c, k;
    cin >> l >> c >> k;
    int m[l][c];
    for (int i = 0; i < l; i++) {
        for (int j = 0; j < c; j++) {
            cin >> m[i][j];
            m[i][j] *= k;
            cout << m[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Multiplicação de duas matrizes A(m x n) e B(n x p)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Operações Avançadas
- Conceitos: Três Laços Encadeados (i, j, k) para Produto Matricial
- Descrição: Realizar o produto de duas matrizes A e B compatíveis.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m, n, p;
    cin >> m >> n >> p;
    int a[m][n], b[n][p], res[m][p];
    for (int i=0; i<m; i++) for (int j=0; j<n; j++) cin >> a[i][j];
    for (int i=0; i<n; i++) for (int j=0; j<p; j++) cin >> b[i][j];
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            res[i][j] = 0;
            for (int k = 0; k < n; k++) {
                res[i][j] += a[i][k] * b[k][j];
            }
            cout << res[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Diagonal principal de uma matriz quadrada
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Matriz Quadrada
- Conceitos: Impressão dos Elementos m[i][i]
- Descrição: Imprimir apenas os elementos contidos na diagonal principal.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i=0; i<n; i++) for (int j=0; j<n; j++) cin >> m[i][j];
    
    for (int i = 0; i < n; i++) {
        cout << m[i][i] << " ";
    }
    cout << endl;
    return 0;
}
```

## Diagonal secundária de uma matriz quadrada
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Matriz Quadrada
- Conceitos: Impressão dos Elementos m[i][N - 1 - i]
- Descrição: Imprimir os elementos da diagonal secundária de uma matriz N x N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i=0; i<n; i++) for (int j=0; j<n; j++) cin >> m[i][j];
    
    for (int i = 0; i < n; i++) {
        cout << m[i][n - 1 - i] << " ";
    }
    cout << endl;
    return 0;
}
```

## Matriz triangular superior
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Matrizes Especiais
- Conceitos: Elementos com j >= i mantidos, j < i zerados
- Descrição: Imprimir os elementos localizados acima ou na diagonal principal.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i=0; i<n; i++) for (int j=0; j<n; j++) cin >> m[i][j];
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (j >= i) cout << m[i][j] << " ";
            else cout << "0 ";
        }
        cout << endl;
    }
    return 0;
}
```

## Matriz triangular inferior
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Matrizes Especiais
- Conceitos: Elementos com i >= j mantidos, i < j zerados
- Descrição: Imprimir a parte triangular inferior de uma matriz quadrada.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i=0; i<n; i++) for (int j=0; j<n; j++) cin >> m[i][j];
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i >= j) cout << m[i][j] << " ";
            else cout << "0 ";
        }
        cout << endl;
    }
    return 0;
}
```

## Matriz simétrica (A == A^T)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Álgebra Linear
- Conceitos: Teste m[i][j] == m[j][i] para todos os Pares (i, j)
- Descrição: Determinar se uma matriz quadrada é perfeitamente simétrica.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i=0; i<n; i++) for (int j=0; j<n; j++) cin >> m[i][j];
    
    bool simetrica = true;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (m[i][j] != m[j][i]) {
                simetrica = false;
                break;
            }
        }
    }
    if (simetrica) cout << "Simetrica" << endl;
    else cout << "Nao Simetrica" << endl;
    return 0;
}
```

## Trocar duas linhas de uma matriz
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Manipulação de Matrizes
- Conceitos: Troca em Laço (swap(m[l1][j], m[l2][j]))
- Descrição: Trocar o conteúdo da linha L1 com a linha L2 de uma matriz.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[3][3] = {{1,1,1},{2,2,2},{3,3,3}};
    int l1 = 0, l2 = 2;
    for (int j = 0; j < 3; j++) {
        swap(m[l1][j], m[l2][j]);
    }
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) cout << m[i][j] << " ";
        cout << endl;
    }
    return 0;
}
```

## Trocar duas colunas de uma matriz
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Manipulação de Matrizes
- Conceitos: Troca em Laço (swap(m[i][c1], m[i][c2]))
- Descrição: Trocar os valores da coluna C1 pelos da coluna C2.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[3][3] = {{1,2,3},{1,2,3},{1,2,3}};
    int c1 = 0, c2 = 2;
    for (int i = 0; i < 3; i++) {
        swap(m[i][c1], m[i][c2]);
    }
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) cout << m[i][j] << " ";
        cout << endl;
    }
    return 0;
}
```

## Girar matriz 90 graus no sentido horário
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Transformações Geométricas
- Conceitos: Transposta + Inversão das Linhas
- Descrição: Rotacionar os elementos de uma matriz quadrada em 90 graus no sentido horário.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 3;
    int m[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    int rot[3][3];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            rot[j][n - 1 - i] = m[i][j];
        }
    }
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) cout << rot[i][j] << " ";
        cout << endl;
    }
    return 0;
}
```

## Desenhar quadrado de asteriscos N x N com laços encadeados
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Desenho de Padrões
- Conceitos: Laços Encadeados com Impressão de '*'
- Descrição: Desenhar um quadrado preenchido por asteriscos de dimensão N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << "* ";
        cout << endl;
    }
    return 0;
}
```

## Desenhar triângulo retângulo de asteriscos
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Desenho de Padrões
- Conceitos: Laço Interno com Limite j <= i
- Descrição: Desenhar um triângulo retângulo de asteriscos com altura N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << "*";
        cout << endl;
    }
    return 0;
}
```

## Desenhar pirâmide de asteriscos
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Desenho de Padrões
- Conceitos: Impressão de Espaços e Asteriscos por Linha
- Descrição: Desenhar uma pirâmide centralizada de asteriscos de altura N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i; j++) cout << " ";
        for (int k = 1; k <= (2 * i - 1); k++) cout << "*";
        cout << endl;
    }
    return 0;
}
```

## Gerar matriz xadrez (0 e 1 alternados)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Padrões de Matriz
- Conceitos: Condição (i + j) % 2 == 0 para Valor 1, senão 0
- Descrição: Gerar um tabuleiro de xadrez N x N representado por 0s e 1s alternados.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int m[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if ((i + j) % 2 == 0) m[i][j] = 1;
            else m[i][j] = 0;
            cout << m[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}
```

## Gerar matriz espiral N x N
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Preenchimento Avançado
- Conceitos: Ponteiros de Limites (cima, baixo, esquerda, direita)
- Descrição: Preencher uma matriz N x N com valores sequenciais de 1 a N^2 em espiral.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 3;
    int m[3][3], val = 1;
    int top = 0, bottom = n - 1, left = 0, right = n - 1;
    
    while (top <= bottom && left <= right) {
        for (int i = left; i <= right; i++) m[top][i] = val++;
        top++;
        for (int i = top; i <= bottom; i++) m[i][right] = val++;
        right--;
        for (int i = right; i >= left; i--) m[bottom][i] = val++;
        bottom--;
        for (int i = bottom; i >= top; i--) m[i][left] = val++;
        left++;
    }
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) cout << m[i][j] << "\t";
        cout << endl;
    }
    return 0;
}
```

## Preenchimento de vetor com os 20 primeiros termos de Fibonacci
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Séries Numéricas
- Conceitos: Vetor de Sequência (fib[i] = fib[i-1] + fib[i-2])
- Descrição: Gerar e armazenar os primeiros 20 termos da Sequência de Fibonacci em um vetor.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    long long fib[20];
    fib[0] = 0; fib[1] = 1;
    for (int i = 2; i < 20; i++) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    for (int i = 0; i < 20; i++) cout << fib[i] << " ";
    cout << endl;
    return 0;
}
```

## Inverter a ordem dos elementos de um vetor
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Manipulação de Vetores
- Conceitos: Troca nos Extremos (swap(v[i], v[N - 1 - i]))
- Descrição: Inverter in-place todos os elementos de um vetor de tamanho N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    for (int i = 0; i < n / 2; i++) {
        swap(v[i], v[n - 1 - i]);
    }
    for (int i = 0; i < n; i++) cout << v[i] << " ";
    cout << endl;
    return 0;
}
```

## Intercalação de dois vetores em um terceiro vetor
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Fusão de Dados
- Conceitos: Preenchimento Alternado (C[2*i] = A[i], C[2*i+1] = B[i])
- Descrição: Intercalar os elementos dos vetores A e B em um vetor C de tamanho 2N.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int a[n], b[n], c[2 * n];
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < n; i++) cin >> b[i];
    
    for (int i = 0; i < n; i++) {
        c[2 * i] = a[i];
        c[2 * i + 1] = b[i];
    }
    for (int i = 0; i < 2 * n; i++) cout << c[i] << " ";
    cout << endl;
    return 0;
}
```

## Eliminar elementos duplicados de um vetor
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Vetores Únicos
- Conceitos: Construção de Vetor sem Repetição
- Descrição: Gerar um novo vetor contendo apenas os valores únicos do vetor original.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n], unicos[n], tamUnicos = 0;
    for (int i = 0; i < n; i++) {
        cin >> v[i];
        bool jTem = false;
        for (int k = 0; k < tamUnicos; k++) {
            if (unicos[k] == v[i]) { jTem = true; break; }
        }
        if (!jTem) unicos[tamUnicos++] = v[i];
    }
    for (int i = 0; i < tamUnicos; i++) cout << unicos[i] << " ";
    cout << endl;
    return 0;
}
```

## Deslocamento circular dos elementos de um vetor (Shift Left/Right)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Manipulação de Vetores
- Conceitos: Shift Esquerda (Salva primeiro elemento, desloca os demais e repõe no final)
- Descrição: Rotacionar os elementos de um vetor 1 posição para a esquerda.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int v[n];
    for (int i = 0; i < n; i++) cin >> v[i];
    
    int primeiro = v[0];
    for (int i = 0; i < n - 1; i++) {
        v[i] = v[i + 1];
    }
    v[n - 1] = primeiro;
    
    for (int i = 0; i < n; i++) cout << v[i] << " ";
    cout << endl;
    return 0;
}
```

## Matriz de distâncias entre N cidades
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Grafos e Redes
- Conceitos: Consulta de Tabela de Distâncias m[cidadeA][cidadeB]
- Descrição: Consultar a distância entre duas cidades A e B em uma matriz simétrica de distâncias.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int dist[3][3] = {{0, 100, 250}, {100, 0, 180}, {250, 180, 0}};
    int c1, c2;
    cin >> c1 >> c2;
    cout << "Distancia: " << dist[c1][c2] << " km" << endl;
    return 0;
}
```

## Matriz de notas de M alunos em N disciplinas
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Controle Escolar
- Conceitos: Média por Aluno (Média da Linha) e Média por Disciplina (Média da Coluna)
- Descrição: Armazenar notas de M alunos em N matérias e exibir as médias.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int alunos = 3, disc = 2;
    float notas[3][2] = {{8.0, 9.0}, {6.5, 7.5}, {10.0, 9.5}};
    
    for (int i = 0; i < alunos; i++) {
        float soma = 0;
        for (int j = 0; j < disc; j++) soma += notas[i][j];
        cout << "Aluno " << i << " Media: " << soma / disc << endl;
    }
    return 0;
}
```

## Matriz de estoque de N produtos em M lojas
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Logística de Vendas
- Conceitos: Somatório de Coluna (Estoque Total do Produto em todas as Lojas)
- Descrição: Calcular o estoque total disponível de cada produto somando todas as filiais.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int estoque[3][2] = {{10, 5}, {20, 15}, {30, 25}}; // 3 produtos em 2 lojas
    for (int p = 0; p < 3; p++) {
        int totalProd = 0;
        for (int l = 0; l < 2; l++) totalProd += estoque[p][l];
        cout << "Produto " << p << " Total: " << totalProd << endl;
    }
    return 0;
}
```

## Matriz jogo da velha (leitura e verificação de vencedor)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Jogos
- Conceitos: Verificação de Linhas, Colunas e Diagonais em Matriz 3x3
- Descrição: Verificar se o jogador 'X' ou 'O' venceu a partida de Jogo da Velha.
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    char t[3][3] = {{'X','X','X'}, {'O','','O'}, {'','',''}};
    char venc = ' ';
    for (int i = 0; i < 3; i++) {
        if (t[i][0] == t[i][1] && t[i][1] == t[i][2] && t[i][0] != ' ') venc = t[i][0];
        if (t[0][i] == t[1][i] && t[1][i] == t[2][i] && t[0][i] != ' ') venc = t[0][i];
    }
    if (venc != ' ') cout << "Vencedor: " << venc << endl;
    else cout << "Sem vencedor" << endl;
    return 0;
}
```

## Matriz de vizinhança / Jogo da Vida de Conway (contagem de vizinhos vivos)
- Linguagem: C++
- Categoria: Repetição e Matrizes
- Subcategoria: Autômatos Celulares
- Conceitos: Contagem de Vizinhança de Moore (8 vizinhos) em Matriz
- Descrição: Contar quantos vizinhos vivos cercam a célula m[i][j].
- Código:
```cpp
#include <iostream>
using namespace std;

int main() {
    int m[3][3] = {{1, 0, 1}, {0, 1, 0}, {1, 1, 0}};
    int r = 1, c = 1, vizinhosVivos = 0; // Célula central
    
    for (int dr = -1; dr <= 1; dr++) {
        for (int dc = -1; dc <= 1; dc++) {
            if (dr == 0 && dc == 0) continue;
            if (m[r + dr][c + dc] == 1) vizinhosVivos++;
        }
    }
    cout << "Vizinhos vivos de (1,1): " << vizinhosVivos << endl;
    return 0;
}
```
