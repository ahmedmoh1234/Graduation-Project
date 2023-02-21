import 'package:flutter/material.dart';
import 'home.dart';

class StartUp extends StatefulWidget {
  @override
  State<StartUp> createState() => _StartUpState();
}

class _StartUpState extends State<StartUp> {
  void _goToHome(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(builder: (_) {
        return Home();
      }),
    );
  }

  @override
  void initState() {
    super.initState();
    Future.delayed(
      Duration(seconds: 2),
      () => _goToHome(context),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF106cb5),
      body: SingleChildScrollView(
        child: Column(
          children: const [
            SizedBox(
              height: 150,
            ),
            Center(
              child: Image(
                fit: BoxFit.fitHeight,
                image: AssetImage('assets/images/icon.jpg'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
