### Python email template agent to generate templates with AI from user inputs

Application sends to OpenAI user prompt, gets response and generate personalized email template

For data privacy only prompt is send to ChatGPT, other details like contacts are stored locally

Application use Django framework and Django Admin panels to let users provides their inputs (just for simplyfing UI development)

Before running locally please generate OpenAI crednetials as specified in `Instructions` section below

### Manuals:

Log in to admin UI, select `Prompt Request` and click `Add Prompt Request`

![Main](MainPage.png)

When completed form list of prompt request select those which should be send to ChatGPT by checking checkboxes and selecting from the `Action` list `Generate templates for selected request` and clicking on button `Go`

![SendingPrompt](SendingPrompt.png)

ChatGPT responses will be saved to `Prompt Response`, generated email tmeplates in JSON format will be saved to `Templates`

![PromptResponse](PromptResponse.png)

![Template](Template.png)


### Instructions:

Install Python3

Generate OpenAI creds:
https://platform.openai.com/settings/organization/general

Clone and run `pip3 install -r requirements.txt` from project directory

Rename file `env.sample` to `.env` and provide credentials there, databse credentails section can be skipped if SqLite local db will be used

Generate database by running migrations:

```python3 manage.py makemigrations template_agent```

```python3 manage.py migrate```

Create superuser to access admin panel:

```python3 manage.py createsuperuser```

Finally run server:

```python3 manage.py runserver```


### Additional links:

For more info on Django please go to: `https://docs.djangoproject.com/en/5.1/`

ChatGPT sample call:
```
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: org-IeylwHKkgHRCyjerI4KgM32A" \
  -H "OpenAI-Project: $PROJECT_ID"
```

OpenAI library docs:

`https://platform.openai.com/docs/api-reference/debugging-requests`
