# Feedback

This is an example application for:

- Learning basics of how modern web applications are built with HTML, CSS, JavaScript, servers, and databases.
- Deploying something a little more advanced than a _Hello world!_ page or unconfigured nginx server.
- Deploying a minimal production like application.

## Getting started

To run the application on your machine, you will need [Docker Compose](https://docs.docker.com/compose/). You can either install it manually or by using Docker Desktop (see also [Installing Docker](https://cicd-tutorials.net/#installing-docker)).

To start the application, run `docker compose up -d`. This will build the container images and start the containers in the background. The application should be soon available in [http://localhost:8080](http://localhost:8080). The API container will create two demo forms, which are available in [/thumbs](http://localhost:8080/thumbs) and [/weather](http://localhost:8080/weather) paths.

```sh
docker compose up -d
```

If you want to inspect the admin panel, print out the content of `/var/feedback/initial_admin_password` in the `api` container with `docker compose exec` for the initial admin account password. Admin panel is available in [http://localhost:8080/admin](http://localhost:8080/admin) and the username for the admin account is `admin`.

```sh
docker compose exec api cat /var/feedback/initial_admin_password
```

For a more production like deployment, there is an OpenTofu/Terraform configuration example in [iac/tf](./iac/tf/) directory.

<!-- TODO: configuration -->

## Three-tier architecture

The application is built using a three-tier architecture. I.e., the application consists of presentation tier, application tier and a data tier.

```mermaid
flowchart LR
  subgraph d [Data tier]
    db["Database<br>_(Postgres)_"]
  end
  subgraph a ["Application tier<br>_(Gunicorn server)_"]
    a_whitespace:::hidden
    admin[Admin interface]
    API["API<br>_(Django application)_"]
    static_build[Static files]
  end
  subgraph p ["Presentation tier<br>_(Nginx server)_"]
    p_whitespace:::hidden
    root["/ _(Svelte application)_"]
    api_proxy["/api"]
    admin_proxy["/admin"]
    static["/static"]
  end

  Browser--Static web page-->root
  Browser--Dynamic web page-->admin_proxy
  Browser-.->api_proxy
  Browser-.->static

  admin_proxy--proxy_pass-->admin
  api_proxy--proxy_pass-->API
  static -.docker build.- static_build

  admin-->db
  API-->db

  classDef hidden display: none;
```

<!-- TODO: paragraph or two on how these are executed with docker compose -->

### Presentation tier

<!-- TODO: Intro to presentation tier -->

The end-user facing user interface (UI) of the application is implemented as Svelte application in [front-end](./front-end) directory. [Svelte](https://svelte.dev/) is a JavaScript user-interface (UI) framework used to build the HTML, JavaScript, and CSS files that the browser renders and runs on the users machine.

The HTML, JavaScript, and CSS files that implement the user UI are delivered to the end-users browser by an static file server. This application uses [nginx](https://nginx.org/) which, in addition to hosting the static files, acts as a reverse proxy towards the application layer: when the user interacts with the application, the browser contacts the presentation tier which then proxies the requests to application tier. <!-- TODO: add note on preventing direct access to the application server -->

The presentation tier of an web application can be implemented either as a static or a dynamic web page. This application provides example for both of these: the end-user facing application is a static web page and the admin panel is a dynamic web page.

#### Static web pages

The word static in static web page means that the files served to the browser are always the same regardless of the user or status of the server. This does not mean that the web page could not be interactive. Many static web pages include JavaScript logic that can change the content of the page from within the web browser by utilizing, for example, calls to a API of a web application.

To summarize, the initial page load will be the same for all users, but the page might use client side logic and API calls to add interaction and to personalize the content visible to the user.

<!-- TODO: paragraph about the Svelte app and e.g. client side routing -->

#### Dynamic web pages

Dynamic web pages, on the other hand, are created dynamically by the web server varying on, for example, the user making requesting the page or the status of the server. Thus, the content returned to the browser when loading the page will already be personalized on the server side.

<!-- TODO: paragraph about the Django admin panel -->

Dynamic web pages often also utilize static content, such as stylesheets and images, to make the page load more efficient. The static content is usually served to the end-user by a static file server instead of the application server. In this application, the static filed required by the admin panel are copied to the nginx server during the Docker build process and served to the end-user from under `/static` path of the server.

### Application tier

<!-- TODO: Intro to application tier -->

The application tier of the application is implemented with Django in [back-end](./back-end) directory. [Django](https://www.djangoproject.com/) is a Python web framework that could be used to implement both presentation and the application tiers as well as managing the data tier. In this project it implements the application programming interface (API), handles interaction with the database, and provides an administrator panel for managing the data stored in the database.

The Django application is exposed using a [Gunicorn](https://gunicorn.org/) server that handles incoming connections using multiple worker threads. I.e., Gunicorn implements a production ready webserver where as the Django application is responsible for implementing the application logic behind the server. Gunicorn server communicates with the Django application using WSGI, a standardized interface for connecting web servers to applications.

<!-- TODO: more detailed description of the DB connection -->

### Data tier

<!-- TODO: Intro to data tier -->

The data tier of the application is provided by Postgres SQL database. The application interacts with the database using Object-Relational Mapping (ORM) of the Django web framework.

The database is only exposed to the private network that connects the application containers to each other. This prevents external access to the database.

<!-- TODO: move relevant parts from here to sections above and/or to README.md files in back-end and front-end directories.

This section describes step-by-step how this application was created. To be able to follow these step-by-step instructions, you will need:

- Web browser, e.g. Firefox or Chrome
- Recent version of `python` and `pip` installed
- Recent version of `docker` and `docker-compose` installed

### 1. HTML page

We will start creating the application from the HTML (Hypertext Markup Language) file that defines the elements in our front-end. Create a directory called `front-end` and file called `index.html` in that directory, for example, by using `mkdir` and `touch` commands.

```sh
mkdir front-end
touch front-end/index.html
```

Then, add following content to the `front-end/index.html` file:

```html
<html lang="en">
  <head>
    <title>Feedback?</title>
    <meta charset="UTF-8" />
  </head>
  <body>
    <main>
      <h1>How was your experience with us?</h1>
      <div>
        <button type="button">👍</button>
        <button type="button">👎</button>
      </div>
    </main>
  </body>
</html>
```

You can open this file with your web browser. It will be rendered with default styling and the buttons will not do anything yet, though.

### 2. CSS styles

Next, we will add styling to our front-end with CSS (Cascading Style Sheets). Create `styles.css` file in the front-end directory.

```sh
touch front-end/styles.css
```

Then, add following content to the `front-end/styles.css` file:

```css
/* Import the font we will be using */
@import url("https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400&display=swap");

/* Define CSS variables */
:root {
  --black: rgb(34, 34, 38);
  --white: rgb(221, 221, 221);
  --white-25: rgba(221, 221, 221, 0.25);
}

body {
  /* Remove default margins added by the browser */
  margin: 0 0;

  /* Set background color, and global styles */
  background: var(--black);
  color: var(--white);
  font-family: "Source Sans Pro", sans-serif;

  /* Use flexbox to allow main element to grow according to screen size */
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  /* Take all available vertical space */
  flex-grow: 1;

  /* Center elements horizontally and vertically */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  /* Add margins on smaller screens */
  max-width: 95%;
  margin: 1rem auto;
}

/* Center text in the header */
header {
  text-align: center;
}

/* Override default h1 styling */
h1 {
  font-size: 1.5em;
  font-weight: 300;
  margin: 1em 0;
}

p {
  /* Use black text on white background and override default p styling */
  background: var(--white);
  color: var(--black);
  font-size: 3rem;
  font-weight: normal;
  line-height: 1.25em;
  margin: 3rem 0;
  padding: 0 0.25em;
}

button {
  /* Override default button styles */
  background: transparent;
  border: none;

  /* Add custom styles */
  border-radius: 50%;
  cursor: pointer;
  font-size: 4rem;

  /* Configure spacing */
  margin: 1rem;
  padding: 2rem;

  /* Add transition animations */
  transition: all 250ms ease-in-out;
}

/* Add semi transparent background and rotate emoji slightly when mouse hovers on the elements or user navigates to the element with their keyboard */
button:hover,
button:focus-visible {
  background: var(--white-25);
  outline: none;
  transform: rotate(15deg);
}
```

If you now reload `index.html` in your browser, the appearance of the page will not change. This is because the created stylesheet is not referenced in the HTML. To tell the browser to load the stylesheet, add `<link>` element to the `index.html` file according to the diff output below.

```diff
diff --git a/front-end/index.html b/front-end/index.html
index bb511f9..a5a9409 100644
--- a/front-end/index.html
+++ b/front-end/index.html
@@ -1,6 +1,7 @@
 <html lang="en">
   <head>
     <title>Feedback</title>
+    <link rel="stylesheet" href="./styles.css" />
   </head>
   <body>
     <header>
```

Try now to reload the page. The page should look different now.

### 3. Server

Next we will create a server to handle the incoming feedback.

Create a new `back-end` directory. Then, in the just created directory, create requirements.txt and server.py files.

```sh
mkdir back-end
touch back-end/requirements.txt
touch back-end/server.py
```

The `requirements.txt` file defines libraries we will need in order to be able to run the server. Add following content to that file:

```txt
gunicorn
flask
```

The `server.py` file implements our initial server. Add following content to that file:

```py
from flask import Flask, request

app = Flask(__name__)

data = dict(positive=0, negative=0)


def get_feedback():
    return data


def post_feedback(input):
    if input["type"] == "positive":
        data['positive'] += 1
    if input["type"] == "negative":
        data['negative'] += 1


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        post_feedback(request.json)
        return '', 204
    return get_feedback(), 200
```

Note that data is now stored to a local varible in the `server` module. Thus data is resetted on every restart.

To run the server in development mode, first install dependencies with `pip3 install` and then use `flask run` command:

```sh
pip3 install -r requirements.txt
flask -A "server:app" run
```

While the server is running, you can test it with, for example, curl.

```sh
# Get current feedback overview
curl localhost:5000/feedback

# Post new feedback
curl -X POST -d '{"type":"positive"}' -H "Content-Type: application/json" localhost:5000/feedback
```

### 4. In memory database

Next, we will add database connection to our server. For that we will need two additional dependencies: `Flask-SQLAlchemy` and `SQLAlchemy`. Add these to the `back-end/requirements.py` according to the diff output below.

```diff
diff --git a/back-end/requirements.txt b/back-end/requirements.txt
index cef5a16..9933987 100644
--- a/back-end/requirements.txt
+++ b/back-end/requirements.txt
@@ -1,2 +1,4 @@
 Flask
+Flask-SQLAlchemy>=3.0.0
 gunicorn
+SQLAlchemy>=2.0.0b1
```

Install the dependencies new dependencies with `pip3 install` command.

```sh
pip3 install -r requirements.txt
```

We will then configure our server to use SQLite in memory database. Modify `back-end/requirements.py` file according to the diff below.

```diff
diff --git a/back-end/server.py b/back-end/server.py
index cbb4b3b..47b2df3 100644
--- a/back-end/server.py
+++ b/back-end/server.py
@@ -1,24 +1,86 @@
-from flask import Flask, request
+from dataclasses import dataclass
+from datetime import datetime
+from os import getenv
+from time import sleep
+from uuid import uuid4
+
+from flask import Flask, jsonify, request
+from flask_sqlalchemy import SQLAlchemy
+from sqlalchemy import func

 app = Flask(__name__)
+app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_URL', 'sqlite:///:memory:')
+app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
+db = SQLAlchemy(app)
+
+
+@dataclass
+class FeedbackItem(db.Model):
+    id: str
+    type: str
+    timestamp: datetime
+
+    id = db.Column(db.String(36), primary_key=True)
+    type = db.Column(db.String(8))
+    timestamp = db.Column(db.DateTime())

-data = dict(positive=0, negative=0)
+    @property
+    def json(self):
+        return dict(
+            id=self.id,
+            type=self.type,
+            timestamp=f'{self.timestamp.isoformat()}Z')
+
+
+# Create table if it does not exist
+for _ in range(5):
+    try:
+        with app.app_context():
+            db.create_all()
+    except BaseException:
+        sleep(2)


 def get_feedback():
-    return data
+    rows = db.session.execute(db.select(FeedbackItem)).all()
+    return jsonify([row.FeedbackItem.json for row in rows])


 def post_feedback(input):
-    if input["type"] == "positive":
-        data['positive'] += 1
-    if input["type"] == "negative":
-        data['negative'] += 1
+    id_ = str(uuid4())
+
+    db.session.add(FeedbackItem(
+        id=id_,
+        type=input["type"],
+        timestamp=datetime.utcnow()
+    ))
+    db.session.commit()
+
+    return dict(id=id_)
+
+
+def get_feedback_summary():
+    rows = db.session.execute(
+        db.select(
+            func.count(
+                FeedbackItem.id),
+            FeedbackItem.type).group_by(
+            FeedbackItem.type)).all()
+
+    data = dict(positive=0, negative=0)
+    for count, type_ in rows:
+        data[type_] = count
+
+    return jsonify(data)


 @app.route("/feedback", methods=['GET', 'POST'])
 def feedback():
     if request.method == "POST":
-        post_feedback(request.json)
-        return '', 204
+        return post_feedback(request.json), 200
     return get_feedback(), 200
+
+
+@app.route("/feedback/summary", methods=['GET'])
+def feedback_summary():
+    return get_feedback_summary(), 200
```

You can use same curl commands as in the [previous step](#3-server) to test the server.

Note that the `GET /feedback` output is now different. This end-point now lists all feedback items with ids and timestamps. For the summary, we introduced a new end-point `GET /feedback/summary`.

```sh
# Get all feedback items
curl localhost:5000/feedback

# Get current feedback overview
curl localhost:5000/feedback/summary
```

### 5. Containerized development setup

Next, we will create container images for our front-end and back-end components, add database running in container, and run these three containers with `docker-compose`.

To do this, we will need to create Dockerfiles for our own containers and docker-compose configuration to define how to run these containers.

```sh
touch front-end/Dockerfile
touch back-end/Dockerfile
touch docker-compose.yml
```

First, we will we add the following content to the Dockerfile in front-end directory.

```Dockerfile
FROM nginx:alpine

COPY index.html styles.css /usr/share/nginx/html/
```

Second, we will add the following content to the Dockerfile in back-end directory.

```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt && pip install psycopg2-binary

COPY server.py /app/
ENTRYPOINT ["gunicorn", "server:app"]
CMD ["-w", "4", "-b", "0.0.0.0:8000"]
```

Finally, we will add the following content to the docker-compose.yaml file.

```yaml
version: "3.4"
services:
  api:
    environment:
      DB_URL: postgresql://user:pass@db:5432/feedback
    build: ./back-end/
    command: -w 4 -b 0.0.0.0:8000
    ports:
      - 5000:8000
  ui:
    build: ./front-end/
    ports:
      - 9080:80
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: feedback
```

To run this docker-compose configuration, use `docker-compose up` command.

```sh
docker-compose up
```

You can use same `curl` commands as in steps [4](#4-in-memory-database) and [5](#5-containerized-development-setup) to test the server and database connection. Try to also terminate the containers (E.g., with `CTRL-C` or `docker-compose down` command) and launch them again. The data should now persist after restarting the server.

### 6. Connecting front-end to the back-end

Finally, we will configure or front-end to send feedback to server when buttons are clicked and show feedback summary after that.

For the browser to communicate with another server than to one serving the static content, we will need to configure our server to include [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) headers into its responses. To do this, we will install and use `flask-cors`.

Edit `back-end/requirements.txt` according to diff below.

```diff
diff --git a/back-end/requirements.txt b/back-end/requirements.txt
index 9933987..d872cfc 100644
--- a/back-end/requirements.txt
+++ b/back-end/requirements.txt
@@ -1,4 +1,5 @@
 Flask
+flask-cors
 Flask-SQLAlchemy>=3.0.0
 gunicorn
 SQLAlchemy>=2.0.0b1
```

If you are running the server without containers, remember to run `pip3 install` again.

```sh
pip3 install -r requirements.txt
```

Edit `back-end/server.py` according to diff below.

```diff
diff --git a/back-end/server.py b/back-end/server.py
index 47b2df3..1124e94 100644
--- a/back-end/server.py
+++ b/back-end/server.py
@@ -5,10 +5,12 @@ from time import sleep
 from uuid import uuid4

 from flask import Flask, jsonify, request
+from flask_cors import CORS
 from flask_sqlalchemy import SQLAlchemy
 from sqlalchemy import func

 app = Flask(__name__)
+CORS(app)
 app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_URL', 'sqlite:///:memory:')
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 db = SQLAlchemy(app)
```

On the front-end side we will need to new files, `script.js` and `config.js`. `script.js` includes function we will execute when user clicks one of the buttons available on the page. `config.js` can be used to define server URL when running this application in production.

Create these files with `touch`.

```sh
touch front-end/script.js
touch front-end/config.js
```

Add following content to `script.js`.

```js
"use strict";

function baseUrl() {
  try {
    return serverUrl;
  } catch (_) {
    return "http://localhost:5000";
  }
}

async function sendFeedback(type) {
  // Post feedback
  // We will ignore possible fetch errors and non-ok HTTP status codes here and later
  await fetch(`${baseUrl()}/feedback`, {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type }),
  });

  // Get feedback summary
  const res = await fetch(`${baseUrl()}/feedback/summary`, {
    mode: "cors",
  });

  if (!res.ok) {
    return;
  }

  // Hide buttons and display results summary
  document.getElementById("buttons-container").classList.add("hidden");
  document.getElementById("results-container").classList.remove("hidden");

  // Set bar chart bar width and count
  const results = await res.json();
  const total = results.positive + results.negative;
  ["positive", "negative"].forEach((type) => {
    const value = results[type];
    const barEl = document.getElementById(`results-bar-${type}`);
    const countEl = document.getElementById(`results-count-${type}`);

    barEl.style = `width: ${(value / total) * 100}%`;
    countEl.textContent = value;
  });
}
```

Add following content to `config.js`.

```js
// To define the server URL, set serverUrl variable here, e.g.:
// const serverUrl = "https://example.com";
```

We will also need to load these files and add markup for displaying the feedback summary to our HTML content. Edit `front-end/index.html` according to the diff below.

```diff
diff --git a/front-end/index.html b/front-end/index.html
index 72b1100..df14048 100644
--- a/front-end/index.html
+++ b/front-end/index.html
@@ -3,16 +3,30 @@
     <title>Feedback</title>
     <meta charset="UTF-8" />
     <link rel="stylesheet" href="./styles.css" />
+    <script src="./config.js"></script>
   </head>
   <body>
+    <script src="./script.js"></script>
     <header>
       <h1>Feedback</h1>
     </header>
     <main>
       <p>How are you feeling?</p>
-      <div class="buttons">
-        <button type="button">👍</button>
-        <button type="button">👎</button>
+      <div id="buttons-container" class="buttons">
+        <button onclick="sendFeedback('positive')" type="button">👍</button>
+        <button onclick="sendFeedback('negative')" type="button">👎</button>
+      </div>
+      <div id="results-container" class="results hidden">
+        <div class="results-row">
+          <span>👍</span>
+          <div id="results-bar-positive" class="results-bar"></div>
+          <span id="results-count-positive">0</span>
+        </div>
+        <div class="results-row">
+          <span>👎</span>
+          <div id="results-bar-negative" class="results-bar"></div>
+          <span id="results-count-negative">0</span>
+        </div>
       </div>
     </main>
   </body>
```

To also include these two new files in our container image, edit `front-end/Dockerfile` according to the diff below.

```diff
diff --git a/front-end/Dockerfile b/front-end/Dockerfile
index 0bb4206..3588daf 100644
--- a/front-end/Dockerfile
+++ b/front-end/Dockerfile
@@ -1,3 +1,3 @@
 FROM nginx:alpine

-COPY index.html styles.css /usr/share/nginx/html/
+COPY index.html styles.css script.js config.js /usr/share/nginx/html/
```

We will also need to define styles for these new elements. Edit `front-end/styles.css` according to the diff below.

```diff
diff --git a/front-end/styles.css b/front-end/styles.css
index 9e966fc..8d1b0f9 100644
--- a/front-end/styles.css
+++ b/front-end/styles.css
@@ -86,3 +86,25 @@ button:focus-visible {
   outline: none;
   transform: rotate(15deg);
 }
+
+.results {
+  font-size: 2em;
+  width: 100%;
+}
+
+.results-row {
+  display: flex;
+  margin: 2rem 0;
+}
+
+.results-bar {
+  background: var(--white);
+  margin: 0 1rem;
+  padding: 0.25rem;
+  transition: width 250ms ease-in-out;
+  width: 0;
+}
+
+.hidden {
+  display: none;
+}
```

After creating and editing the files, we will need to build the container and restart them to see the effects. Shutdown the local development setup with `CTRL-C` or by running `docker-compose down`. Then, run `docker-compose build` and `docker-compose up`.

```sh
docker-compose build
docker-compose up
```

Open then `http://localhost:8081` with your browser. You should see the feedback page, be able to post feedback by clicking the buttons, and see the feedback summary after clicking either one of the buttons.
-->
