# Multi-Bot CLI Chatbot System

A versatile CLI chatbot system powered by **Google's Generative AI** and styled with **Rich**. This application provides a suite of AI agents directly in your terminal with a beautiful, interactive user interface.

## 🤖 Available Agents

- **Code Made Easy**: Debug code, generate snippets, and rate code quality.
- **Study Buddy**: A dedicated study assistant to help you learn new topics.
- **Lingua Link**: Practice languages and translate text.
- **Explain Like X**: Get explanations tailored to specific audiences (e.g., "Explain like I'm 5").
- **Time Travel**: Chat with simulated historical figures.
- **Future Simulator**: Explore hypothetical future scenarios.
- **Conversation Replay**: Review and analyze your past conversation history.

## 🚀 Installation

1. **Clone the repository** (if you haven't already).

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up API Key**:
   - Ensure you have a Google Gemini API key.
   - Configure it as per the application's configuration (likely in an `.env` file or environment variable `GOOGLE_API_KEY`).

## 🎮 Usage

Run the main application entry point:

```bash
python chat-bot.py
```

Use the interactive menu to select an agent and start chatting!

## 🛠️ Tech Stack

- **Python**: Core language.
- **Google Generative AI SDK**: For accessing Gemini models.
- **Rich**: For beautiful terminal formatting and UI.
