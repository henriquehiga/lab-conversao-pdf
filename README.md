## Documentação do Serviço Flask para Conversão de PDF para Texto

### Sumário

- [Introdução](#introdução)
- [Configuração](#configuração)
- [Endpoints](#endpoints)
  - [POST /converte-pdf-para-txt](#post-converte-pdf-para-txt)
  - [GET /download/<filename>](#get-download-filename)
  - [POST /emite-relatorio](#post-emite-relatorio)
  - [GET /](#get)
- [Funções Auxiliares](#funções-auxiliares)
- [Execução](#execução)
- [Dockerização](#dockerização)

### Introdução

Este serviço Flask fornece uma API para conversão de arquivos PDF em arquivos de texto, além de possibilitar o download dos arquivos convertidos e a emissão de relatórios de log.

### Configuração

As principais configurações do aplicativo estão definidas na seção de configuração do Flask:

- `PASTA_UPLOAD`: Diretório onde os arquivos enviados serão armazenados.
- `EXTENSOES_PERMITIDAS`: Conjunto de extensões de arquivos permitidas (atualmente, apenas PDF).
- `PASTA_LOGS`: Diretório onde os logs da aplicação serão armazenados.
- `TOKEN_SERVICO`: Token de autenticação para acesso ao endpoint de emissão de relatório.

### Endpoints

#### POST /converte-pdf-para-txt

Converte um arquivo PDF enviado para um arquivo de texto.

**Parâmetros de Entrada:**

- Arquivo PDF no campo 'file' da requisição.

**Respostas:**

- `201 Created`: Conversão bem-sucedida.
  - Corpo da resposta:
    ```json
    {
      "mensagem": "Conversão concluída",
      "arquivo_txt": "nome_do_arquivo.txt",
      "link_download": "/download/nome_do_arquivo.txt"
    }
    ```
- `400 Bad Request`: Nenhum arquivo enviado ou arquivo não permitido.
  - Corpo da resposta:
    ```json
    {
      "erro": "Mensagem de erro"
    }
    ```
- `500 Internal Server Error`: Erro na conversão do arquivo.
  - Corpo da resposta:
    ```json
    {
      "erro": "Mensagem de erro"
    }
    ```

#### GET /download/<filename>

Permite o download do arquivo convertido.

**Parâmetros de URL:**

- `filename`: Nome do arquivo a ser baixado.

**Respostas:**

- `200 OK`: Retorna o arquivo solicitado.
- `404 Not Found`: Arquivo não encontrado.

#### POST /emite-relatorio

Emite um relatório de log.

**Cabeçalhos:**

- `Authorization`: Token de autenticação necessário para acessar o serviço.

**Respostas:**

- `200 OK`: Relatório emitido com sucesso.
  - Corpo da resposta:
    ```json
    {
      "relatorio": "Conteúdo do log"
    }
    ```
- `403 Forbidden`: Acesso não autorizado.
  - Corpo da resposta:
    ```json
    {
      "erro": "Acesso não autorizado"
    }
    ```
- `500 Internal Server Error`: Erro ao emitir o relatório.
  - Corpo da resposta:
    ```json
    {
      "erro": "Mensagem de erro"
    }
    ```

#### GET /

Serve a página `index.html` a partir do diretório raiz.

**Respostas:**

- `200 OK`: Retorna a página `index.html`.

### Funções Auxiliares

- `arquivo_permitido(nome_arquivo)`: Verifica se a extensão do arquivo é permitida.
- `pdf_para_texto(caminho_pdf)`: Converte o conteúdo de um PDF em texto.
- `registra_log(mensagem)`: Registra uma mensagem no log da aplicação.
- `decode_text(input_text)`: Decodifica o texto do log em UTF-8, tratando possíveis erros de decodificação.

### Execução

Para executar o serviço, utilize o comando abaixo no terminal:

```bash
python nome_do_arquivo.py
```

O serviço estará disponível no endereço `http://0.0.0.0:5000`.

#### Passos para Construir e Executar o Container Docker

1. **Construa a imagem Docker:**
   ```bash
   docker build -t nome_da_imagem .
   ```

2. **Execute o container Docker:**
   ```bash
   docker run -p 5000:5000 nome_da_imagem
   ```

O serviço estará disponível no endereço `http://0.0.0.0:5000` quando executado dentro de um container Docker.
