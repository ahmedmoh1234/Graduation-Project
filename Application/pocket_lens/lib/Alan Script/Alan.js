// {Name: Basic_example_for_voice_AI_assistant}
// {Description: Learn how to create a dialog script and integrate your AI assistant with the app}

// Use this sample to create your own voice commands
intent('hello world', p => {
    p.play('(hello|hi there)');
});


intent('What is your name ?', p => {
    p.play(`My name is Pocket lens.
           I am here to help you navigate the world`);
});



intent('(Open|Go to|) Scene Descriptor',
       'Scene',
       'Describe',
       'Describe the Scene',
       'What(\'s| is) in front of me ?',
       'What am I seeing ?',
       'What are you seeing ?',
       p=> {
    p.play('Going to scene descriptor.');
    p.play({command: 'Scene Descriptor'});
})

intent('(Open|Go to|) Face Recognizer',
       'Who is this?',
       'Who (\'s| is) in front of me ?',
       p=> {
    p.play('Going to Face Recognizer.');
    p.play({command: 'Face Recognizer'});
})

intent('Back', 
      'Go back',
      p => {
       p.play({command: 'Back'});
})

intent('(Read|Scan) (this|) (document|text|)',
       '(Open|Go to|) Document (scanner|reader|)',
      p=>{
    p.play('Going to document reader.');
    p.play({command: 'Document Reader'});
})

intent('(Open|Go to|) Currency (Recognizer|Descriptor|)',
      'How much ?',
      'How much is this ?',
      'Currency',
      'Denomination',
        p=>{
    p.play('Going to currency recognizer.');
    p.play({command: 'Currency Recognizer'})
})

intent('(Open|Go to|) Menu',
       p=>{
    p.play('Opening Menu');
    p.play({command: 'Menu'});
})

intent('(Open|Go to|) Clothes (Descriptor|)',
       'Clothes',
      'What cloth is this ?',
      'Is this a (t-shirt|dress|shirt|trousers)',
      'What to wear ?',
      p=>{
    p.play('Going to clothes descriptor.');
    p.play({command: 'Clothes'});
})
       
intent('(Open|Go to|) Emotion (Recognizer|Detector|)',
       'Emotion',
       'Feeling',
       'What is (he|she) feeling?',
       'What are they feeling?', 
       p=> {
    p.play('Going to emotion recognizer.');
    p.play({command: 'Emotion Recognizer'});
})

intent('(Open|Go to|) Barcode (Scanner|Reader|)',
      '(Scan this|) Barcode',
      '(What is this|) Product',
      'What product is this ?',
      p => {
    p.play('Going to barcode reader.');
    p.play({command: 'Barcode'});
})


intent('(Go|) Home',
      p=>{
       p.play({command: 'Home'});
})

intent('Exit',
       'Goodbye',
       'Quit',
      p => {
    p.play('Goodbye');
    p.play({command: 'Exit'});
})

corpus(`
       Hello, I'm Pocket Lens.
       I am here to help you navigate the world.
`)

// Give Alan some knowledge about the world
// corpus(`
//     Hello, I'm Alan.
//     This is a demo application.
//     You can learn how to teach Alan useful skills.
//     I can teach you how to write Alan Scripts.
//     I can help you. I can do a lot of things. I can answer questions. I can do tasks.
//     But they should be relevant to this application.
//     I can help with this application.
//     I'm Alan. I'm a virtual assistant. I'm here to help you with applications.
//     This is a demo script. It shows how to use Alan.
//     You can create dialogs and teach me.
//     For example: I can help navigate this application.
// `);
