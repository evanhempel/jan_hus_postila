---
layout: default
title: Jan Hus Sermons
---

# Jan Hus Sermons

{% for sermon in site.data.sermons %}
{% assign any_version = site.pages | where:"sermon_id", sermon.id | first %}

{% if any_version %}
### [{{ sermon.title }}]({{ any_version.url }})

Available versions:
<ul>
{% assign versions = site.pages | where:"sermon_id", sermon.id | sort:"version_name" %}
{% for v in versions %}
  <li>{{ v.version_name }}</li>
{% endfor %}
</ul>

{% endif %}
{% endfor %}
