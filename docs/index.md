---
layout: default
title: "Home"
permalink: /
---

# This is the index page of my website!

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>