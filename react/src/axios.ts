import axiosBase from "axios";

const axios = axiosBase.create({
  baseURL: "http://localhost:8888",
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "http://localhost:8888",
  },
  withCredentials: true,
  responseType: "json",
});

axios.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem("access_token");

  if (config.headers) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

export default axios;
