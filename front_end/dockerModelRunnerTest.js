// # Using curl (OpenAI-compatible API)
// curl http://localhost:12434/engines/llama.cpp/v1/chat/completions \
//     -H "Content-Type: application/json" \
//   -d '{
// "model": "ai/smollm2:360M-instruct-q4_K_M",
//     "messages": [{"role": "user", "content": "Explain what Docker is in one sentence."}]
// }'
//


async function getResponse(prompt) {
    const response = await fetch("http://localhost:12434/engines/llama.cpp/v1/chat/completions", {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": JSON.stringify({
            "model": "ai/gemma4:E4B",
            "messages": [{"role": "user", "content": prompt}]
        })
    })

    return response.json()
}

getResponse("Explain what Docker is in one sentence.").then((data) => {
    console.log(data)
    console.log(data.choices[0].message)
})