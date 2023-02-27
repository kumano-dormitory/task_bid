import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { BidPage } from './BidPage';
import { Register } from './Register';
import { Login } from './Login';
import { Layout } from './Layout';
const  App:React.FC =()=> {
  return (
    <BrowserRouter>
      <Routes>
      <Route path='/' element={<Layout />} >
        <Route path={`/bidpage/`} element={<BidPage />} />
        <Route path={`/register/`} element={<Register />} />
        <Route path={`/login/`} element={<Login />} />
      </Route>
    </Routes>
  </BrowserRouter>
  );
}

export default App;
