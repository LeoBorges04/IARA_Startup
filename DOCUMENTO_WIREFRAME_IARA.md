# Justificativa Técnica e Estratégica para o Uso de Wireframes no Projeto IARA 🧠

**Projeto:** IARA — Inteligência Artificial de Raciocínio Algorítmico  
**Domínio:** Plataforma Educacional de Engenharia / Ciência da Computação  
**Data:** 14 de Agosto de 2026  
**Documento:** Justificativa de Engenharia de Software e UX Design  

---

## 1. Introdução e Contexto do Projeto IARA

O **IARA** (*Inteligência Artificial de Raciocínio Algorítmico*) é uma plataforma educacional desenvolvida para atuar como tutora virtual interativa, auxiliando estudantes universitários no desenvolvimento de habilidades em lógica de programação, estruturas de dados e algoritmos.

Por se tratar de um ambiente onde o aluno lida com conceitos de alta complexidade abstrata e resolução de problemas estruturados, a **interface de usuário (UI)** e a **experiência do usuário (UX)** desempenham um papel crítico no sucesso pedagógico. Uma interface poluída, confusa ou mal estruturada pode gerar sobrecarga cognitiva, desviando a atenção do aluno do aprendizado dos algoritmos.

Para garantir que a plataforma ofereça uma experiência fluida, intuitiva e focada no aprendizado, a equipe adotou a **técnica de Wireframe** nas etapas iniciais de concepção e design de software.

---

## 2. O que é a Técnica de Wireframe?

Um **wireframe** é um guia visual de baixa ou média fidelidade que representa a estrutura óssea (esqueleto) de uma interface web ou aplicação. Ele funciona como o "blueprint" ou planta baixa do software, priorizando:

- **Estrutura e Layout:** Disposição espacial dos elementos na tela.
- **Arquitetura da Informação:** Hierarquia e organização do conteúdo visual e textual.
- **Fluxos de Navegação:** Como o usuário se desloca entre diferentes telas e seções.
- **Funcionalidades:** Identificação dos botões, áreas de entrada de dados (prompts), histórico de mensagens e componentes operacionais.

Diferente de um *mockup* (que foca nas cores, tipografia e estilo gráfico final) ou de um *protótipo funcional* (que contém interatividade real), o wireframe intencionalmente desconsidera elementos estéticos detalhados para focar estritamente no **funcionamento, usabilidade e lógica estrutural**.

---

## 3. Por que usamos Wireframes no Projeto IARA?

A adoção da técnica de wireframe para a plataforma IARA justifica-se por cinco pilares fundamentais da Engenharia de Software e do Design de Interação:

### 3.1. Minimização da Sobrecarga Cognitiva (Ergonomia Cognitiva no Ensino)
O aprendizado de raciocínio algorítmico exige grande esforço mental por parte do estudante. Ao desenhar wireframes antes da implementação:
- Garantimos que os elementos essenciais (caixa de chat com a IA, bloco de código, explicações conceituais e botões de ação) estejam organizados de forma clara e sem distrações visuais.
- Definimos uma hierarquia visual intuitiva, permitindo que o aluno foque 100% no diálogo pedagógico com a tutora inteligente.

### 3.2. Mapeamento da Arquitetura da Informação do Chat de IA
Diferente de sites institucionais estáticos, a IARA é uma aplicação dinâmica baseada em conversas (Chat UI) conectada a um sistema RAG (*Retrieval-Augmented Generation*). O wireframe permitiu planejar estrategicamente:
- **Painel Lateral (Sidebar):** Gestão e histórico de conversas passadas, criação de novos chats e alternância rápida.
- **Área Central de Mensagens:** Exibição clara de prompts do aluno e respostas da IARA com suporte a formatação markdown e blocos de código com destaque sintático.
- **Barra de Entrada de Dados (Prompt Bar):** Posicionamento acessível do campo de digitação e botão de envio, com espaço para ações rápidas (dicas, limpeza de contexto, etc.).
- **Painel Administrativo (`admin.html`):** Estrutura funcional para gestão de bases de conhecimento RAG, prompts do sistema e monitoramento.

### 3.3. Validação Ágil dos Fluxos de Usuário (*User Journey*)
O wireframe permite simular e validar os fluxos fundamentais da aplicação antes de escrever qualquer linha de código no frontend ou backend:
1. **Fluxo de Autenticação:** Acesso via `login.html` e `register.html`, garantindo redirecionamentos seguros e intuitivos.
2. **Fluxo do Estudo Guiado:** Seleção de fases e tópicos de exercícios (`conceitos_fase3.md`, `exercicios_fase3.md`, etc.), permitindo que a IARA entregue conteúdos adequados ao nível do aluno.
3. **Fluxo de Administração:** Navegação do administrador para inserção de novos exercícios e ajuste de hiperparâmetros da IA.

### 3.4. Redução drástica de Custos e Retrabalho (Engenharia Ágil)
Alterar a posição de uma sidebar, botão ou modal em um wireframe no Figma/Miro leva **segundos**. Alterar a mesma estrutura após o código HTML5, CSS3 moderno e Vanilla JavaScript estar pronto e integrado às rotas FastAPI em Python consome **horas ou dias de refatoração**.
- O uso de wireframes eliminou retrabalho no desenvolvimento do `script.js` e do `style.css`.
- As especificações de layout ficaram claras desde o início, acelerando a fase de codificação.

### 3.5. Alinhamento Multidisciplinar da Equipe
O desenvolvimento da IARA envolve competências de **Frontend**, **Backend em Python (FastAPI/MongoDB)**, **Engenharia de Prompt/RAG** e **Pedagogia/Didática**.
- O wireframe serve como uma **linguagem universal** entre desenvolvedores, designers e especialistas em conteúdo.
- Todos visualizam exatamente o mesmo produto final antes de iniciar a construção, alinhando expectativas de negócios e funcionais.

---

## 4. Resumo dos Benefícios da Técnica para a IARA

| Benefício | Descrição no Contexto da IARA |
| :--- | :--- |
| **Clareza de Requisitos** | Mapeou todos os componentes das telas (`index.html`, `login.html`, `register.html`, `admin.html`). |
| **Foco na UX Educacional** | Garantia de uma interface sem ruídos visuais, priorizando a leitura de código e diálogo com a IA. |
| **Agilidade de Prototipagem** | Permitiu iterar e testar múltiplos layouts em minutos antes de codificar em JS/CSS. |
| **Integração Frontend-Backend** | Facilitou a definição de quais dados seriam consumidos das APIs (`/api/chats`, `/api/auth`) em cada tela. |
| **Economia de Recursos** | Evitou refatorações custosas durante o desenvolvimento das rotas e scripts da plataforma. |

---

## 5. Conclusão

A utilização da técnica de wireframe no desenvolvimento da plataforma **IARA** foi uma decisão estratégica fundamental. Ela garantiu que a complexidade técnica do backend (FastAPI, RAG, OpenAI e MongoDB) fosse entregue através de uma interface limpa, ergonômica e estritamente alinhada às necessidades pedagógicas de estudantes de raciocínio algorítmico.

Através dos wireframes, a IARA foi concebida com foco no usuário desde o primeiro momento, estabelecendo as bases para um desenvolvimento ágil, econômico e de alta qualidade.
