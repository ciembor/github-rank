<h1 id="{{ location_id }}">{{ location_name }}</h1>

<h2>Top Users</h2>
<table>
  <tr>
    <th></th>
    <th></th>
    <th>User</th>
    <th>Name</th>
    <th>Stars</th>
    <th></th>
  </tr>
  {% for u in top['users'] %}
  <tr>
    <th>{{ u.position }}</th>
    <td style="display: block; width: 36px; height: 36px; padding: 2px; border: 0; background: #fff url('http://gravatar.com/avatar/{{ u.gravatar_id }}?s=36') 2px 2px no-repeat"></td>
    <td>
    {% if u.name %}
      <strong>{{ u.name }}</strong>
    {% endif %}  
    </td>
    <td><a href="{{ u.html_url }}">{{ u.login }}</a></td>
    <td>{{ u.stars }}</td>
    <td>    
    {% if u.link %}
      <a href="{{ u.link }}">website</a>
    {% endif %}
    </td>
  </tr>
  {% endfor %}
</table>

<h2>Top Repositories</h2>
<table>
  <tr>
    <th></th>
    <th></th>
    <th>Name</th>
    <th>Owner</th>
    <th>Stars</th>
    <th>Language</th>
    <th></th>
  </tr>
  {% for r in top['repositories'] %}
  <tr>
    <th>{{ r.position }}</th>
    <td style="display: block; width: 36px; height: 36px; padding: 2px; border: 0; background: #fff url('http://gravatar.com/avatar/{{ r.owner.gravatar_id }}?s=36') 2px 2px no-repeat"></td>
    <td><a href="{{ r.html_url }}">{{ r.name }}</a></td>
    <td><a href="{{ r.owner.html_url }}">{{ r.owner.login }}</a></td>
    <td>{{ r.watchers }}</td>
    <td>
    {% if r.language %}
      {{ r.language }}
    {% endif %}
    </td>
    <td>
    {% if r.link %}
      <a href="{{ r.link }}">website</a>
    {% endif %}
    </td>
  </tr>
  {% endfor %}
</table>
