
# Kickstarter Project Success Prediction

What is Kickstarter? 💭

Kickstarter campaigns make ideas into reality. It’s where creators share new visions for creative work with the communities that will come together to fund them.
Check out more about [kickstarter](https://www.kickstarter.com/about)

Using the Streamlit application users can enter their project details. These project details will be used to classify if the users project is going to be successful or fail. Through which they can take necessary measures if their projects are at the verge of failing.


## Demo

https://github.com/MaruthiKo/kickstarter_projects/assets/63769209/ac0b9535-88aa-4271-aa8f-01930da4dc0c

## Run Locally

Clone the project

```bash
  git clone https://github.com/MaruthiKo/kickstarter_projects.git
```

Go to the project directory

```bash
  cd kickstarter_projects
```

Creating an Environment and activate !OPTIONAL

```bash
  python3 -m venv environment_name
  environment_name/Scripts/activate
```

Install dependencies 

```bash
  pip install -r requirements.txt
```

Start the Streamlit application

```bash
  streamlit run app.py
```

For running the server, move to the app folder

```bash
  cd app
```

Start the server

```bash
  uvicorn main:app --reload
```

## Features

- A great User Interface 🌟
- A backend server for serving model requests 🗄️
- Documentation for the API used in the project  ![octicons/wiki](https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/Wiki.svg)
- Dockerized Application for running locally 🐳
- Input Validation ✅

## Built with

- [Streamlit](https://docs.streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://docs.docker.com/get-started/)
- [PyDantic](https://docs.pydantic.dev/latest/)

## Contributing

Contributions🤝 are always welcome! Given below are few ways to contribute:
- Creating an Authentication for users to login / signup
- Integrating their kickstarter projects 
- Report bugs: If you encounter any bugs. Open up an issue
- Suggestions: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or imporvements you would like to see!
- Documentation: If you see the need for some additional documentation, feel free to add some!
