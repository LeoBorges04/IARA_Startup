import os
import json
import random

# Definindo templates de exercicios e erros comuns para sintese do dataset de Fine-Tuning (IARA PBL)
EXERCISES_DATA = [
    {
        "topic": "Vetor e Maior Elemento em C++",
        "user_prompt": "Quero aprender como ler 5 notas em um vetor e encontrar a maior nota em C++",
        "problem_desc": "Você deve criar um programa que leia 5 notas em um vetor e encontre a maior nota digitada.",
        "step1_title": "Declaração do vetor e leitura das 5 notas",
        "step2_title": "Processamento para encontrar a maior nota",
        "step3_title": "Exibição do resultado",
        "flawed_code": "#include <iostream>\nusing namespace std;\nint main() {\n    float notas[5];\n    for (int i = 0; i <= 5; i++) {\n        cin >> notas;\n    }\n    return 0;\n}",
        "flawed_feedback": "Excelente tentativa! Porém há dois pontos de atenção na sua lógica:\n1. Estouro de Índice: O vetor tem 5 posições (índices 0 a 4). A condição i <= 5 tenta acessar o índice 5, o que é inválido.\n2. Leitura no Vetor: Em cin >> notas;, você precisa especificar o índice do vetor utilizando notas[i].\n\nPor favor, corrija a condição do laço e a leitura da variável e me envie a versão ajustada do Passo 1!",
        "correct_code": "#include <iostream>\nusing namespace std;\nint main() {\n    float notas[5];\n    for (int i = 0; i < 5; i++) {\n        cin >> notas[i];\n    }\n    return 0;\n}",
        "pass_feedback": "Perfeito! O Passo 1 está 100% correto. O vetor foi declarado adequadamente e a leitura das 5 notas foi feita com controle de índice seguro.\n\nAgora vamos para o Passo 2: Inicialize uma variável maior com o primeiro elemento do vetor (notas[0]) e percorra o vetor comparando cada elemento. Escreva o código apenas para o Passo 2."
    },
    {
        "topic": "Busca Binária em Vetor Ordenado",
        "user_prompt": "Como implementar uma busca binária em C++?",
        "problem_desc": "Você deve implementar uma busca binária eficiente em um vetor previamente ordenado de 10 elementos.",
        "step1_title": "Declaração e inicialização dos ponteiros inicio, fim e meio",
        "step2_title": "Laço while (inicio <= fim) e comparação da chave com o elemento meio",
        "step3_title": "Retorno do índice encontrado ou -1",
        "flawed_code": "int buscaBinaria(int arr[], int n, int chave) {\n    int inicio = 0, fim = n;\n    while (inicio < fim) {\n        int meio = (inicio + fim) / 2;\n        if (arr[meio] == chave) return meio;\n        if (arr[meio] < chave) inicio = meio;\n    }\n}",
        "flawed_feedback": "Ótima estrutura base! Vamos ajustar alguns detalhes de lógica:\n1. Ajuste de Limites: Ao atualizar o ponteiro inicio quando a chave é maior, use inicio = meio + 1 para evitar laço infinito.\n2. Condição de Parada: A condição do laço deve ser inicio <= fim para testar o último elemento remanescente.\n\nCorrija essa atualização de limites e me envie novamente!",
        "correct_code": "int buscaBinaria(int arr[], int n, int chave) {\n    int inicio = 0, fim = n - 1;\n    while (inicio <= fim) {\n        int meio = inicio + (fim - inicio) / 2;\n        if (arr[meio] == chave) return meio;\n        if (arr[meio] < chave) inicio = meio + 1;\n        else fim = meio - 1;\n    }\n    return -1;\n}",
        "pass_feedback": "Excelente! A função de busca binária foi implementada com perfeição lógica. Os ponteiros de limite são ajustados corretamente a cada iteração.\n\nAgora vamos para o próximo passo: crie a função main para ler a chave desejada e testar o retorno da busca binária."
    },
    {
        "topic": "Contagem de Números Pares",
        "user_prompt": "Como ler N números e contar quantos são pares em C++?",
        "problem_desc": "Você deve criar um programa que receba N números inteiros e conte a quantidade de números pares digitados.",
        "step1_title": "Declaração das variáveis (N, valor, contador pares) e leitura de N",
        "step2_title": "Laço de repetição com teste de módulo (valor % 2 == 0) e incremento",
        "step3_title": "Exibição do total de números pares",
        "flawed_code": "#include <iostream>\nusing namespace std;\nint main() {\n    int n, num, pares;\n    cin >> n;\n    for(int i=0; i<n; i++) {\n        cin >> num;\n        if (num % 2 = 0) pares + 1;\n    }\n}",
        "flawed_feedback": "Muito bem! Fique atento a dois detalhes sintáticos importantes:\n1. Operador de Comparação: No teste do if, utilize == (dois sinais de igual) para comparar igualdade, pois um único = é operador de atribuição.\n2. Incremento de Contador: Para incrementar a variável pares, utilize pares++ ou pares = pares + 1.\n3. Inicialização: Lembre-se de inicializar pares = 0 antes do laço.\n\nAjuste esses pontos e me envie a versão corrigida do Passo 1 e 2!",
        "correct_code": "#include <iostream>\nusing namespace std;\nint main() {\n    int n, num, pares = 0;\n    cin >> n;\n    for(int i = 0; i < n; i++) {\n        cin >> num;\n        if (num % 2 == 0) pares++;\n    }\n    cout << pares << endl;\n    return 0;\n}",
        "pass_feedback": "Parabéns! O código está perfeitamente correto. O teste de paridade com o operador módulo e o incremento da variável contadora foram implementados com sucesso!"
    },
    {
        "topic": "Conversão de Temperatura Celsius para Fahrenheit",
        "user_prompt": "Como fazer uma conversão de temperatura de Celsius para Fahrenheit em C++?",
        "problem_desc": "Você deve criar um algoritmo que receba a temperatura em graus Celsius e calcule o equivalente em Fahrenheit.",
        "step1_title": "Declaração das variáveis float para Celsius e Fahrenheit e leitura de Celsius",
        "step2_title": "Aplicação da fórmula fahrenheit = (celsius * 9.0 / 5.0) + 32.0",
        "step3_title": "Exibição da temperatura convertida",
        "flawed_code": "#include <iostream>\nusing namespace std;\nint main() {\n    int c, f;\n    cin >> c;\n    f = c * (9 / 5) + 32;\n    cout << f;\n}",
        "flawed_feedback": "Bom começo! Mas há uma pegadinha clássica com divisão inteira:\n1. Divisão de Inteiros: Em C++, 9 / 5 entre inteiros resulta em 1 (a parte decimal é descartada). Para obter o valor real 1.8, utilize 9.0 / 5.0.\n2. Tipos de Dados: Como temperaturas possuem decimais, use o tipo float ou double para c e f.\n\nAjuste a divisão e o tipo das variáveis e me envie o código corrigido!",
        "correct_code": "#include <iostream>\nusing namespace std;\nint main() {\n    float c, f;\n    cin >> c;\n    f = (c * 9.0 / 5.0) + 32.0;\n    cout << f << endl;\n    return 0;\n}",
        "pass_feedback": "Perfeito! Usar 9.0 / 5.0 garante a precisão decimal necessária na conversão. O algoritmo funciona perfeitamente!"
    }
]

CONCEPTUAL_QUESTIONS = [
    {
        "user": "Por que devemos usar float e não int para calcular a média de alunos?",
        "assistant": "Em C++, a média aritmética frequentemente resulta em um valor fracionário (por exemplo, a soma 15 dividida por 2 resulta em 7.5). Se você utilizar o tipo int, a linguagem realiza uma divisão inteira e descarta a parte decimal, resultando em 7. O tipo float permite armazenar e representar números reais com casas decimais, garantindo a precisão exata do resultado."
    },
    {
        "user": "Qual a diferença entre o laço for e o laço while?",
        "assistant": "O laço for é ideal quando você sabe antecipadamente a quantidade de iterações (por exemplo, percorrer um vetor de 10 posições), pois ele agrupa inicialização, condição e incremento no cabeçalho. Já o laço while é recomendado quando a quantidade de iterações é indeterminada e depende de uma condição que muda durante a execução (como ler valores até o usuário digitar zero)."
    },
    {
        "user": "Para que serve o operador módulo % em programação?",
        "assistant": "O operador módulo (%) calcula o resto inteiro da divisão entre dois números inteiros. Ele é amplamente utilizado para verificar se um número é par ou ímpar (num % 2 == 0), se é múltiplo de outro número (num % K == 0), para alternar posições em estruturas circulares ou para extrair dígitos de um número."
    },
    {
        "user": "Por que precisamos inicializar uma variável acumuladora de soma com zero?",
        "assistant": "Variáveis locais em C++ contêm valores residuais da memória (conhecidos como lixo de memória) antes de serem inicializadas. Se você tentar acumular valores usando soma += valor sem inicializar soma = 0, o resultado final incluirá o valor inicial aleatório da memória, gerando um cálculo incorreto."
    }
]

def generate_finetune_dataset(output_path: str, target_count: int = 250):
    print(f"=== GERANDO DATASET DE FINE-TUNING PARA IARA PBL ({target_count} EXEMPLOS) ===")
    
    system_prompt = (
        "Você é IARA, tutora virtual de programação baseada em Aprendizagem Baseada em Problemas (PBL Interativo). "
        "Sua postura é atenciosa, empática, encorajadora e estritamente objetiva. "
        "Quando o aluno solicitar um exercício, divida o problema em passos prioritários e peça o código do Passo 1. "
        "Quando o aluno enviar uma tentativa de código com erros, explique as falhas conceituais e lógicas em português com ZERO blocos de código na resposta. "
        "Quando o aluno acertar o passo, parabenize e apresente a instrução para o próximo passo."
    )

    examples = []

    # 1. Gerar variações de Apresentação do Desafio PBL (Turno 1)
    while len(examples) < target_count * 0.35:
        ex = random.choice(EXERCISES_DATA)
        msg_user = ex["user_prompt"]
        msg_assistant = (
            f"Ótimo! Vamos resolver este desafio de **{ex['topic']}** passo a passo.\n\n"
            f"**Enunciado do Problema:**\n{ex['problem_desc']}\n\n"
            f"**Passos Lógicos Necessários:**\n"
            f"- **Passo 1:** {ex['step1_title']}\n"
            f"- **Passo 2:** {ex['step2_title']}\n"
            f"- **Passo 3:** {ex['step3_title']}\n\n"
            f"Por favor, escreva o código em C++ apenas para o **Passo 1**, que envolve: {ex['step1_title']}."
        )
        examples.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg_user},
                {"role": "assistant", "content": msg_assistant}
            ]
        })

    # 2. Gerar variações de Correção de Código com Erro (Zero Código na Resposta) (Turno 2 Erro)
    while len(examples) < target_count * 0.70:
        ex = random.choice(EXERCISES_DATA)
        examples.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Quero resolver {ex['topic']}"},
                {"role": "assistant", "content": f"Vamos lá! Escreva apenas o código do Passo 1: {ex['step1_title']}."},
                {"role": "user", "content": ex["flawed_code"]},
                {"role": "assistant", "content": ex["flawed_feedback"]}
            ]
        })

    # 3. Gerar variações de Aprovação de Passo e Avanço (Turno 3 Sucesso)
    while len(examples) < target_count * 0.85:
        ex = random.choice(EXERCISES_DATA)
        examples.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Aqui está o meu código do Passo 1:\n{ex['correct_code']}"},
                {"role": "assistant", "content": ex["pass_feedback"]}
            ]
        })

    # 4. Gerar dúvidas conceituais diretas
    while len(examples) < target_count:
        q = random.choice(CONCEPTUAL_QUESTIONS)
        examples.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": q["user"]},
                {"role": "assistant", "content": q["assistant"]}
            ]
        })

    random.shuffle(examples)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for item in examples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Dataset salvo com sucesso em '{output_path}' com {len(examples)} exemplos JSONL!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ds_path = os.path.join(base_dir, "data", "finetune_dataset.jsonl")
    generate_finetune_dataset(ds_path, target_count=250)
