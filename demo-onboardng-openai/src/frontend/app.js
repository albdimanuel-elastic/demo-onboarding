const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
const axios = require("axios");
const pino = require("pino");
const pinoHttp = require("pino-http");
const fs = require("fs");

// Configure Pino logger to write logs to /var/log/app.log
const logStream = fs.createWriteStream("/var/log/app.log", { flags: "a" }); // Append mode
const logger = pino(
  {
    level: "info", // Adjust logging level as needed
    formatters: {
      level: (label) => ({ level: label.toUpperCase() }),
    },
  },
  logStream
);

// Express app setup
const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public"))); // Serve static files (HTML, CSS)

// Attach Pino HTTP middleware
app.use(
  pinoHttp({
    logger, // Use Pino logger
    customLogLevel: (res, err) => {
      // Set log level based on HTTP response status
      if (res.statusCode >= 500 || err) return "error";
      if (res.statusCode >= 400) return "warn";
      return "info";
    },
  })
);

// Serve the main page
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Handle the form submission
app.post("/query", async (req, res) => {
  const { sentence } = req.body;
  req.log.info({ sentence }, "Received query from user");
  try {
    req.log.info({ backendUrl: "http://backend-service:5000/query" }, "Querying backend...");
    const response = await axios.post("http://backend-service:5000/query", { sentence });
    req.log.info({ response: response.data.response }, "Received response from backend");
    res.json({ response: response.data.response });
  } catch (error) {
    req.log.error({ error: error.message }, "Error querying backend");
    res.status(500).json({ error: "Failed to communicate with the backend." });
  }
});

app.listen(port, () => {
  logger.info(`Frontend listening at http://localhost:${port}`);
});