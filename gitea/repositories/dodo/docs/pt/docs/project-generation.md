# Geração de Projetos - Modelo

Você pode usar um gerador de projetos para começar, por já incluir configurações iniciais, segurança, banco de dados e os primeiros _endpoints_ API já feitos para você.

Um gerador de projetos sempre terá uma pré-configuração que você pode atualizar e adaptar para suas próprias necessidades, mas pode ser um bom ponto de partida para seu projeto.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Recursos

* Integração completa **Docker**.
* Modo de implantação Docker Swarm.
* Integração e otimização **Docker Compose** para desenvolvimento local.
* **Pronto para Produção** com servidor _web_ usando Uvicorn e Gunicorn.
* _Backend_ <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> Python:
    * **Rápido**: Alta performance, no nível de **NodeJS** e **Go** (graças ao Starlette e Pydantic).
    * **Intuitivo**: Ótimo suporte de editor. <abbr title="também conhecido como auto-complete, auto completação, IntelliSense">_Auto-Complete_</abbr> em todo lugar. Menos tempo _debugando_.
    * **Fácil**: Projetado para ser fácil de usar e aprender. Menos tempo lendo documentações.
    * **Curto**: Minimize duplicação de código. Múltiplos recursos para cada declaração de parâmetro.
    * **Robusto**: Tenha código pronto para produção. Com documentação interativa automática.
    * **Baseado em Padrões**: Baseado em (e completamente compatível com) padrões abertos para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> e <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**Muitos outros recursos**</a> incluindo validação automática, serialização, documentação interativa, autenticação com _tokens_ OAuth2 JWT etc.
* **Senha segura** _hashing_ por padrão.
* Autenticação **Token JWT**.
* Modelos **SQLAlchemy** (independente de extensões Flask, para que eles possam ser usados com _workers_ Celery diretamente).
* Modelos básicos para usuários (modifique e remova conforme suas necessidades).
* Migrações **Alembic**.
* **CORS** (_Cross Origin Resource Sharing_ - Compartilhamento de Recursos Entre Origens).
* _Worker_ **Celery** que pode importar e usar modelos e códigos do resto do _backend_ seletivamente.
* Testes _backend_ _REST_ baseados no **Pytest**, integrados com Docker, então você pode testar a interação completa da API, independente do banco de dados. Como roda no Docker, ele pode construir um novo repositório de dados do zero toda vez (assim você pode usar ElasticSearch, MongoDB, CouchDB, ou o que quiser, e apenas testar que a API esteja funcionando).
* Fácil integração com Python através dos **Kernels Jupyter** para desenvolvimento remoto ou no Docker com extensões como Atom Hydrogen ou Visual Studio Code Jupyter.
* _Frontend_ **Vue**:
    * Gerado com Vue CLI.
    * Controle de **Autenticação JWT**.
    * Visualização de _login_.
    * Após o _login_, visualização do painel de controle principal.
    * Painel de controle principal com criação e edição de usuário.
    * Edição do próprio usuário.
    * **Vuex**.
    * **Vue-router**.
    * **Vuetify** para belos componentes _material design_.
    * **TypeScript**.
    * Servidor Docker baseado em **Nginx** (configurado para rodar "lindamente" com Vue-router).
    * Construção multi-estágio Docker, então você não precisa salvar ou _commitar_ código compilado.
    * Testes _frontend_ rodados na hora da construção (pode ser desabilitado também).
    * Feito tão modular quanto possível, então ele funciona fora da caixa, mas você pode gerar novamente com Vue CLI ou criar conforme você queira, e reutilizar o que quiser.
* **PGAdmin** para banco de dados PostgreSQL, você pode modificar para usar PHPMyAdmin e MySQL facilmente.
* **Flower** para monitoração de tarefas Celery.
* Balanceamento de carga entre _frontend_ e _backend_ com **Traefik**, então você pode ter ambos sob o mesmo domínio, separados por rota, mas servidos por diferentes containers.
* Integração Traefik, incluindo geração automática de certificados **HTTPS** Let's Encrypt.
* GitLab **CI** (integração contínua), incluindo testes _frontend_ e _backend_.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **WARNING** ⚠️

Se você está iniciando um novo projeto do zero, verifique as alternativas aqui.

Por exemplo, o gerador de projetos <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a> pode ser uma alternativa melhor, como ele é ativamente mantido e utilizado. E ele inclui todos os novos recursos e melhorias.

Você ainda é livre para utilizar o gerador baseado em Couchbase se quiser, ele provavelmente ainda funciona bem, e você já tem um projeto gerado com ele que roda bem também (e você provavelmente já atualizou ele para encaixar nas suas necessidades).

Você pode ler mais sobre nas documentaçãoes do repositório.

## Full Stack FastAPI MongoDB

...pode demorar, dependendo do meu tempo disponível e outros fatores. 😅 🎉

## Modelos de Aprendizado de Máquina com spaCy e FastAPI

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### Modelos de Aprendizado de Máquina com spaCy e FastAPI - Recursos

* Integração com modelo NER **spaCy**.
* Formato de requisição **Busca Cognitiva Azure** acoplado.
* Servidor Python _web_ **Pronto para Produção** usando Uvicorn e Gunicorn.
* Implantação **Azure DevOps** Kubernetes (AKS) CI/CD acoplada.
* **Multilingual** facilmente escolhido como uma das linguagens spaCy acopladas durante a configuração do projeto.
* **Facilmente extensível** para outros modelos de _frameworks_ (Pytorch, Tensorflow), não apenas spaCy.
