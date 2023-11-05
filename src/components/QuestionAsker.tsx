import React, { useState, ChangeEvent, MouseEvent } from 'react';
import axios from 'axios';

const QuestionAsker: React.FC = () => {
  const [question, setQuestion] = useState<string>('');
  const [context, setContext] = useState<string>('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const askQuestion = async (event: MouseEvent) => {
    setLoading(true)
    event.preventDefault();
    try {
      const apiUrl = 'http://localhost:80/query';
      const result = await axios.post(apiUrl, { question, context });
      setResponse(result.data.body.message.content);
    } catch (error) {
      console.error('Error fetching data:', error);
      setResponse({ error: 'Error fetching data' });
    }
    setLoading(false)
  };

  const containerStyle = {
    color: '#333',
    width: '100vw',
    maxWidth: '100%',
    padding: '20px',
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f8f8f8',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)'
  };

  const inputStyle = {
    width: '90%',
    padding: '10px',
    margin: '10px 0',
    borderRadius: '4px',
    border: '1px solid #ddd',
    fontSize: '16px'
  };

  const buttonStyle = {
    padding: '10px 20px',
    backgroundColor: '#4CAF50',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  };

  const responseStyle = {
    marginTop: '20px',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    backgroundColor: '#fff',
    overflowX: 'auto'
  };

  return (
    <div style={containerStyle}>
      <h2>Question Asker</h2>
      <div>
        <p>Literature Text</p>
        <textarea
          placeholder="Enter the context"
          value={context}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setContext(e.target.value)}
          style={{...inputStyle,height: '200px'}}
        />
      </div>
      <div>
        <div>Question</div>
        <textarea
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setQuestion(e.target.value)}
          style={inputStyle}
        />
      </div>
      {loading?"Loading...":<button onClick={askQuestion} style={buttonStyle}>Ask</button>}

      {response && (
        <div style={responseStyle}>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default QuestionAsker;
