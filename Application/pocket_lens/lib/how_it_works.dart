import 'package:flutter/material.dart';

class HowItWorks extends StatelessWidget {
  const HowItWorks({Key? key}) : super(key: key);
  void _goBack(BuildContext ctx) {
    Navigator.of(ctx).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('How It Works'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Expanded(
            flex: 1,
            child: Container(),
          ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 16.0),
            child: Center(
              child: Text(
                '''
Welcome to Pocket Lens.
With Pocket Lens, you can take a picture of your surroundings and get a description of what's in the picture.
You can also use the app to estimate depths, read text, recognize currency, detect faces and more.
Just speak the module name and the app will guide you through the process.

To get started, say 'Scene Descriptor' to describe your surroundings.
Our goal is to empower you with the information you need to navigate the 
world with confidence and independence.
''',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                ),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Container(),
          ),
        ],
      ),
    );
  }
}
