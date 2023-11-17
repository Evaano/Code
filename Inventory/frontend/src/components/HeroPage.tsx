import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Hero from './Hero';
import Inventory from './Inventory';
import AddItemPage from './AddItemPage';

const App = () => {
    return (
        <Router>
            <div style={{ display: 'flex', height: '100vh', width: '100vw' }}>
                <Navbar />
                <div style={{ flex: 1 }}>
                    <Routes>
                        <Route path="/" element={<Hero />} />
                        <Route path="/inventory" element={<Inventory />} />
                        <Route path="/new-item" element={<AddItemPage />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;
