# CodeExporterApp

**CodeExporterApp** é uma ferramenta em Python projetada para exportar a estrutura de diretórios de projetos e o conteúdo de arquivos selecionados, criando um arquivo de saída que é ideal para consultas com IAs (como o ChatGPT) ou para facilitar a revisão e compartilhamento de código entre desenvolvedores.

## Motivação

Este projeto foi criado com o objetivo de simplificar a exportação das **estruturas de projetos** e o **conteúdo de arquivos** para situações onde você precisa fornecer contexto para IAs ou outros desenvolvedores ao tirar dúvidas sobre um projeto. Muitas vezes, é necessário compartilhar a estrutura completa de pastas de um projeto, juntamente com o conteúdo de arquivos específicos, de maneira organizada. O **CodeExporterApp** resolve esse problema, criando automaticamente um arquivo de texto `project_export.txt` com:
- Árvores de diretórios de um ou mais projetos.
- O conteúdo de arquivos específicos, organizados com seus respectivos caminhos (caso haja arquivos especificados no `config.json`).

## Requisitos

Para rodar o **CodeExporterApp**, você precisa ter:
- **Python 3.6** ou superior instalado em sua máquina.
- Acesso a um terminal ou prompt de comando para rodar scripts Python.

### Verifique se o Python está instalado

Para verificar se você tem o Python instalado, execute o seguinte comando no terminal:

```bash
python --version
```
Se o Python não estiver instalado, você pode baixá-lo e instalá-lo no [site oficial](https://www.python.org/downloads/).

## Entendendo o `config.json`

O arquivo `config.json` é a configuração principal que define quais diretórios de projeto e arquivos específicos serão exportados. Aqui está um exemplo de um arquivo `config.json` típico:

```json
{
    "projects": [
        "C:/dev/meu_projeto1",
        "C:/pessoal/meu_projeto2"
    ],
    "files": [
        "meu_projeto1/Controllers/UsuarioController.cs",
        "meu_projeto1/Models/UsuarioModel.cs",
        "meu_projeto2/src/components/Tabela/TabelaComponent.tsx",
        "meu_projeto2/src/components/Tabela/TabelaComponent.scss"
    ],
    "ignored_dirs": [
        ".git",
        "bin",
        "obj",
        "node_modules",
        "venv",
        ".idea",
        "...",
        "...",
        "..."
    ]
}
```

### Estrutura do `config.json`

1. `projects`:
    - É uma lista de diretórios de projetos cujas árvores de diretórios serão exportadas.
    - Deve conter um ou mais diretórios.

2. `files`:
    - Lista de arquivos específicos cujo conteúdo será exportado. Os caminhos devem incluir o nome do projeto (como no exemplo acima), e os arquivos devem estar contidos dentro dos diretórios listados em `projects`.
    - Pode conter um ou mais arquivos.
    - Se essa chave não for fornecida ou estiver vazia, o script apenas gerará a árvore de diretórios dos projetos especificados.

3. `ignored_dirs` (opcional):
    - Lista de diretórios que devem ser ignorados ao exportar a árvore de diretórios. Se essa chave não for especificada, uma lista padrão será usada.

### Porque modificar o `config.json`?

Você deve modificar o `config.json` para:

- Especificar quais projetos e arquivos você deseja exportar.
- Personalizar a lista de diretórios ignorados, dependendo das suas necessidades.

## Como rodar o projeto

Após configurar o `config.json`, siga os passos abaixo para rodar o **CodeExporterApp**:

1. Abra o terminal ou prompt de comando:
    - Navegue até o diretório onde o **CodeExporterApp** está localizado (onde o script `code_exporter.py` e o arquivo `config.json` estão).

2. Execute o script:
    - Execute o script Python no terminal com o seguinte comando:

```bash
python code_exporter.py
```

3. Saída:
    - Após a execução do script, ele irá gerar um arquivo chamado `project_export.txt`. Esse arquivo conterá:
        - A **árvore de diretórios** dos projetos especificados no `config.json`.
        - O **conteúdo dos arquivos** que você listou na chave `files` do `config.json` (se houver arquivos listados).

Verifique o arquivo gerado no mesmo diretório onde o script foi executado.

## Possíveis erros e como corrigi-los

### 1. Erro: O arquivo não está dentro de nenhum dos diretórios do projeto

Esse erro ocorre quando você especifica um arquivo na chave `files` que não está contido dentro de nenhum dos diretórios listados em `projects`. Verifique se o caminho do arquivo está correto e se ele realmente está dentro de um dos projetos especificados.

### 2. Erro: Arquivo `config.json` não encontrado

Esse erro ocorre porque o script depende do arquivo `config.json` para funcionar corretamente. Certifique-se de que o arquivo está presente na mesma pasta que o script e está devidamente configurado.

### 3. Erro ao analisar o arquivo `config.json`

Esse erro pode ser corrigido revisando o `config.json` e garantindo que ele esteja bem formatado (todas as chaves e valores estejam corretamente configurados, e que as listas estejam fechadas corretamente).

<br></br>
**青木**