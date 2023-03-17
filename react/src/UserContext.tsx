import axios from "./axios";
import React, { createContext } from "react";
import useSWR, { Fetcher } from "swr";
import { useNavigate } from "react-router-dom";
import { SlotResponse, TaskResponse } from "./ResponseType";
type User = {
  id: string;
  name: string;
  block: string;
  room_number: string;
  achivement: [];
  exp_task: TaskResponse[];
  slots: [];
  create_slot: [];
  create_task: [];
  point: number;
  bid: [];
  is_active: boolean;
};

type UserContextType = {
    user:User
}

const getCurrentUser: Fetcher<User> = (url:string) => {
    return axios.get(url).then((response) => response.data);
};

type UserManagerProps = {
    children:React.ReactNode
}

export const UserContext=createContext({} as UserContextType)

export const UserManager: React.FC<UserManagerProps> = (props:UserManagerProps) => {
    const navigate=useNavigate()
    const { data, error } = useSWR('/me', getCurrentUser)
    if (error) navigate('/login')
    if (!data) return <div>Loading...</div>
    const value = {
        user:data
    }
    return <UserContext.Provider value={value}>{props.children}</UserContext.Provider>
};
