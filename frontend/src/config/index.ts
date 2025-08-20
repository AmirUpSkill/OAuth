const config = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL as string,
};

if (!config.apiBaseUrl) {
  throw new Error("VITE_API_BASE_URL is not defined. Please check your .env file.");
}

export default config;