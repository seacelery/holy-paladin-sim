const isDevelopment = window.location.hostname === "localhost";

const CONFIG = {
    backendUrl: isDevelopment ? "http://localhost:5000" : 'https://holy-paladin-sim-6479e85b188f.herokuapp.com'
};

export { CONFIG };