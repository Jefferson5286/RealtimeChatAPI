## Estrutura do Projeto

Este projeto segue uma organização modular para facilitar a manutenção e o desenvolvimento de novas funcionalidades. Abaixo, explicamos a função de cada pasta e arquivo, assim como instruções para contribuir seguindo a estrutura:

```
├── apps
│   ├── authentication
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── __init__.py
├── exceptions
│   └── __init__.py
├── main.py
├── requirements.txt
└── tools
    ├── caching.py
    ├── email.py
    ├── __init__.py
    └── token.py
```

### Descrição dos Diretórios

- **apps/**: Contém os aplicativos principais e módulos do projeto, separados por domínio. Cada novo módulo deve ter uma estrutura semelhante ao `authentication/`, com arquivos específicos para rotas, esquemas e lógica adicional.
  - **authentication/**: Módulo de autenticação, incluindo rotas de login e registro.
    - `routes.py`: Define as rotas e os endpoints de autenticação.
    - `schemas.py`: Define os modelos de dados para validação e transferência de informações no módulo.
    - `__init__.py`: Arquivo de inicialização do módulo, responsável por importar as rotas e adicioná-las à lista de rotas do aplicativo.

- **exceptions/**: Define exceções personalizadas do projeto. Cada módulo pode adicionar suas próprias exceções neste diretório.

- **main.py**: Arquivo principal do projeto, onde o aplicativo FastAPI é inicializado e os módulos são incluídos.

- **requirements.txt**: Lista de dependências do projeto. Adicione bibliotecas necessárias para o funcionamento do projeto aqui.

- **tools/**: Contém utilitários e ferramentas auxiliares usados em várias partes do projeto.
  - `caching.py`: Funções para lidar com caching em memória.
  - `email.py`: Funções para envio de emails assíncronos.
  - `token.py`: Funções relacionadas à criação e validação de tokens.

### Diretrizes para Contribuidores

Ao adicionar novas funcionalidades, siga estas diretrizes para manter a consistência da estrutura:

1. **Novos módulos**: Adicione novos módulos dentro do diretório `apps/`. Cada módulo deve conter pelo menos os arquivos `routes.py` e `schemas.py` para manter a separação de responsabilidades.
2. **Exceções**: Se seu módulo exige novas exceções, adicione-as dentro do diretório `exceptions/` ou como subdiretórios, caso seja um conjunto específico de exceções.
3. **Ferramentas**: Ferramentas ou funções utilitárias reutilizáveis devem ser adicionadas no diretório `tools/`.
4. **Dependências**: Atualize o arquivo `requirements.txt` com quaisquer novas dependências necessárias para o funcionamento da sua funcionalidade.
5. **`__init__.py`**: O arquivo `__init__.py` dentro de cada módulo (como o módulo `authentication/`) deve incluir a importação de suas rotas e adicioná-las à lista de rotas do aplicativo. O conteúdo do `__init__.py` deve seguir este padrão:

    ```python
    from fastapi import APIRouter
    from typing import List

    import apps.authentication.routes  # Importar o módulo de rotas

    routes: List[APIRouter] = [
        apps.<application-name>.routes.route,  # Adicionar as rotas do módulo
    ]
    ```

Mantendo essa estrutura, facilitamos a colaboração e asseguramos a escalabilidade do projeto.