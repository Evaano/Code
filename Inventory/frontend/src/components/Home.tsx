import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Hero from './Hero';
import Inventory from './Inventory';
import AddItemPage from './AddItemPage';
import UpdateItemPage from './UpdateItemPage';
import '../App.css'

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Hero />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/new-item" element={<AddItemPage />} />
            <Route path="/update-items" element={<UpdateItemPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
