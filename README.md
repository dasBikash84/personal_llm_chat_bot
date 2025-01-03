# Gradio LLM Chatbot

This project is a simple web application that allows users to interact with different language models (LLMs) using the Gradio library. It supports models from OpenAI, Anthropic, and Google.

## Features

- Chat with various AI models, including OpenAI's GPT-3.5 and GPT-4, Anthropics's Claude, and Google Gemini.
- A user-friendly interface using Gradio.
- Streaming responses for an interactive experience.
- Environment configuration with API keys using a `.env` file.

## Prerequisites

- Docker installed on your machine.
- API keys from OpenAI, Anthropic, and Google (if you want to use their services).

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/dasBikash84/personal_llm_chat_bot.git
   cd personal_llm_chat_bot


2. **Create a `.env` file: Create a file named .env in the root of the project directory with the following contents:**:

   ```bash
    OPENAI_API_KEY=your_openai_key
    ANTHROPIC_API_KEY=your_anthropic_key
    GOOGLE_API_KEY=your_google_key


3. **Build and run the Docker container: Use the provided run.sh script to build and run the application**:

   ```bash
    chmod +x run.sh  # Make the script executable
    ./run.sh 7860  # You can specify the port, default is 7860

3. **Access the application: Open a web browser and go to http://localhost:7860 (or the specified port) to interact with the chatbot.**:

## Troubleshooting

If you encounter issues accessing the Gradio application, consider the following troubleshooting steps:

1. **Check if the Application is Running**:
   Use the command below to view the logs and check for any errors:
   ```bash
   docker logs <container_id>

2. **Confirm Port Mapping**:
  Ensure the command used to run the Docker container correctly maps the internal port (7860 by default):
   ```bash
   docker run --env-file .env -p $PORT:7860 personal_llm_chat_bot

3. **Firewall Rules**:
  If you are running Docker on a cloud server, make sure that firewall rules allow traffic on the specified port.

4. **Access the Container Shell**:
  If you want to debug further, you can access the shell of the running container:
   ```bash
   docker exec -it <container_id> /bin/bash    # Or /bin/sh if bash is not available
   # Inside the container, check if the service is running on the defined port using curl:
   curl http://localhost:7860


### Customization
- You can modify the models available in the model_choices list in app.py to include or exclude models based on your needs.
- The application's CSS can be customized by modifying the css variable in the app.py file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- [Gradio](https://gradio.app) - For building the interface.
- [OpenAI](https://openai.com) - Providing powerful language models.
- [Anthropic](https://www.anthropic.com) - For their Claude model.
- [Google](https://cloud.google.com/generative-ai) - For the Gemini model.

## Contact

For questions or comments, please contact me via GitHub or at your-email@example.com.