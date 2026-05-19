# FastAPI 社区

FastAPI 有一个非常棒的社区，它欢迎来自各个领域和背景的朋友。

## 创建者 & 维护者

嘿! 👋

这就是我:

{% if people %}
<div class="user-list user-list-center">
{% for user in people.maintainers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Answers: {{ user.answers }}</div><div class="count">Pull Requests: {{ user.prs }}</div></div>
{% endfor %}

</div>
{% endif %}

我是 **FastAPI** 的创建者和维护者. 你能在 [帮助 FastAPI - 获取帮助 - 与作者联系](help-fastapi.md#connect-with-the-author){.internal-link target=_blank} 阅读有关此内容的更多信息。

...但是在这里我想向您展示社区。

---

**FastAPI** 得到了社区的大力支持。因此我想突出他们的贡献。

这些人：

* [帮助他人解决 GitHub 的 issues](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}。
* [创建 Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}。
* 审核 Pull Requests， 对于 [翻译](contributing.md#translations){.internal-link target=_blank} 尤为重要。

向他们致以掌声。 👏 🙇

## 上个月最活跃的用户

上个月这些用户致力于 [帮助他人解决 GitHub 的 issues](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}。

{% if people %}
<div class="user-list user-list-center">
{% for user in people.last_month_active %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## 专家组

以下是 **FastAPI 专家**。 🤓

这些用户一直以来致力于 [帮助他人解决 GitHub 的 issues](help-fastapi.md#help-others-with-issues-in-github){.internal-link target=_blank}。

他们通过帮助许多人而被证明是专家。✨

{% if people %}
<div class="user-list user-list-center">
{% for user in people.experts %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Issues replied: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## 杰出贡献者

以下是 **杰出的贡献者**。 👷

这些用户 [创建了最多已被合并的 Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}。

他们贡献了源代码，文档，翻译等。 📦

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_contributors %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Pull Requests: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

还有很多其他贡献者（超过100个），你可以在 <a href="https://github.com/tiangolo/fastapi/graphs/contributors" class="external-link" target="_blank">FastAPI GitHub 贡献者页面</a> 中看到他们。👷

## 杰出审核者

以下用户是「杰出的评审者」。 🕵️

### 翻译审核

我只会说少数几种语言（而且还不是很流利 😅）。所以，具备[能力去批准文档翻译](contributing.md#translations){.internal-link target=_blank} 是这些评审者们。如果没有它们，就不会有多语言文档。

---

**杰出的评审者** 🕵️ 评审了最多来自他人的 Pull Requests，他们保证了代码、文档尤其是 **翻译** 的质量。

{% if people %}
<div class="user-list user-list-center">
{% for user in people.top_reviewers %}

<div class="user"><a href="{{ user.url }}" target="_blank"><div class="avatar-wrapper"><img src="{{ user.avatarUrl }}"/></div><div class="title">@{{ user.login }}</div></a> <div class="count">Reviews: {{ user.count }}</div></div>
{% endfor %}

</div>
{% endif %}

## 赞助商

以下是 **赞助商** 。😎

他们主要通过<a href="https://github.com/sponsors/tiangolo" class="external-link" target="_blank">GitHub Sponsors</a>支持我在 **FastAPI** (和其他项目)的工作。

{% if sponsors.gold %}

### 金牌赞助商

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.silver %}

### 银牌赞助商

{% for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

{% if sponsors.bronze %}

### 铜牌赞助商

{% for sponsor in sponsors.bronze -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

### 个人赞助

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

## 关于数据 - 技术细节

该页面的目的是突出社区为帮助他人而付出的努力。

尤其是那些不引人注目且涉及更困难的任务，例如帮助他人解决问题或者评审翻译 Pull Requests。

该数据每月计算一次，您可以阅读 <a href="https://github.com/tiangolo/fastapi/blob/master/.github/actions/people/app/main.py" class="external-link" target="_blank">源代码</a>。

这里也强调了赞助商的贡献。

我也保留更新算法，栏目，统计阈值等的权利（以防万一🤷）。
