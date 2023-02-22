import 'package:flutter/material.dart';
import 'home.dart';
import 'config.dart';

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
    ).then((_) {
      _goToHomeDelayed(context);
    });
  }

  void _goToHomeDelayed(BuildContext ctx) {
    Future.delayed(
      const Duration(seconds: 3),
      () => _goToHome(ctx),
    );
  }

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback(
      (_) => _goToHomeDelayed(context),
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
