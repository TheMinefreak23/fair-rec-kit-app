import words from 'an-array-of-english-words';

var metadata = {}
var form = {}
async function sendMockData() {
    form = {
        recommendations : rand(),
        split : rand(),
        splitMethod : 'timesplit',
        approaches : randomWords(),
        metrics : randomWords(),
        datasets : randomWords(),
        filters : randomWords()
    }

    metadata = {
        name : "Test" + rand(),
        email : randomWord() + "@" + randomWord() + ".com",
        tags : randomWords()
    }

    console.log(randomWords())

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ metadata: metadata, settings: form }),
    }
    console.log(form.value)
    fetch('http://localhost:5000/computation/calculation', requestOptions).then(
        () => {
        }
    )
}

function rand(n = 1000){
    return Math.floor(Math.random() * n)
}

function randomWord(){
    return words[Math.floor(Math.random()*words.length)]
}

function randomWords(){
    var array = []
    for (let i = 0; i < 5; i++) {
        array[i] = randomWord()
    }
    return array
}


export {sendMockData}