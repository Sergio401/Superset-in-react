const express = require('express');
const axios = require('axios');
//const cors = require('cors');

/*const PORT = 3001;
const app = express();
app.use(cors());

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
 */

const router = express.Router();

async function fetchAccessToken() {
  try {
    const body = {
      username: "admin",
      password: "admin",
      provider: "db",
      refresh: true,
    }

    const response = await axios.post(
        "http://localhost:8088/api/v1/security/login",
        body,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
    )

    const jsonResponse = response.data;
    return jsonResponse?.access_token
  } catch (e) {
    console.error(error)
  }
}

async function fetchGuestToken() {
  const accessToken = await fetchAccessToken()
  try {
    const body = {
      resources: [
        {
          type: "dashboard",
          id: "663bebff-a142-4d84-9f83-6d321eed47b3",
        },
      ],
      rls: [],
      user: {
        username: "guest",
        first_name: "Guest",
        last_name: "user",
      },
    }
    const response = await axios.post(
        "http://localhost:8088/api/v1/security/guest_token",
        body,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        }
    )
    const jsonResponse = response.data;
    return jsonResponse?.token
  } catch (error) {
    console.error(error)
  }
}

async function getRickAndMortyCharacters() {
  try {
    const response = await axios.get('https://rickandmortyapi.com/api/character');
    return response.data.results;
  } catch (error) {
    console.error(error);
  }
}

router.get("/", async (req, res) => {
  const token = await fetchGuestToken()
  res.json(token)
})

module.exports = router;

/*app.get("/guest-token", async (req, res) => {
  const token = await getRickAndMortyCharacters()
  res.json(token)
})

 */