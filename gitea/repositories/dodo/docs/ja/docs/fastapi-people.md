# FastAPI People

FastAPIには、様々なバックグラウンドの人々を歓迎する素晴らしいコミュニティがあります。

## Creator - Maintainer

こんにちは！ 👋

これが私です:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>

{% endif %}

私は **FastAPI** の作成者および Maintainer です。詳しくは [FastAPIを応援 - ヘルプの入手 - 開発者とつながる](help-fastapi.md#開発者とつながる){.internal-link target=_blank} に記載しています。

...ところで、ここではコミュニティを紹介したいと思います。

---

**FastAPI** は、コミュニティから多くのサポートを受けています。そこで、彼らの貢献にスポットライトを当てたいと思います。

紹介するのは次のような人々です:

* [GitHub issuesで他の人を助ける](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}。
* [プルリクエストをする](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}。
* プルリクエストのレビューをする ([特に翻訳に重要](contributing.md#translations){.internal-link target=_blank})。

彼らに大きな拍手を。👏 🙇

## 先月最もアクティブだったユーザー

彼らは、先月の[GitHub issuesで最も多くの人を助けた](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}ユーザーです。☕

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Experts

**FastAPI experts** を紹介します。🤓

彼らは、*これまでに* [GitHub issuesで最も多くの人を助けた](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}ユーザーです。

多くの人を助けることでexpertsであると示されています。✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Top Contributors

**Top Contributors** を紹介します。👷

彼らは、*マージされた* [最も多くのプルリクエストを作成した](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}ユーザーです。

ソースコード、ドキュメント、翻訳などに貢献してくれました。📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

他にもたくさん (100人以上) の contributors がいます。<a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub Contributors ページ</a>ですべての contributors を確認できます。👷

## Top Reviewers

以下のユーザーは **Top Reviewers** です。🕵️

### 翻訳のレビュー

私は少しの言語しか話せません (もしくはあまり上手ではありません😅)。したがって、reviewers は、ドキュメントの[**翻訳を承認する権限**](contributing.md#translations){.internal-link target=_blank}を持っています。それらがなければ、いくつかの言語のドキュメントはなかったでしょう。

---

**Top Reviewers** 🕵️は、他の人からのプルリクエストのほとんどをレビューし、コード、ドキュメント、特に**翻訳**の品質を保証しています。

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## Sponsors

**Sponsors** を紹介します。😎

彼らは、<a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a> を介して私の **FastAPI** などに関する活動を支援してくれています。

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

## データについて - 技術詳細

このページの目的は、他の人を助けるためのコミュニティの努力にスポットライトを当てるためです。

特に、他の人の issues を支援したり、翻訳のプルリクエストを確認したりするなど、通常は目立たず、多くの場合、より困難な作業を含みます。

データは毎月集計されます。<a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">ソースコードはこちら</a>で確認できます。

ここでは、スポンサーの貢献も強調しています。

アルゴリズム、セクション、閾値などは更新されるかもしれません (念のために 🤷)。
