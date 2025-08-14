import axoisInstance from "../../axois";

export const getUser = (id: string) => axoisInstance.get(`/api/v1/users/${id}`);
export const loginUser = (data: { email: string; password: string }) => {
  return axoisInstance.post(`/api/v1/users/authenticate`, data);
};

export const refreshToken = (data: { refresh_token: string }) => {
  return axoisInstance.post("/auth/refresh", data);
};

export const forgetPassword = (data: { email: string | null }) => {
  return axoisInstance.post("/auth/forgot-password", data);
};

export const resetPassword = (data: {
  token: string | null;
  confirm_password: string | null;
  new_password: string | null;
}) => {
  return axoisInstance.post("/auth/reset-password", data);
};

export const signupUser = (data: { name: string; email: string; password: string; is_active: boolean; role?: 'admin' | 'tenant' | 'user' }) => {
  return axoisInstance.post("/api/v1/users/", data);
};

export const getAllUsers = async () => {
  const response = await axoisInstance.get("/api/v1/users/");
  console.log("users response", response.data);
  return response.data;
};
export const deleteUser = (id: string) =>
  axoisInstance.delete(`/api/v1/users/${id}`);
