const isDevelopment = window.location.hostname === 'localhost';
console.log(isDevelopment)

const CONFIG = {
    backendUrl: isDevelopment ? 'http://localhost:5500' : 'https://holy-paladin-sim-6479e85b188f.herokuapp.com'
};

export { CONFIG };