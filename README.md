
# Noah's Portfolio Q&A: AI-Powered Professional Background Chatbot

This is an end-to-end LLM project based on OpenAI GPT-4 and Langchain. It's a Q&A system for Noah's professional portfolio that provides instant answers about his background, skills, experience, and qualifications. Built with modern AI technologies and a professional web interface to showcase technical abilities while providing comprehensive information about Noah's professional journey.

## Project Highlights

- **Professional Web Interface**: Modern, responsive design with Noah's headshot and professional branding
- Uses Noah's professional portfolio data in CSV format containing career highlights and experience  
- AI-powered chatbot that can answer questions about Noah's background instantly
- Built with OpenAI GPT-4 for high-quality, contextual responses
- Vector database for semantic search through professional experience
- Flask web application with real-time chat functionality

## Features
- **Professional Portfolio Website**: Showcases Noah's photo, background, and key qualifications
- **Real-time AI Chat**: Interactive chatbot with suggested questions and professional responses
- **Semantic Search**: Finds relevant information even with varied question phrasing  
- **Instant Responses**: Get comprehensive answers about Noah's background in seconds
- **Modern Tech Stack**: Showcases proficiency with cutting-edge AI and web technologies
- **Responsive Design**: Works perfectly on desktop and mobile devices

## Technologies Used
- **Flask**: Modern Python web framework
- **LangChain + OpenAI GPT-4**: LLM-based Q&A system
- **HTML5/CSS3/JavaScript**: Frontend user interface
- **OpenAI Embeddings**: Text embeddings for semantic search
- **FAISS**: Vector database for efficient similarity search
- **Python**: Backend development

## Installation

1. Clone this repository to your local machine using:

```bash
git clone https://github.com/iNoahCodeGuy/Chatbot_With_RAG.git
```

2. Navigate to the project directory:

```bash
cd Chatbot_With_RAG
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

4. Acquire an OpenAI API key and put it in .env file:

```bash
OPENAI_API_KEY="your_openai_api_key_here"
```

## Usage

1. Run the Flask web application by executing:

```bash
python app.py
```

2. Open your web browser and navigate to: `http://localhost:5000`

3. You'll see Noah's professional portfolio website with:
   - Professional headshot and background information
   - Interactive AI chatbot interface
   - Suggested questions to get started

4. To create the knowledge base from Noah's portfolio data, click on "Initialize Knowledge Base" button. It will take some time to process the data so please wait.

5. Once the knowledge base is created, you will see a directory called `faiss_index` in your current folder.

6. Now you are ready to ask questions about Noah's professional background. Type your question and hit Enter or click the send button.

## Sample Questions

- What is Noah's professional background?
- Tell me about Noah's sales experience
- What education does Noah have?
- What certifications does Noah hold?
- What skills does Noah possess?
- Can you describe Noah's B2B sales experience?
- How would you describe Noah as a candidate for a sales position?

## Project Structure

- `app.py` - Flask web application and API endpoints
- `templates/index.html` - Professional portfolio website template
- `static/styles.css` - Modern responsive CSS styling
- `static/script.js` - Interactive JavaScript for chat functionality
- `static/noah-headshot.jpg` - Professional headshot image (add your photo here)
- `noah_portfolio.csv` - Contains Noah's professional information and background
- `langchain_helper.py` - Core Q&A functionality with OpenAI integration
- `config.py` - Configuration management
- `.env` - Environment variables (API keys)
- `requirements.txt` - Python dependencies

## Adding Your Headshot

To personalize the website with your professional headshot:

1. Add your professional photo to the `static/` directory
2. Name it `noah-headshot.jpg` (or update the HTML template to match your filename)
3. Recommended specifications:
   - Size: 400x400 pixels minimum
   - Format: JPG or PNG
   - Professional business attire
   - Clean background
   - High resolution for crisp display

If no image is provided, the website will display a professional placeholder with your initial.

## Project Structure

- main.py: The main Streamlit application script.
- langchain_helper.py: This has all the langchain code
- requirements.txt: A list of required Python packages for the project.
- .env: Configuration file for storing your Google API key.