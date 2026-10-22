# 2. DESENVOLVIMENTO

O processo de desenvolvimento da IARA envolveu diferentes etapas, abrangendo desde o planejamento inicial e a prototipação das interfaces até a implementação técnica do sistema. Neste tópico, serão apresentados os métodos de organização utilizados para estruturar o projeto, as tecnologias aplicadas na implementação e as telas desenvolvidas com suas respectivas funcionalidades, detalhando as decisões de design tomadas ao longo do processo.

---

## 2.1. Métodos de Organização

Para a estruturação do projeto, foram utilizados diferentes métodos de organização que auxiliaram a equipe a planejar tanto o conteúdo das telas quanto as funcionalidades do sistema. Esses métodos permitiram acompanhar o percurso do usuário desde os primeiros esboços até a definição do fluxo de navegação. Nesse processo, destacam-se três etapas principais: a criação do protótipo de baixa fidelidade, a elaboração do wireframe e a construção do fluxo do usuário.

### 2.1.1. Protótipo de Baixa Fidelidade

O primeiro passo foi elaborar um protótipo de baixa fidelidade. Nessa etapa, foram esboçadas as telas principais e suas funcionalidades básicas, permitindo que a equipe tivesse uma visão inicial de como o sistema deveria se organizar. Esse processo foi essencial para validar as ideias de forma rápida, possibilitando ajustes antes da digitalização e do detalhamento das interfaces.

O protótipo contemplou cinco telas principais: a tela de Login, por onde o usuário acessa o sistema; a tela de Cadastro, para criação de novas contas; a Tela Inicial de Chat, que representa o núcleo de interação do aluno com a IARA; a tela de Configurações, para ajuste de dados do perfil; e a Tela Administrativa (Tela Prof.), destinada ao gerenciamento de turmas e materiais pelo professor.

> **FIGURA 1 – Protótipo de Baixa Fidelidade (Wireframing)**
> *(Inserir aqui a imagem do arquivo `Wireframing.jpeg`)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.1.2. Wireframe

Com base no protótipo de baixa fidelidade, foi elaborado o wireframe digital do sistema, utilizando a ferramenta **Figma**. O wireframe representou a estrutura das telas de forma mais detalhada, definindo o posicionamento dos elementos visuais, a hierarquia das informações e os fluxos de navegação entre as páginas. Essa etapa intermediária permitiu alinhar as decisões de design antes da construção do protótipo de alta fidelidade, garantindo que a organização das interfaces estivesse coerente com os objetivos do sistema e com as necessidades dos usuários.

---

### 2.1.3. Fluxo de Usuário

A partir do wireframe, foi construído o fluxo de usuário, representando o caminho percorrido pelo usuário ao interagir com o sistema desde o acesso inicial até a conclusão de suas tarefas. O fluxo evidencia as principais rotas de navegação, os pontos de decisão e as telas acessadas em cada etapa, diferenciando o percurso do aluno do percurso do professor.

> **FIGURA 2 – Fluxo de Usuário da IARA**
> *(Inserir aqui o diagrama de fluxo de usuário gerado no Mermaid ou Figma)*
>
> FONTE: Elaborado pelos autores (2025)

---

## 2.2. Tecnologias Utilizadas

O sistema IARA foi desenvolvido com tecnologias web consolidadas, priorizando a compatibilidade, o desempenho e a facilidade de execução em diferentes ambientes. O frontend foi construído com **HTML**, **CSS** e **JavaScript** puros (Vanilla), sem dependência de frameworks front-end, garantindo leveza e portabilidade. A estilização adota um sistema de design próprio, com paleta de cores baseada em gradientes rosa e roxo, tipografia da família *Outfit* e *Plus Jakarta Sans* (via Google Fonts) e componentes responsivos.

O backend foi desenvolvido em **Python** com o framework **FastAPI**, responsável pelo gerenciamento de rotas, autenticação de usuários, persistência de conversas e integração com o motor de respostas. O sistema de respostas da IARA é baseado em **RAG** (*Retrieval-Augmented Generation*), que combina uma base de conhecimento estruturada em Markdown com a geração de respostas orientadas pelo método socrático. O banco de dados utilizado é o **MongoDB Atlas**, com suporte a um modo de operação local em memória (*In-Memory Store*) para execução sem necessidade de conexão externa.

---

## 2.3. Telas Desenvolvidas

As telas foram elaboradas em protótipo de alta fidelidade no Figma, com base nos protótipos, wireframes e fluxo de usuário previamente definidos, garantindo consistência entre planejamento e implementação. Cada interface foi projetada para facilitar a navegação, organizar as informações de forma clara e proporcionar uma experiência interativa ao usuário.

O sistema é composto por seis telas principais: a tela de **Login**, a tela de **Escolha de Perfil**, a tela de **Cadastro**, a **Interface de Chat** (área do aluno), a tela de **Seleção e Gerenciamento de Turmas** e o **Painel de Conteúdo** (área do professor). A seguir, cada tela será descrita com seus elementos visuais, funcionalidades e decisões de design.

---

### 2.3.1. Tela de Login

A tela de Login é o ponto de entrada do sistema e foi projetada para oferecer uma experiência clara, acolhedora e objetiva. O layout adota uma divisão em dois painéis: o painel esquerdo exibe a identidade visual da plataforma, com o logotipo da IARA, o nome completo do sistema e uma ilustração representativa da assistente virtual; o painel direito concentra o formulário de autenticação, com campos de e-mail e senha, botão de acesso e link para criação de conta.

A hierarquia visual conduz o olhar do usuário de forma natural: a saudação em destaque ("Seja Bem-vindo!") estabelece o tom acolhedor da plataforma, seguida dos campos do formulário e, por fim, do botão de ação principal. A cor de destaque rosa (#FF5C8A) é utilizada nos ícones dos campos e no botão, reforçando a identidade visual do sistema.

Em relação ao *affordance*, todos os elementos interativos — campos de texto e botão de envio — são visualmente autoexplicativos, com ícones que indicam claramente a natureza de cada campo (envelope para e-mail, cadeado para senha).

> **FIGURA 3 – Protótipo de Alta Fidelidade: Tela de Login**
> *(Inserir aqui a captura de tela do protótipo Figma da tela de Login)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.3.2. Tela de Escolha de Perfil

Antes de prosseguir para o cadastro, o usuário é direcionado a uma tela intermediária de escolha de perfil, cujo objetivo é personalizar a experiência desde o início. A tela apresenta a pergunta "Quem vai usar a IARA?" e oferece duas opções em formato de cartões clicáveis: **Aluno** e **Professor**.

Cada cartão exibe um ícone representativo, o nome do perfil e uma breve descrição de sua finalidade dentro do sistema — o aluno é descrito como aquele que aprende programação e pratica exercícios, enquanto o professor é apresentado como quem cria turmas, acompanha alunos e acessa relatórios. Essa distinção orientada a papéis garante que o fluxo de cadastro seja direcionado corretamente e que o perfil do usuário seja definido desde o primeiro contato com a plataforma.

O mesmo painel esquerdo da tela de Login é mantido nesta tela, preservando a identidade visual e a continuidade da experiência entre as páginas do fluxo de autenticação.

> **FIGURA 4 – Protótipo de Alta Fidelidade: Tela de Escolha de Perfil**
> *(Inserir aqui a captura de tela do protótipo Figma da tela de Escolha de Perfil)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.3.3. Tela de Cadastro

A tela de Cadastro mantém a estrutura visual de dois painéis, em continuidade com as telas anteriores do fluxo de autenticação. O formulário solicita quatro informações: nome completo, e-mail, senha e confirmação de senha. O sistema realiza validações visuais em tempo real durante o preenchimento: o campo de e-mail exibe um indicador verde quando o formato é válido e vermelho quando inválido; os campos de senha apresentam feedback visual de correspondência entre os dois campos.

Após o preenchimento e a submissão bem-sucedida do formulário, o usuário é automaticamente autenticado e redirecionado à área correspondente ao seu perfil — a Interface de Chat, para alunos, ou a tela de Seleção de Turmas, para professores. Esse comportamento de *auto-login* após o cadastro elimina uma etapa desnecessária na experiência do novo usuário, reduzindo a fricção no início da jornada.

> **FIGURA 5 – Protótipo de Alta Fidelidade: Tela de Cadastro**
> *(Inserir aqui a captura de tela do protótipo Figma da tela de Cadastro)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.3.4. Interface de Chat — Área do Aluno

A Interface de Chat representa o núcleo da experiência do aluno na plataforma e foi projetada com base em padrões consolidados de interfaces de assistentes conversacionais. O layout é dividido em dois blocos: uma barra lateral à esquerda (*sidebar*) e a área principal de conversa à direita.

A barra lateral concentra os elementos de gerenciamento: o botão de criação de novas conversas, a lista de conversas recentes com indicação de turma associada e o rodapé com as informações do usuário logado, acesso às configurações de perfil e botão de encerramento de sessão. Professores e administradores têm acesso a um botão adicional no cabeçalho, que os direciona ao painel de gerenciamento de conteúdo.

A área principal exibe as mensagens em bolhas diferenciadas por remetente — o usuário à direita e a IARA à esquerda —, com suporte à renderização de Markdown e fórmulas matemáticas. A resposta da IARA é exibida com efeito de digitação progressiva (*typewriter*), que reforça a percepção de uma conversa em tempo real. Durante a geração da resposta, o botão de envio é substituído por um botão de cancelamento, permitindo ao usuário interromper a resposta a qualquer momento.

Quando o aluno inicia uma nova conversa e existem múltiplas turmas cadastradas pelo professor, o sistema exibe um modal de seleção de turma, associando a conversa ao acervo de conhecimento correspondente.

> **FIGURA 6 – Protótipo de Alta Fidelidade: Interface de Chat (Área do Aluno)**
> *(Inserir aqui a captura de tela do protótipo Figma da Interface de Chat)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.3.5. Tela de Seleção e Gerenciamento de Turmas — Área do Professor

Após o login ou cadastro como professor, o usuário é direcionado à tela de Seleção de Turmas, que funciona como o painel inicial da área docente. A tela apresenta em grade as turmas cadastradas pelo professor, cada uma exibida em um cartão com nome, código identificador, descrição e tipo de disciplina. Um botão de ação no topo da página permite ao professor criar uma nova turma.

Ao clicar em "Criar Nova Turma", um modal é exibido com campos para nome, código identificador (opcional), descrição (opcional) e tipo da disciplina. O tipo da disciplina oferece duas opções: **Programação (PBL Estrito)**, que ativa o modo socrático padrão da IARA para lógica e algoritmos, e **Outra Matéria (Diretrizes Customizadas)**, que disponibiliza um campo de texto para o professor definir as orientações de comportamento da IARA para aquela turma específica. Essa flexibilidade permite que o sistema seja utilizado em diferentes contextos pedagógicos além da programação.

> **FIGURA 7 – Protótipo de Alta Fidelidade: Tela de Seleção de Turmas**
> *(Inserir aqui a captura de tela do protótipo Figma da tela de Seleção de Turmas)*
>
> FONTE: Elaborado pelos autores (2025)

---

### 2.3.6. Painel de Conteúdo e Materiais — Área do Professor

Após selecionar uma turma, o professor é direcionado ao Painel de Conteúdo, que concentra as ferramentas de gestão do acervo de conhecimento (*RAG*) da turma selecionada. O nome da turma ativa é exibido de forma destacada no cabeçalho da página, conferindo clareza ao contexto de trabalho.

O painel é organizado em seções distintas. A seção de upload permite ao professor enviar arquivos nos formatos PDF, Markdown e texto simples, que são processados e indexados pelo sistema como base de conhecimento da turma. A seção de documentos exibe a lista de materiais já enviados, com a opção de remoção individual de cada item. Por fim, uma seção exibe a lista de alunos associados à turma, permitindo ao professor acompanhar quem está utilizando o sistema naquele contexto.

Um botão de retorno no topo da página permite ao professor voltar à tela de Seleção de Turmas, preservando a continuidade da navegação entre as áreas administrativas.

> **FIGURA 8 – Protótipo de Alta Fidelidade: Painel de Conteúdo (Área do Professor)**
> *(Inserir aqui a captura de tela do protótipo Figma do Painel de Conteúdo)*
>
> FONTE: Elaborado pelos autores (2025)

---

> **Nota para o grupo:** Substituir cada marcação *(Inserir aqui...)* pela captura de tela correspondente do protótipo de alta fidelidade desenvolvido no Figma. As figuras devem ser centralizadas, com legenda abaixo no formato "FIGURA X – [Nome]" e fonte "Elaborado pelos autores (2025)", seguindo o padrão ABNT adotado no documento.
