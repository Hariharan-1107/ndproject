const express = require("express");
const http = require("http");
const WebSocket = require("ws");
const { spawn } = require("child_process");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on("connection", function connection(ws) {
  console.log("Client connected");

  ws.on("message", function incoming(data) {
    console.log("Received encrypted data:", data);

    // Call Python script for decryption
    const pythonProcess = spawn("python3", [
      "encrypt_decrypt.py",
      "YourSecretKey",
    ]);
    pythonProcess.stdin.write(`decrypt ${data}\n`);
    pythonProcess.stdin.end();

    pythonProcess.stdout.on("data", (data) => {
      const decryptedData = data.toString().trim();
      console.log("Decrypted data:", decryptedData);

      // Send decrypted data to client
      ws.send(decryptedData);
    });
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, function listening() {
  console.log(`Server listening on port ${PORT}`);
});
