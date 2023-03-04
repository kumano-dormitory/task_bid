import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { BidPage } from "./component/RecruitPage";
import { Register } from "./component/form/Register";
import { Login } from "./component/form/Login";
import { Layout } from "./component/Layout";
import { UserManager } from "./UserContext";
import { SlotForm } from "./component/form/SlotForm";
import { TaskForm } from "./component/form/TaskForm";
import { BidForm } from "./component/form/BidForm";
const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route
            path={`/bidpage/`}
            element={
              <UserManager>
                <BidPage />
              </UserManager>
            }
          />
          <Route path={`/register/`} element={<Register />} />
          <Route path={`/login/`} element={<Login />} />
          <Route path="/newslot/" element={<SlotForm />} />
          <Route path="/newtask/" element={<TaskForm />} />
          <Route path="/newbid/" element={<BidForm />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
