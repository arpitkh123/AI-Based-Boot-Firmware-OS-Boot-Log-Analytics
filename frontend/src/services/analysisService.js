import api from "./api";

export const analyzeLog = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/analyze",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const checkBackend = async () => {
  const response = await api.get("/health");

  return response.data;
};

export const getHistory = async () => {
  const response = await api.get("/history");
  return response.data;
};

export const deleteHistoryItem = async (analysisId) => {
  const response = await api.delete(`/history/${analysisId}`);
  return response.data;
};