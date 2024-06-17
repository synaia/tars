// src/index.jsx
import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { MyApp } from './components/MyApp'; // Update the import path

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<MyApp />);
