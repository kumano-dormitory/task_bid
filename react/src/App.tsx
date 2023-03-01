import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { BidPage } from "./RecruitPage";
import { Register } from "./Register";
import { Login } from "./Login";
import { Layout } from "./Layout";
import { UserManager } from "./UserContext";
const App: React.FC = () => {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path={`/bidpage/`} element={<UserManager><BidPage /></UserManager>} />
            <Route path={`/register/`} element={<Register />} />
          <Route path={`/login/`} element={<Login />} />
          <Route path="/newtask/" element={<></>} />
          <Route path="/newslot" element={<></>} />
          </Route>
        </Routes>
    </BrowserRouter>
  );
};

export default App;
