import 'package:flutter/material.dart';
import 'package:alan_voice/alan_voice.dart';

class AlanChatBot extends StatefulWidget {
  @override
  State<AlanChatBot> createState() => _AlanChatBotState();
}

class _AlanChatBotState extends State<AlanChatBot> {
  @override
  void initState() {
    super.initState();

    /// Init Alan Button with project key from Alan AI Studio
    AlanVoice.addButton(
        "95aec1209fe5ec07ce09fa461da220842e956eca572e1d8b807a3e2338fdd0dc/stage");

    /// Handle commands from Alan AI Studio
    AlanVoice.onCommand.add(
      (command) {
        debugPrint("got new command ${command.toString()}");
      },
    );
  }

  //Deactivate Alan Button when exiting the widget
  @override
  void dispose() {
    AlanVoice.deactivate();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Chatbot'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      body: Center(),
    );
  }
}
