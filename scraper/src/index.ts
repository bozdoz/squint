import express from "express";
import { encrypt } from "./encrypt";
const app = express();
const port = 3000;

app.use(express.json());

app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.send("hello world");
});

app.post("/encrypt", async (req, res) => {
  const { login, password } = req.body;

  if (login && password) {
    const encUser = await encrypt(login);
    const encPass = await encrypt(password);
    res.send({
      user: { ...encUser },
      pass: { ...encPass },
    });
    return;
  }

  res.status(500).send("You dummy");
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
