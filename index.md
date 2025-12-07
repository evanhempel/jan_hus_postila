---
layout: default
title: Jan Hus Sermons
---

# Jan Hus Sermons

{% comment %}
  Group all sermon pages by their sermon_id and show one entry per sermon
{% endcomment %}

{% assign sermons_with_pages = site.pages | where_exp: "p", "p.sermon_id" | sort: "sermon_id" %}

{% for page in sermons_with_pages %}
  {% assign sermon_id = page.sermon_id %}

  {% comment %} Only show the sermon once (skip duplicates) {% endcomment %}
  {% unless shown_sermons contains sermon_id %}
    {% assign shown_sermons = shown_sermons | push: sermon_id %}

    {% assign all_versions = site.pages | where: "sermon_id", sermon_id | sort: "version_name" %}
    {% assign first_version = all_versions.first %}

    <h3>
      <a href="{{ first_version.url | relative_url }}">
        {{ first_version.title | split: " – " | first | default: "Sermon " + sermon_id }}
      </a>
    </h3>

    <p><strong>Available versions:</strong></p>
    <ul>
      {% for v in all_versions %}
        <li>
          <a href="{{ v.url | relative_url }}">{{ v.version_name }}</a>
        </li>
      {% endfor %}
    </ul>

  {% endunless %}
{% endfor %}
