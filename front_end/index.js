const express = require('express');

const app = express();
// Set EJS as the view engine and define the views directory
app.set('view engine', 'ejs');
app.set('views', 'views');

// Serve static files from the "public" directory
app.use(express.static('public'));
app.use(express.json());

app.get('/', (req, res) => {
    res.render('main'); // Render the "index.ejs" view file
});

app.get('/records', async (req, res) => {
    const response = await fetch('http://localhost:8000/items')
    const data = await response.json();
    res.json(data);
});

app.post('/records', async (req, res) => {
    console.log(req.body.data);
    await fetch('http://localhost:8000/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(req.body.data)
    })
    res.send('ok');
})

app.put('/records', async (req, res) => {
    console.log("hit put route")
    console.log(req.body.id);
    console.log(req.body.data);
    await fetch(`http://localhost:8000/item/${req.body.id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: req.body.data
    })
    res.send('ok');
})

app.delete('/records', async (req, res) => {
    console.log(req.body.id);
    await fetch(`http://localhost:8000/item/${req.body.id}`, {
        method: "DELETE"
    })
    res.send('ok');
})

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});