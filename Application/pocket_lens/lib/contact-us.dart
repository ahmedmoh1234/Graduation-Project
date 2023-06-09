import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class ContactUS extends StatefulWidget {
  @override
  State<ContactUS> createState() => _ContactUSState();
}

class _ContactUSState extends State<ContactUS> {
  bool isAndroid = true;

  double screenWidth = 0;
  double screenHeight = 0;

  void _goBack(BuildContext ctx) {
    Navigator.of(ctx).pop();
  }

  void initState() {
    isAndroid = (defaultTargetPlatform == TargetPlatform.android);
  }

  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: RichText(
          text: const TextSpan(
            children: [
              TextSpan(
                text: "Contact Us",
                style: TextStyle(
                  //fontFamily: 'RalewayMedium',
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
        leading: BackButton(
          onPressed: () {
            _goBack(context);
          },
        ),
      ),
      body: Column(
        children: <Widget>[
          Card(
            clipBehavior: Clip.antiAlias,
            child: Column(
              children: <Widget>[
                SizedBox(
                  height: 10,
                ),
                ListTile(
                  leading: Icon(
                    Icons.facebook,
                    color: Colors.blue,
                  ),
                  title: Text(
                    'Facebook',
                    style: TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  subtitle: Text('https://www.facebook.com/PocketLens'),
                ),
                SizedBox(
                  height: 10,
                ),
                ListTile(
                  leading: IconButton(
                    // Use the FaIcon Widget + FontAwesomeIcons class for the IconData
                    icon: FaIcon(
                      FontAwesomeIcons.whatsapp,
                      color: Colors.green,
                    ),
                    onPressed: () {},
                  ),
                  title: Text(
                    'Whatsapp',
                    style: TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  subtitle: Text('+201285003523'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
