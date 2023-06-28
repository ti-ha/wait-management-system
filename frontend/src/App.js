import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Landing from './components/Landing/Landing.js';
import StaffLanding from './components/Staff/StaffLanding.js'
import TableSelection from './components/Customer/TableSelection.js';
import Manager from './components/Manager/Manager.js';
import Customer from './components/Customer/Customer.js';
import Kitchen from './components/Staff/Kitchen.js';
import WaitStaff from './components/Staff/WaitStaff.js';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Landing />} />
          <Route path="/staff" element={<StaffLanding />} />
          <Route path="/select-table" element={<TableSelection />} />
          <Route path="/manager" element={<Manager />} />
          <Route path="/customer/:tableNumber" element={<Customer />} />
          <Route path="/kitchen" element={<Kitchen />} />
          <Route path="/wait-staff" element={<WaitStaff />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;
