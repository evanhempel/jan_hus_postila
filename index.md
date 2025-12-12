---
layout: default
title: Jan Hus Sermons
---

# Jan Hus Sermons
<style>
.sermons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.sermon-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sermon-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.sermon-title {
  margin: 0;
  font-size: 1.2rem;
  line-height: 1.3;
}

.sermon-title a {
  color: #1a0dab;
  text-decoration: none;
}

.sermon-title a:hover {
  text-decoration: underline;
}

.versions strong {
  font-size: 0.9rem;
  color: #444;
}

.versions ul {
  margin: 0.4rem 0 0 0;
  padding-left: 1.2rem;
  list-style: none;
}

.versions li {
  margin-bottom: 0.35rem;
  font-size: 0.95rem;
}

.versions li::before {
  content: "▸ ";
  color: #666;
}
</style>

<div class="sermons-grid">
{% comment %}
  Group all sermon pages by their sermon_id and show one entry per sermon
{% endcomment %}

{% assign shown_sermons = "" | split: "" %}

{% assign sorted_pages = site.pages | where_exp: "p", "p.sermon_id != nil" | sort: "sermon_id" %}

{% for page in sorted_pages %}
{% assign sermon_id = page.sermon_id %}

{% comment %} Only show each sermon once {% endcomment %}
{% unless shown_sermons contains sermon_id %}
{% assign shown_sermons = shown_sermons | push: sermon_id %}

{% assign all_versions = site.pages | where: "sermon_id", sermon_id | sort: "version_name" %}
{% assign first_version = all_versions.first %}

<article class="sermon-card">
<h3 class="sermon-title">
<a href="{{ first_version.url | relative_url }}">
{% assign fallback_title = "Sermon " | append: sermon_id %}
{{ first_version.title | split: " – " | first | default: fallback_title }}
</a>
</h3>

<div class="versions">
<ul>
{% for v in all_versions %}
<li>
  <a href="{{ v.url | relative_url }}">{{ v.version_name }}</a>
</li>
{% endfor %}
</ul>
</div>
</article>

{% endunless %}
{% endfor %}
</div>
