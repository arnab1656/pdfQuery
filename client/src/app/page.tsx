"use client";

import axios from "axios";
import { ChangeEvent, useState } from "react";
import { Logo } from "./component/logo";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isUploaded, setIsUploaded] = useState<boolean>(false);

  const [query, setQuery] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [error, setError] = useState<string>("");

  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;

    if (selectedFile) {
      if (selectedFile.type === "application/pdf") {
        setFile(selectedFile);
        setFileName(selectedFile.name);
        setErrorMessage("");
      } else {
        setErrorMessage("Please select a PDF file.");
        setFile(null);
        setFileName("");
      }
    }
  };

  const handleSubmit = async () => {
    if (file) {
      // Process the file as needed
      console.log("File uploaded:", file);
      // You can add logic here to send the file to a server, read its contents, etc.

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post(
          `http://127.0.0.1:8001/uploadfile/?query=${fileName}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        console.log("File uploaded successfully:", response.data);
        setIsUploaded(true);
      } catch (error) {
        console.error("Error uploading file:", error);
        setIsUploaded(false);
      }
    }
  };

  const handleAskClick = async () => {
    console.log("ASk is clicked");

    console.log(query);

    // Remove the file extension

    const encodedQuery = encodeURIComponent(
      fileName.substring(0, fileName.lastIndexOf("."))
    );
    setLoading(true); // Set loading to true when starting the upload
    try {
      // Make GET request to the /ask/ endpoint with the query as a parameter
      const response = await axios.get(
        `http://127.0.0.1:8001/ask/?query=${query}&query2=${encodedQuery}`
      );

      // Extract the answer from the response data and set it in the state

      console.log(response);

      const { answer } = response.data;
      setAnswer(answer);
      setError("");
    } catch (error) {
      // Handle errors if any
      console.error("Error fetching answer:", error);
      // Set error state
      setError("Error fetching answer");
      setAnswer("");
    } finally {
      setLoading(false); // Set loading to false after the upload is completed
    }
  };

  return (
    <div className="p-4">
      <header className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 items-center justify-between p-4 bg-gray-100 border-b border-gray-300">
        {/* <h1 className="text-2xl font-bold col-span-1">Logo</h1> */}
        <Logo></Logo>
        <div className="flex items-center space-x-4 col-span-2 md:col-span-1 lg:col-span-2 py-5">
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="file-input"
          />
          {fileName && (
            <div className="border border-green-500 p-2 rounded-lg flex items-center space-x-2 text-green-700">
              <PdfIcon />
              <p>{fileName}</p>
            </div>
          )}
        </div>
        <button
          onClick={handleSubmit}
          className="col-span-1 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Upload PDF
        </button>
      </header>
      {isUploaded && (
        <div className="mt-4 p-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question"
            className="w-full p-2 border border-gray-300 rounded mb-4"
          />
          <button
            onClick={handleAskClick}
            className="px-4 py-2 bg-green-500 text-white rounded"
          >
            Ask
          </button>
          {/* <div className="mt-4">
            {error && <p className="text-red-500">Error: {error}</p>}
            {answer && <p className="text-gray-800">Answer: {answer}</p>}
          </div> */}
          {loading ? (
            <Spinner />
          ) : (
            <div>
              {error && <p className="text-red-500">Error: {error}</p>}
              {answer && <p className="text-gray-800">Answer: {answer}</p>}
            </div>
          )}
          {loading}
        </div>
      )}
    </div>
  );
}

const PdfIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-6 w-6 text-green-500"
    viewBox="0 0 20 20"
    fill="currentColor"
  >
    <path
      fillRule="evenodd"
      d="M2 0a2 2 0 00-2 2v16a2 2 0 002 2h16a2 2 0 002-2V4a2 2 0 00-2-2H2zm12 12a1 1 0 01-2 0V8H8a1 1 0 110-2h4V3a1 1 0 112 0v7h1a1 1 0 110 2h-1v1zm4-5H9a1 1 0 110-2h9a1 1 0 011 1v9a1 1 0 01-1 1h-1a1 1 0 110-2h1V7zM6 13a1 1 0 100-2 1 1 0 000 2z"
      clipRule="evenodd"
    />
  </svg>
);

const Spinner = () => {
  return (
    <div className="flex justify-center items-center h-full">
      <div className="w-16 h-16 border-t-4 border-b-4 border-gray-800 rounded-full animate-spin"></div>
    </div>
  );
};
