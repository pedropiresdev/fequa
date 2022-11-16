## FEQUA - Ferramentas que Amamos


#### API para gerenciar ferramentas com seus respectivos nomes, links, descrições e tags.

Versão: 1.0 - Data: 14/11/2022 - Escrito por: Pedro Pires


Foi utilizado FastAPI para construir a API de gerenciamento, persistindo os dados em arquivo sqlite. Foi criado um
arquivo chamado database_requests para demonstrar os conhecimentos em MySQL, ainda que os requisitos não tenham sido
complexos no nível de demandar conhecimentos mais profundos. Contudo, preferi utilizar a ferramenta SQLModel para
criar os models e manipular o banco baseado em ORM. Desta forma me parece mais simples criar validações para os
dados recebidos.

### Autenticação

Usuários que desejem utilizar a ferramenta deverão se cadastrar fornecendo nome de usuário, e-mail, nome completo e uma
senha. O FEQUA armazenará estes dados no banco, já convertendo a senha em um hash. Estes dados serão serializados no
formato de dicionário, convertidos para base_64 e enviados ao microserviço de autenticação.

A autenticação que está em desenvolvimento será implementada usando Oauth2 em um outro microserviço chamado FEQUA_Auth.
A ideia é criar uma aplicação reativa e síncrona. Seguindo modelo de arquitetura distribuída, este serviço de
autenticação será acionado via RPC, por meio do Nameko / AMQP. Poderia ter utilizado arquitetura REST, mas como
utilizei neste microserviço, decidi fazer algo diferente. O serviço de autenticação receberá os dados de usuário
cadastrado e salvará estas informações num banco REDIS sempre que a action contida na RPC for do tipo save_credentials.
Para consultar credenciais e gerar Token Bearer JWT o action será get_token.

A API deverá receber um payload contendo as informações necessárias para a autenticação, validação, e roteamento
para os demais serviços.

Específico para comunicação entre máquinas, este Token **não ficará persistido em browsers**. O token não expira e não
contem informações sensíveis, mas poderemos mudar a sua assinatura a qualquer indício de vazamento ou abuso do mesmo.

Mais informações podem ser encontradas em https://jwt.io/

Este token é configurado no Header da requisição na chave **Authorization**.

### Endereços para solicitações (URLS) e padrões OAS e REST

Baseado no padrão OAS "**The OpenAPI Specification**", toda a nomenclatura, tanto no conteúdo das requisições
quanto nos endereços requisitados, seguem rigorosamente este padrão. Em caso de dúvida, o assunto pode ser aprofundado
em https://github.com/OAI/OpenAPI-Specification.

O padrão REST pode ser consultado em https://docs.microsoft.com/pt-br/azure/architecture/best-practices/api-design.

### Documentação da API

----------------------


### https://
Metodo `POST` Código de sucesso `202` Códigos de falha `404 422`

**Requisição**

| Chave   | Tipo  | Obrigatório | Opções | Descrição                                                      |
|---------|-------|-------------|--------|----------------------------------------------------------------|
|  `task` | `map` | Sim         |        | Este campo representa uma tarefa a ser executado pelo serviço. |


**Resposta**

| Chave      | Tipo     | Descrição                                                                       |
|------------|----------|---------------------------------------------------------------------------------|
|  `task_id` | `string` | Identificador único da tarefa, será utilizado para saber o resultado da tarefa. |


### Exemplos de Payload
<table>
    <thead>
        <tr>
            <th>Exemplo de Requisição</th>
        </tr>
    </thead><tbody>
<tr><td>

```json
{
  "task": {
    "username": ""
  }
}
```
</td>
</tr>
</tbody>
</table>

<table>
    <thead>
        <tr>
            <th>Exemplo de Resposta</th>
        </tr>
    </thead><tbody>
<tr><td>

```json
{
    "task_id": "fac1356c69c94d2180106b10c13c00ea",
}
```
</td>
</tr>
</tbody>
</table>

-----------------------------------------------

## Executar serviço

