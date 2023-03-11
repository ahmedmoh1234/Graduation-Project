import 'package:flutter/material.dart';
import 'config.dart';

class ChangeIPAddress extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //Take input from user and change IP_ADDRESS
    return Scaffold(
      appBar: AppBar(
        title: const Text('Change IP Address'),
      ),
      body: Center(
        child: Column(
          children: [
            const SizedBox(
              height: 100,
            ),
            const Text('Change IP Address'),
            TextField(
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'IP Address',
              ),
              onChanged: (v) {
                IP_ADDRESS = '$v:5000';
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // IP_ADDRESS = '192.168.1.18:5000';
        },
        // tooltip: 'Increment',
        child: const Icon(
          Icons.save,
        ),
      ),
    );
  }
}
