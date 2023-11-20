// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Hero from './Hero';
import Inventory from './Inventory';
import AddItemPage from './AddItemPage';
import UpdateItemPage from './UpdateItemPage';
import { ScrollArea } from '@mantine/core';

const App = () => {
  return (
    <Router>
      <div style={{ display: 'flex', height: '100vh' }}>
        {/* Sticky Navbar */}
        <Navbar />

        {/* Scrollable content */}
        <div style={{ flex: 1, overflow : 'hidden' }}>
          <ScrollArea style={{ height: '90vh', width: '100%' }}>
            <Routes>
              <Route path="/" element={<Hero />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/new-item" element={<AddItemPage />} />
              <Route path="/update-items" element={<UpdateItemPage />} />
            </Routes>
          </ScrollArea>
        </div>
      </div>
    </Router>
  );
};

export default App;
