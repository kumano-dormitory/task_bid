import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { BidPage } from "./RecruitPage";
import { Register } from "./Register";
import { Login } from "./Login";
import { Layout } from "./Layout";
import { UserManager } from "./UserContext";
import { SlotForm } from "./SlotForm";
import { TaskForm } from "./TaskForm";
const App: React.FC = () => {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path={`/bidpage/`} element={<UserManager><BidPage /></UserManager>} />
            <Route path={`/register/`} element={<Register />} />
          <Route path={`/login/`} element={<Login />} />
          <Route path="/newslot/" element={<SlotForm/>} />
          <Route path="/newtask/" element={<TaskForm/>} />
          </Route>
        </Routes>
    </BrowserRouter>
  );
};

export default App;
