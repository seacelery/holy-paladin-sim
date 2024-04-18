const isDevelopment = window.location.hostname === 'http://127.0.0.1:5500/';
console.log(isDevelopment)

const CONFIG = {
    backendUrl: isDevelopment ? 'http://127.0.0.1:5500/' : 'https://holy-paladin-sim-6479e85b188f.herokuapp.com'
};

export { CONFIG };