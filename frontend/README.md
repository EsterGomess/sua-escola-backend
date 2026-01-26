# Frontend — `index.html`

Descrição
- Interface web estática para gerenciamento simples de estudantes (CRUD) com armazenamento em `localStorage`.
- Funciona sem servidor (via `file://`) e também com templates externos se servido por HTTP.

Tecnologias
- HTML5, JavaScript (Vanilla), Bootstrap 5 (CDN)
- Arquivo principal: `frontend/index.html`
- Estilos: `frontend/styles/style.css`

Como usar
- Abrir diretamente: abrir `frontend/index.html` no navegador (funciona via `file://`).


Funcionalidades
- Listar estudantes cadastrados em uma tabela.
- Adicionar, editar e remover estudantes via modal.
- Adicionar múltiplos responsáveis (guardians) com dados pessoais, endereço e contato.
- Busca simples (campo de pesquisa no cabeçalho).
- Responsivo graças ao Bootstrap.

Armazenamento e formato de dados
- Dados salvos em `localStorage` com a chave: `suaescola_students_v1`
- Estrutura de exemplo de um estudante:
```json
{
  "id": 1,
  "name": "Ana",
  "surname": "Costa",
  "address": { "street": "Rua A", "city": "Cidade" },
  "contact": { "ddd": "11", "phone": "99999-0000" },
  "guardians": [
    {
      "name": "Maria",
      "surname": "Oliveira",
      "address": { "street": "Rua B", "city": "Outra" },
      "contact": { "ddd": "11", "phone": "98888-1111" }
    }
  ]
}