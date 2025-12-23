FROM python:3.11
WORKDIR /app

# Jupyter
RUN pip install jupyter ipykernel

# LLM фреймворки
RUN pip install transformers accelerate torch sentencepiece

COPY . .

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
