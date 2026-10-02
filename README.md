# MecQP

**MecQP** is an open-source question paper repository built for the students of **Government Model Engineering College (MEC), Thrikkakara**.

The goal of MecQP is to provide students with a centralized place to find and download previous-year question papers, while also allowing students to submit papers that are not yet available in the repository.

🌐 **Live website:** https://mecqp.com

---

## Features

* 🔎 Search question papers using multiple filters
* 📄 Download available question papers as PDFs
* 📤 Submit question papers for review
* 📋 Check the status of submitted papers
* 🛠️ Admin dashboard for managing papers and submissions
* 🔐 Admin authentication and CSRF protection
* 📢 Admin announcements/messages
* 📚 Rules and submission guidelines

---

## Search

Question papers can be searched using details such as:

* Scheme
* Branch
* Semester
* Exam type
* Month
* Year
* Subject code
* Subject

---

## Submission System

If a question paper is not available in the repository, students can submit a PDF through the website.

Submitted papers are manually reviewed by the administrator before being added to the public repository.

This ensures that papers are verified before they become publicly available.

---

## Tech Stack

* **Python**
* **Flask**
* **SQLite**
* **HTML**
* **CSS**
* **JavaScript**
* **Nginx**
* **Gunicorn**

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/AchindBabuCS/mecqp.git
cd mecqp
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file containing the environment variables required by the application.

**Do not commit `.env` or any other files containing secrets to the repository.**

### 5. Run the application

```bash
flask --app mecqp run
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## Project Structure

```text
mecqp/
├── mecqp.py
├── papers/
├── submissions/
├── static/
├── templates/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Deployment

The production deployment uses:

```text
Internet
    ↓
Nginx
    ↓
Gunicorn
    ↓
Flask
    ↓
SQLite
```

Persistent files such as the production database and uploaded question papers are stored separately from the application source.

---

## Third-Party Software

### Bulma

MecQP uses [Bulma](https://bulma.io/), a modern CSS framework based on Flexbox, for parts of its user interface.

Bulma is developed by **Jeremy Thomas** and is licensed under the **MIT License**.

The Bulma source code included in this repository retains its original copyright and license information.

For more information:

* [Bulma Website](https://bulma.io/)
* [Bulma GitHub Repository](https://github.com/jgthms/bulma)

---

## Contributing

MecQP is open source and contributions are welcome.

If you find a bug, have a suggestion, or would like to contribute:

1. Open an issue describing the problem or suggestion.
2. Fork the repository.
3. Make your changes.
4. Submit a pull request.

Please keep contributions focused on improving MecQP for its intended users.

---

## Author

**Achind Babu**

B.Tech Computer Science and Business Systems
Government Model Engineering College, Thrikkakara

GitHub: [@AchindBabuCS](https://github.com/AchindBabuCS)

---

## License

MecQP is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

Copyright © 2026 Achind Babu.

MecQP also includes third-party software, including **Bulma**, which is distributed under its respective license and copyright notice.
