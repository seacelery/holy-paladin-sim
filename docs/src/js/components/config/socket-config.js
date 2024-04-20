import { CONFIG } from "../config.js";

const initialiseSocket = () => {
    const socket = io(CONFIG.backendUrl, {
        withCredentials: true,
        transports: ["websocket"],
    });

    socket.on("connect", function() {
        console.log("Connected to the server");
    });

    socket.on("disconnect", function() {
        console.log("Disconnected from the server");
    });

    socket.on("connect_error", (error) => {
        console.log("Connection failed:", error);
    });

    return socket;
};

export { initialiseSocket };