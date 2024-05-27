PDF Query App

PDF Query App is a web application that allows users to upload PDF files and ask questions about their content. The app processes the uploaded PDFs, analyzes their content, and provides accurate answers based on the text within the documents.


Features

- **PDF Upload**: Easily upload PDF files through a user-friendly interface.
- **Question Input**: Enter questions related to the content of the uploaded PDF files.
- **Content Analysis**: The backend server processes the PDF files to analyze their content.
- **Answer Generation**: Receive accurate answers based on the content of the uploaded PDFs.
- **Loading Indicator**: Visual feedback while the application processes the PDF and generates answers.
- **Error Handling**: Clear error messages for invalid file types and other potential issues.
- **Responsive Design**: Fully responsive design for optimal viewing on different devices.
- **Cross-Origin Support**: CORS middleware is enabled to allow communication between the frontend and backend servers.

- ## Getting Started

- 
### Installation and Running

1. **Clone the repository:**

   git clone https://github.com/your-username/pdf-query-app.git
   cd pdfQuery

2. **Set up the backend:**

   Navigate to the server directory:
   cd server
   
   Create and activate a virtual environment:

   python -m venv venv
   On Windows, use `venv\Scripts\activate`

4. **Set up the frontend:**

   Navigate to the frontend directory:

   cd client
   npm install

   Starting the frontend:
   npm run dev
   
5. **Start the backend server:**

   uvicorn main:app --reload --port 8000

   
Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or new features to suggest.
   
