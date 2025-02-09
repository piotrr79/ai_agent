## Python email template agent to generate templates with AI from inputs

### ChatGPT sample call:
```
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: org-IeylwHKkgHRCyjerI4KgM32A" \
  -H "OpenAI-Project: $PROJECT_ID"
```

### OpenAI library docs:
https://platform.openai.com/docs/api-reference/debugging-requests

### OpenAI creds:
https://platform.openai.com/settings/organization/general

### Run by:
```python3 email_generator.py```
```python3 connector.py```

### Run Django:
From ai_agent_email_template directory run: ```python3 manage.py runserver```

### Database:
```python3 manage.py makemigrations template_agent```
```python3 manage.py migrate```

### Superuser:
```python3 manage.py createsuperuser```