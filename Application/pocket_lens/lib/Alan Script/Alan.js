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



intent('(Scene Descriptor|Scene|Describe|Describe the Scene)', p=> {
    p.play('Going to scene descriptor.');
    p.play({command: 'Scene Descriptor'});
})

intent('(Face Recognizer|Who is this?)', p=> {
    p.play('Going to Face Recognizer.');
    p.play({command: 'Face Recognizer'});
})

//(Emotion|Emotion Detector|What is (he|she|they) feeling ?)

intent('(Emotion|Emotion Detector|What is he feeling?)', p=> {
    p.play('Going to emotion recognizer.');
    p.play({command: 'Emotion Recognizer'});
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
