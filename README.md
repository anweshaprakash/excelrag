# 🧠 Tabular Data Assistant with LangChain

This project builds an interactive command-line assistant that can **analyze** and **edit tabular data** (Excel files) using **LangChain**, **FAISS**, and **OpenAI GPT-4o**. It supports natural language interaction and can even modify data directly when instructed.

---

## 📦 Features

- Read and analyze Excel files as unstructured documents.
- Use `text-embedding-3-small` to embed document chunks.
- Store and retrieve relevant chunks using FAISS vectorstore.
- Query the assistant naturally using GPT-4o via LangChain.
- Modify the data using structured instructions like:
  
  ```
  EDIT||row_index||column_name||new_value
  ```

---

## 📁 File Structure

```
.
├── main.py                  # Main application file (interactive loop)
├── Historicalinvesttemp.xlsx # Sample input Excel file
├── .env                     # Your OpenAI API key stored securely
├── requirements.txt         # All required Python dependencies
└── README.md                # Project documentation
```

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/anweshaprakash/excelrag.git
cd excelrag
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate     # On Linux/macOS
venv\Scripts\activate        # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the root directory and add:

```env
OPENAI_API_KEY=your_openai_key_here
```

---

## 🚀 Usage

### Start the Assistant

```bash
python main.py
```

You will be prompted in an infinite loop to ask questions about the data in `Historicalinvesttemp.xlsx`. The assistant will return answers based on embedded document context.

### Example Commands

- "What are the average values per column?"
- "What is the value in row 5, column `Temperature`?"
- "Replace the NaN in row 3, column `Pressure` with 101.3"

If the assistant suggests an edit using:

```
EDIT||3||Pressure||101.3
```

The file will be automatically updated and reloaded.

---

## 🧠 Technologies Used

- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4o](https://platform.openai.com/)
- [FAISS VectorStore](https://github.com/facebookresearch/faiss)
- [Pandas](https://pandas.pydata.org/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 🛠️ Notes

- Designed for small to medium Excel files.
- Make sure the Excel file is well-formatted and tabular.
- Ensure consistent column naming (no unnamed columns).

---

## 📜 License

MIT License

---

## ✨ Acknowledgments

Built using the power of LangChain and OpenAI. Special thanks to the open-source community 🚀
