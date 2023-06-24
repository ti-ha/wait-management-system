import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Landing from './components/Landing/Landing';
import StaffLanding from './components/Staff/StaffLanding'
import TableSelection from './components/Customer/TableSelection';
import Manager from './components/Manager/Manager';
import Customer from './components/Customer/Customer';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route path="/staff" element={<StaffLanding />} />
        <Route path="/select-table" element={<TableSelection />} />
        <Route path="/manager" element={<Manager />} />
        <Route path="/customer/:tableNumber" element={<Customer />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
