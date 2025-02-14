const express = require('express');
const cors = require('cors');
const { Pool } = require('pg'); // Подключаем пакет pg
const app = express();
const port = 3000;

// Настройки подключения к PostgreSQL
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'mydatabase', // Укажите вашу базу данных
  password: 'yourpassword', // Укажите пароль
  port: 5432,
});

app.use(cors({
  origin: 'http://localhost:4200',
  methods: ['GET', 'POST'],
}));
app.use(express.json());

app.post('/login', async (req, res) => {
  const { name } = req.body;

  try {
    const result = await pool.query('SELECT * FROM users WHERE name = $1', [name]);

    if (result.rows.length > 0) {
      res.status(200).json({ message: 'Login successful!' });
    } else {
      res.status(401).json({ message: 'Invalid name' });
    }
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
