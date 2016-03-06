{% extends "b64.tpl" %}
{% block shellcode %}${{obfs.set('shellcode')}}='{{obfs.add_comment(obfs.shellcode,'php')|base64}}';{% endblock %}
