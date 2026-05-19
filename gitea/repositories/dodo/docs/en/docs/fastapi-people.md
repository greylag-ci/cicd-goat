# FastAPI People

FastAPI has an amazing community that welcomes people from all backgrounds.

## Creator - Maintainer

Hey! 👋

This is me:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

I'm the creator and maintainer of **FastAPI**. You can read more about that in [Help FastAPI - Get Help - Connect with the author](help-fastapi.md#connect-with-the-author){.internal-link target=_blank}.

...But here I want to show you the community.

---

**FastAPI** receives a lot of support from the community. And I want to highlight their contributions.

These are the people that:

* [Help others with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}.
* [Create Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}.
* Review Pull Requests, [especially important for translations](contributing.md#translations){.internal-link target=_blank}.

A round of applause to them. 👏 🙇

## Most active users last month

These are the users that have been [helping others the most with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} during the last month. ☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Experts

Here are the **FastAPI Experts**. 🤓

These are the users that have [helped others the most with issues (questions) in GitHub](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank} through *all time*.

They have proven to be experts by helping many others. ✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top Contributors

Here are the **Top Contributors**. 👷

These users have [created the most Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank} that have been *merged*.

They have contributed source code, documentation, translations, etc. 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

There are many other contributors (more than a hundred), you can see them all in the <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors page</a>. 👷

## Top Reviewers

These users are the **Top Reviewers**. 🕵️

### Reviews for Translations

I only speak a few languages (and not very well 😅). So, the reviewers are the ones that have the [**power to approve translations**](contributing.md#translations){.internal-link target=_blank} of the documentation. Without them, there wouldn't be documentation in several other languages.

---

The **Top Reviewers** 🕵️ have reviewed the most Pull Requests from others, ensuring the quality of the code, documentation, and especially, the **translations**.

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsors

These are the **Sponsors**. 😎

They are supporting my work with **FastAPI** (and others), mainly through <a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>.

{% if sponsors %}

{% if sponsors.gold %}

### Gold Sponsors

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Silver Sponsors

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### Bronze Sponsors

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% endif %}

### Individual Sponsors

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

## About the data - technical details

The main intention of this page is to highlight the effort of the community to help others.

Especially including efforts that are normally less visible, and in many cases more arduous, like helping others with issues and reviewing Pull Requests with translations.

The data is calculated each month, you can read the <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">source code here</a>.

Here I'm also highlighting contributions from sponsors.

I also reserve the right to update the algorithm, sections, thresholds, etc (just in case 🤷).
