# Pessoas do FastAPI

FastAPI possue uma comunidade incrível que recebe pessoas de todos os níveis.

## Criador - Mantenedor

Ei! 👋

Este sou eu:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Respostas: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

Eu sou o criador e mantenedor do **FastAPI**. Você pode ler mais sobre isso em [Help FastAPI - Get Help - Connect with the author](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...Mas aqui eu quero mostrar a você a comunidade.

---

**FastAPI** recebe muito suporte da comunidade. E quero destacar suas contribuições.

Estas são as pessoas que:

* [Help others with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Create Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Revisar Pull Requests, [especially important for translations](contributing.md#translations){.internal-link target=_blank}.

Uma salva de palmas para eles. 👏 🙇

## Usuários mais ativos do ultimo mês

Estes são os usuários que estão [helping others the most with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} durante o ultimo mês. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Especialistas

Aqui está os **Especialistas do FastAPI**. 🤓


Estes são os usuários que [helped others the most with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} em *todo o tempo*.

Eles provaram ser especialistas ajudando muitos outros. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues respondidas: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top Contribuidores

Aqui está os **Top Contribuidores**. 👷

Esses usuários têm [created the most Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} que tem sido *mergeado*.

Eles contribuíram com o código-fonte, documentação, traduções, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

Existem muitos outros contribuidores (mais de uma centena), você pode ver todos eles em <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">Página de Contribuidores do FastAPI no GitHub</a>. 👷

## Top Revisores

Esses usuários são os **Top Revisores**. 🕵️

### Revisões para Traduções

Eu só falo algumas línguas (e não muito bem 😅). Então, os revisores são aqueles que têm o [**poder de aprovar traduções**](contributing.md#translations){.internal-link target=_blank} da documentação. Sem eles, não haveria documentação em vários outros idiomas.

---

Os **Top Revisores** 🕵️ revisaram a maior parte de Pull Requests de outros, garantindo a qualidade do código, documentação, e especialmente, as **traduções**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Revisões: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Patrocinadores

Esses são os **Patrocinadores**. 😎

Eles estão apoiando meu trabalho **FastAPI** (e outros), principalmente através de <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}
{% if sponsors.gold %}

### Patrocinadores Ouro

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Patrocinadores Prata

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Patrocinadores Bronze

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

### Patrocinadores Individuais

{% if github_sponsors %}
{% for group in github_sponsors.sponsors %}

<div class="user-list user-list-center">

{% for user in group %}
{% if user.login not in sponsors_badge.logins %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a></div>

{% endif %}
{% endfor %}

</div>

{% endfor %}
{% endif %}

{% endif %}

## Sobre os dados - detalhes técnicos

A principal intenção desta página é destacar o esforço da comunidade para ajudar os outros.

Especialmente incluindo esforços que normalmente são menos visíveis, e em muitos casos mais árduo, como ajudar os outros com issues e revisando Pull Requests com traduções.

Os dados são calculados todo mês, você pode ler o <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">código fonte aqui</a>.

Aqui também estou destacando contribuições de patrocinadores.

Eu também me reservo o direito de atualizar o algoritmo, seções, limites, etc (só para prevenir 🤷).
