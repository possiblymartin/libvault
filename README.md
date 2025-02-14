# libvault
libvault is a web application for fetching and summarizing online articles. It also allows users (once logged in) to save summarized articles for future reference. Think of it as a personal knowledge vault for quick reading and archiving.

## Features
- Article Sumarization: Enter an article URL, and the server will parse the page and return a _concise (in the works)_ summary alongside the full extracted text.

- User Authentication: Logged-in users can save their summarized articles to their vault.

- Unsaved Summaries. Guests can still fetch one summary, but they must log in to save more.

- Simple UI: A React-based interface that allows users to input a URL, and not much more.

## Installation
Below is one possible way to run the project locally.

1. Clonse the repo
```bash
git clone https://github.com/possiblymartin/libvault.git
cd libvault
```

2. Setting up the local server using flask
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or:
# .\venv\Scripts\activate  # On Windows
```

3. Running the local server
```bash
cd server
flask run --host=0.0.0.0 --port=5001
```

4. Setting up the client
Install Node
```bash
cd client
npm install
```

Start the development server
```bash
npm run dev
```
By default your app will run on `http://localhost:5173`

## Common issues
- **Weird characters (Â£) appear in text**\
_This is currently being addressed_

- **CORS errors**\
Make sure you have configured Cross-Origin Resource Sharing in your Python backend if you're connecting from a different port.

- **Missing `.env` files**\
If you store environment varialbes (e.g., DB credentials, secret keys) in `.env` files, ensure they're not committed to version control.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues or submit pull request.