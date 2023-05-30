import 'package:flutter/material.dart';
import 'home.dart';

class StartUp extends StatefulWidget {
  const StartUp({super.key});

  @override
  State<StartUp> createState() => _StartUpState();
}

class _StartUpState extends State<StartUp> {
  void _goToHome(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(builder: (_) {
        return const Home();
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
    return const Scaffold(
      backgroundColor: Color(0xFF106cb5),
      body: SingleChildScrollView(
        child: Column(
          children: [
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
