import React from "react";
import { BrowserRouter, Routes, Route, useParams } from "react-router-dom";
import { BidPage } from "./component/RecruitPage";
import { Register } from "./component/form/Register";
import { Login } from "./component/form/Login";
import { Layout } from "./component/Layout";
import { UserManager } from "./UserContext";
import { SlotForm } from "./component/form/SlotForm";
import { TaskForm } from "./component/form/TaskForm";
import { BidForm } from "./component/form/BidForm";
import { SnackbarContextProvider } from "./component/Snackbar";
import { SlotFromTemplate } from "./component/form/SlotsFromTemplate";
import { SelectTemplate } from "./component/form/SelectTemplate";
import { TemplateForm } from "./component/form/TemplateForm";
const App: React.FC = () => {
  return (
    <BrowserRouter>
      <SnackbarContextProvider>
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
            <Route path="/selecttemplate" element={<SelectTemplate/>} />
            <Route path="/fromtemp/" element={<SlotFromTemplate />} />
            <Route path="/newtemplate" element={<TemplateForm/>}/>
          </Route>
        </Routes>
      </SnackbarContextProvider>
    </BrowserRouter>
  );
};

export default App;
